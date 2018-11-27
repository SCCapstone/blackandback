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

#supress cmd output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class RecolorNN(object):
	def __init__(self,**kwargs):
		self.inception = InceptionResNetV2(weights=None, include_top=True)
		self.saveNotFound = True
		self.model = Sequential()
		self.datagen = ImageDataGenerator(
							shear_range=0.2,
							zoom_range=0.2,
							rotation_range=20,
							horizontal_flip=True)
		self.batch_size = 20
		self.color_me = []
		self.output = []
		self.numEpochs = 1
		self.numSteps = 1
		
		
	def loadTrainFiles(self):
		X = []
		for filename in os.listdir('../train/'):
			X.append(img_to_array(load_img('../train/'+filename)))
		X = np.array(X, dtype=float)
		self.Xtrain = 1.0/255*X	
		
	def loadWeights(self):
		#Load weights
		try:
			self.inception.load_weights('color_tensorflow_real_mode.h5')
		except Exception as e:
			print("Error " + str(e))
		self.inception.graph = tf.get_default_graph()

		self.saveNotFound = True
		try:
			list_of_files = glob.glob('../saves/*.h5') # * means all if need specific format then *.csv
			latest_file = max(list_of_files, key=os.path.getctime)
			answer = input("File found! " + latest_file + " would you like to load it? [y/n]\n") #admin function
			if answer is "y" or answer is "Y":
				self.model = load_model(latest_file)
				self.saveNotFound = False
			else:
				customAns = input("Would you like to load in a custom network? [y/n]\n")
				if customAns is 'y' or customAns is 'Y':
					customFile = input("Please input filepath \n")
					self.model = load_model(customFile)
					self.saveNotFound = False
				else:
			
					print("User elected not to use save, training new network")
					self.saveNotFound = True
		except Exception as e:
			print("saved model not found. " + str(e))
			self.saveNotFound = True
	def buildLayers(self):
		embed_input = Input(shape=(1000,))
		if(self.saveNotFound):
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

			self.model = Model(inputs=[encoder_input, embed_input], outputs=decoder_output)





	#Create embedding
	def create_inception_embedding(self,grayscaled_rgb):
		grayscaled_rgb_resized = []
		for i in grayscaled_rgb:
			i = resize(i, (299, 299, 3), mode='constant')
			grayscaled_rgb_resized.append(i)
		grayscaled_rgb_resized = np.array(grayscaled_rgb_resized)
		grayscaled_rgb_resized = preprocess_input(grayscaled_rgb_resized)
		with self.inception.graph.as_default():
			embed = self.inception.predict(grayscaled_rgb_resized)
		return embed

#Generate training data

	def image_a_b_gen(self):
		for batch in self.datagen.flow(self.Xtrain, batch_size=self.batch_size):
			grayscaled_rgb = gray2rgb(rgb2gray(batch))
			embed = self.create_inception_embedding(grayscaled_rgb)
			lab_batch = rgb2lab(batch)
			X_batch = lab_batch[:,:,:,0]
			X_batch = X_batch.reshape(X_batch.shape+(1,))
			Y_batch = lab_batch[:,:,:,1:] / 128
			yield ([X_batch, self.create_inception_embedding(grayscaled_rgb)], Y_batch)

#Train model      
#tensorboard = TensorBoard(log_dir="/output")
	def trainModel(self):
		if(self.saveNotFound):
			self.numEpochs = int(input("How many epochs? [int] \n")) # admin function
			self.numSteps = int(input("How many steps per epochs? [int] \n")) # admin function
			self.model.compile(optimizer='adam', loss='mse')
			self.model.fit_generator(self.image_a_b_gen(), epochs=self.numEpochs, steps_per_epoch=self.numSteps)
	def saveModel(self):
	# Save model
		model_json = self.model.to_json()
		with open("model.json", "w") as json_file:
			json_file.write(model_json)
		savefilename = '../saves/recolorNetSave' + str(datetime.datetime.today().strftime('%Y_%m_%d')) + '.h5'
		print(savefilename)
		self.model.save_weights("color_tensorflow_real_mode.h5")
		self.model.save(savefilename)
	
	def makePredictions(self):
	#Make predictions on validation images
		for filename in os.listdir('../Test/'):
			self.color_me.append(img_to_array(load_img('../Test/'+filename)))
		self.color_me = np.array(self.color_me, dtype=float)
		self.color_me = 1.0/255*self.color_me
		self.color_me = gray2rgb(rgb2gray(self.color_me))
		self.color_me_embed = self.create_inception_embedding(self.color_me)
		self.color_me = rgb2lab(self.color_me)[:,:,:,0]
		self.color_me = self.color_me.reshape(self.color_me.shape+(1,))

	def testModel(self):
		# Test model
		self.output = self.model.predict([self.color_me, self.color_me_embed])
		self.output = self.output * 128

	def outputColors(self):
		# Output colorizations
		for i in range(len(self.output)):
			cur = np.zeros((256, 256, 3))
			cur[:,:,0] = self.color_me[i][:,:,0]
			cur[:,:,1:] = self.output[i]
			imsave("result/img_"+str(i)+".png", lab2rgb(cur))	
if __name__ == '__main__':
	NN = RecolorNN()
	print("Loading files")
	NN.loadTrainFiles()
	print("Loaded files")
	print("Loading weights")
	NN.loadWeights()
	print("Loaded weights")
	print("Building layers")
	NN.buildLayers()
	print("Built layers")
	print("Training model")
	NN.trainModel()
	print("Trained model")
	print("Saving model")
	NN.saveModel()
	print("saved model")
	print("Making predictions")
	NN.makePredictions()
	print("Made predictions")
	print("Testing model")
	NN.testModel()
	print("Tested model")
	print("Outputting images")
	NN.outputColors()
	print("Outputted images")
	