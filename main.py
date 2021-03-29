import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
import numpy as np
from math import atan2

matplotlib.rc('figure', figsize=(7.5, 7.5))

import argparse

PAUSE_TIME = 0.01
EPS = 1e-6

def area_segment(x0, y0, x1, y1, x2, y2):
	return ((x1-x0)*(y2-y0) - (x2-x0)*(y1-y0))/2.0

def collinear(a, b, c):
	return np.cross(b-a, c-a) == 0

def left_on(a, b, c):
	return np.cross(b-a, c-a) >= 0

def dist_2d(x, y):
	return np.linalg.norm(x-y)

def change_title(s):
    plt.title(s, fontsize=16)
    plt.draw()

def area_sector(x0, y0, r, x1, y1, x2, y2):
	vector_1, vector_2 = [x1-x0, y1-y0], [x2-x0, y2-y0]
	unit_vector_1, unit_vector_2 = vector_1 / np.linalg.norm(vector_1), vector_2 / np.linalg.norm(vector_2)
	dot_product = np.dot(unit_vector_1, unit_vector_2)
	if(dot_product > 1.0):
		dot_product = 1.0
	if(dot_product < -1.0):
		dot_product = -1.0
	theta = np.arccos(dot_product)
	return 0.5*theta*np.square(r) if left_on(np.array([x0, y0]), np.array([x1, y1]), np.array([x2, y2])) else -0.5*theta*np.square(r)

# In this function I take the parametric equation of line passing x1, y1 and x2, y2.
# This is substituted in the equation of circle to solve for parameter t.
# It is 0 for one of the endpoints of segment and 1 for the other.
def circle_segment_area(x0, y0, r, x1, y1, x2, y2):
	if(collinear(np.array([x0, y0]), np.array([x1, y1]), np.array([x2, y2]))):
		return 0
	a = np.square(x2-x1) + np.square(y2-y1)
	b = 2*((x2-x1)*(x1-x0)+(y2-y1)*(y1-y0))
	c = np.square(x1-x0) + np.square(y1-y0) - np.square(r)
	# line doesn't intersect circle, area is the chord of angle subtended by the segment at the circle
	if(np.square(b) < 4*a*c):
		return area_sector(x0, y0, r, x1, y1, x2, y2)
	t_1 = (-b + np.sqrt(np.square(b)-(4*a*c)))/(2.0*a)
	t_2 = (-b - np.sqrt(np.square(b)-(4*a*c)))/(2.0*a)
	t1, t2 = min(t_1, t_2), max(t_1, t_2)
	# segment is cmopletely outside the circle
	if((t1 <= 0 and t2 <= 0) or (t1 >= 1 and t2 >= 1)):
		return area_sector(x0, y0, r, x1, y1, x2, y2)
	# point 1 is interior and point 2 is exterior
	if(t1 <= 0 and 0 <= t2 and t2 <= 1):
		return area_segment(x0, y0, x1, y1, x1+t2*(x2-x1), y1+t2*(y2-y1)) + area_sector(x0, y0, r, x1+t2*(x2-x1), y1+t2*(y2-y1), x2, y2)
	# intersection at two points with the circle
	if(t1 <= 0 and t2 >= 1):
		return area_segment(x0, y0, x1, y1, x2, y2)
	# both points are exterior and intersect at two positions
	if(0 <= t1 and t2 <= 1):
		return area_sector(x0, y0, r, x1, y1, x1+t1*(x2-x1), y1+t1*(y2-y1)) + area_segment(x0, y0, x1+t1*(x2-x1), y1+t1*(y2-y1), x1+t2*(x2-x1), y1+t2*(y2-y1)) + area_sector(x0, y0, r, x1+t2*(x2-x1), y1+t2*(y2-y1), x2, y2)
	# point 1 is exterior and point 2 is interior
	if(0 <= t1 and t1 <= 1 and 1 <= t2):
		return area_sector(x0, y0, r, x1, y1, x1+t1*(x2-x1), y1+t1*(y2-y1)) + area_segment(x0, y0, x1+t1*(x2-x1), y1+t1*(y2-y1), x2, y2)
	return 0

def draw_polygon(points):
	n = len(points)
	for i in range(n):
		plt.plot(points[i]['x'], points[i]['y'], 'ko')
		ax.add_line(Line2D([points[i]['x'], points[(i+1)%n]['x']], [points[i]['y'], points[(i+1)%n]['y']], color='k'))
	plt.draw()
	plt.waitforbuttonpress()

