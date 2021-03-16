import pygame
from .tower import Tower
from gui_parts.utility_methods import Utility

class Bomber(Tower):
    def __init__(self, pos):
        super().__init__(pos, 50)
        self.bomb_img = Utility.get_img("assets/towers/bomb.png", self.rect.w - 10, self.rect.w - 10)

    def draw(self, surface, pos):
        super().draw(surface, pos)
        self.draw_bomb(surface)

    def draw_bomb(self, surface):
        surface.blit(self.bomb_img, (self.rect.x + 5, self.rect.bottom - 10 - self.bomb_img.get_height()))