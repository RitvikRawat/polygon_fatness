import json

def scale_points(i, points):
	x_min, x_max, y_min, y_max = 99999, -99999, 99999, -99999
	del_x, del_y, coordinates_range = 0.0, 0.0, 0.0
	for p in points[0][0]:
		x_min, x_max = min(x_min, p[0]), max(x_max, p[0])
		y_min, y_max = min(y_min, p[1]), max(y_max, p[1])
		del_x, del_y = x_max-x_min, y_max-y_min
		coordinates_range = max(del_x, del_y)
	with open('nyc_data/example_%05d' % i, 'w') as f:
		for p in points[0][0][:-1]:
			x = -4.0 + 8*(p[0]-x_min)/coordinates_range
			y = -4.0 + 8*(p[1]-y_min)/coordinates_range
			f.write(str(x)+' '+str(y)+'\n')



with open('data.geojson') as f:
    data = json.load(f)

for i, feature in enumerate(data['features']):
    scale_points(i, feature['geometry']['coordinates'])
    # if i > 10:
    # 	break