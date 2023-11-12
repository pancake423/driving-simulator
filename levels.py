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
    STUB_ROAD_LEN = 200 #pixels
    STOP_LINE_WIDTH = 25 #pixels
    DASH_LEN = 30

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
        self.add_diagonal_road(start_x, y, end_x, y)

    def add_vertical_road(self, x, start_y, end_y):
        self.add_diagonal_road(x, start_y, x, end_y)

    def add_diagonal_road(self, x1, y1, x2, y2):
        #road implementation supporting diagonals
        total_width = Level.LANE_WIDTH * 2 + Level.LINE_WIDTH * 9
        slope = math.atan2(y2-y1, x2-x1)
        move_para = lambda x, y, dist: (x + math.cos(slope)*dist, y + math.sin(slope)*dist)
        def move_perp (x, y, dist): 
            return (x + math.cos(slope + math.pi/2)*dist, y + math.sin(slope + math.pi/2)*dist)

        self.sub_layer.add(
            RoadLane(x1, y1, x2, y2, width=total_width)
        )
        self.road_layer.add(
            RoadLane(
                *move_perp(x1, y1, Level.LANE_WIDTH/2 + Level.LINE_WIDTH*1.5),
                *move_perp(x2, y2, Level.LANE_WIDTH/2 + Level.LINE_WIDTH*1.5),
            ),
            RoadLane(
                *move_perp(x2, y2, Level.LANE_WIDTH/-2 + Level.LINE_WIDTH*-1.5),
                *move_perp(x1, y1, Level.LANE_WIDTH/-2 + Level.LINE_WIDTH*-1.5),
            )
        )
        self.top_layer.add(
            RoadLane(
                *move_perp(x1, y1, Level.LINE_WIDTH),
                *move_perp(x2, y2, Level.LINE_WIDTH),
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                *move_perp(x1, y1, -1*Level.LINE_WIDTH),
                *move_perp(x2, y2, -1*Level.LINE_WIDTH),
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                *move_perp(x1, y1, Level.LINE_WIDTH*2 + Level.LANE_WIDTH),
                *move_perp(x2, y2, Level.LINE_WIDTH*2 + Level.LANE_WIDTH),
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            RoadLane(
                *move_perp(x1, y1, Level.LINE_WIDTH*-2 - Level.LANE_WIDTH),
                *move_perp(x2, y2, Level.LINE_WIDTH*-2 - Level.LANE_WIDTH),
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            )
        )

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

    def add_intersection_2(self, x, y):
        #intersection is a square with a side length of 2*LANE_WIDTH + 3*LINE_WIDTH
        #the stub roads have a length of STUB_ROAD_LEN on each side.
        #total width/height: 2*LANE_WIDTH + 3*LINE_WIDTH + 2*STUB_ROAD_LEN
        intersection_width = 2*Level.LANE_WIDTH + 3*Level.LINE_WIDTH + 2*Level.STUB_ROAD_LEN
        road_width = 2*Level.LANE_WIDTH+9*Level.LINE_WIDTH;
        self.sub_layer.add(
            RoadLane(x - intersection_width/2, y, x + intersection_width/2, y, width=road_width),
            RoadLane(x, y  - intersection_width/2, x, y + intersection_width/2, width=road_width)
        )

        self.top_layer.add(
            #lines
            RoadLane(
                x - intersection_width/2, y + Level.LINE_WIDTH, 
                x - intersection_width/2 + Level.STUB_ROAD_LEN, y + Level.LINE_WIDTH, 
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                x - intersection_width/2, y - Level.LINE_WIDTH, 
                x - intersection_width/2 + Level.STUB_ROAD_LEN, y - Level.LINE_WIDTH, 
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                x + intersection_width/2, y + Level.LINE_WIDTH, 
                x + intersection_width/2 - Level.STUB_ROAD_LEN, y + Level.LINE_WIDTH, 
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                x + intersection_width/2, y - Level.LINE_WIDTH, 
                x + intersection_width/2 - Level.STUB_ROAD_LEN, y - Level.LINE_WIDTH, 
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                x - intersection_width/2, y + (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), 
                x - intersection_width/2 + Level.STUB_ROAD_LEN, y + (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), 
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            RoadLane(
                x - intersection_width/2, y - (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), 
                x - intersection_width/2 + Level.STUB_ROAD_LEN, y - (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), 
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            RoadLane(
                x + intersection_width/2, y + (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), 
                x + intersection_width/2 - Level.STUB_ROAD_LEN, y + (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), 
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            RoadLane(
                x + intersection_width/2, y - (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), 
                x + intersection_width/2 - Level.STUB_ROAD_LEN, y - (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), 
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            RoadLane(
                x + Level.LINE_WIDTH, y - intersection_width/2, 
                x + Level.LINE_WIDTH, y - intersection_width/2 + Level.STUB_ROAD_LEN,  
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                x - Level.LINE_WIDTH, y - intersection_width/2,  
                x - Level.LINE_WIDTH, y - intersection_width/2 + Level.STUB_ROAD_LEN,  
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                x + Level.LINE_WIDTH, y + intersection_width/2,  
                x + Level.LINE_WIDTH, y + intersection_width/2 - Level.STUB_ROAD_LEN,  
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                x - Level.LINE_WIDTH, y + intersection_width/2, 
                x - Level.LINE_WIDTH, y + intersection_width/2 - Level.STUB_ROAD_LEN, 
                width=Level.LINE_WIDTH, color=Level.Y_LINE_COLOR
            ),
            RoadLane(
                x + (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), y - intersection_width/2, 
                x + (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), y - intersection_width/2 + Level.STUB_ROAD_LEN,  
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            RoadLane(
                x - (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), y - intersection_width/2,  
                x - (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), y - intersection_width/2 + Level.STUB_ROAD_LEN,  
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            RoadLane(
                x + (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), y + intersection_width/2,  
                x + (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), y + intersection_width/2 - Level.STUB_ROAD_LEN,  
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            RoadLane(
                x - (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), y + intersection_width/2,  
                x - (Level.LINE_WIDTH*2 + Level.LANE_WIDTH), y + intersection_width/2 - Level.STUB_ROAD_LEN,  
                width=Level.LINE_WIDTH, color=Level.W_LINE_COLOR
            ),
            #stop markers
            RectSprite(
                x - intersection_width/2 + Level.STUB_ROAD_LEN - Level.STOP_LINE_WIDTH,
                y + Level.LINE_WIDTH*1.5,
                Level.STOP_LINE_WIDTH,
                Level.LANE_WIDTH,
                Level.W_LINE_COLOR
            ),
            RectSprite(
                x + intersection_width/2 - Level.STUB_ROAD_LEN,
                y - Level.LINE_WIDTH*1.5 - Level.LANE_WIDTH,
                Level.STOP_LINE_WIDTH,
                Level.LANE_WIDTH,
                Level.W_LINE_COLOR
            ),
            RectSprite(
                x - Level.LINE_WIDTH*1.5 - Level.LANE_WIDTH,
                y - intersection_width/2 + Level.STUB_ROAD_LEN - Level.STOP_LINE_WIDTH,
                Level.LANE_WIDTH,
                Level.STOP_LINE_WIDTH,
                Level.W_LINE_COLOR
            ),
            RectSprite(
                x + Level.LINE_WIDTH*1.5,
                y + intersection_width/2 - Level.STUB_ROAD_LEN,
                Level.LANE_WIDTH,
                Level.STOP_LINE_WIDTH,
                Level.W_LINE_COLOR
            )
        )

    def add_4_way_stop(self, x, y):
        #same dimensions as intersection_2
        self.add_intersection_2(x, y)
        sign_dist = Level.LANE_WIDTH + 7.5*Level.LINE_WIDTH
        x_trans = x - 30 #hardcoded half of stop sign image width because I am a terrible programmer
        y_trans = y - 98 #hardcoded entire stop sign height (see above) ^
        path = os.path.join("assets", "stop-sign.png")
        self.top_layer.add(
            ImageSprite(x_trans - sign_dist, y_trans - sign_dist, path),
            ImageSprite(x_trans - sign_dist, y_trans + sign_dist, path),
            ImageSprite(x_trans + sign_dist, y_trans - sign_dist, path),
            ImageSprite(x_trans + sign_dist, y_trans + sign_dist, path)
        )

    def add_4_way_light(self, x, y):
        #same dimensions as intersection_2
        self.add_intersection_2(x, y)
        sign_dist = Level.LANE_WIDTH + 7.5*Level.LINE_WIDTH
        x_trans = x - 15 #hardcoded half of stop sign image width because I am a terrible programmer
        y_trans = y - 122 #hardcoded entire stop sign height (see above) ^
        path = os.path.join("assets", "traffic-light-red.png")
        self.top_layer.add(
            ImageSprite(x_trans - sign_dist, y_trans - sign_dist, path),
            ImageSprite(x_trans - sign_dist, y_trans + sign_dist, path),
            ImageSprite(x_trans + sign_dist, y_trans - sign_dist, path),
            ImageSprite(x_trans + sign_dist, y_trans + sign_dist, path)
        )

    def add_dashed_line(self, x1, y1, x2, y2, color):
        angle = math.atan2(y2 - y1, x2 - x1)
        length = math.floor(math.dist((x1, y1), (x2, y2)))
        for pos in range(0, length, Level.DASH_LEN*2):
            self.top_layer.add(
                RoadLane(
                    x1 + pos * math.cos(angle), y1 + pos * math.sin(angle),
                    x1 + (pos + Level.DASH_LEN) * math.cos(angle), y1 + (pos + Level.DASH_LEN) * math.sin(angle),
                    Level.LINE_WIDTH, color
                )
            )

    def add_4_lane_divided(self, x1, y1, x2, y2):
        #each side is as wide as a two lane road, plus a 1/2 lane width median.
        side_width = Level.LANE_WIDTH*2 + Level.LINE_WIDTH*7
        slope = math.atan2(y2-y1, x2-x1)
        def move_perp (x, y, dist): 
            return (x + math.cos(slope + math.pi/2)*dist, y + math.sin(slope + math.pi/2)*dist)

        side_1 = (
            *move_perp(x1, y1, side_width/-2 + Level.LANE_WIDTH/-4), 
            *move_perp(x2, y2, side_width/-2 + Level.LANE_WIDTH/-4)
        )
        side_2 = (
            *move_perp(x1, y1, side_width/2 + Level.LANE_WIDTH/4), 
            *move_perp(x2, y2, side_width/2 + Level.LANE_WIDTH/4)
        )
        self.sub_layer.add(
            RoadLane(*side_1, side_width),
            RoadLane(*side_2, side_width)
        )
        self.add_dashed_line(*side_1, Level.W_LINE_COLOR)
        self.add_dashed_line(*side_2, Level.W_LINE_COLOR)
        self.top_layer.add(
            RoadLane(
                *move_perp(side_1[0], side_1[1], Level.LANE_WIDTH + Level.LINE_WIDTH),
                *move_perp(side_1[2], side_1[3], Level.LANE_WIDTH + Level.LINE_WIDTH),
                Level.LINE_WIDTH, Level.Y_LINE_COLOR
            ),
            RoadLane(
                *move_perp(side_1[0], side_1[1], -Level.LANE_WIDTH - Level.LINE_WIDTH),
                *move_perp(side_1[2], side_1[3], -Level.LANE_WIDTH - Level.LINE_WIDTH),
                Level.LINE_WIDTH, Level.W_LINE_COLOR
            ),
            RoadLane(
                *move_perp(side_2[0], side_2[1], Level.LANE_WIDTH + Level.LINE_WIDTH),
                *move_perp(side_2[2], side_2[3], Level.LANE_WIDTH + Level.LINE_WIDTH),
                Level.LINE_WIDTH, Level.W_LINE_COLOR
            ),
            RoadLane(
                *move_perp(side_2[0], side_2[1], -Level.LANE_WIDTH - Level.LINE_WIDTH),
                *move_perp(side_2[2], side_2[3], -Level.LANE_WIDTH - Level.LINE_WIDTH),
                Level.LINE_WIDTH, Level.Y_LINE_COLOR
            )
        )
        self.road_layer.add(
            RoadLane(
                *move_perp(side_2[0], side_2[1], (Level.LANE_WIDTH + Level.LINE_WIDTH)/2),
                *move_perp(side_2[2], side_2[3], (Level.LANE_WIDTH + Level.LINE_WIDTH)/2)
            ),
            RoadLane(
                *move_perp(side_2[0], side_2[1], (Level.LANE_WIDTH + Level.LINE_WIDTH)/-2),
                *move_perp(side_2[2], side_2[3], (Level.LANE_WIDTH + Level.LINE_WIDTH)/-2)
            ),
            RoadLane(
                *move_perp(side_1[2], side_1[3], (Level.LANE_WIDTH + Level.LINE_WIDTH)/2),
                *move_perp(side_1[0], side_1[1], (Level.LANE_WIDTH + Level.LINE_WIDTH)/2)
            ),
            RoadLane(
                *move_perp(side_1[2], side_1[3], (Level.LANE_WIDTH + Level.LINE_WIDTH)/-2),
                *move_perp(side_1[0], side_1[1], (Level.LANE_WIDTH + Level.LINE_WIDTH)/-2)
            ),
        )




    def add_random_decorations(self,n):
        #adds n random decorations. Flowers, grass, rocks.
        DECORATION_PATHS = [
            os.path.join("assets", "flower-blue.png"),
            os.path.join("assets", "flower-white.png"),
            os.path.join("assets", "grass.png"),
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
        pass

    #internal method used to set the translation of all sprites relative to their starting position.
    def _set_translate(self, x, y):
        for sprite in self.sub_layer.sprites():
            sprite._set_translate(x, y)
        for sprite in self.road_layer.sprites():
            sprite._set_translate(x, y)
        for sprite in self.top_layer.sprites():
            sprite._set_translate(x, y)

    def get_targets(self, sprite):
        #returns the road lane that the given sprite is colliding with
        collisions = []
        for lane in self.road_layer.sprites():
            if pygame.sprite.collide_mask(sprite, lane) != None:
                collisions.append(lane)
        return collisions


#just a plain rectangle.
#since roads are dynamic in length and made up of these,
#they will consist of these.
class RectSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.rel_x = x-1;
        self.rel_y = y-1;

        self.image = pygame.Surface([width+2, height+2], pygame.SRCALPHA)
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

        self.direction = -1*math.degrees(math.atan2(y2 - y, x2 - x))
        self.center = ((x + x2) / 2, (y + y2) / 2)

        #figure out rotation and movement of rel_x and rel_y
        self.image = pygame.transform.rotate(self.image, self.direction)
        self.rect = self.image.get_rect()

        size = self.image.get_size()
        self.rel_x = math.floor(self.center[0] - 0.5*size[0])
        self.rel_y = math.floor(self.center[1] - 0.5*size[1])

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
    def get_center(self):
        return self.center

class StopZone(RoadLane):
    def __init__(self, x, y, x2, y2):
        super().__init__(x, y, x2, y2)
        self.target_points = [
            (x, y, False),
            (*self.center, True),
            (x2, y2, False)
        ]
        self.can_go = False