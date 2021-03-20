import random
import sys

import pygame
from gui_parts.utility_methods import Utility


class Tower:
    """
    An abstract class that takes care of drawing, moving, collisions, and updating
    It is a superclass of bomber, archer, and coiner
    """
    def __init__(self, pos, radius, cost):
        self.tower_img = Utility.get_img("assets/towers/tower.png", 40, 110)
        self.man_img = Utility.get_img("assets/towers/man.png", 15, 35)
        self.rect = self.tower_img.get_rect(center=pos)
        self.price = 500
        self.placed = False
        self.radius = radius
        self.attack_count = 0

        self.cost = cost

        self.damage = 0

    def draw(self, surface, pos):
        if self.is_over(pos):
            pygame.draw.circle(surface, (128, 128, 128, 255), (self.rect.centerx, self.rect.bottom - 20), self.radius)

        if not self.placed:
            surface.blit(self.tower_img, self.rect)
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]
        else:
            surface.blit(self.tower_img, self.rect)
        surface.blit(self.man_img, (self.rect.centerx - self.man_img.get_width() // 2, self.rect.y - 15))

    def update(self, enemies):
        """
        Updates the enemy every frame
        :param enemies: list of enemies
        :return: None
        """
        if self.placed:
            self.attack_count += 1
            if self.attack_count > sys.maxsize:
                self.attack_count = 0
            self.attack(enemies)

    def set_placed(self):
        self.placed = True

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

    def attack(self, enemies):
        for enemy in enemies:
            if Utility.pyth_dis(self.rect.centerx, self.rect.centery, enemy.rect.centerx, enemy.rect.centery) < self.radius:
                enemy.handle_attacked(self.damage)
