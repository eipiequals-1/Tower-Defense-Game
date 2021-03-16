import pygame
from .tower import Tower
from gui_parts.utility_methods import Utility

class Archer(Tower):
    def __init__(self, pos):
        super().__init__(pos, 65)
        self.bow_img = Utility.get_img("assets/towers/bow.png", self.rect.w - 10, self.rect.w - 5)

    def draw(self, surface, pos):
        super().draw(surface, pos)
        self.draw_bow(surface)

    def draw_bow(self, surface):
        surface.blit(self.bow_img, (self.rect.x + 5, self.rect.bottom - 10 - self.bow_img.get_height()))

    def attack(self, enemies):
        super().attack(enemies)
        