import math
import random

import pygame

from enemies.crow import Crow
from enemies.enemy import Enemy
from enemies.gnu import Gnu
from enemies.mage import Mage
from enemies.wizard import Wizard
from gui_parts.menu import Menu
from gui_parts.text import Text
from gui_parts.utility_methods import Utility
from towers.archer import Archer
from towers.bomber import Bomber
from towers.coiner import Coiner
from towers.tower_types import TowerTypes


class Background:
    """
    Handles updating, drawing, and playing the game state
    """
    def __init__(self, screen_w, screen_h):
        """
        Initializes the enemies, waves, towers, text, and menu bar
        :param screen_w: int - width of the pygame screen
        :param screen_h: int - height of the pygame screen
        """
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
        self.imgs = [Utility.get_img("assets/background.jpg", screen_w, screen_h)]  # list of images in case more backgrounds are added
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.costs = {TowerTypes.BOMBER: 750, TowerTypes.ARCHER: 250, TowerTypes.COINER: 125}

        self.menu = Menu(screen_w, screen_h, self.costs[TowerTypes.BOMBER], self.costs[TowerTypes.ARCHER], self.costs[TowerTypes.COINER])
        self.create_text()

        self.coin_img = Utility.get_img("assets/coin.png", 45, 45)

        self.towers = []
        self.enemies = []
        self.current_tower = None  # indicates if the player is placing a tower
        self.create_enemies()

        self.killed = 0

        self.win = False
        self.lose = False

        self.money = 600

        self.lives = 15

        self.night_surf = pygame.Surface((self.screen_w, screen_h), pygame.SRCALPHA)

    def draw(self, surface, pos):
        """
        Redraws the window each frame
        :param surface: pygame.Surface - screen to draw on
        :param pos: tuple - of x, y coords
        :return: None
        """
        surface.blit(self.imgs[0], (0, 0))  # draws the background
        for enemy in self.enemies:
            enemy.draw(surface)

        for tower in self.towers:
            tower.draw(surface, pos)
        self.menu.draw(surface, pos)

        surface.blit(self.coin_img, (self.money_text.x - 10 - self.coin_img.get_width(), self.menu.rect.centery - self.coin_img.get_height() // 2))  # draws the coin to represent money to the player

        # draws the text onto the screen
        self.wave_num_text.set_text("WAVE# " + str(self.current_wave))
        self.wave_num_text.draw(surface)

        self.killed_text.set_text("SLAUGHTERED: " + str(self.killed))
        self.killed_text.draw_right(surface, 10, self.screen_w)

        self.money_text.set_text(str(self.money))
        self.money_text.draw_right(surface, 10, self.menu.rect.right)

        self.lives_text.set_text("LIVES: " + str(self.lives))
        self.lives_text.draw_centered(surface, 0, self.screen_w)

        # add the purple hue
        self.night_surf.fill((255, 0, 255, 30))
        surface.blit(self.night_surf, (0, 0))

    def update(self):
        """
        Main updating method which handles towers and enemy movement, collisions,
        Money changes, and towers life and death
        :return: None
        """
        self.update_waves()  # updates enemies

        for tower in self.towers:
            if isinstance(tower, Coiner):
                if tower.new_money() and tower.get_placed():
                    self.money += 20
            if tower.is_dead():
                self.towers.remove(tower)
            tower.update(self.enemies)

        if self.lives <= 0:
            self.lose = True

    def update_waves(self):
        """
        Handles enemy lives and wave changing
        :return: None
        """
        for i, enemy in enumerate(self.enemies):
            enemy.update()
            if enemy.passed_map(self.screen_w):
                self.lives -= 1
                self.enemies.pop(i)
            if enemy.is_dead():
                self.killed += 1
                self.money += 25
                self.enemies.pop(i)

        if len(self.enemies) == 0:
            if self.current_wave < len(self.waves) - 1:
                self.costs[TowerTypes.BOMBER] = self.costs[TowerTypes.BOMBER] + 25
                self.costs[TowerTypes.ARCHER] += 25
                self.costs[TowerTypes.COINER] += 25
                Enemy.vel += 0.05
                self.current_wave += 1
                self.create_enemies()

            else:
                self.win = True

    def create_new_tower(self, pos, mode):
        """
        Creates a new tower depending on type
        :param pos: tuple - x, y coords of the mouse pos
        :param mode: TowerTypes(Enum) - type of tower (bomber, archer, coiner)
        """
        if mode == TowerTypes.BOMBER:
            self.towers.append(Bomber(pos))
        elif mode == TowerTypes.ARCHER:
            self.towers.append(Archer(pos))
        elif mode == TowerTypes.COINER:
            self.towers.append(Coiner(pos))
        self.current_tower = self.towers[-1]

    def set_current_tower_placed(self):
        """
        Places a new tower
        :return: None
        """
        self.current_tower = None
        self.towers[-1].set_placed()

    def handle_mouse_clicks(self, event, pos):
        """
        Handles selecting towers and placing them
        :param event: pygame.event
        :param pos: tuple - of x, y mouse coords
        :return: None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the player is not holding a tower
            if self.current_tower is None:
                # check if there is enough money to buy the tower for each
                if self.menu.bomber_tower.is_over(pos) and self.money >= self.costs[TowerTypes.BOMBER]:
                    self.create_new_tower(pos, TowerTypes.BOMBER)
                    self.money -= self.costs[TowerTypes.BOMBER]

                elif self.menu.archer_tower.is_over(pos) and self.money >= self.costs[TowerTypes.ARCHER]:
                    self.create_new_tower(pos, TowerTypes.ARCHER)
                    self.money -= self.costs[TowerTypes.ARCHER]

                elif self.menu.coiner_tower.is_over(pos) and self.money >= self.costs[TowerTypes.COINER]:
                    self.create_new_tower(pos, TowerTypes.COINER)
                    self.money -= self.costs[TowerTypes.COINER]
            else:
                # if the player is holding a tower
                self.set_current_tower_placed()

    def create_text(self):
        """
        Sets Text() objects that give the user some information regarding
        Game state and points
        :return: None
        """
        self.wave_num_text = Text("uroob", 28, "", (255, 255, 255), 10, 10)
        self.killed_text = Text("uroob", 28, "", (255, 255, 255), 10, 10)
        self.money_text = Text("uroob", 28, "", (0, 0, 0), 0, self.menu.rect.height // 3)
        self.lives_text = Text("uroob", 30, "", (0, 0, 0), 0, self.screen_h - 50, True)

    def get_win(self):
        """
        Simple getter method
        :return: bool
        """
        return self.win

    def get_lose(self):
        return self.lose

    def create_enemies(self):
        """
        Makes new enemies based off of the waves made previously
        :return: None
        """
        self.enemies.clear()
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

        enemy_x = 40  # append an enemy at a new x coord

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
