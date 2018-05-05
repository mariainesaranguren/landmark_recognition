'''
This script will iteratively test the trained model using the generated testing,
which is imported and stored in loaded pickle file. To test the model the following
shell command is performed:
		python -m scripts.label_image> --graph=<PATH_TO_TRAINED_MODEL> --image=<PATH_TO_TEST_IMAGE>
'''

import os, sys
from subprocess import PIPE, run
import pickle

''' Helper function to execute shell commands'''
def out(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

''' Helper function to format label_image output into csv file to allow for further analysis on results'''
def get_result(output, true_landmark_id, imageName):
	prediction_confidence = 0.0
	prediction_rank = 0		# Model returns top 5 predictions for given image, this will store the rank of the prediction
	rank_counter = 1			# Counter used to keep track of line number in output therefore getting rank of prediction
	for line in output.split("\n"):
		if line.split(' ')[0] != "Evaluation" and line != '':	# Used to ignore useless header in output
			prediction_landmark = line.split(' ')[0]
			if prediction_landmark == landmark_id:				# If predicted class equals actual class:
				prediction_confidence = line.split(' ')[1]		# prediction confidence value is stored
				prediction_rank = rank_counter					# prediction rank is stored
			rank_counter = rank_counter + 1
	return true_landmark_id + "," + str(imageName) + "," + str(prediction_rank) + "," + str(prediction_confidence) + "\n"	# Results are returned in csv format

''' Helper function to keep track of progress '''
def get_progress(progress_counter, landmark_count):
	progress_percentage = int(progress_counter)/int(landmark_count)			# Progess as a percentage
	print(str(progress_percentage) + "% of the landmarks have been processed (" + str(progress_counter) + "/" + str(landmark_count) + ")")			# Prints to screen progress percentage

if __name__ == '__main__':
	if len(sys.argv) != 5 or sys.argv[1] == "-h":
		print ("Usage: python newtest2.py pickle_file graph_path output_path images_path")

	pickle_file = sys.argv[1]
	model_path = sys.argv[2]
	output_path = sys.argv[3]
	images_path = sys.argv[4]

	file_object = open(pickle_file, 'rb')		# open the binary file for reading {landmark_id:[img_files]}
	testing_set = pickle.load(file_object)		# load the dictionary from the file into testing_set
	progress_counter = 0

	# Iterate through all test images and print results to csv
	with open(output_path, 'w') as outputfile_object:
		for folder_path, image_list in testing_set.items():								# Iterating through landmark in dict
			landmark_id = folder_path.split('/')[len(folder_path.split('/')) - 1]		# Extracting landmark_id from folder_path
			for image in image_list:													# Iterating through testing set images for given landmark
				image_path = images_path + landmark_id + "/" + image					# Full path to image using folder path and image name
				command = "python -m scripts.label_image --graph=" + model_path + " --image=" + image_path		# Shell command is generated
				output = out(command)													# Calls helper function to execute command and stores output (TEMP)*
				outputfile_object.write(get_result(output, landmark_id, image))			# Calls helper function to parse output and get CSV formated results	(TEMP)*
			get_progress(progress_counter, len(testing_set))							# Calling helper function to display progress
			progress_counter = progress_counter + 1										# counter to keep track of processed landmarks

