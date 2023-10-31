import pygame
import math
import os
import random

class Level:
    BG_COLOR = (100, 200, 100) #grass color
    LANE_COLOR = (120, 120, 120)
    Y_LINE_COLOR = (200, 200, 100)
    W_LINE_COLOR = (200, 200, 200)

    LANE_WIDTH = 100 #pixels
    LINE_WIDTH = 5 #pixels

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sub_layer = pygame.sprite.Group();
        self.road_layer = pygame.sprite.Group();
        self.top_layer = pygame.sprite.Group();
        self.x = -1
        self.y = -1

    #draw the level on the target surface such that the pixel at x, y is at the top left of the target.
    def draw(self, target, x, y, debug=False):

        self._set_translate(x, y)

        target.fill(Level.BG_COLOR)
        if debug:
            self.road_layer.draw(target)
        else:
            self.sub_layer.draw(target)
            self.top_layer.draw(target)

        self.x = x
        self.y = y

    def add_horizontal_road(self, start_x, end_x, y):
        #two lanes.
        #gap b/t lanes is 3x line width
        #outside shoulder is 3x line width on each side.
        total_width = Level.LANE_WIDTH * 2 + Level.LINE_WIDTH * 9
        total_length = end_x - start_x

        top = math.floor(y - total_width/2)
        lane_1_y = math.floor(top + Level.LINE_WIDTH*3 + Level.LANE_WIDTH/2)
        lane_2_y = math.floor(top + Level.LINE_WIDTH*6 + Level.LANE_WIDTH*1.5)

        self.sub_layer.add(
            #1px padding to protect from rounding errors
            RectSprite(start_x - 1, top - 1, total_length + 2, total_width + 2, Level.LANE_COLOR)
        )
        self.road_layer.add(
            RoadLane(end_x, lane_1_y, start_x, lane_1_y),
            RoadLane(start_x, lane_2_y, end_x, lane_2_y)
        )
        self.top_layer.add(
            RectSprite(start_x, top + Level.LINE_WIDTH*2, 
                total_length, Level.LINE_WIDTH, 
                Level.W_LINE_COLOR),
            RectSprite(start_x, top + Level.LINE_WIDTH*3 + Level.LANE_WIDTH, 
                total_length, Level.LINE_WIDTH, 
                Level.Y_LINE_COLOR),
            RectSprite(start_x, top + Level.LINE_WIDTH*5 + Level.LANE_WIDTH, 
                total_length, Level.LINE_WIDTH, 
                Level.Y_LINE_COLOR),
            RectSprite(start_x, top + Level.LINE_WIDTH*6 + Level.LANE_WIDTH*2, 
                total_length, Level.LINE_WIDTH, 
                Level.W_LINE_COLOR),
        )

    def add_vertical_road(self, x, start_y, end_y):
        total_width = Level.LANE_WIDTH * 2 + Level.LINE_WIDTH * 9
        total_length = end_y - start_y

        left = math.floor(x - total_width/2)
        lane_1_x = math.floor(left + Level.LINE_WIDTH*3 + Level.LANE_WIDTH/2)
        lane_2_x = math.floor(left + Level.LINE_WIDTH*6 + Level.LANE_WIDTH*1.5)

        self.sub_layer.add(
            RectSprite(left-1, start_y-1, total_width+2, total_length+2, Level.LANE_COLOR)
        )
        self.road_layer.add(
            RoadLane(lane_1_x, start_y, lane_1_x, end_y),
            RoadLane(lane_2_x, end_y, lane_2_x, start_y)
        )
        self.top_layer.add(
            RectSprite(left + Level.LINE_WIDTH*2, start_y,
                Level.LINE_WIDTH, total_length,
                Level.W_LINE_COLOR),
            RectSprite(left + Level.LINE_WIDTH*3 + Level.LANE_WIDTH, start_y, 
                Level.LINE_WIDTH, total_length, 
                Level.Y_LINE_COLOR),
            RectSprite(left + Level.LINE_WIDTH*5 + Level.LANE_WIDTH, start_y,  
                Level.LINE_WIDTH, total_length, 
                Level.Y_LINE_COLOR),
            RectSprite(left + Level.LINE_WIDTH*6 + Level.LANE_WIDTH*2, start_y, 
                Level.LINE_WIDTH, total_length, 
                Level.W_LINE_COLOR),
        )
    def add_diagonal_road(self, x1, y1, x2, y2):
        #road implementation supporting diagonals
        total_width = Level.LANE_WIDTH * 2 + Level.LINE_WIDTH * 9
        slope = math.atan2(y2 - y1, x2 - x1)
        move_para = lambda x, y, dist: (x + math.cos(slope)*dist, y + math.sin(slope)*dist)
        move_perp = lambda x, y, dist: (x + math.cos(slope + math.pi/2)*dist, y + math.sin(slope + math.pi/2)*dist)

        self.sub_layer.add(
            RoadLane(x1, y1, x2, y2, width=total_width)
        )
        #TODO: lines and lanes

    def add_intersection(self, x, y):
        #x, y is the center of the intersection
        #intersection is a square with a side length of 2*LANE_WIDTH + 3*LINE_WIDTH
        width = 2*Level.LANE_WIDTH + 3*Level.LINE_WIDTH
        sx = math.floor(x - width/2)
        sy = math.floor(y - width/2)

        inner_lane = Level.LANE_WIDTH*0.5
        outer_lane = Level.LANE_WIDTH*1.5 + Level.LINE_WIDTH*3

        self.sub_layer.add(
            RectSprite(sx, sy, width, width, Level.LANE_COLOR)
        )
        self.road_layer.add(
            #only straight-line lanes for now.
            RoadLane(sx, sy + inner_lane, sx + width, sy + inner_lane),
            RoadLane(sx, sy + outer_lane, sx + width, sy + outer_lane),
            RoadLane(sx + inner_lane, sy, sx + inner_lane, sy + width),
            RoadLane(sx + outer_lane, sy, sx + outer_lane, sy + width)
        )

    def add_random_decorations(self,n):
        #adds n random decorations. Flowers, grass, rocks.
        DECORATION_PATHS = [
            os.path.join("assets", "flower-blue.png"),
            os.path.join("assets", "flower-white.png"),
            #os.path.join("assets", "pebbles.png"),
        ]
        self._set_translate(self.x, self.y)
        for _ in range(n):
            img = ImageSprite(
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.choice(DECORATION_PATHS)
            )
            img.scale(0.5)
            img._set_translate(self.x, self.y)
            if pygame.sprite.spritecollideany(img, self.sub_layer) == None:
                self.sub_layer.add(img)

    def join_road_paths(self):
        #searches for road lanes that are connected and automatically stitches their paths together
        #ignores any roads that already have a connection set for nextTarget

    #internal method used to set the translation of all sprites relative to their starting position.
    def _set_translate(self, x, y):
        for sprite in self.sub_layer.sprites():
            sprite._set_translate(x, y)
        for sprite in self.road_layer.sprites():
            sprite._set_translate(x, y)
        for sprite in self.top_layer.sprites():
            sprite._set_translate(x, y)

    def get_target(self, sprite):
        #returns the road lane that the given sprite is colliding with
        for lane in self.road_layer.sprites():
            if pygame.sprite.collide_mask(sprite, lane) != None:
                return lane
        return None;


