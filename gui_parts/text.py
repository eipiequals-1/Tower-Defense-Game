import pygame

class Text:
    def __init__(self, font_name="uroob", size=25, text="", color=(255, 255, 255), x=0, y=0):
        self.font = pygame.font.SysFont(font_name, size)
        self.text = self.font.render(text, 1, color)
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.text, (x, y))

    def draw_centered(self, surface, left, right):
        surface.blit(self.text, (left + (right - left) // 2 - self.text.get_width() // 2, self.y))

    def get_width(self):
        return self.text.get_width()

    def get_height(self):
        return self.text.get_height()

    def set_y(self, y):
        self.y = y