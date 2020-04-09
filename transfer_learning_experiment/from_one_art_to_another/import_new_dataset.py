import pandas as pd 

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from keras.utils import np_utils
 
import numpy as np 

import glob
import os 
import csv
import time
import h5py

CHALLENGE = 'dc_creator'
CHALLENGES = ['dc_creator']

class ExperimentHandler(object):
	def __init__(self, neural_network, dataset_name, metadata_path, jpg_images_path, results_path, dataset_path, tl_mode):
		self.neural_network = neural_network
		self.dataset_name = dataset_name
		self.metadata_path = metadata_path
		self.jpg_images_path = jpg_images_path
		self.tl_mode = tl_mode
		self.dataset_storing_path = dataset_path + dataset_name + "/" 
		self.results_storing_path = results_path + dataset_name + "/"

		self.make_dataset_path()
		self.make_results_path()
	
	def make_dataset_path(self):
		if not os.path.exists(self.dataset_storing_path):
			os.makedirs(self.dataset_storing_path)

	def make_results_path(self):
		if not os.path.exists(self.results_storing_path):
			os.makedirs(self.results_storing_path)
	
	def get_metadata(self):
		return(pd.read_csv(self.metadata_path, error_bad_lines=False))
		
	def get_images(self):
	
		paths = sorted(glob.glob(self.jpg_images_path+"*.jpg"))
		filenames = sorted(os.listdir(self.jpg_images_path))
	
		images_df = pd.DataFrame({'ImageId':filenames, 'path': paths})

		return images_df

	def filter_images_and_labels(self, images, labels):
		labels = labels.rename(columns = {'ImageId;;;;':'ImageId'})
		
		labels['ImageId'] = labels['ImageId'].str.replace(';;;;','')
		print(labels.head())
		df = pd.merge(images, labels, on='ImageId')

		df.dropna(inplace=True)
		df = df[~df['dc_creator'].str.contains('anoniem')]
		df = df[df['dc_creator'] != ' ']

		return df['path'].to_list(), df[CHALLENGE].to_list()

	def one_hot_encoding(self, labels):
		one_hot_encodings = list()
		encoder = LabelEncoder()
		self.n_labels = len(set(labels))

		encoder.fit(labels)
		encoded_y = encoder.transform(labels)

		final_y = np_utils.to_categorical(encoded_y, self.n_labels)

		one_hot_encodings.append(final_y)

		return one_hot_encodings

	def store_images_to_hdf5(self, path, images, split):
		f = h5py.File(path)
		dt = h5py.special_dtype(vlen=np.dtype('uint8'))
		dset = f.create_dataset(split, (len(images), ), dtype=dt)
			
		for i in range(0, len(images)):

			filename = images[i]
			with open(filename, 'rb') as fin:
				dset[i] = np.fromstring(fin.read(), dtype='uint8')

	def store_encodings_to_hdf5(self, path, encodings, split):
		f = h5py.File(path)
		dset = f.create_dataset(split, data=encodings)

	def make_data_splits(self, images, one_hot_encodings):
		for challenge in CHALLENGES:
			if not os.path.exists(self.dataset_storing_path+challenge+"/"): 
				os.makedirs(self.dataset_storing_path+challenge+"/")	

				training_images_path = self.dataset_storing_path+challenge+"/"+"test_newdata_images.hdf5"
				training_labels_path = self.dataset_storing_path+challenge+"/"+"test_newdata_labels.hdf5"
		
				self.hdf5_path = os.path.dirname(training_images_path)

				print("Storing in: ", self.hdf5_path)


				for labels in one_hot_encodings:
					#X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.1, random_state=42)
					X_train = images
					y_train = labels
					self.store_images_to_hdf5(training_images_path, X_train, 'X_train')
					self.store_encodings_to_hdf5(training_labels_path, y_train, 'y_train')

				print("The splits have been created!")
			else:
				print("The splits are already there!")
				self.hdf5_path = os.path.dirname(self.dataset_storing_path+challenge+"/")

	
	def start_experiment(self):

		images = self.get_images()
		labels = self.get_metadata()
		
		images, total_labels = self.filter_images_and_labels(images, labels)

		one_hot_encodings = self.one_hot_encoding(total_labels)

		self.make_data_splits(images, one_hot_encodings)

if __name__ == '__main__':
	
	import argparse 

	parser = argparse.ArgumentParser()

	parser.add_argument('--dataset_name', type=str)
	parser.add_argument('--ANN', type=str)
	parser.add_argument('--metadata_path', type=str)
	parser.add_argument('--jpg_images_path', type=str)
	parser.add_argument('--results_path', type=str)
	parser.add_argument('--datasets_path', type=str)
	parser.add_argument('--tl_mode', type=str)

	args = parser.parse_args()

	dataset_name = args.dataset_name
	ANN = args.ANN
	metadata_path = args.metadata_path
	jpg_images_path = args.jpg_images_path
	results_path = args.results_path
	datasets_path = args.datasets_path
	tl_mode = args.tl_mode
	experiment = ExperimentHandler(ANN, dataset_name, metadata_path, jpg_images_path, results_path, datasets_path, tl_mode)
	experiment.start_experiment()