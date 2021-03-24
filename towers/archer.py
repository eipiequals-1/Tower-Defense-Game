import random

import pygame
from gui_parts.utility_methods import Utility

from .tower import Tower


class Archer(Tower):
    """
    Subtype of Tower()
    Changes include: radius, life, image
    :param pos: tuple() of x, y coords of the mouse
    """
    def __init__(self, pos):
        super().__init__(pos=pos, radius=90, life=4_000)
        self.bow_img = Utility.get_img("assets/towers/bow.png", self.rect.w - 10, self.rect.w - 5)

    def draw(self, surface, pos):
        """
        Overrides the original method by drawing a bow on the tower
        :param surface: screen to draw on
        :param pos: tuple() of x, y coords of the mouse
        :return: None
        """
        super().draw(surface, pos)
        self.draw_bow(surface)

    def draw_bow(self, surface):
        """
        Simply draws the bow onto the screen
        :param surface: screen to draw on
        :return: None
        """
        surface.blit(self.bow_img, (self.rect.x + 5, self.rect.bottom - 10 - self.bow_img.get_height()))

    def update(self, enemies):
        """
        Overrides the orginal method by changing the amount
        Of damage to deal to the enemy
        :param enemies: List[] of enemies
        :return: None
        """
        super().update(enemies)
        self.damage = random.randint(25, 40)