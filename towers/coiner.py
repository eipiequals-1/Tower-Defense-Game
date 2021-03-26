import sys

import pygame
from gui_parts.utility_methods import Utility

from .tower import Tower


class Coiner(Tower):
    """
    Subtype of Tower()
    Changes include: radius, life, image, attacking, damage
    """
    def __init__(self, pos):
        """
        Initializes most of the same things as the superclass
        Creates its own tower img
        :param pos: tuple - of x, y coords of the mouse
        """
        super().__init__(pos=pos, radius=0, life=10_000)
        self.coin_img = Utility.get_img("assets/coin.png", self.rect.w - 10, self.rect.w - 10)
        self.coin_count = 1

    def draw(self, surface, pos):
        """
        Overrides the original method by drawing a coin on the tower
        :param surface: pygame.Surface - screen to draw on
        :param pos: tuple - of x, y coords of the mouse
        :return: None
        """
        if not self.placed:
            surface.blit(self.tower_img, self.rect)
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]
        else:
            surface.blit(self.tower_img, self.rect)
            self.draw_health_bar(surface)
        # draw the man on the tower
        surface.blit(self.man_img, (self.rect.centerx - self.man_img.get_width() // 2, self.rect.y - 15))        
        self.draw_coin(surface)

    def draw_coin(self, surface):
        """
        Simply draws the coin onto the screen
        :param surface: pygame.Surface - screen to draw on
        :return: None
        """
        surface.blit(self.coin_img, (self.rect.x + 5, self.rect.bottom - 10 - self.coin_img.get_height()))

    def update(self, enemies):
        """
        Overrides the orginal method by changing the amount
        Of damage to deal to the enemy
        :param enemies: List[] - of enemies; unecessary
        :return: None
        """
        if self.placed:
            self.count += 1
            self.coin_count += 1
            # reset the count
            if self.coin_count >= sys.maxsize:
                self.coin_count = 0
            
    def new_money(self):
        """
        Returns if a new coin should be made
        :return: bool
        """
        return self.coin_count % 600 == 0

    def get_placed(self):
        """
        Returns if the tower is placed
        :return: bool
        """
        return self.placed
