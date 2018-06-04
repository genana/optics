 
class Cluster:
	def __init__(self, points, dist, minPts, eps):
		self.X = points
		self.processed = [False] * len(points)
		self.vreachdist = [float('infinity')] * len(points)
		self.vkernldist = [float('infinity')] * len(points)
		
		self.minPts = minPts
		self.eps = eps
		self.dist = dist
	
	def kernldist(self, x):
		if len(self.X) < self.minPts: 
			return float('infinity')
		if(type(x) == int):
			if self.vkernldist[x] < float('infinity'):
				return self.vkernldist[x]
			x = self.X[x]
			
		distances = map(lambda y: self.dist(x,y), self.X)
		distances.sort()
		i = 0
		while(i < self.minPts and distances[i] <= self.eps): i = i+1
		
		#undefined, because N_eps has not enough
		if i < self.minPts:
			return float('infinity')
		else:
			return distances[i-1]

	def reachdist(self, x, p):
		if type(x) == int:
			if self.vkernldist[x] < float('infinity'):
				kd = self.vkernldist[x]
			else:
				kd = self.kernldist(x)
			x = self.X[x]
		else:
			kd = self.kernldist(x)
			
		if(type(p) == int):
			p = self.X[p]
			
		#return self.dist(x,p)
		return max(kd, self.dist(x,p))
		
	def markProcessed(self, i):
		self.processed[i] = True
	
	def isProcessed(self, i):
		return self.processed[i]
	
	'''
	returns kernel vectors sorted by length
	'''		
	def kernlVectors(self, x, scale=1, rtype = 'vec'):
		if len(self.X) < self.minPts: 
			return [], float('infinity')
		if type(x) == int: 
			x = self.X[x]
		
		# like kernel distance
		distances = map(lambda y: self.dist(x,y), self.X)
		perm = sorted(range(len(distances)), key = lambda key: distances[key])
		distances.sort()
		i = 0
		while i < self.minPts and distances[i] <= self.eps*scale: i = i+1
		
		#undefined, because N_eps has not enough
		if i < self.minPts:
			return [], float('infinity')
		else:
			self.vkernldist[perm[self.minPts-1]] = distances[self.minPts-1]
			if rtype == 'vec':
				vectors = [[0,0,0]]*self.minPts
				for i in range(self.minPts):
					vectors[i] = X[perm[i]]
				return vectors, distances[self.minPts-1]
			if rtype == 'id':
				return perm[:i], distances[self.minPts-1]
