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

'''

class Level():
	def __init__(self, filepath):
		#import data from static file
		self.tile_grid = []
		self.width = 0
		self.height = 0
		self.scale = 100 #constant
		self.start_pos = (0, 0) #tuple of (x, y) position
		self.finish_pos = (0, 0) #tuple of (x, y) position

	def draw(self, x, y):
		pass