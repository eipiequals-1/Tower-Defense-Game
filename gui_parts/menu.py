import pygame
from .button import Button
from gui_parts.utility_methods import Utility

class Menu:
    def __init__(self, s_width, s_height):
        self.rect = pygame.Rect(s_width // 2 - 400, 0, 800, 75)
        self.color = (155, 103, 60)
        self.space_btwn_buttons = 80
        self.start_x = 20
        self.button_y = self.rect.h // 40
        self.bomb_tower = Button((214, 214, 10), self.rect.x + self.start_x, self.button_y, 50, 50, "BOMB", "assets/towers/bomb.png")
        self.archer_tower = Button((204, 234, 255), self.bomb_tower.rect.right + self.space_btwn_buttons, self.button_y, 50, 50, "ARCHER", "assets/towers/bow.png")
        self.buttons = [self.bomb_tower, self.archer_tower]
        self.coin_img = Utility.get_img("assets/coin.png", 25, 25)

    def draw(self, surface, pos):
        pygame.draw.rect(surface, self.color, self.rect)
        for button in self.buttons:
            button.draw_with_image(surface, pos)

        self.draw_costs(surface)
        
    def update(self):
        pass

    def draw_costs(self, surface):
        """
        
        """
        x, y = 10, 5
        # draw the bomb cost
        surface.blit(self.coin_img, (self.bomb_tower.rect.right + x, self.button_y + y))
        # draw the archer cost
        surface.blit(self.coin_img, (self.archer_tower.rect.right + x, self.button_y + y))

    def enough_money(self, tower, cost):
        if tower == "archer":
            return cost > 500
        elif tower == "bomber":
            return cost > 1000