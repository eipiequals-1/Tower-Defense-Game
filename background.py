import math
import random

import pygame

from enemies.crow import Crow
from enemies.gnu import Gnu
from enemies.mage import Mage
from enemies.wizard import Wizard
from enemies.enemy import Enemy
from gui_parts.menu import Menu
from gui_parts.text import Text
from gui_parts.utility_methods import Utility
from towers.archer import Archer
from towers.bomber import Bomber
from towers.coiner import Coiner


class Background:
    COSTS = {"bomber": 800, "archer": 300, "coiner": 125}
    def __init__(self, screen_w, screen_h):
        self.waves = [
            # crow, mage, wizard, gnu
            # corresponds to the frequency
            # of each enemy per wave
            [],
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
        self.current_wave = 1
        self.imgs = [Utility.get_img("assets/background.jpg", screen_w, screen_h)]
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.menu = Menu(screen_w, screen_h, self.COSTS["bomber"], self.COSTS["archer"], self.COSTS["coiner"])
        self.create_text()

        self.coin_img = Utility.get_img("assets/coin.png", 45, 45)

        self.towers = []
        self.enemies = []
        self.current_tower = None
        self.create_enemies()

        self.killed = 0

        self.game_over = False

        self.money = 50000

        self.lives = 10

    def draw(self, surface, pos):
        surface.blit(self.imgs[0], (0, 0))
        for enemy in self.enemies:
            enemy.draw(surface)

        for tower in self.towers:
            tower.draw(surface, pos)
        self.menu.draw(surface, pos)

        surface.blit(self.coin_img, (self.money_text.x - 10 - self.coin_img.get_width(), self.menu.rect.centery - self.coin_img.get_height() // 2))

        self.wave_num_text.set_text("WAVE# " + str(self.current_wave))
        self.wave_num_text.draw(surface)

        self.killed_text.set_text("SLAUGHTERED: " + str(self.killed))
        self.killed_text.draw_right(surface, 10, self.screen_w)

        self.money_text.set_text(str(self.money))
        self.money_text.draw_right(surface, 10, self.menu.rect.right)

        self.lives_text.set_text("LIVES: " + str(self.lives))
        self.lives_text.draw_centered(surface, 0, self.screen_w)

    def update(self):
        self.update_waves()

        self.menu.update()
        for tower in self.towers:
            if isinstance(tower, Coiner):
                if tower.new_money() and tower.get_placed():
                    self.money += 50
            tower.update(self.enemies)

        if self.lives <= 0:
            self.game_over = True

    def update_waves(self):
        for enemy in self.enemies:
            enemy.update()
            if enemy.passed_map(self.screen_w):
                self.lives -= 1
                self.enemies.remove(enemy)
            if enemy.is_dead():
                self.killed += 1
                self.money += 25
                self.enemies.remove(enemy)
                # print("popped the enemy")

        if len(self.enemies) == 0:
            if self.current_wave < len(self.waves) - 1:
                Enemy.vel += 0.05
                self.current_wave += 1
                # print(self.current_wave)
                self.create_enemies()

            else:
                self.game_over = True

    def create_new_tower(self, pos, mode, cost):
        """
        Creates a new tower depending on type
        :param pos: mouse position relative to (0, 0)
        :param mode: type of tower (bomb, archer)
        """
        if mode == "bomber":
            self.towers.append(Bomber(pos, cost))
        elif mode == "archer":
            self.towers.append(Archer(pos, cost))
        elif mode == "coiner":
            self.towers.append(Coiner(pos, cost))
        self.current_tower = self.towers[-1]

    def set_current_tower_placed(self):
        self.current_tower = None
        self.towers[-1].set_placed()

    def handle_mouse_clicks(self, event, pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_tower is None:

                if self.menu.bomber_tower.is_over(pos) and self.money >= self.COSTS["bomber"]:
                    self.create_new_tower(pos, "bomber", self.COSTS["bomber"])
                    self.money -= self.COSTS["bomber"]

                elif self.menu.archer_tower.is_over(pos) and self.money >= self.COSTS["archer"]:
                    self.create_new_tower(pos, "archer", self.COSTS["archer"])
                    self.money -= self.COSTS["archer"]

                elif self.menu.coiner_tower.is_over(pos) and self.money >= self.COSTS["coiner"]:
                    self.create_new_tower(pos, "coiner", self.COSTS["coiner"])
                    self.money -= self.COSTS["coiner"]
            else:
                self.set_current_tower_placed()

    def create_text(self):
        self.wave_num_text = Text("uroob", 28, "", (255, 255, 255), 10, 10)
        self.killed_text = Text("uroob", 28, "", (255, 255, 255), 10, 10)
        self.money_text = Text("uroob", 28, "", (0, 0, 0), 0, self.menu.rect.height // 3)
        self.lives_text = Text("uroob", 30, "", (0, 0, 0), 0, self.screen_h - 50, True)

    def get_game_over(self):
        """
        Simple getter method
        :return: bool
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

            count += 1  # moves the next enemy to add
