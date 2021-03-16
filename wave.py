import pygame
import random
from enemies.crow import Crow
from enemies.mage import Mage
from enemies.wizard import Wizard
from enemies.gnu import Gnu

class Wave:
    def __init__(self):
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
        self.current_wave = 1
        self.create_enemies()
        self.game_over = False

    def draw(self, surface):
        for enemy in self.enemies:
            enemy.draw(surface)

    def update(self):
        for enemy in self.enemies:
            enemy.update()
            if enemy.passed_map():
                self.enemies.remove(enemy)
                # print("popped the enemy")

        if len(self.enemies) == 0:
            if self.current_wave < len(self.waves) - 1:
                self.current_wave += 1
                self.create_enemies()

            else:
                self.game_over = True

    def is_over(self):
        return self.game_over

    def create_enemies(self):
        self.enemies = []
        crows = self.waves[self.current_wave][0]
        mages = self.waves[self.current_wave][1]
        wizards = self.waves[self.current_wave][2]
        gnus = self.waves[self.current_wave][3]
        total = crows + mages + wizards + gnus
    
        order = ["crow", "mage", "wizard", "gnu"]

        crow_count = 0
        mage_count = 0
        wizard_count = 0
        gnu_count = 0

        count = 0

        enemy_x = 0

        i = 0
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

            count += 1