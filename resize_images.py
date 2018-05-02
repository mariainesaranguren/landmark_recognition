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

if len(sys.argv) < 2:
	print ("Usage: python resize_images.py path/to/images")
	exit()

# image_dir = "/Users/mariainesaranguren/Desktop/ML_luigi/Images"
image_dir = sys.argv[1]

NEW_WIDTH = 256
NEW_HEIGHT = 256

print ("Opening up images on ", image_dir)

# Traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(image_dir_maggie):
	# Ignore hidden files
	files = [f for f in files if not f[0] == '.']
    	dirs[:] = [d for d in dirs if not d[0] == '.']

    	# Continue program
	path = root.split(os.sep)
	print("Currently on directory", os.path.basename(root))
	for image_file in files:
	# Go through each image in the list and resize it
		print ("Resizing image", image_dir_maggie+"/"+os.path.basename(root)+"/"+image_file)
		# Read the images and landmark ids into the dictionary
		with open(image_dir_maggie+"/"+os.path.basename(root)+"/"+image_file, "rb") as f:
			try:
				# Resize the image
				img = Image.open(image_dir_maggie+"/"+os.path.basename(root)+"/"+image_file)
				img_resized = resizeimage.resize_cover(img, [NEW_WIDTH, NEW_HEIGHT])
				img_resized.save(image_dir_maggie+"/"+os.path.basename(root)+"/"+image_file)
			except:
				print ("Error")
				pass















			#
