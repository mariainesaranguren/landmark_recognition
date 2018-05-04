''' Analyzes results from csv files created from newtest2.py '''

import sys
import pandas as pd

def get_average(l):
    return (sum(l)/len(l))

def get_statistics(l):
    s = pd.Series(l)
    return s.describe()

input_files = ["Results/res0.csv", "Results/res1.csv", "Results/res3.csv"]   # TODO replace with correct files
bootstrap_predict_made = []
bootstrap_landmarks_involved = []
bootstrap_conf_sum = []
bootstrap_conf_min = []
bootstrap_conf_std = []
bootstrap_conf_25 = []
bootstrap_conf_50 = []
bootstrap_conf_75 = []
bootstrap_conf_max = []
bootstrap_rank_counts = []
bootstrap_identified_P = [[],[],[],[],[]]

# ****** PART ONE: Collects results from csv and records results ******
for input in input_files:
    # Parses csv files
    f = open(input, "r")
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
    bootstrap_predict_made.append(len(all_rank))
    bootstrap_landmarks_involved.append(len(landmark_confidence.keys()))

    # CONFIDENCE
    # Confidence is 0 if it is not in one of the top five guesses
    confidence_summation = sum(all_confidence)
    bootstrap_conf_sum.append(confidence_summation)
    confidence_spread = get_statistics(average_landmark_confidence)
    bootstrap_conf_min.append(confidence_spread['min'])
    bootstrap_conf_std.append(confidence_spread['std'])
    bootstrap_conf_25.append(confidence_spread['25%'])
    bootstrap_conf_50.append(confidence_spread['50%'])
    bootstrap_conf_75.append(confidence_spread['75%'])
    bootstrap_conf_max.append(confidence_spread['max'])


    # RANK
    # Count of each rank
    count_rank = {}
    for rank in all_rank:
        if rank in count_rank.keys():
            count_rank[rank] += 1
        else:
            count_rank[rank] = 1
    bootstrap_rank_counts.append(count_rank)
    bootstrap_identified_P[0].append(count_rank[0]/len(all_rank) if 0 in count_rank.keys() else 0)
    for n in range(1, 5):                   # Iterating on lists in bootstrap_identified_P where index i matches to i+1 top votes
        identified = 0
        for i in range(1,n+1):              # Cumulative sum (ex: top 3 means rank==1 + rank==2 + rank==3)
            identified += count_rank[i] if i in count_rank.keys() else 0
        bootstrap_identified_P[n].append(identified/len(all_rank))


# ****** PART TWO: Averages results across bootstraps  ******
print ("------- Overall results across bootstraps: ------- ")
print ("*** General: ***")
print ("Average number of predictions made: ", get_average(bootstrap_predict_made))
print ("Number of landmarks involved:", get_average(bootstrap_landmarks_involved))      # In this case they're all the same because of how the sampling was done

print ("\n*** Ranking in predictions: ***")
for rank in range(6):        # [0, 1, 2, 3, 4, 5]
    count = 0
    for bootstrap in bootstrap_rank_counts:
        count += bootstrap[rank]
    if rank == 0:
        print ("Average count of landmarks not identified:\t\t\t", count/float(len(bootstrap_rank_counts)))
    else:
        print ("Average count of correct identifications with prediction #", rank, ":", count/float(len(bootstrap_rank_counts)))
for n in range(len(bootstrap_identified_P)):
    print ("Average P(Identified in top", n+1, "guesses): ", get_average(bootstrap_identified_P[n]))


print ("\n*** Confidence: ***")
print ("Average summation of all confidences:", get_average(bootstrap_conf_sum))
print ("Average confidence min:", get_average(bootstrap_conf_min))
print ("Average confidence std dev:", get_average(bootstrap_conf_std))
print ("Average confidence 25%:", get_average(bootstrap_conf_25))
print ("Average confidence 50%:", get_average(bootstrap_conf_50))
print ("Average confidence 75%:", get_average(bootstrap_conf_75))
print ("Average confidence max:", get_average(bootstrap_conf_max))









#
