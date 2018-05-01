'''
'''
import math
import numpy as np
from PIL import Image
from scipy import misc
from resizeimage import resizeimage
import pickle
import sys
import os

image_dir = "/Users/mariainesaranguren/Desktop/ML_luigi/Images"
NEW_WIDTH = 256
NEW_HEIGHT = 256

# Traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(image_dir):
	path = root.split(os.sep)
	print("Resizing directory", os.path.basename(root))
	for image_file in files:
	# Go through each image in the list and resize it
		print ("Resizing image", image_dir+"/"+os.path.basename(root)+"/"+image_file)
		# Read the images and landmark ids into the dictionary
		with open(image_dir+"/"+os.path.basename(root)+"/"+image_file, "rb") as f:
			try:
				# Resize the image
				img = Image.open(image_dir+"/"+os.path.basename(root)+"/"+image_file)
				img_resized = resizeimage.resize_cover(img, [NEW_WIDTH, NEW_HEIGHT])
				img_resized.save(image_dir+"/"+os.path.basename(root)+"/"+image_file)
			except:
				print ("Error")
				pass















			#
