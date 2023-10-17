'''
Design considerations:

A level consists of a grid of Tiles, which may contain roads, intersections, background, or scenery.
Levels will be imported from a static file of some sort, perhaps a JSON file?


Other attributes
width (in tiles)
height (in tiles)

scale (pixels per tile)

starting car position (pixels)
finish line position (pixels)

methods:
draw(x, y) -> draw the level, offset by (x, y) pixels. 
That is, draw the level such that (x, y) is at the center of the screen.

get_path(x, y) -> get the path closest to the point x, y.
each path will have a method get_neighbors

'''
from Tile import Tile

class Level():
	#map tile id numbers to class names
	tile_map = [

	]
	def __init__(self, filepath):
		#import data from static file
		self.tile_grid = []
		self.width = 0
		self.height = 0
		self.scale = 100 #constant
		self.start_pos = (0, 0) #tuple of (x, y) position
		self.finish_pos = (0, 0) #tuple of (x, y) position
		self.route [] #car starts at a specific path. we can then define its route as a set of directions ("straight", "left", "right")

	def draw(self, x, y):
		pass
	def get_path(self, x, y):
		pass

