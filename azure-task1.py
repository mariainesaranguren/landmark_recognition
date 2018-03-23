#!/usr/bin/env python
# # -*- coding: utf-8 -*-
'''
Course:		Machine Learning CSE 40625
Assignment:	Final Project
Date:		Friday March 23 2018
Author:		Margaret Thomann
Decription:	To establish initial results for this final project, a test set of 50 
			landmarks was identified.  The ids for these 50 landmarks were recorded in the
			file "trial_ids.txt."  This program reads in those images and passes them to 
			the Microsoft Azure Computer Vision API, which assigns each image a set of 
			tags related to the content of the image.  These tags are then stored in a
			dictionary of dictionaries.  The key of the outer dictionary is the landmark
			id and the value of that is a dictionary where the key is the image id and the
			value is the list of tags related to the content of the image.
'''
# Imports
import requests

# API Keys
KEY_1 = "0f03da15d4534a5a84f8c8924d66dc51"
KEY_2 = "85097f8cf94a4753bbbd692b7f521330"

# Azure Code
subscription_key = KEY_1
assert subscription_key
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
vision_analyze_url = vision_base_url + "analyze"

# Open the trial_ids.txt file and read in the landmark ids into a list
print "Reading in trial ids..."
print "------"
trial_ids_file = open("trial_ids.txt", "r")
trial_ids_list = []
for id in trial_ids_file:
	trial_ids_list.append(id.split("--> ",1)[1].strip())
	
# Process each of the ids in the trial_ids_list and retrieve the images for that landmark
# id: store these image urls in a list.  Create a dictionary that is indexed by the 
# landmark id as a string and has the list of image urls as a value.
print "Retreiving image links for ids..."
print "------" 
training_file = open("train.csv", "r")
trial_ids_images_dict = {}
for id in trial_ids_list:
	image_url_list = []
	for line in training_file:
		data = line.strip().split(",")
		landmark_id = data[2]
		landmark_image_url = data[1]
		if landmark_id == id:
			image_url_list.append(landmark_image_url.replace('"', ''))
	trial_ids_images_dict[id] = image_url_list
	
# Process each image stored in the trial_ids_images_dict
azure_results_dict = {}
for id in trial_ids_images_dict.keys():
	list_of_image_urls = trial_ids_images_dict[id]
	for image_url in list_of_image_urls:
		print "Image url:", image_url
		headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
		params   = {'visualFeatures': 'Categories,Description,Color'}
		data     = {'url': image_url}
		response = requests.post(vision_analyze_url, headers=headers, params=params, json=data)
		response.raise_for_status()
		analysis = response.json()
		print analysis
		break
		

	