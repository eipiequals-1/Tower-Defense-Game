import random
import sys

import pygame
from gui_parts.utility_methods import Utility


class Tower:
    """
    An abstract class that takes care of drawing, moving, collisions, and updating
    It is a superclass of bomber, archer, and coiner.
    """
    def __init__(self, pos, radius, life):
        """
        Initializes important tower attributes
        
        :param pos: tuple() starting x, y coords of the tower
        :param radius: int() how far the tower can attack enemies
        :param life: int() number of frames to be alive
        """
        self.tower_img = Utility.get_img("assets/towers/tower.png", 40, 110)
        self.man_img = Utility.get_img("assets/towers/man.png", 15, 35)
        self.rect = self.tower_img.get_rect(center=pos)
        self.placed = False
        self.radius = radius
        self.count = 0  # keeps track of frame count and is used for remaining health

        self.damage = 0  # damage that the tower gives to the enemy

        self.life = life
        # attributes that store animation state
        self.animation_radius = 0
        self.animation_opening = True

    def draw(self, surface, pos):
        """
        Redraws the tower each frame
        :param surface: screen to draw on
        :param pos: tuple() of x, y coords of the mouse
        :return: None
        """
        if self.is_over(pos):
            surf = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
            pygame.draw.circle(surf, (128, 128, 128, 128), (self.radius, self.radius), self.radius, 0)
            surface.blit(surf, (self.rect.centerx - self.radius, self.rect.centery - self.radius))

        if not self.placed:
            surface.blit(self.tower_img, self.rect)
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]
        else:
            self.animation(surface)
            surface.blit(self.tower_img, self.rect)
            self.draw_health_bar(surface)
        # draw the man on the tower
        surface.blit(self.man_img, (self.rect.centerx - self.man_img.get_width() // 2, self.rect.y - 15))

    def update(self, enemies):
        """
        Updates the enemy every frame
        :param enemies: list of enemies
        :return: None
        """
        if self.placed:
            self.count += 1
            if self.count > sys.maxsize:
                self.count = 0
            self.attack(enemies)

    def set_placed(self):
        """
        Simple setter method
        :return: None
        """
        self.placed = True

    def is_over(self, pos):
        """
        Checks if the tower collides with the mouse pointer
        :param pos: tuple() of x, y coords
        :return: bool
        """
        return self.rect.collidepoint(pos)

    def attack(self, enemies):
        """
        Checks for each enemy in range
        :param enemies: List[] of enemies
        :return: None
        """
        for enemy in enemies:
            if Utility.pyth_dis(self.rect.centerx, self.rect.centery, enemy.rect.centerx, enemy.rect.centery) < self.radius:
                enemy.handle_attacked(self.damage)

    def draw_health_bar(self, surface):
        """
        Draws a health bar above enemy
        :param surface: screen to draw on
        :return: None
        """
        length, width = self.rect.w, 10  # hardcoded values for health bar size
        remain_health = length - (length * self.count // self.life)
        # convert health to the correct size for drawing by using similar rectangles
        new_surface = pygame.Surface((length, width), pygame.SRCALPHA, 32)  # create a surface for drawing transparent things

        # draw onto the new surface
        pygame.draw.rect(new_surface, (255, 0, 0, 230), (0, 0, length, width))
        pygame.draw.rect(new_surface, (0, 255, 0, 230), (0, 0, remain_health, width))

        surface.blit(new_surface, (self.rect.centerx - length // 2, self.rect.y - 15))  # draw the new surface onto the screen

    def is_dead(self):
        """
        Returns if the tower's life is over
        :return: bool
        """
        return self.count > self.life

    def animation(self, surface):
        """
        Draws an animation of opening and closing circles
        To look like a bomb detonating
        :param surface: screen to draw on
        :return: None
        """
        new_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)  # transparent surface
        pygame.draw.circle(new_surface, (245, 12, 12, 48), (self.radius, self.radius), self.animation_radius)
        surface.blit(new_surface, (self.rect.centerx - self.radius, self.rect.centery - self.radius))  # draw the new surface onto the screen

        if self.animation_opening:
            self.animation_radius += 1
        else:
            self.animation_radius -= 1

        # checks if the animation radius is greater than or less than the fixed radius
        if self.animation_radius >= self.radius:
            self.animation_opening = False
        elif self.animation_radius <= 0:
            self.animation_opening = True