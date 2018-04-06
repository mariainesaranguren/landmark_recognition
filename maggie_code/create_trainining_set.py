'''
'''
import math
import numpy as np
from PIL import Image
from urllib import urlopen
from scipy import misc
import os
from urlparse import urlparse
from os.path import splitext, basename
from resizeimage import resizeimage
import tensorflow as tf
from collections import OrderedDict

def read_csv_to_dict():
	TRAINING_FILE = "../train.csv"

	# Total number of images in the csv
	total_num_imgs = 1225029

	# Current number of imgs processed
	num_imgs_processed = 0

	# Target number of imgs processed (the ones we want to handle so far)
	target_num_imgs_processed = int(math.ceil(total_num_imgs * .2))

	# Dictionary where the value is the list of landmark image urls and the key is
	# the landmark image id
	landmarks = OrderedDict()

	# Read the images and landmark ids into the dictionary
	with open(TRAINING_FILE, "r") as f:
		while num_imgs_processed < target_num_imgs_processed:
			line = f.readline()
			if not line:
				break
			data = line.strip().split(",")
			landmark_id = data[2]
			landmark_link = data[1]
			image_id = data[0]

			if landmark_link[1:-1] == "url":
				continue
			else:
			

				if landmark_id in landmarks:
					landmarks[landmark_id].append([landmark_link, image_id])
				else:
					landmarks[landmark_id]  = []
					landmarks[landmark_id].append([landmark_link, image_id])
				num_imgs_processed += 1
	return landmarks

def download_landmark_imgs(landmarks):
	NEW_WIDTH = 96
	NEW_HEIGHT = 96

	print "Beginning landmark imgs download to data folder"
	# Download the landmark images to separate directories
	# Download the images for only 100 landmarks for now
	landmark_download_num = 100
	current_downloaded_num = 0

	# Making sure there's not too many images downloaded
	images_downloaded = 0
	max_images_downloaded = 100

	# Dictionaries for 
	for landmark_id in landmarks.keys():
		images_downloaded = 0
		if current_downloaded_num <= landmark_download_num:
			print "Processing: ", landmark_id

			# Make a directory for this landmark id
			if not os.path.exists(landmark_id):
				os.makedirs("data/"+landmark_id)

			# Download the images into the appropriate dir for this landmark
			list_of_imgs = landmarks[landmark_id]
			for landmark_img_link_and_id in list_of_imgs:
				if images_downloaded >= max_images_downloaded:
					break

				# Get the link and id
				img_link = landmark_img_link_and_id[0][1:-1]
				img_id = landmark_img_link_and_id[1][1:-1]

				# Open the url
				url_object = urlopen(img_link)

				# Download the img
				try: 
					im = Image.open(url_object)
					images_downloaded += 1

					# Resize the image
					cover = resizeimage.resize_cover(im, [NEW_WIDTH, NEW_HEIGHT])

					# Convert to rgb
					rgb = cover.convert('RGB')

					# Save the image to appropriate directory
					rgb.save("data/"+landmark_id+"/"+img_id+".jpg", 'JPEG')

				except IOError as error:
					print error
			current_downloaded_num += 1

		else:
			print "Done downloading ", landmark_download_num, " landmarks."
			break

def generate_lists():

	print "Generating lists for tensorflow"
	
	folders_list = []
	labels_list = []
	images_list = []
	tf_label_landmark_label = OrderedDict()
	counter = 0

	for folder in os.listdir("data"):
		# Map the tf label to the landmark label
		if folder not in tf_label_landmark_label.keys():
			tf_label_landmark_label[folder] = counter

		folders_list.append(folder)
		images = []
		labels = []
		for image in os.listdir("data/"+folder):
			images.append("data/"+folder+"/"+image)
			labels.append(counter)
		images_list.append(images)
		labels_list.append(labels)
		counter += 1

	for folder_key in tf_label_landmark_label.keys():
		print folder_key, " = ", tf_label_landmark_label[folder_key]

	print "There are ", len(folders_list), " different landmarks."

	hstack_image_list = np.hstack(images_list)
	hstack_label_list = np.hstack(labels_list)

	temp = np.array([hstack_image_list, hstack_label_list])
	temp = temp.transpose()
	np.random.shuffle(temp)

	image_list = list(temp[:, 0])
	label_list = list(temp[:, 1])
	label_list = [int(i) for i in label_list]


	return image_list, label_list

def get_batch(image, label, image_W, image_H, batch_size, capacity):
	'''
	Args:
		image: list type
		label: list type
		image_W: image width
		image_H: image height
		batch_size: batch size
		capacity: the maximum elements in queue
	Returns:
		image_batch: 4D tensor [batch_size, width, height, 3], dtype=tf.float32
		label_batch: 1D tensor [batch_size], dtype=tf.int32
	'''
	
	image = tf.cast(image, tf.string)
	label = tf.cast(label, tf.int32)

	# make an input queue
	input_queue = tf.train.slice_input_producer([image, label])
	
	label = input_queue[1]
	image_contents = tf.read_file(input_queue[0])
	image = tf.image.decode_jpeg(image_contents, channels=3)
	
	######################################
	# data argumentation should go to here
	######################################
	
	image = tf.image.resize_image_with_crop_or_pad(image, image_W, image_H)
	
	# if you want to test the generated batches of images, you might want to comment the following line.

	image = tf.image.per_image_standardization(image)
	
	image_batch, label_batch = tf.train.batch([image, label],
						batch_size= batch_size,
						num_threads= 64, 
						capacity = capacity)
	
	#you can also use shuffle_batch 
#    image_batch, label_batch = tf.train.shuffle_batch([image,label],
#                                                      batch_size=BATCH_SIZE,
#                                                      num_threads=64,
#                                                      capacity=CAPACITY,
#                                                      min_after_dequeue=CAPACITY-1)
	
	label_batch = tf.reshape(label_batch, [batch_size])
	image_batch = tf.cast(image_batch, tf.float32)
	
	return image_batch, label_batch

	











