import keras
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.preprocessing import image
from keras.engine import Layer
from keras.applications.inception_resnet_v2 import preprocess_input
from keras.layers import Conv2D, UpSampling2D, InputLayer, Conv2DTranspose, Input, Reshape, merge, concatenate, Activation, Dense, Dropout, Flatten
from keras.layers.normalization import BatchNormalization
from keras.callbacks import TensorBoard 
from keras.models import Sequential, Model, load_model
from keras.layers.core import RepeatVector, Permute
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.transform import resize
from skimage.io import imsave
import numpy as np
import os
import random
import tensorflow as tf
import datetime
import glob
# Get images
# Change to '/data/images/Train/' to use all the 10k images
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

X = []
for filename in os.listdir('../train/'):
    X.append(img_to_array(load_img('../train/'+filename)))
X = np.array(X, dtype=float)
Xtrain = 1.0/255*X

#Load weights
inception = InceptionResNetV2(weights=None, include_top=True)
try:
	inception.load_weights('color_tensorflow_real_mode.h5')
except Exception as e:
	print("Error " + str(e))
inception.graph = tf.get_default_graph()

saveNotFound = True
try:
	list_of_files = glob.glob('../saves/*.h5') # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)
	answer = input("File found! " + latest_file + " would you like to load it? [y/n]\n") #admin function
	if answer is "y" or answer is "Y":
		model = load_model(latest_file)
		saveNotFound = False
	else:
		customAns = input("Would you like to load in a custom network? [y/n]\n")
		if customAns is 'y' or answer is 'Y':
			customFile = input("Please input filepath \n")
			model = load_model(customFile)
			saveNotFound = False
		else:
			
			print("User elected not to use save, training new network")
			saveNotFound = True
except Exception as e:
	print("saved model not found. " + str(e))
	saveNotFound = True

embed_input = Input(shape=(1000,))
if(saveNotFound):
	#Encoder
	encoder_input = Input(shape=(256, 256, 1,))
	encoder_output = Conv2D(64, (3,3), activation='relu', padding='same', strides=2)(encoder_input)
	encoder_output = Conv2D(128, (3,3), activation='relu', padding='same')(encoder_output)
	encoder_output = Conv2D(128, (3,3), activation='relu', padding='same', strides=2)(encoder_output)
	encoder_output = Conv2D(256, (3,3), activation='relu', padding='same')(encoder_output)
	encoder_output = Conv2D(256, (3,3), activation='relu', padding='same', strides=2)(encoder_output)
	encoder_output = Conv2D(512, (3,3), activation='relu', padding='same')(encoder_output)
	encoder_output = Conv2D(512, (3,3), activation='relu', padding='same')(encoder_output)
	encoder_output = Conv2D(256, (3,3), activation='relu', padding='same')(encoder_output)

	#Fusion
	fusion_output = RepeatVector(32 * 32)(embed_input) 
	fusion_output = Reshape(([32, 32, 1000]))(fusion_output)
	fusion_output = concatenate([encoder_output, fusion_output], axis=3) 
	fusion_output = Conv2D(256, (1, 1), activation='relu', padding='same')(fusion_output) 

	#Decoder
	decoder_output = Conv2D(128, (3,3), activation='relu', padding='same')(fusion_output)
	decoder_output = UpSampling2D((2, 2))(decoder_output)
	decoder_output = Conv2D(64, (3,3), activation='relu', padding='same')(decoder_output)
	decoder_output = UpSampling2D((2, 2))(decoder_output)
	decoder_output = Conv2D(32, (3,3), activation='relu', padding='same')(decoder_output)
	decoder_output = Conv2D(16, (3,3), activation='relu', padding='same')(decoder_output)
	decoder_output = Conv2D(2, (3, 3), activation='tanh', padding='same')(decoder_output)
	decoder_output = UpSampling2D((2, 2))(decoder_output)

	model = Model(inputs=[encoder_input, embed_input], outputs=decoder_output)

#Create embedding
def create_inception_embedding(grayscaled_rgb):
    grayscaled_rgb_resized = []
    for i in grayscaled_rgb:
        i = resize(i, (299, 299, 3), mode='constant')
        grayscaled_rgb_resized.append(i)
    grayscaled_rgb_resized = np.array(grayscaled_rgb_resized)
    grayscaled_rgb_resized = preprocess_input(grayscaled_rgb_resized)
    with inception.graph.as_default():
        embed = inception.predict(grayscaled_rgb_resized)
    return embed

# Image transformer
datagen = ImageDataGenerator(
        shear_range=0.2,
        zoom_range=0.2,
        rotation_range=20,
        horizontal_flip=True)

#Generate training data
batch_size = 20

def image_a_b_gen(batch_size):
    for batch in datagen.flow(Xtrain, batch_size=batch_size):
        grayscaled_rgb = gray2rgb(rgb2gray(batch))
        embed = create_inception_embedding(grayscaled_rgb)
        lab_batch = rgb2lab(batch)
        X_batch = lab_batch[:,:,:,0]
        X_batch = X_batch.reshape(X_batch.shape+(1,))
        Y_batch = lab_batch[:,:,:,1:] / 128
        yield ([X_batch, create_inception_embedding(grayscaled_rgb)], Y_batch)

#Train model      
#tensorboard = TensorBoard(log_dir="/output")
if(saveNotFound):
	numEpochs = input("How many epochs? [int]") # admin function
	numSteps = input("How many steps per epochs? [int]") # admin function
	model.compile(optimizer='adam', loss='mse')
	model.fit_generator(image_a_b_gen(batch_size), epochs=1, steps_per_epoch=1)

# Save model
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
savefilename = '../saves/recolorNetSave' + str(datetime.datetime.today().strftime('%Y_%m_%d')) + '.h5'
print(savefilename)
model.save_weights("color_tensorflow_real_mode.h5")
model.save(savefilename)

#Make predictions on validation images
# Change to '/data/images/Test/' to use all the 500 test images
color_me = []
for filename in os.listdir('../Test/'):
    color_me.append(img_to_array(load_img('../Test/'+filename)))
color_me = np.array(color_me, dtype=float)
color_me = 1.0/255*color_me
color_me = gray2rgb(rgb2gray(color_me))
color_me_embed = create_inception_embedding(color_me)
color_me = rgb2lab(color_me)[:,:,:,0]
color_me = color_me.reshape(color_me.shape+(1,))


# Test model
output = model.predict([color_me, color_me_embed])
output = output * 128

# Output colorizations
for i in range(len(output)):
    cur = np.zeros((256, 256, 3))
    cur[:,:,0] = color_me[i][:,:,0]
    cur[:,:,1:] = output[i]
    imsave("result/img_"+str(i)+".png", lab2rgb(cur))	