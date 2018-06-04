import numpy as np
from heap import Heap
from cluster import Cluster

def optics(cluster):
	j = 0
	L = [[float('infinity'),float('infinity')]] * len(cluster.X)
	X = range(len(cluster.X))
	
	for p in X:
		if not cluster.isProcessed(p):
			N, pkerndist = cluster.kernlVectors(p, rtype = 'id')
			cluster.markProcessed(p)
			L[j] = [float('infinity'), pkerndist, p] # push p
			j = j+1
			
			seeds = Heap()
			update(N, p, seeds, cluster)
			q = seeds.pop()
			
			while(q):
				NN, qkerndist = cluster.kernlVectors(q, rtype = 'id')
				L[j] = [cluster.vreachdist[q], qkerndist, q]
				j = j+1
				cluster.markProcessed(q)
				
				update(NN, q, seeds, cluster)
				q = seeds.pop()
	return L
	
	
def update(N, p, seeds, cluster):
	for q in N:
		if not cluster.isProcessed(q):
			reachdist = cluster.reachdist(q,p)
			if cluster.vreachdist[q] == float('infinity'):
				cluster.vreachdist[q] = reachdist
				seeds.push(q, reachdist)
			if cluster.vreachdist[q] > reachdist:
				cluster.vreachdist[q] = reachdist
				seeds.remove(q)
				seeds.push(q, reachdist)

'''extrahiere nur taeler'''		
def extract(L, points, threshold): 
	clusters =[[]]
	
	splits = [(rd < threshold, p) for rd, kd, p in L]
	for iscluster, p in splits:
		if iscluster: clusters[-1].append(points[p])
		elif len(clusters[-1]) > 0: clusters.append([])
	return clusters
	
	
	
