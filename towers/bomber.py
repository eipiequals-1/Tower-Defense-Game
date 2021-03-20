import random

import pygame
from gui_parts.utility_methods import Utility

from .tower import Tower


class Bomber(Tower):
    def __init__(self, pos, cost):
        super().__init__(pos=pos, radius=130, cost=cost, life=50_000)
        self.bomb_img = Utility.get_img("assets/towers/bomb.png", self.rect.w - 10, self.rect.w - 10)

    def draw(self, surface, pos):
        super().draw(surface, pos)
        self.draw_bomb(surface)

    def draw_bomb(self, surface):
        surface.blit(self.bomb_img, (self.rect.x + 5, self.rect.bottom - 10 - self.bomb_img.get_height()))

    def update(self, enemies):
        super().update(enemies)
        self.damage = random.randint(35, 55)