#just a plain rectangle.
#since roads are dynamic in length and made up of these,
#they will consist of these.
class RectSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rel_x = x;
        self.rel_y = y;

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def _set_translate(self, x, y):
        self.rect.x = self.rel_x - x
        self.rect.y = self.rel_y - y


#will be used for grass, flowers, road signs, decorations, etc
#basically evertything that isnt a simple rectangle.
class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.rel_x = x;
        self.rel_y = y;

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def scale(self, factor):
        size = self.rect.size
        new_size = (math.floor(size[0] * factor), math.floor(size[1] * factor))
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()


    def _set_translate(self, x, y):
        self.rect.x = self.rel_x - x
        self.rect.y = self.rel_y - y

class RoadLane(RectSprite):
    #(x, y) and (x2, y2) are the endpoints of the center of the lane.
    def __init__(self, x, y, x2, y2, width=Level.LANE_WIDTH, color=Level.LANE_COLOR):
        super().__init__(x, y, math.dist((x, y), (x2, y2)), width, color)

        self.direction = math.degrees(math.atan2(y2 - y, x2 - x))
        center = ((x + x2) / 2, (y + y2) / 2)

        #figure out rotation and movement of rel_x and rel_y
        self.image = pygame.transform.rotate(self.image, self.direction)
        self.rect = self.image.get_rect()

        size = self.image.get_size()
        self.rel_x = math.floor(center[0] - 0.5*size[0])
        self.rel_y = math.floor(center[1] - 0.5*size[1])

        #x, y, stop
        self.target_points = [
            (x, y, False),
            (x2, y2, False)
        ]

        #other RoadLane objects.
        self.next_target = {
            "left": None,
            "straight": None,
            "right": None
        }

class StopZone(RoadLane):
    def __init__(self, x, y, x2, y2):
        super().__init__(x, y, x2, y2)
        self.target_points = [
            (x, y, False),
            (math.floor((x + x2) / 2), math.floor((y + y2) / 2), True),
            (x2, y2, False)
        ]
        self.can_go = False

