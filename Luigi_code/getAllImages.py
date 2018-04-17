
import urllib.request
import os, sys

filename = "train.csv"

Landmarks = {}
Counts = {}

with open(filename, "r") as f:
		while True:
			line = f.readline()
			if not line:
				break
			data = line.strip().split(",")
			lID = data[2]
			iLink = data[1].strip("\"")
			iID = data[0].strip("\"")
			if lID in Landmarks:
				Landmarks[lID].add((iID,iLink))
			else:
				Landmarks[lID] = set([(iID, iLink)])

for k, v in Landmarks.items():
	Counts[k] = len(v)

#sum = 0
#sum2 = 0
#sum3 = 0
#for k, v in Counts.items():
#	if v < 975  or v > 1025:
#		if v > 850 and v < 1150:
#			print(k, v)
#			sum = sum + v
#	if v > 500:
#		if v < 1500:
#			sum2 = sum2 + 1
#			sum3 = sum3 + v
#		else:
#			sum2 = sum2 + 1
#			sum3 = sum3 + 1500
#print(sum)
#
#print(len(Counts.keys()))
#print(sum2, sum3)

ImageLimit = 100

# Make all directories
for k in Landmarks.keys():
	if Counts[k] > 250:
#		path = "/Users/Luigi/Desktop/M_Learning/Landmarks/Images/"+k
		path = "/Volumes/LG/Test/"+k
		os.mkdir(path);

for k, v in Landmarks.items():
	if Counts[k] > 250:
		i = 1
		for e in v:
			if i <= ImageLimit:
				path = "/Users/Luigi/Desktop/M_Learning/Landmarks/Images/"+k+"/"+str(i)+".jpg"
				path = "/Volumes/LG/Test/"+k+"/"+str(i)+".jpg"
				try:
					urllib.request.urlretrieve(e[1],path)
					i = i + 1
				except:
					pass
		print(k)








##Counts Checking
#Lsum = len(Counts.keys())
#sum1 = 0
#c1 = 100
#sum2 = 0
#c2 = 250
#sum3 = 0
#c3 = 200
#for k, v in Counts.items():
#	if v > c1:
#		sum1 = sum1 + 1
#	if v > c2:
#		sum2 = sum2 + 1
#	if v > c3:
#		sum3 = sum3 + 1
#
#t1 = (((sum1*c1)/1000.0)*7.25)/60.0
#t2 = (((sum2*c1 )/1000.0)*7.25)/60.0
#t3 = (((sum3*c3)/1000.0)*7.25)/60.0
#
#print(str(Lsum)+" Landmarks\n")
#print(str(sum1)+" Landmarks (>"+str(c1)+") and would take: "+str(t1)+" hours")
#print(str(Lsum - sum1)+" Landmarks (<"+str(c1)+")\n")
#print(str(sum2)+" Landmarks (>"+str(c2)+") and would take: "+str(t2)+" hours")
#print(str(Lsum - sum2)+" Landmarks (<"+str(c2)+")\n")
#print(str(sum3)+" Landmarks (>"+str(c3)+") and would take: "+str(t3)+" hours")
#print(str(Lsum - sum3)+" Landmarks (<"+str(c3)+")")


