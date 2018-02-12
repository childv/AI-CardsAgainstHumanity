# RNN that gives a sentence a 'Funny' ratings

# Inspired by: https://sourcedexter.com/tensorflow-text-classification-python/

import nltk
from nltk.stem.lancaster import LancasterStemmer
import tensorflow as tf
import tflearn
import numpy as np
import sys
import unicodedata
import json
import random

class RNN:
	def __init__(self):
		self.categories = []
		self.stemmer = LancasterStemmer() # initialize stemmer


		categorized_word_data, word_data = self.processTextData()
		train_set_words, train_set_labels = self.convertTextData(categorized_word_data, word_data)
		self.startTextClassification(train_set_words, train_set_labels)

	# method to remove punctuations from sentences.
	def remove_punctuation(self, text, tbl):
	    return text.translate(tbl)

	# Clean JSON data and form bag of words
	# Create lists "words" - hold unique stemmed words - and "categories" - hold classification categories
	# @return	list containing words from each sentence and category they belong to
	def processTextData(self):
		# a table structure to hold the different punctuation used
		tbl = dict.fromkeys(i for i in range(sys.maxunicode)
		                      if unicodedata.category(chr(i)).startswith('P'))
		 		 
		#variable to hold the Json data read from the file
		data = None
		 
		# read the json file and load the training data
		print("Reading data from json...")
		with open('data.json') as json_data:
		    data = json.load(json_data)
		    #print(data)
		 
		# get a list of all categories to train for
		self.categories = list(data.keys())
		words = []
		# a list of tuples with words in the sentence and category name 
		docs = []
		
		# Iterate through each classification 
		for each_category in data.keys():
			for each_sentence in data[each_category]: 
				# remove any punctuation from the sentence
				each_sentence = self.remove_punctuation(each_sentence, tbl)
				#print(each_sentence)

				# extract words from each sentence and append to the word list
				w = nltk.word_tokenize(each_sentence)
				#print ("tokenized words: ", w)
				words.extend(w)
				docs.append((w, each_category))
		 
		# stem and lower each word and remove duplicates
		words = [self.stemmer.stem(w.lower()) for w in words]
		words = sorted(list(set(words)))
		 
		#print(words)
		#print(docs)
		return docs, words

	# Apply bag of words model to convert text into numeric binary array for tensor flow
	# Storey labels/category in a numeric binary array
	def convertTextData(self, categorized_word_data, word_data):
		# create our training data
		training = []
		output = []
		# create an empty array for our output
		output_empty = [0] * len(self.categories)
		
		print("Creating bag of words array...")
		for doc in categorized_word_data:
			# initialize our bag of words(bow) for each document in the list
			bow = []
			# list of tokenized words for the pattern
			token_words = doc[0]
			# stem each word
			token_words = [self.stemmer.stem(word.lower()) for word in token_words]
			
			count = 0
			# create our bag of words array
			for w in word_data:

				# Print to one line dynamically
				count += 1
				sys.stdout.write("On word " + str(count) + " out of " + str(len(word_data) - count) + "                         \r",)
				sys.stdout.flush()

				bow.append(1) if w in token_words else bow.append(0)
			 
			output_row = list(output_empty)
			output_row[self.categories.index(doc[1])] = 1
			 
			# our training set will contain a the bag of words model and the output row that tells which catefory that bow belongs to.
			training.append([bow, output_row])

		# shuffle our features and turn into np.array as tensorflow  takes in numpy array
		random.shuffle(training)
		training = np.array(training)
		 
		# trainX contains the Bag of words and train_y contains the label/ category
		train_x = list(training[:,0])
		train_y = list(training[:,1])

		return train_x, train_y

	# Begin text classification
	# Build simple Deep Neural Net to train our model
	# @param train_x	bag of words list
	# @param train_y	label/category list
	def startTextClassification(self, train_x, train_y):
		print("Reseting underlying graph data...")
		# reset underlying graph data
		tf.reset_default_graph()
		# Build neural network
		print("Building neural network...")
		net = tflearn.input_data(shape=[None, len(train_x[0])])
		net = tflearn.fully_connected(net, 8)
		net = tflearn.fully_connected(net, 8)
		net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
		net = tflearn.regression(net)
		 
		# Define model and setup tensorboard
		print("Defining model...")
		model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
		# Start training (apply gradient descent algorithm)
		model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
		print("Saving model as: model.tflearn")
		model.save('model.tflearn')



def main():
	rnn = RNN()

if __name__ == '__main__':
	main()
