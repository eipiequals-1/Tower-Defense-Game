import math
import os
import sys
import random
import pygame
from gui_parts.utility_methods import Utility

class Enemy:
    """
    An abstract class that takes care of drawing, moving, collisions, and updating.
    Is a superclass of wizard, mage, ogre, crow and scorpion
    """
    def __init__(self, x, width, height, num_of_sprites, asset_dir, frequency):
        self.set_path(x)

        self.path_pos = 1  # where the enemy is going
        self.rect = pygame.Rect(self.path[self.path_pos - 1][0] - width // 2, self.path[self.path_pos - 1][1] - height // 2, width, height)
        
        self.imgs = []
        self.num_of_sprites = num_of_sprites
        for i in range(self.num_of_sprites):
            self.imgs.append(Utility.get_img("assets/" + asset_dir + str(i) + ".png", self.rect.width, self.rect.height))

        self.pix_pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.vel = 0.1  # total pixels enemy moves per frame
        self.dir = pygame.math.Vector2(0, 0)

        self.max_health = 100
        self.health = self.max_health

        self.sprite_count = 0
        self.draws = 35  # number of frames each img is drawn
        
        self.ready_to_be_attacked = True
        self.attacked_count = 0
        self.attack_frequency = frequency
        
    def draw(self, surface):
        """
        Draws the enemy with the given images
        :param surface: surface
        :return: None
        """
        if self.sprite_count >= len(self.imgs) * self.draws:
            self.sprite_count = 0

        surface.blit(self.imgs[self.sprite_count // self.draws], (int(self.rect.x), int(self.rect.y), self.rect.w, self.rect.h))
        self.draw_health_bar(surface)

        self.sprite_count += 1

    def update(self):
        """
        Handles updating every frame. Updates drawing, moving, and collisions
        :return: None
        """
        # moves while making sure that there are no path errors by a frame
        try:
            self.move()
        except IndexError:
            pass

    def move(self):
        """
        Move enemy throughout the map
        :return: None
        """
        # update the rect sprite with the pixel position
        self.rect.centerx = self.pix_pos.x
        self.rect.centery = self.pix_pos.y

        self.dir = self.convert_slope()
        # adding both pygame.math.Vectors
        self.pix_pos += self.dir

        if self.is_on_point():
            self.path_pos += 1  # increments 1 if a point on the path has been passed

    def convert_slope(self):
        """
        Uses the concept of similar triangles to make the enemy move a total of 2 pixels per frame
        :return: pygame.math.Vector2
        """
        x_move = 0
        y_move = 0
        change = self.get_pos_changes()
        dis = Utility.pyth_dis(self.rect.centerx, self.rect.centery, self.path[self.path_pos][0], self.path[self.path_pos][1])
        try:
            x_move = change[0] * self.vel / dis
            y_move = change[1] * self.vel / dis
        except ZeroDivisionError:
            pass
        return pygame.math.Vector2(x_move, y_move)

    def get_pos_changes(self):
        """
        Return the change in y over change in x
        :return: tuple
        """
        path = self.path[self.path_pos]
        x_change = -(self.rect.centerx - path[0])
        y_change = -(self.rect.centery - path[1])

        return (x_change, y_change)

    def draw_health_bar(self, surface):
        """
        draw a health bar above enemy
        :param surface: surface
        :return: None
        """
        length = 40
        remain_health = length * self.health / self.max_health
        
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.centerx - length // 2, self.rect.y - 15, length, 10))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.centerx - length // 2, self.rect.y - 15, remain_health, 10))

    def handle_attacked(self, loss):
        if self.ready_to_be_attacked:
            self.health -= loss
            self.ready_to_be_attacked = False

        self.attacked_count += 1
        if self.attacked_count >= sys.maxsize:
            self.attacked_count = 0

        if self.attacked_count % self.attack_frequency == 0:
            self.ready_to_be_attacked = True

    def is_on_point(self):
        """
        Checks if enemy has passed a certain point on the path
        :return: bool
        """
        on_point_tolerance = self.vel
        if self.rect.centerx - on_point_tolerance < self.path[self.path_pos][0] < self.rect.centerx + on_point_tolerance:
            if self.rect.centery - on_point_tolerance < self.path[self.path_pos][1] < self.rect.centery + on_point_tolerance:
                return True
        return False

    def passed_map(self, width):
        return self.rect.right > width

    def set_path(self, start_x):
        """
        Generate a path that deviates slightly from the hardcoded value
        :param start_x: x coord of enemy when constructed
        """
        self.path = [(-40 - start_x, 419), (13, 419), (70, 418), (125, 427), (149, 469), (157, 699), (234, 703), (317, 700), (367, 651), (367, 585), (353, 506), (375, 454), (425, 416), (488, 412), (545, 421), (660, 422), (721, 461), (775, 490), (836, 490), (885, 453), (911, 421), (981, 425), (1052, 423), (1136, 417), (1201, 420), (1250, 419)]  # hardcoded values for enemy turning and path
        diff = 10  # random factor
        r = random.randint
        for i in range(1, len(self.path)):
            self.path[i] = (self.path[i][0], r(self.path[i][1] - diff, self.path[i][1] + diff))  # generates a random y value for each point on the path

    def is_dead(self):
        """
        Returns if enemy has no more health
        """
        return self.health <= 0