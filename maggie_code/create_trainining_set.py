'''
'''
import math
import numpy as np
from PIL import Image
from urllib import urlopen
from scipy import misc
from resizeimage import resizeimage

TRAINING_FILE = "train.csv"
NEW_WIDTH = 96
NEW_HEIGHT = 96

# Total number of images in the csv
total_num_imgs = 1225029

# Current number of imgs processed
num_imgs_processed = 0

# Target number of imgs processed (the ones we want to handle so far)
target_num_imgs_processed = int(math.ceil(total_num_imgs * .2))

# Dictionary where the value is the list of landmark image urls and the key is
# the landmark image id
landmarks = {}

# Read the images and landmark ids into the dictionary
with open(TRAINING_FILE, "r") as f:
	while num_imgs_processed < target_num_imgs_processed:
		line = f.readline()
		if not line:
			break
		data = line.strip().split(",")
		landmark_id = data[2]
		landmark_link = data[1]
		if landmark_id in landmarks:
			landmarks[landmark_id].add(landmark_link)
		else:
			landmarks[landmark_id] = set([landmark_link])
		num_imgs_processed += 1

# Process the dictionary images by cropping them and converting them to
# a binary representation

# Dictionary below will contain rgb matrices
# 		key = landmark id
# 		value = list of rgb matrices
landmark_rgb_matrix = {}
counter = 0
for landmark_id in landmarks.keys():
	print "Processing: ", landmark_id, "\n"
	list_of_imgs = landmarks[landmark_id]
	for landmark_img_link in list_of_imgs:

		# Download the img
		im = Image.open(urlopen(landmark_img_link[1:-1]))

		# Resize the image
		cover = resizeimage.resize_cover(im, [NEW_WIDTH, NEW_HEIGHT])

		# Get the rgb pixels
		pixels = list(cover.getdata())
		
		# Add it to the dictionary
		if landmark_id not in landmark_rgb_matrix.keys():
			landmark_rgb_matrix[landmark_id] = []
			landmark_rgb_matrix[landmark_id].append(pixels)
		else:
			landmark_rgb_matrix[landmark_id].append(pixels)
	


	











