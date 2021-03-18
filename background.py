import math
import random
import pygame
from gui_parts.menu import Menu
from gui_parts.utility_methods import Utility
from towers.bomber import Bomber
from towers.archer import Archer
from enemies.crow import Crow
from enemies.mage import Mage
from enemies.wizard import Wizard
from enemies.gnu import Gnu

class Background:
    def __init__(self, screen_w, screen_h):
        self.waves = [
            # crow, mage, wizard, gnu
            # corresponds to the frequency
            # of each enemy per wave
            [          ],
            [9, 7, 3, 1],  # 1
            [15, 0, 10, 24],  # 2
            [0, 0, 15, 0],  # 3
            [30, 10, 0, 0],  # 4
            [55, 0, 0, 40],  # 5
            [0, 0, 10, 0],  # 6
            [0, 0, 0, 34],  # 7
            [15, 35, 23, 53],  # 8
            [2, 41, 0, 0],  # 9
            [0, 0, 50, 100],  # 10
        ]
        self.imgs = [Utility.get_img("assets/background.jpg", screen_w, screen_h)]
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.menu = Menu(screen_w, screen_h)
        self.towers = []
        self.enemies = []
        self.current_tower = None
        self.current_wave = 1
        self.create_enemies()
        self.game_over = False

    def draw(self, surface, pos):
        surface.blit(self.imgs[0], (0, 0))
        for enemy in self.enemies:
            enemy.draw(surface)

        self.menu.draw(surface, pos)
        for tower in self.towers:
            tower.draw(surface, pos)

    def update(self):
        for enemy in self.enemies:
            enemy.update()
            if enemy.passed_map():
                self.enemies.remove(enemy)
                # print("popped the enemy")

        if len(self.enemies) == 0:
            if self.current_wave < len(self.waves) - 1:
                self.current_wave += 1
                print(self.current_wave)
                self.create_enemies()

            else:
                self.game_over = True

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

    def get_game_over(self):
        """
        Simple getter method
        :return: boolean
        """
        return self.game_over

    def create_enemies(self):
        """
        Makes new enemies based off of the waves made previously
        :return: None
        """
        # total number of each enemy
        crows = self.waves[self.current_wave][0]
        mages = self.waves[self.current_wave][1]
        wizards = self.waves[self.current_wave][2]
        gnus = self.waves[self.current_wave][3]

        total = crows + mages + wizards + gnus  # num of enemies to add    
        order = ["crow", "mage", "wizard", "gnu"]  # order of appending new enemies

        # tracks the number of crows, mages, wizards, and gnus added
        crow_count = 0
        mage_count = 0
        wizard_count = 0
        gnu_count = 0

        count = 0  # keeps track of the next enemy to add

        enemy_x = 0  # append an enemy at a new x coord

        i = 0  # number of enemies added
        while i < total:
            if count >= len(order):
                count = 0

            if order[count] == order[0] and crow_count < crows:
                self.enemies.append(Crow(enemy_x))
                i += 1
                crow_count += 1
                enemy_x += 35
            elif order[count] == order[1] and mage_count < mages:
                self.enemies.append(Mage(enemy_x))
                i += 1
                mage_count += 1
                enemy_x += 35
            elif order[count] == order[2] and wizard_count < wizards:
                self.enemies.append(Wizard(enemy_x))
                i += 1
                wizard_count += 1
                enemy_x += 35
            elif order[count] == order[3] and gnu_count < gnus:
                self.enemies.append(Gnu(enemy_x))
                i += 1
                gnu_count += 1
                enemy_x += 35

            count += 1  # moves the next enemy each increment