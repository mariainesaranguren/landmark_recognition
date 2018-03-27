#!/usr/bin/python

FeatureCounts = {}
Totals ={}
FeatureProbs = {}

filename = 'clarifaiResults.csv'

with open(filename, "r") as f:
		while True:
			line = f.readline()
			if not line:
				break
			data = line.split(",")
			if data[0] not in FeatureCounts:
				FeatureCounts[data[0]] = {}
				Totals[data[0]] = 0
			Totals[data[0]] += 1
			for e in data[2:]:
				if e not in FeatureCounts[data[0]]:
					FeatureCounts[data[0]][e] = 0
				if e in FeatureCounts[data[0]]:
					FeatureCounts[data[0]][e] += 1

for k, v in FeatureCounts.items():
	features = []
	for ek, ev in v.items():
		if float(ev)/float(Totals[k]) > 0.5:
			features.append((ek.strip(), float(ev)/float(Totals[k])))
#		if float(ev)/float(Totals[k]) > 1:
##			print "error", k, ev, Totals[k]
		FeatureProbs[k] = features

for k, v in FeatureProbs.items():
#	print(k+","+(",".join(v)))
	print k, v

