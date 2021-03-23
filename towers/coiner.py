import sys

import pygame
from gui_parts.utility_methods import Utility

from .tower import Tower


class Coiner(Tower):
    def __init__(self, pos, cost):
        super().__init__(pos=pos, radius=0, cost=cost, life=25_000)
        self.coin_img = Utility.get_img("assets/coin.png", self.rect.w - 10, self.rect.w - 10)
        self.coin_count = 1

    def draw(self, surface, pos):
        if not self.placed:
            surface.blit(self.tower_img, self.rect)
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]
        else:
            surface.blit(self.tower_img, self.rect)
        # draw the man on the tower
        surface.blit(self.man_img, (self.rect.centerx - self.man_img.get_width() // 2, self.rect.y - 15))        
        self.draw_coin(surface)

    def draw_coin(self, surface):
        surface.blit(self.coin_img, (self.rect.x + 5, self.rect.bottom - 10 - self.coin_img.get_height()))

    def update(self, enemies):
        if self.placed:
            self.attack_count += 1
            self.coin_count += 1
            if self.coin_count >= sys.maxsize:
                self.coin_count = 0
            
    def new_money(self):
        return self.coin_count % 600 == 0

    def get_placed(self):
        return self.placed
