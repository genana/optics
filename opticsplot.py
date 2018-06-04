import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import axes3d

import numpy as np

import itertools
import random

from heap import Heap
from cluster import Cluster
from optics import *

' standard distance is the euclidian norm, override '
def eucldist(x,y):
	d = x-y
	norm = np.sqrt(np.dot(d,d))
	return norm
	
def transpose(dimensionVec):
	dim = len(dimensionVec)
	count = len(dimensionVec[0])
	vectors = [[0 for k in range(dim)]] * count
	for i in range(count):
		v =  [0 for k in range(dim)]
		for j in range(dim):
			v[j] = dimensionVec[j][i]
		vectors[i] = v
	return vectors

def plotOpticCurve(rdist, plt):
	x = np.arange(0.0, len(rDistance), 1)
	plt.figure(1)
	plt.fill_between(x, 0, rdist, label='reachdistance')
	#line, = plt.plot(kDistance, 'ro', label='sdfsdf')
	#plt.legend([line])
	#plt.plot(rDistance, 'bo')	
	plt.ylabel('some numbers')

def plotData(data, plt): 
	colors = ("red", "green", "blue", 'gray', 'yellow')
	groups = ("0", "1", "2", '3', '4')
	
	# Create plot
	#ax = fig.add_subplot(1, 1, 1, axisbg="1.0")
	fig, ax = plt.subplots()
	ax.legend(loc="upper right")
	ax = fig.gca(projection='3d')
	proxy = []
	for data, color, group in zip(data, colors, groups):
		x, y, z = data
		ax.scatter(x, y, z, alpha=0.8, c=color, edgecolors='none', s=30, label=group)
		proxy.append(matplotlib.lines.Line2D([0],[0], linestyle="none", c=color, marker = 'o'))
		
	ax.legend(proxy, groups, numpoints = 1)
	
	plt.title('sample data')

# Create data
N = 80
R = 5*N
g1 = (5 + 0.96*np.random.rand(N), 1+2*np.random.rand(N),2+0.8*np.random.rand(N))
g2 = (3+ 1.4 * np.random.rand(N), 2+1.1*np.random.rand(N),4+np.random.rand(N))
g3 = (4+1.6*np.random.rand(N),5+1.4*np.random.rand(N),2+1.7*np.random.rand(N))
g4 = (1+np.random.rand(N),3+0.9*np.random.rand(N),1.1*np.random.rand(N))
g5 = (8*np.random.rand(R),6*np.random.rand(R),6*np.random.rand(R)) #rauschen

origdata = (g1, g2, g3, g4, g5)
orig_clusters = [transpose(d) for d in origdata]
X = []
for c in orig_clusters: X += c
#X = transpose(g1) + transpose(g2) + transpose(g3) + transpose(g4) + transpose(g5)
random.shuffle(X)
print(len(X))

X = map(np.array, X)

cluster = Cluster(X, eucldist, 12, 99)
L = optics(cluster)

# extract clusters from optic curve
s = 0
for rd, kd, p in L: 
	if rd < float('infinity'): s += rd
avg = s / len(X)
threshold = 0.9*avg
print('sum',s, 'avg', avg, 'threshold', threshold) 

clusters = extract(L, X, threshold)
clusters = filter(lambda c: len(c) > 0, clusters)
print('clusters', len(clusters))
clusteredData = [transpose(c) for c in clusters]

# show accuracy
all_errors = 0
all_points = N*4
for i in range(len(clusters)):
	cluster = clusters[i]
	max_indx = -1
	max_acc = -float('infinity')
	max_inc = 0
	max_err = 0
	for j in range(len(orig_clusters)):
		org_cluster = orig_clusters[j]
		r = 0
		for v in cluster: 
			for w in org_cluster:
				if np.array_equal(v,w): 
					r += 1
					break
			
		err = len(cluster)+len(org_cluster) - 2*r
		acc = 1.00-float(err)/len(org_cluster)
		inc = float(r)/len(org_cluster)
		if acc > max_acc:
			max_acc = acc
			max_indx = j
			max_err = err
		if(inc > max_inc):
			max_inc = inc
	if(max_acc > 0.01): all_errors += max_err
	print('gen. cluster ' + str(i) + ' could extract cluster ' + str(max_indx) + ' with acc. ' + str(max_acc))
	print('gen. cluster ' + str(i) + ' inherts points of cluster ' + str(max_indx) + ' with acc. ' + str(max_inc))
print ('accuracy sum: ' + str(1.0-float(all_errors)/all_points))
				

rDistance = map(lambda v: v[0], L)
kDistance = map(lambda v: v[1], L)

plotOpticCurve(rDistance, plt)
plotData(origdata, plt)
plotData(clusteredData, plt)

plt.show()
