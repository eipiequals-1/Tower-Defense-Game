import random

import pygame
from gui_parts.utility_methods import Utility

from .tower import Tower


class Archer(Tower):
    def __init__(self, pos, cost):
        super().__init__(pos=pos, radius=90, cost=cost, life=4_000)
        self.bow_img = Utility.get_img("assets/towers/bow.png", self.rect.w - 10, self.rect.w - 5)

    def draw(self, surface, pos):
        super().draw(surface, pos)
        self.draw_bow(surface)
        #print(self.attack_count)

    def draw_bow(self, surface):
        surface.blit(self.bow_img, (self.rect.x + 5, self.rect.bottom - 10 - self.bow_img.get_height()))

    def update(self, enemies):
        super().update(enemies)
        self.damage = random.randint(25, 40)