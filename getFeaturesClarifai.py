
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='cb8f9f6480f14aa19f97546ad12b55c3')

model = app.models.get('general-v1.3')

filename = 'trial_ids2.txt'

with open(filename, "r") as f:
		while True:
			line = f.readline()
			if not line:
				break
			data = line.split(",")
			try:
				image = ClImage(url=data[2])
				json = model.predict([image])
				output = json['outputs'][0]
				concepts = output['data']['concepts']
				features = [data[0], data[1]]
				for e in concepts:
					features.append(str(e['name']))
				print(",".join(features))
			except:
				pass
