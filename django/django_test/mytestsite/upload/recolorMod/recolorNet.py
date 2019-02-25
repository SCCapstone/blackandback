#based originally off of https://medium.freecodecamp.org/colorize-b-w-photos-with-a-100-line-neural-network-53d9b4449f8d by Emil Walner


import keras
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.preprocessing import image
from keras.engine import Layer
from keras.applications.inception_resnet_v2 import preprocess_input
from keras.layers import Conv2D, UpSampling2D, InputLayer, Conv2DTranspose, Input, Reshape, merge, concatenate, Activation, Dense, Dropout, Flatten
from keras.layers.normalization import BatchNormalization
from keras.callbacks import TensorBoard 
from keras.models import Sequential, Model, load_model, model_from_json
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

from keras import backend as K

from PIL import Image
from django.conf import settings


#is kiki running the newest thing

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
		if(self.saveNotFound):
			X = []
			for filename in os.listdir('upload/recolorMod/train'):
				X.append(img_to_array(load_img('upload/recolorMod/train/'+filename)))
			X = np.array(X, dtype=float)
			self.Xtrain = 1.0/255*X	
		
		
	def loadWeights(self):
		
		
		try:
			self.inception.load_weights('upload/saves/model.h5')
		except Exception as e:
			print(e)
		self.inception.graph = tf.get_default_graph()
		
		
		self.saveNotFound = True
		
		
		try:
			json_file = open("upload/saves/model.json", 'r')
			loaded_model_json = json_file.read()
			json_file.close()
			self.model = model_from_json(loaded_model_json)
			self.model.load_weights("upload/saves/model.h5")
			self.saveNotFound = False
		except Exception as e:
			print(e)
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
	def trainModel(self):
		if(self.saveNotFound):
			self.numEpochs = int(input("How many epochs? [int] \n")) # admin function
			self.numSteps = int(input("How many steps per epochs? [int] \n")) # admin function
			self.model.compile(optimizer='adam', loss='mse')
			print("model compiled")
			self.model.fit_generator(self.image_a_b_gen(), epochs=self.numEpochs, steps_per_epoch=self.numSteps)
			print("model fit")
	def saveModel(self):
	# Save model
		if(self.saveNotFound):
			self.model.save_weights("model.h5")
			model_json = self.model.to_json()
			with open("upload/saves/model.json", "w") as json_file:
				json_file.write(model_json)
			json_file.close()
	
	
	def resize_image(self,path, username):
		outfile = 'upload/files/' + username + '/output.jpg'
		im = Image.open(path)
		im = im.resize( (256,256), Image.ANTIALIAS)
		return im
		
	def makePredictions(self,username,recolorFile):
	#Make predictions on validation images
		FILE_DIR = ''
		if self.saveNotFound :
			FILE_DIR = 'upload/recolorMod/test/'
		else:
			FILE_DIR = 'upload/files/' + username + "/" + recolorFile
	
		
		resized_image = self.resize_image(FILE_DIR, username)
		self.color_me.append(img_to_array(resized_image)) #work here, maybe scratch load_img 
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

	def outputColors(self, username, recolorFile):
		# Output colorizations
		for i in range(len(self.output)):
			cur = np.zeros((256, 256, 3))
			cur[:,:,0] = self.color_me[i][:,:,0]
			cur[:,:,1:] = self.output[i]
			recolorFile = os.path.splitext(recolorFile)[0] 
			imsave("upload/files/" + username + "/" + recolorFile + "_recolored.png" , lab2rgb(cur))	
def runNN(username,recolorFile):
	NN = RecolorNN()
	NN.loadWeights()
	NN.loadTrainFiles()
	NN.buildLayers()
	NN.trainModel()
	NN.saveModel()
	NN.makePredictions(username,recolorFile)
	NN.testModel()
	print("Outputting images")
	NN.outputColors(username, recolorFile)
	print("Outputted images")

