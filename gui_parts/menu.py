import pygame
from .button import Button
from .utility_methods import Utility
from .text import Text

class Menu:
    def __init__(self, s_width, s_height, bomber_cost, archer_cost, coiner_cost):
        self.rect = pygame.Rect(s_width // 2 - 400, 0, 800, 75)
        self.color = (155, 103, 60)

        self.space_btwn_buttons = 80
        self.start_x = 20
        self.button_y = self.rect.h // 40

        self.bomber_tower = Button((214, 214, 10), self.rect.x + self.start_x, self.button_y, 50, 50, "BOMB", "assets/towers/bomb.png")
        self.archer_tower = Button((204, 234, 255), self.bomber_tower.rect.right + self.space_btwn_buttons, self.button_y, 50, 50, "ARCHER", "assets/towers/bow.png")
        self.coiner_tower = Button((245, 23, 13), self.archer_tower.rect.right + self.space_btwn_buttons, self.button_y, 50, 50, "ENERGY", "assets/coin.png")

        self.buttons = [self.bomber_tower, self.archer_tower, self.coiner_tower]
        self.coin_img = Utility.get_img("assets/coin.png", 25, 25)

        self.set_all_texts(bomber_cost, archer_cost, coiner_cost)

    def draw(self, surface, pos):
        pygame.draw.rect(surface, self.color, self.rect)
        for button in self.buttons:
            button.draw_with_image(surface, pos)

        self.draw_costs(surface)
        
    def update(self):
        pass

    def draw_costs(self, surface):
        """
        Simple method that draws the prices of each tower
        :param surface: surface to draw
        """
        x, y = 10, 5
        # draw the bomb cost
        surface.blit(self.coin_img, (self.bomber_tower.rect.right + x, self.button_y + y))
        # draw the archer cost
        surface.blit(self.coin_img, (self.archer_tower.rect.right + x, self.button_y + y))
        # draw the coin generater cost
        surface.blit(self.coin_img, (self.coiner_tower.rect.right + x, self.button_y + y))

        surface.blit(self.bomber_cost_text.get_text(), (self.bomber_tower.rect.right + x, self.rect.centery))
        surface.blit(self.archer_cost_text.get_text(), (self.archer_tower.rect.right + x, self.rect.centery))
        surface.blit(self.coiner_cost_text.get_text(), (self.coiner_tower.rect.right + x, self.rect.centery))

    def enough_money(self, tower, cost):
        if tower == "archer":
            return cost > 500
        elif tower == "bomber":
            return cost > 1000

    def set_all_texts(self, bomber_cost, archer_cost, coiner_cost):
        """
        Creates text objects for the cost of each tower
        """
        self.bomber_cost_text = Text("uroob", 20, str(bomber_cost), (0, 0, 0), 0, self.bomber_tower.rect.centery)
        self.archer_cost_text = Text("uroob", 20, str(archer_cost), (0, 0, 0), 0, self.archer_tower.rect.centery)
        self.coiner_cost_text = Text("uroob", 20, str(coiner_cost), (0, 0, 0), 0, self.coiner_tower.rect.centery)
        
    