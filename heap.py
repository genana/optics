'idea https://docs.python.org/2/library/heapq.html'

REMOVED = '<removed-item>'
from heapq import *

class Heap:
	def __init__(self):
		self.pq = []
		self.entry_finder = {} 

	def push(self,item, priority=0):
		'Add a new task or update the priority of an existing task'
		if item in self.entry_finder:
			remove(task)
		entry = [priority, item]
		self.entry_finder[item] = entry
		heappush(self.pq, entry)

	def remove(self,item):
		'Mark an existing task as REMOVED.  Raise KeyError if not found.'
		entry = self.entry_finder.pop(item)
		entry[-1] = REMOVED

	def pop(self):
		'Remove and return the lowest priority task. Raise KeyError if empty.'
		while self.pq:
			priority, item = heappop(self.pq)
			if item is not REMOVED:
				del self.entry_finder[item]
				return item
		return False
