import math
import os
import random
import pygame
from gui_parts.utility_methods import Utility

class Enemy:
    """
    An abstract class that takes care of drawing, moving, collisions, and updating.
    Is a superclass of wizard, mage, ogre, crow and scorpion
    :param width: width of sprite
    :param height: height of sprite
    """
    def __init__(self, x, width, height, num_of_sprites, asset_dir):
        self.path = [(-40 - x, 419), (13, 419), (70, 418), (125, 427), (149, 469), (157, 699), (234, 703), (317, 700), (367, 651), (367, 585), (353, 506), (375, 454), (425, 416), (488, 412), (545, 421), (660, 422), (721, 461), (775, 490), (836, 490), (885, 453), (911, 421), (981, 425), (1052, 423), (1136, 417), (1201, 420), (1255, 419)]
        diff = 10
        r = random.randint
        for i in range(1, len(self.path)):
            self.path[i] = (self.path[i][0], r(self.path[i][1] - diff, self.path[i][1] + diff))

        self.path_pos = 1  # where the enemy is going
        self.rect = pygame.Rect(self.path[self.path_pos - 1][0] - width // 2, self.path[self.path_pos - 1][1] - height // 2, width, height)
        
        self.imgs = []
        self.num_of_sprites = num_of_sprites
        for i in range(self.num_of_sprites):
            self.imgs.append(Utility.get_img("assets/" + asset_dir + str(i) + ".png", self.rect.width, self.rect.height))

        self.pix_pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.vel = 0.1
        self.dir = pygame.math.Vector2(0, 0)

        self.max_health = 100
        self.health = 45

        self.sprite_count = 0
        self.draws = 35
        
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
        :param surface: surface
        :return: None
        """
        try:
            self.move()
        except IndexError:
            pass

    def move(self):
        """
        Move enemy throughout the map
        :return: None
        """
        self.rect.centerx = self.pix_pos.x
        self.rect.centery = self.pix_pos.y

        self.dir = self.convert_slope()

        self.pix_pos += self.dir

        if self.is_on_point():
            self.path_pos += 1


        #print(f"centerX = {self.rect.centerx} centerY = {self.rect.centery}")

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
        except ZeroDivisionError:
            pass
        try:
            y_move = change[1] * self.vel / dis
        except ZeroDivisionError:
            pass

        #print(f"x_move = {abs(x_move)}, y_move = {abs(y_move)}, total = {abs(x_move) + abs(y_move)}")
        
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


    def is_on_point(self):
        on_point_tolerance = self.vel
        if self.rect.centerx - on_point_tolerance < self.path[self.path_pos][0] < self.rect.centerx + on_point_tolerance:
            if self.rect.centery - on_point_tolerance < self.path[self.path_pos][1] < self.rect.centery + on_point_tolerance:
                #print("going to new point", self.path_pos)
                return True
        return False

    def passed_map(self):
        return self.rect.right > 1250