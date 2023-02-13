import sys
import time # For timing
import math
import numpy as np
import matplotlib.pyplot as plt

import heapq

def create_KdTree(P, depth = 0):
	n = len(P)
	if n == 1:
		return [None, None, P[0]]
	if n > 1:
		P.sort(key=lambda x: x[:][depth % 2]) # Sorting based on the 1st or 2nd coordinate, depending from depth being even or odd
		median = math.floor(n/2)
		return [create_KdTree(P[:median], depth + 1), create_KdTree(P[median + 1:], depth + 1), P[median]]

def euclidean_distance(p1,p2):
	x1, y1 = p1
	x2, y2 = p2
	
	dx = x1-x2
	dy = y1-y2

	return math.sqrt(dx * dx + dy * dy)

def manhattan_distance(p1,p2):
	x1, y1 = p1
	x2, y2 = p2

	dx = x1-x2
	dy = y1-y2
	return abs(dx) + abs(dy)

def brute_force_knn(P,newP,dist,k):
	pointDistances = []
	for point in P: 
		pointDist = (point,dist(point[0],newP)) # Get the point and the distance from the newP
		pointDistances.append(pointDist)

	pointDistances.sort(key=lambda x : x[1])

	return [tup[0] for tup in pointDistances[:k]]

def kd_nearest(kd,newP,dist,best_node,best_distance,li,depth = 0):
	if kd is None:
		return best_node,best_distance
	
	node = kd[2][0]
	
	if not node:
		return best_node, _best_distance

	d = dist(newP, node)

	if d < best_distance and node not in li: # if node is in l, just ignore it
		best_node = node
		best_distance = d

	if newP[depth % 2] < node[depth % 2]:
		good_side = kd[0]
		bad_side = kd[1]
	else:
		good_side = kd[1]
		bad_side = kd[0]


	best_node, best_distance = kd_nearest(good_side,newP,dist,best_node,best_distance,li,depth + 1)

	if abs(node[depth % 2] - newP[depth % 2]) < best_distance:
		best_node, best_distance = kd_nearest(bad_side,newP,dist,best_node,best_distance,li,depth + 1)

	return best_node, best_distance

def kd_get_knn(kd,newP,dist,k):
	li = []
	for i in range(0,k):
		best_node,best_distance = kd_nearest(kd,newP,dist,None,np.infty,li)
		li.append(best_node)
	return li

def main():
	try:
		N = int(sys.argv[1])
	except:
		N = int(input("How many random points do you want to be generated? "))

	try:
		k = int(sys.argv[2])
	except:
		k = int(input("How many nearest neighbours do you want to have? "))

	# (x,y) coordinates and a random boolean indicating what "type" of point it is 
	P = [((np.random.uniform(0,200),np.random.uniform(0,200)),np.random.randint(2)) for i in range(N)] 
	newP = (np.random.uniform(0,200),np.random.uniform(0,200))

	t0 = time.time()
	knn = brute_force_knn(P,newP,euclidean_distance,k)
	t1 = time.time()

	print("Calculating knn with brute force did " + str(t1-t0) + " seconds")

	print(knn)
	print('\n')

	count_zero = 0
	for p in knn:
		if p[1] == 0:
			count_zero += 1

	if count_zero > k/2:
		print("By naive knn with k = " + str(k) +  ", newP probably belongs to the \"zero\" category!")
	else:
		print("By naive knn with k = " + str(k) +  ", newP probably belongs to the \"one\" category!")

	# We remove the type of the point in order to print it
	P_plot = [pl[0] for pl in P] 
	knn_plot = [pl[0] for pl in knn]
	# In order to plot
	P_plot = np.array(P_plot)
	knn_plot = np.array(knn_plot)

	t0 = time.time()
	kd = create_KdTree(P)
	t1 = time.time()

	print("Kdtree creating did " + str(t1-t0) + " seconds")

	t0 = time.time()
	print(kd_get_knn(kd,newP,euclidean_distance,k))
	t1= time.time()

	print("Calculating knn with use of kdtrees did " + str(t1-t0) + " seconds")

	plt.plot(P_plot[:,0],P_plot[:,1], '.r') # Red for the other points
	plt.plot(newP[0],newP[1],'.k') # Black for newP, the point we calculate its neighbours
	plt.plot(knn_plot[:,0],knn_plot[:,1], '.b') # Blue for the k-nearest neigbours
	plt.show()



if __name__ == '__main__':
	main()
