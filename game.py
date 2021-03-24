import pygame

from background import Background
from game_states import GameStates
from gui_parts.text import Text
from gui_parts.utility_methods import Utility
from gui_parts.word_wrap import WordWrap

class Game:
    def __init__(self):
        self.width = 1250
        self.height = 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tower Defense")
        pygame.init()
        self.clock = pygame.time.Clock()
        self.state = GameStates.PLAYING
        self.running = True

    def run(self):
        """
        Handles switching from one game state to another
        """
        while self.running:
            if self.state == GameStates.PLAYING:
                self.playing(self.screen)
            elif self.state == GameStates.INTRO:
                self.intro(self.screen)
            elif self.state == GameStates.WIN:
                self.win(self.screen)
            elif self.state == GameStates.RULES:
                self.rules(self.screen)

        pygame.quit()
        quit()

    def playing(self, surface):
        """
        The game loop that controls events, drawing, and updating the game
        :param surface: screen to draw on
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
                self.state = GameStates.WIN

            background.draw(surface, pos)  
            background.update()
            pygame.display.update()
            self.clock.tick(60)

    def intro(self, surface):
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
                self.state = GameStates.RULES
                run = False

            surface.blit(background, (0, 0))
            pygame.draw.circle(surface, (0, 0, 0), (self.width // 2, self.height // 2), circle_radius)
            title.draw_centered(surface, 0, self.width)
            start_text.draw_centered(surface, 0, self.width)
            pygame.display.update()

    def rules(self, surface):
        run = True
        instructions = WordWrap("HOW TO PLAY \n - Use your mouse to create towers \n - Archers last about 2 minutes \n - Bombers last about 3 minutes \n - Coiners last about 7 minutes \n - Number of enemies increases each wave \n - 10 WAVES \n - Strategically place your towers using the radius drawing \n - Enemies gradually go faster \n \n \n PRESS ANY KEY TO START", 200, self.width - 200, 35, "uroob", 35)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    run = False
                    self.state = GameStates.PLAYING

            surface.fill((0, 0, 0))
            instructions.draw(surface, 100)
            pygame.display.update()

    def win(self, surface):
        run = True
        win_text = Text(font_name="uroob", size=45, text="YOU SURVIVED THE ATTACK!", color=(0, 0, 0), y=self.height // 3)
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

            surface.fill((255, 255, 255))
            win_text.draw_centered(surface, 0, self.width)
            pygame.display.update()
