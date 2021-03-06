import math
import os
import random
import sys

import pygame
from gui_parts.utility_methods import Utility


class Enemy:
    """
    An abstract class that takes care of drawing, moving, collisions, and updating.
    Is a superclass of wizard, mage, ogre, crow and scorpion
    """
    vel = 0.5  # total pixels enemy moves per frame
    def __init__(self, x, width, height, num_of_sprites, asset_dir, frequency):
        """
        Initializes velocities, rectangles, vectors, and images necessary to move and
        Interact with the towers
        :param x: int - the starting x value
        :param width: int - desired width of enemy in pixels
        :param height: int - desired height of enemy in pixels
        :param num_of_sprites: int - length of files(.png) in the directory
        :param asset_dir: str - relative path to the assets
        :param frequency: int - the frequency at which the enemy is dealt damage
        """
        self.set_path(x)

        self.path_pos = 1  # where the enemy is going
        self.rect = pygame.Rect(self.path[self.path_pos - 1][0] - width // 2, self.path[self.path_pos - 1][1] - height // 2, width, height)
        
        self.imgs = []
        self.num_of_sprites = num_of_sprites
        for i in range(self.num_of_sprites):
            self.imgs.append(Utility.get_img("assets/" + asset_dir + str(i) + ".png", self.rect.width, self.rect.height))

        self.pix_pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.dir = pygame.math.Vector2(0, 0)

        self.max_health = 100
        self.health = self.max_health

        self.sprite_count = 0
        self.draws = 9  # number of frames each img is drawn
        
        self.ready_to_be_attacked = True
        self.attacked_count = 0
        self.attack_frequency = frequency  # the greater the attack frequency, the stronger the enemy
        
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
        # moves while making sure that there are no path errors by a frame off
        try:
            self.move()
        except IndexError:
            pass

        self.attacked_count += 1
        if self.attacked_count >= sys.maxsize:
            self.attacked_count = 0

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

    def draw_health_bar(self, surface) -> None:
        """
        Draws a health bar above enemy
        :param surface: screen to draw on
        :return: None
        """
        length, width = 35, 9  # hardcoded values for health bar size
        # convert health to the correct size for drawing by using similar rectangles
        remain_health = length * self.health // self.max_health

        new_surface = pygame.Surface((length, width), pygame.SRCALPHA, 32)  # create a surface for drawing transparent things
        
        # draw onto the new surface
        pygame.draw.rect(new_surface, (255, 0, 0, 220), (0, 0, length, width))
        pygame.draw.rect(new_surface, (0, 255, 0, 220), (0, 0, remain_health, width))

        surface.blit(new_surface, (self.rect.centerx - length // 2, self.rect.y - 15))  # draw the new surface onto the screen

    def handle_attacked(self, loss):
        if self.ready_to_be_attacked:
            self.health -= loss
            self.ready_to_be_attacked = False

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
        return self.rect.left > width

    def set_path(self, start_x):
        """
        Generate a path that deviates slightly from the hardcoded value
        :param start_x: x coord of enemy when constructed
        """
        self.path = [(-40 - start_x, 419), (13, 419), (70, 418), (125, 427), (149, 469), (157, 699), (234, 703), (317, 700), (367, 651), (367, 585), (353, 506), (375, 454), (425, 416), (488, 412), (545, 421), (660, 422), (721, 461), (775, 490), (836, 490), (885, 453), (911, 421), (981, 425), (1052, 423), (1136, 417), (1201, 420), (1350, 419)]  # hardcoded values for enemy turning and path
        diff = 15  # random factor
        r = random.randint
        for i in range(1, len(self.path)):
            self.path[i] = (self.path[i][0], r(self.path[i][1] - diff, self.path[i][1] + diff))  # generates a random y value for each point on the path

    def is_dead(self):
        """
        Returns if enemy has no more health
        """
        return self.health <= 0
