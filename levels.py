import pygame

class Level:
	BG_COLOR = (100, 200, 100) #grass color
	LANE_WIDTH = 100 #pixels
	LINE_WIDTH = 20 #pixels

	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.sub_layer = pygame.sprite.Group();
		self.road_layer = pygame.sprite.Group();
		self.top_layer = pygame.sprite.Group();

	#draw the level on the target surface such that the pixel at x, y is at the top left of the target.
	def draw(self, target, x, y):
		self._set_translate(x, y)
		w = target.get_width()
		h = target.get_height()

		target.fill(Level.BG_COLOR)
		self.sub_layer.draw(target)
		self.road_layer.draw(target)
		self.top_layer.draw(target)
		pass

	def add_horizontal_road(self, start_x, end_x, y):
		pass

	def add_vertical_road(self, x, start_y, end_y):
		pass

	def add_intersection(self, x, y):
		#x, y is the center of the intersection
		#intersection is a square with a side length of 2*LANE_WIDTH
		pass

	#internal method used to set the translation of all sprites relative to their starting position.
	def _set_translate(self, x, y):
		for sprite in self.sub_layer.sprites():
			sprite._set_translate(x, y)
		for sprite in self.road_layer.sprites():
			sprite._set_translate(x, y)
		for sprite in self.top_layer.sprites():
			sprite._set_translate(x, y)

class rectSprite(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color):
		super().__init__(self)
		self.rel_x = x;
		self.rel_y = y;

		self.image = pygame.Surface([width, height])
       	self.image.fill(color)

      	self.rect = self.image.get_rect()

	def _set_translate(self, x, y):
		self.rect.x = x - self.rel_x
		self.rect.y = y - self.rel_y

class imageSprite(pygame.sprite.Sprite):
	def __init__(self, x, y, image_path):
		super().__init__(self)
		self.rel_x = x;
		self.rel_y = y;

		self.image = pygame.image.load(image_path)
		self.rect = self.image.get_rect()

	def _set_translate(self, x, y):
		self.rect.x = x - self.rel_x
		self.rect.y = y - self.rel_y
