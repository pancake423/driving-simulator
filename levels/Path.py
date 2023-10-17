'''
defines a valid path (lane or route through an intersection) for a car to travel on.


'''
class Path:
	def __init__(self):
		self.nodes = [] #each node needs to have an x, y location. Does it also need 
		self.next = {
			"left": None,
			"straight": None,
			"right": None,
		}
	
	def get_distance(x, y):
		#return the distance from the point (x, y) to the closest point on the path.
		pass

	def get_nodes():
		#return a list of the path's nodes (AI cars will follow these nodes to trace the path)
	def get_next(direction="straight"):
		return self.next[direction]

	def join():
		#append another path to the current path.
		pass

	def translate(x, y):
		#shift every node in the current path by x, y pixels. Erases next (since roads will no longer be connected.)
		pass

	def copy():
		#returns a copy of a path.
		pass
