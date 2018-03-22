#!/usr/bin/python

filename = "train.csv"

Landmarks = {}

with open(filename, "r") as f:
		while True:
			line = f.readline()
			if not line:
				break
			data = line.strip().split(",")
			lID = data[2]
			lLink = data[1]
			if lID in Landmarks:
				Landmarks[lID].add(lLink)
			else:
				Landmarks[lID] = set([lLink])

for k, v in Landmarks.items():
	print k
	for e in v:
		print e.strip('\"')
	break
