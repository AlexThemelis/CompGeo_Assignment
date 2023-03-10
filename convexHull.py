import sys
import time # For timing
import numpy as np
import matplotlib.pyplot as plt

def CW(p0, p1, p2): # Predicate gives true if the 3 points define a right turn
	if (p2[1]-p0[1])*(p1[0]-p0[0]) - (p1[1]-p0[1])*(p2[0]-p0[0]) < 0: # The determinant in its computational form
		return True
	return False

def predicate_3D(p0,p1,p2,p3):
	a = np.array([[1,p0[0],p0[1],p0[2]], [1,p1[0],p1[1],p1[2]], [1,p1[0],p1[1],p1[2]], [1,p2[0],p2[1],p2[2]], [1,p3[0],p3[1],p3[2]]])
	if np.linalg.det(a) > 0:
		return True
	return False


def Incremental(P):
	P.sort()			# Sort the set of points by the x coordinate
	L_upper = [P[0], P[1]]		# Initialization of L_upper
	# We compute L_upper
	for i in range(2,len(P)):
		L_upper.append(P[i])
		while len(L_upper) > 2 and not CW(L_upper[-1],L_upper[-2],L_upper[-3]): # If the 3 points define a left turn, delete the medium one
			del L_upper[-2]
	L_lower = [P[-1], P[-2]]	# Initialization of L_upper
	# We compute L_lower
	for i in range(len(P)-3,-1,-1):
		L_lower.append(P[i])
		while len(L_lower) > 2 and not CW(L_lower[-1],L_lower[-2],L_lower[-3]): # If the 3 points define a left turn, delete the medium one
			del L_lower[-2]
	# We delete first and last points of L_lower because there are in L_upper 
	del L_lower[0]
	del L_lower[-1]
	L = L_upper + L_lower		# Build the full hull, '+' here means connecting the 2 lists
	return np.array(L)

def GiftWrapping_2D(S):
	n = len(S)
	P = [None] * n
	r0 = np.where(S[:,0] == np.min(S[:,0])) # This way you get the point with the smallest x coordinate (probably change the code, make it clearer)
	r = S[r0[0][0]] # Initialization of that point
	i = 0
	while True:
		P[i] = r
		u = S[0]
		for j in range(n):
			t = S[j]
			if (u[0] == r[0] and u[1] == r[1]) or CW(r,u,t):
				u = t
		i += 1
		r = u
		if u[0] == P[0][0] and u[1] == P[0][1]: # If the end point is the starting point, then we finished
			break

	for i in range(n): # We created in the start as P = [none] * n because we didn't knew the exact number of points in the convex hull
		if P[-1] is None: # So we delete from the end all the empty spaces, in order to create an array of size exactly the number of points in the convex Hull
			del P[-1]
	return np.array(P)

# def Incremental_3D(S):
# 	n = len(S)
# 	P = [None] * n
	

def plot_2D(L,P_2D):	
	plt.figure()
	plt.plot(L[:,0],L[:,1], 'r-')
	plt.plot([L[-1,0],L[0,0]],[L[-1,1],L[0,1]], 'r-') # Check why is this the last part of the convex hull, the last 2 dots connected and why it can't be in above
	plt.plot(P_2D[:,0],P_2D[:,1],".b")
	plt.show()


def main():
	try:
		N = int(sys.argv[1])
	except:
		N = int(input("How many random points do you want to be generated? "))
	
	# N points with coordinates in [0,200)x[0,200)
	P_2D = [(np.random.uniform(0,200),np.random.uniform(0,200)) for i in range(N)]
	#  N points with coordinates in [0,200)x[0,200)x[0,200)
	P_3D = np.array([(np.random.uniform(0,200),np.random.uniform(0,200),np.random.uniform(0,200)) for i in range(N)])

	# GrahamScan algorithm for computing Convex Hull 2D
	t0 = time.time()
	L = Incremental(P_2D)
	t1 = time.time()
	print("The points of the convex Hull generated by incremental algorithm are ")
	print(L)
	P_2D = np.array(P_2D) # in order to plot, we make the P_2D array (We didn't create an array from the start in order to sort the points lexicographically) 
	print("Incremental did " + str(t1-t0) + " seconds")
	
	plot_2D(L,P_2D)

	# GiftWrapping algorithm for computing Convex Hull 2D
	t0 = time.time()
	L = GiftWrapping_2D(P_2D)
	t1 = time.time()
	print("The points of the convex Hull generated by the GiftWrapping algorithm are ")
	print(L)
	print("GiftWrapping_2D did " + str(t1-t0) + " seconds")

	plot_2D(L,P_2D)

	# # Plot the computed Convex Hull for 3D
	# fig = plt.figure()
	# ax = fig.add_subplot(111,projection='3d')
	# ax.set_xlabel('X Label')
	# ax.set_ylabel('Y Label')
	# ax.set_zlabel('Z Label')
	# for i in range(N):
	# 	ax.scatter(P_3D[i,0], P_3D[i,1], P_3D[i,2], c='b', marker='o')
	# plt.show()

if __name__ == '__main__':
  main()