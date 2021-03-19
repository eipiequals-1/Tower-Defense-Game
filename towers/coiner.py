import pygame
from gui_parts.utility_methods import Utility

from .tower import Tower


class Coiner(Tower):
    def __init__(self, pos, cost):
        super().__init__(pos, 0, cost)
        self.coin_img = Utility.get_img("assets/coin.png", self.rect.w - 10, self.rect.w - 10)

    def draw(self, surface, pos):
        super().draw(surface, pos)
        self.draw_coin(surface)

    def draw_coin(self, surface):
        surface.blit(self.coin_img, (self.rect.x + 5, self.rect.bottom - 10 - self.coin_img.get_height()))
