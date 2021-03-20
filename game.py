import pygame

from background import Background
from gui_parts.text import Text
from gui_parts.utility_methods import Utility


class Game:
    def __init__(self):
        self.width = 1250
        self.height = 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tower Defense")
        pygame.init()
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.running = True

    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing(self.screen)
            elif self.state == "menu":
                self.menu(self.screen)
            elif self.state == "win":
                self.win(self.screen)

        pygame.quit()
        quit()

    def playing(self, surface):
        """
        The game loop that controls events, drawing, and updating the game
        :param surface: surface to draw on
        :return: None
        """
        run = True
        background = Background(self.width, self.height)
        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                background.handle_mouse_clicks(event, pos)

            if background.get_game_over():
                run = False
                self.state = "win"

            background.draw(surface, pos)  
            background.update()
            pygame.display.update()

    def menu(self, surface):
        title = Text(font_name="uroob", size=45, text="TOWER DEFENSE", color=(255, 255, 255), y=self.height // 3)
        start_text = Text(font_name="uroob", size=35, text="PRESS ANY KEY TO BEGIN", color=(234, 231, 0), y=self.height // 2)
        background = Utility.get_img("assets/background.jpg", self.width, self.height)
        run = True
        circle_radius = self.width
        animation_start = False
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    animation_start = True

            if animation_start:
                circle_radius -= 1

            if circle_radius <= 0:
                self.state = "playing"
                run = False

            surface.blit(background, (0, 0))
            pygame.draw.circle(surface, (0, 0, 0), (self.width // 2, self.height // 2), circle_radius)
            title.draw_centered(surface, 0, self.width)
            start_text.draw_centered(surface, 0, self.width)
            pygame.display.update()

    def win(self, surface):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

            surface.fill((255, 255, 255))
            pygame.display.update()
