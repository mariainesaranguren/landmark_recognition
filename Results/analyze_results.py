''' Analyzes results from csv files created from newtest2.py '''

import sys
import pandas as pd

def get_average(l):
    return (sum(l)/len(l))

def get_statistics(l):
    s = pd.Series(l)
    return s.describe()

if len(sys.argv) != 2 or sys.argv[1] == "-h":
    print ("Usage: python analyze_predictions.py results.csv")
    exit()
input_file = sys.argv[1]

# Parses csv files
f = open(input_file, "r")
results = f.readlines()
landmark_confidence = {}                # landmark_id : [confidence]
landmark_rank = {}                      # landmark_id : [rank]
all_confidence = []
all_rank = []
f.close()
for img in results:
    img = img[:-2]                      # Strip new line character
    img_result = img.split(",")
    landmark_id = img_result[0]
    img_id = img_result[1].split(".")[0]
    rank = float(img_result[2])
    confidence = float(img_result[3])

    all_rank.append(rank)
    all_confidence.append(confidence)

    if landmark_id in landmark_confidence.keys() and landmark_id in landmark_rank.keys():
        landmark_confidence[landmark_id].append(confidence)
        landmark_rank[landmark_id].append(rank)
    else:
        landmark_confidence[landmark_id] = [confidence]
        landmark_rank[landmark_id] = [rank]

# Average confidence and rank per landmark:
average_landmark_confidence = []        # List of average confidence of each landmark
average_landmark_rank = []              # List of average rank of each landmark
for landmark_id in landmark_confidence.keys():
    average_landmark_confidence.append(get_average(landmark_confidence[landmark_id]))
    average_landmark_rank.append(get_average(landmark_rank[landmark_id]))

# Total number of predictions
print ("*** General ***")
print ("Total number of predictions made:\t", len(all_rank))
print ("Total number of landmarks involved:\t", len(landmark_confidence.keys()))

# CONFIDENCE
# Confidence is 0 if it is not in one of the top five guesses
print ("\n*** Confidence ***")
weighted_score = sum(all_confidence)
print ("Summation of all confidences:\t\t", weighted_score)
confidence_spread = get_statistics(average_landmark_confidence)
print ("Spread of confidence results:")
print ("\tMin:", confidence_spread['min'])
print ("\tStd:", confidence_spread['std'])
print ("\t25%:", confidence_spread['25%'])
print ("\t50%:", confidence_spread['50%'])
print ("\t75%:", confidence_spread['75%'])
print ("\tMax:", confidence_spread['max'])
print ("* Note that a confidence of 0 is given to images that are not identified with 5 guesses.")


# RANK
# Count of each rank
count_rank = {}
for rank in all_rank:
    if rank in count_rank.keys():
        count_rank[rank] += 1
    else:
        count_rank[rank] = 1
print ("\n*** Rank ***")
print ("Count of each rank level:\t\t", count_rank)
print ("P(Not Identified):\t\t\t", count_rank[0]/len(all_rank))
for n in range(1, 6):
    identified = 0
    for i in range(1,n+1):
        identified += count_rank[i]
    print ("P(Identified landmark in top", n, "guesses):", identified/len(all_rank))











#
