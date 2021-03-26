import pygame


class Text:
    """
    A modular class that works with pygame
    """
    def __init__(self, font_name="uroob", size=25, text="", color=(255, 255, 255), x=0, y=0, bold=False):
        """
        Initializes font and text attributes
        :param font_name: str - sys font name
        :param size: int - size in pixels
        :param text: str - words to render
        :param color: tuple - RGB form
        :param x: int - top left x
        :param y: int - top left y
        :param bold: bool - bold font or not?
        """
        self.font = pygame.font.SysFont(font_name, size, bold)
        self.color = color
        self.text = self.font.render(text, 1, self.color)
        self.x = x
        self.y = y

    def draw(self, surface):
        """
        Renders the text surface onto the screen
        :param surface: pygame.Surface - screen to draw on
        :return: None
        """
        surface.blit(self.text, (self.x, self.y))

    def draw_centered(self, surface, left, right):
        """
        Renders the text surface centered between a left and right border
        :param surface: pygame.Surface - screen to draw on
        :param left: int - left border
        :param right: int - right border
        :return: None
        """
        surface.blit(self.text, (left + (right - left) // 2 - self.text.get_width() // 2, self.y))

    def get_width(self):
        """
        Returns the text's width in pixels
        :return: int
        """
        return self.text.get_width()

    def get_height(self):
        """
        Returns the text's height in pixels
        :return: int
        """
        return self.text.get_height()

    def set_y(self, y):
        """
        Sets the y value for moving text
        :param y: int - y coord
        :return: None
        """
        self.y = y

    def set_x(self, x):
        """
        Sets the x value for moving text
        :param x: int - x coord
        :return: None
        """
        self.x = x

    def set_text(self, text):
        """
        Changes the text surface because of dynamic words
        :param text: str - words to render
        :return: None
        """
        self.text = self.font.render(text, 1, self.color)

    def draw_right(self, surface, padding, right):
        """
        Render the text on the left of a given value
        :param surface: pygame.Surface - screen to draw on
        :param padding: int - padding in pix to the left of the margin
        :param right: int - where the text needs to be to the left of
        :return: None
        """
        self.x = right - padding - self.get_width()
        surface.blit(self.text, (self.x, self.y))

    def get_text(self):
        """
        Returns a pygame.Surface with text
        :return: pygame.Surface
        """
        return self.text
