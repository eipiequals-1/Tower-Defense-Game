import pygame

from gui_parts.text import Text
from gui_parts.utility_methods import Utility


class Button:
    """
    A reusable button class that has images and/or text
    """
    def __init__(self, color, x, y, w, h, text="", img=""):
        self.rect = pygame.Rect(x, y, w, h)
        if img != "":
            self.img = Utility.get_img(img, self.rect.w, self.rect.h)
            self.text = Text("uroob", 25, text, (0, 0, 0), x=self.rect.left, y=self.rect.bottom + 5)
        else:
            self.text = Text("uroob", 25, text, (0, 0, 0), self.rect.left, self.rect.y + 15)
        self.color = color
        self.over_color = self.get_new_color(self.color)

    def draw_with_image(self, surface, pos):
        if not self.is_over(pos):
            pygame.draw.rect(surface, self.color, self.rect)            
        else:
            pygame.draw.rect(surface, self.over_color, self.rect)

        surface.blit(self.img, self.rect)
        self.text.draw_centered(surface, self.rect.left, self.rect.right)

    def draw_without_image(self, surface, pos):
        if not self.is_over(pos):
            pygame.draw.rect(surface, self.color, self.rect)
        else:
            pygame.draw.rect(surface, self.over_color, self.rect)

        self.text.draw_centered(surface, self.rect.left, self.rect.right)
            
    def is_over(self, pos):
        return self.rect.collidepoint(pos)

    @staticmethod
    def get_new_color(color):
        r = color[0]
        g = color[1]
        b = color[2]

        new_r = r + 30
        new_g = g + 30
        new_b = b + 30
        if new_r > 255:
            new_r = r - 30
        if new_g > 255:
            new_g = g - 30
        if new_b > 255:
            new_b = b - 30

        return (new_r, new_g, new_b)
