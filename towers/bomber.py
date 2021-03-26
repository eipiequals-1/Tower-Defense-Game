import random

import pygame
from gui_parts.utility_methods import Utility

from .tower import Tower


class Bomber(Tower):
    """
    Subtype of Tower()
    Changes include: radius, life, image
    """
    def __init__(self, pos):
        """
        Initializes most of the same things as the superclass
        Creates its own tower img
        :param pos: tuple - of x, y coords of the mouse
        """
        super().__init__(pos=pos, radius=130, life=7_000)
        self.bomb_img = Utility.get_img("assets/towers/bomb.png", self.rect.w - 10, self.rect.w - 10)

    def draw(self, surface, pos):
        """
        Overrides the original method by drawing a bomb on the tower
        :param surface: pygame.Surface - screen to draw on
        :param pos: tuple - of x, y coords of the mouse
        :return: None
        """
        super().draw(surface, pos)
        self.draw_bomb(surface)

    def draw_bomb(self, surface):
        """
        Simply draws the bomb onto the screen
        :param surface: pygame.Surface - screen to draw on
        :return: None
        """
        surface.blit(self.bomb_img, (self.rect.x + 5, self.rect.bottom - 10 - self.bomb_img.get_height()))

    def update(self, enemies):
        """
        Overrides the orginal method by changing the amount
        Of damage to deal to the enemy
        :param enemies: List[] - of enemies
        :return: None
        """
        super().update(enemies)
        self.damage = random.randint(35, 55)