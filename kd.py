import sys
import math
import numpy as np
import matplotlib.pyplot as plt

def create_KdTree(P, depth = 0):
	n = len(P)
	if n == 1:
		return [None, None, P[0]]
	if n > 1:
		P.sort(key=lambda x: x[depth % 2]) # Sorting based on the 1st or 2nd coordinate, depending from depth being even or odd
		median = math.floor(n/2)
		return [create_KdTree(P[:median], depth + 1), create_KdTree(P[median + 1:], depth + 1), P[median]]

def plot_KdTree(P,kd,N,depth = 0):
	if kd is None:
		return
	if depth % 2 == 0:
		plt.axvline(x = kd[2][0], color = 'b')
	else:
		plt.axhline(y = kd[2][1], color = 'r')

	plot_KdTree(P, kd[0], N, depth + 1)
	plot_KdTree(P, kd[1], N, depth + 1)


def main():
	try:
		N = int(sys.argv[1])
	except:
		N = int(input("How many random points do you want to be generated? "))
	
	P = [(np.random.randint(0,200),np.random.randint(0,200)) for i in range(N)] 

	kd = create_KdTree(P)

	print(kd)

	P = np.array(P) 
	plt.figure()
	plt.plot(P[:,0],P[:,1], '.r') # Red for the other points
	plot_KdTree(P,kd,N)
	plt.show()


if __name__ == '__main__':
	main()