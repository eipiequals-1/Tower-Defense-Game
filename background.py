import math
import pygame
from gui_parts.menu import Menu
from gui_parts.utility_methods import Utility
from towers.bomber import Bomber
from towers.archer import Archer
from wave import Wave

class Background:
    def __init__(self, screen_w, screen_h):
        self.imgs = [Utility.get_img("assets/background.jpg", screen_w, screen_h)]
        self.wave = Wave()
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.towers = []
        self.menu = Menu(screen_w, screen_h)
        self.current_tower = None
        self.current_tower_idx = None

    def draw(self, surface, pos):
        surface.blit(self.imgs[0], (0, 0))
        self.wave.draw(surface)

        self.menu.draw(surface, pos)
        for tower in self.towers:
            tower.draw(surface, pos)

    def update(self):
        self.wave.update()

        self.menu.update()
        for tower in self.towers:
            tower.update()

    def create_new_tower(self, pos, mode):
        """
        Creates a new tower depending on type
        :param pos: mouse position relative to (0, 0)
        :param mode: type of tower (bomb, archer)
        """
        if mode == "bomb":
            self.towers.append(Bomber(pos))
        elif mode == "archer":
            self.towers.append(Archer(pos))
        self.current_tower = self.towers[-1]

    def set_current_tower_placed(self):
        self.current_tower = None
        self.towers[-1].set_placed()

    def handle_user_events(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_tower == None:
                if self.menu.bomb_tower.is_over(pos):
                    self.create_new_tower(pos, "bomb")
                elif self.menu.archer_tower.is_over(pos):
                    self.create_new_tower(pos, "archer")
            else:
                self.set_current_tower_placed()

    def game_over(self):
        return self.wave.is_over()