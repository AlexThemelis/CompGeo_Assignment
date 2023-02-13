import sys
import time # For timing
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.spatial import Delaunay

def main():
    try:
        N = int(sys.argv[1])
    except:
        N = int(input("How many random points do you want to be generated? "))
    
    P = np.array([(np.random.randint(0,200),np.random.randint(0,200)) for i in range(N)])

    t0 = time.time()
    vor = Voronoi(P)
    t1 = time.time()
    fig = voronoi_plot_2d(vor)
    #plt.show()

    t2 = time.time()
    tri = Delaunay(P)
    t3 = time.time()
    plt.triplot(P[:,0], P[:,1], tri.simplices)
    plt.plot(P[:,0], P[:,1], 'o')
    

    plt.show()

    print("The Voronoi diagram took  " + str(t1-t0) + " seconds to be created with " + str(N) + " number of points!")
    print("The Delaunay triangulation took  " + str(t3-t2) + " seconds to be created with " + str(N) + " number of points!")

if __name__ == '__main__':
  main()