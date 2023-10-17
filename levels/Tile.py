class Tile:
	def __init__(self, scale):
		#each tile type will have a fixed image and set of paths (based on its type)
		self.scale = scale #pixel dimensions of tile.
		self.image = "" #path to image
		self.paths = [] #list of road paths through tile.

	def get_path(self, x, y):
		#scan paths, return closest path
		pass
