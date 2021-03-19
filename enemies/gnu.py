import os
import pygame
from .enemy import Enemy

class Gnu(Enemy):
    def __init__(self, x):
        super().__init__(x, 30, 40, len(os.listdir("assets/gnu")), "gnu/", 3500)

    def draw(self, surface):
        surface.blit(self.imgs[0], (int(self.rect.x), int(self.rect.y), self.rect.w, self.rect.h))
        self.draw_health_bar(surface)