def circle_poly_area(args, x0, y0, r, points):
	if(args.animation):
		circle = ax.add_artist(Circle((x0, y0), radius=r))
		plt.draw()
	area = 0.0
	n = len(points)
	for i in range(n):
		area += circle_segment_area(x0, y0, r, points[i]['x'], points[i]['y'], points[(i+1)%n]['x'], points[(i+1)%n]['y'])
	if(args.animation):
		plt.pause(PAUSE_TIME)
		circle.remove()
	return area

def make_dense_points(points, delta):
	n = len(points)
	dense_points = []
	for i in range(n):
		dense_points.append(points[i])
		dist = dist_2d(np.array([points[i]['x'], points[i]['y']]), np.array([points[(i+1)%n]['x'], points[(i+1)%n]['y']]))
		if(dist > delta):
			x = int(dist/(delta+EPS))+1
			dense_points += [ 
				{'x': points[i]['x'] + (float(t)/float(x))*(points[(i+1)%n]['x']-points[i]['x']), 
				'y':points[i]['y'] + (float(t)/float(x))*(points[(i+1)%n]['y']-points[i]['y'])} 
				for t in range(1, x)
			]
	return dense_points

def contained_in_disk(c, points, r):
	max_dist = -1.0
	for p in points:
		max_dist = max(max_dist, dist_2d(np.array([c['x'], c['y']]), np.array([p['x'], p['y']])))
	return max_dist <= r

def toy_test():
	p1 = {'x':-1, 'y':0}
	p2 = {'x':-1.414, 'y':-1.414}

	c = {'x':0, 'y':0}
	r = 1

	ax.add_line(Line2D([p1['x'], p2['x']], [p1['y'], p2['y']], color='k'))
	ax.add_artist(Circle((c['x'], c['y']), radius=r))

	print( circle_segment_area(c['x'], c['y'], r, p1['x'], p1['y'], p2['x'], p2['y']) )
	plt.show()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Fatness of a polygon.')
	parser.add_argument('--input_type', type=str, help='path to the dataset, stdin for mousing in the points')
	parser.add_argument('--delta', type=float, help='the input parameter delta')
	parser.add_argument('--rho', type=float, help='the input parameter rho')
	parser.add_argument('--animation', type=int, default=0, help='show the animation')

	args = parser.parse_args()

	plt.clf()
	plt.axis([-5.0, 5.0, -5.0, 5.0])
	ax = plt.gca()
	ax.set_aspect('equal')
	plt.setp(ax, autoscale_on=False)

	if args.input_type is None:
		print("USAGE: python main.py --input_type input.txt --delta 1.0 --rho 0.5 --animation 0")
		print ("Please specify the input type. Exiting.")
		exit()
	elif args.input_type == "stdin":
		num_points = int(input('Enter the number of points: '))
		points = []
		while(num_points > 0):
			points += plt.ginput(1, timeout=-1)
			if(len(points) > 1):
				plt.plot([points[len(points)-2][0], points[len(points)-1][0]], [points[len(points)-2][1], points[len(points)-1][1]], 'g-')
				plt.plot([points[len(points)-2][0], points[len(points)-1][0]], [points[len(points)-2][1], points[len(points)-1][1]], 'go')
				plt.draw()
			else:
				plt.plot(points[0][0], points[0][1], 'go')
				plt.draw()
			num_points -= 1
		plt.waitforbuttonpress()
		points = [ {'x':float(p[0]), 'y':float(p[1])} for p in points]
	else:
		points = []
		with open(args.input_type, 'r') as f:
			points = [ { 'x':float(line.strip().split(' ')[0]), 'y':float(line.strip().split(' ')[1]) }  for line in f.readlines()]

	draw_polygon(points)
	# print(points)
	dense_points = make_dense_points(points, args.delta)
	draw_polygon(dense_points)

	min_int = 99999999999999.0
	for i in range(1, 15):
		for p in dense_points:
			if(contained_in_disk(p, points, args.rho*i) == True):
				continue
			intersection_area = abs(circle_poly_area(args, p['x'], p['y'], args.rho*i, dense_points))
			ratio = intersection_area/(np.pi*np.square(args.rho*i))
			min_int = min(min_int, ratio)
	print("Fatness value: ", min_int)
	change_title("Fatness value: "+str(min_int))

	plt.show()


