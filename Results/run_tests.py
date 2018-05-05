'''
This script will iteratively test the trained model using the generated testing,
whcih is imported and stored in loaded pickle file. To test the model the following
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
def getResult(output, landmarkID, imageName):
	predictionConfidence = 0.0
	predictionRank = 0		# Model returns top5 predictions for given image, this will store the rank of the prediction
	rankCounter = 1			# Counter used to keep track of line number in output therefore getting rank of prediction
	for line in output.split("\n"):
		if line.split(' ')[0] != "Evaluation" and line != '':	# Used to ignore useless header in output
			if line.split(' ')[0] == landmarkID:				# If predicted class equals actual class:
				predictionConfidence = line.split(' ')[1]			# prediction confidence value is stored
				predictionRank = rankCounter						# prediction rank is stored
			rankCounter = rankCounter + 1
	#print(landmarkID + "," + str(imageName) + "," + str(predictionRank) + "," + str(predictionConfidence) + "\n")
	return landmarkID + "," + str(imageName) + "," + str(predictionRank) + "," + str(predictionConfidence) + "\n"		# Results are returned in csv format

''' Helper function to keep track of progress '''
def getProgress(progressCounter, landmarkCount):
	progressPercentage = int(progressCounter)/int(landmarkCount)			# Progess as a percentage
	print(str(progressPercentage) + "% of the landmarks have been processed (" + str(progressCounter) + "/" + str(landmarkCount) + ")")			# Prints to screen progress percentage

'''
Loading dictionary that contains testing set images stored in the following format:
	{
		Key = Path to image (Landmark ID) -> Class
		Value = List of Image names
	}
 '''

pklFile = "/Users/Luigi/Desktop/retrained/testing_images_bootstrap_1.pkl"			# Path to pickle file (TEMP)

fileObject = open(pklFile, 'rb')			# open the binary file for reading
testingSet = pickle.load(fileObject)		# load the dictionary from the file into testingSet

modelPath = "/Users/Luigi/Desktop/retrained/retrained_graph_1.pb"					# Path to model will change depending on testing iteration (TEMP)*
progressCounter = 0

outputPath = "/Users/Luigi/Desktop/res1.csv"						# Path to output file (TEMP)*

imagesFolderPath = "/Users/Luigi/Desktop/Images/"

'''
Code to iterate and test all images in testign set, while printed csv formated results to outfile
'''
with open(outputPath, 'w') as outputFileObject:
	for folderPath, imageList in testingSet.items():		# Iterating through landmark in dict
		landmarkID = folderPath.split('/')[len(folderPath.split('/')) - 1]		# Extracting landmarkID from folderPath
		for image in imageList:							# Iterating through testing set images for given landmark
			imagePath = imagesFolderPath + landmarkID + "/" + image		# Full path to image using folder path and image name
			command = "python -m scripts.label_image --graph=" + modelPath + " --image=" + imagePath		# Shell command is generated
			#outputFileObject.write(command+"\n")				# printing output for verification (TEMP)*
			output = out(command)				# Calls helper function to execute command and stores output (TEMP)*
			outputFileObject.write(getResult(output, landmarkID, image))			# Calls helper function to parse output and get CSV formated results	(TEMP)*
		getProgress(progressCounter, len(testingSet))			# Calling helper function to display progress
		progressCounter = progressCounter + 1					# counter to keep track of processed landmarks
