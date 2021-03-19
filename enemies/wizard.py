import os
import pygame
from .enemy import Enemy

class Wizard(Enemy):
    def __init__(self, x):
        super().__init__(x, 33, 39, len(os.listdir("assets/wizard")), "wizard/", 3600)
        # 0: right, 1: down, 2: left, 3: up

    def draw(self, surface):
        """
        Override the super method for changes in sprite direction
        :param surface: surface for drawing
        :return: None
        """
        # left or right
        if self.dir.x > self.dir.y:
            if self.dir.x > 0:
                self.draw_by_dir(surface, 0)
            else:
                self.draw_by_dir(surface, 2)          
            
        else:
            # up or down
            if self.dir.y > 0:
                self.draw_by_dir(surface, 1)
            else:
                self.draw_by_dir(surface, 3)

        self.draw_health_bar(surface)

    def draw_by_dir(self, surface, idx):
        """
        Draws the image based off of its index, which corresponds to its direction
        :param surface: surface for drawing
        :param idx: num from 0-3 corresponding to direction
        :return: None
        """
        surface.blit(self.imgs[idx], (int(self.rect.x), int(self.rect.y), self.rect.w, self.rect.h))