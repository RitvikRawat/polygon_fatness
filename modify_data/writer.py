import json

values  = []
with open('all.txt') as f:
	values = [x.strip() for x in f.readlines()]

with open('data.geojson') as f:
		data = json.load(f)

for idx, _ in enumerate(data['features']):
	data['features'][idx]['properties']['fatness'] = values[idx]

with open('data_new.geojson', 'w') as f:
		json.dump(data, f)

