import os

import pygame

from background import Background
from game_states import GameStates
from gui_parts.text import Text
from gui_parts.utility_methods import Utility
from gui_parts.word_wrap import WordWrap
from gui_parts.button import Button

class Game:
    def __init__(self):
        """
        Initializes the pygame screen and game states
        """
        pygame.init()
        self.width = 1250
        self.height = 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tower Defense")
        self.clock = pygame.time.Clock()
        self.state = GameStates.INTRO
        self.running = True

    def run(self):
        """
        Handles switching from one game state to another
        :return: None
        """
        pygame.mixer.music.load(os.path.join("music", "dark_music.ogg"))
        pygame.mixer.music.set_volume(0.5)
        while self.running:
            pygame.mixer.music.stop()
            if self.state == GameStates.PLAYING:
                pygame.mixer.music.load(os.path.join("music", "music.ogg"))
                pygame.mixer.music.play(loops=-1)
                self.playing(self.screen)
            elif self.state == GameStates.INTRO:
                pygame.mixer.music.load(os.path.join("music", "dark_music.ogg"))
                pygame.mixer.music.play(loops=-1)
                self.intro(self.screen)
            elif self.state == GameStates.WIN:
                self.win(self.screen)
            elif self.state == GameStates.RULES:
                self.rules(self.screen)
            elif self.state == GameStates.LOSE:
                self.lose(self.screen)
        pygame.quit()
        quit()

    def playing(self, surface):
        """
        The game loop that controls events, drawing, and updating the game
        :param surface: pygame.Surface - screen to draw on
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

            if background.get_win():
                run = False
                self.state = GameStates.WIN
            if background.get_lose():
                run = False
                self.state = GameStates.LOSE

            background.draw(surface, pos)  
            background.update()
            pygame.display.update()
            self.clock.tick(60)

    def intro(self, surface):
        """
        Extra game loop that handles the intro
        :param surface: pygame.Surface - screen to draw on
        :return: None
        """
        title = Text(font_name="uroob", size=45, text="TOWER DEFENSE", color=(255, 255, 255), y=self.height // 3)
        background = Utility.get_img("assets/background.jpg", self.width, self.height)
        run = True
        circle_radius = self.width
        animation_start = False

        start_btn = Button((254, 223, 0), self.width // 2 - 50, self.height * 13 // 25, 100, 50, "PLAY")
        rules_btn = Button((210, 193, 255), self.width // 2 - 50, self.height * 15 // 25, 100, 50, "HELP")
        quit_btn = Button((210, 10, 15), self.width // 2 - 50, self.height * 17 // 25, 100, 50, "QUIT")

        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_btn.is_over(pos):
                        animation_start = True
                    if rules_btn.is_over(pos):
                        run = False
                        self.state = GameStates.RULES
                    if quit_btn.is_over(pos):
                        run = False
                        self.running = False

            if animation_start:
                circle_radius -= 1

            if circle_radius <= 0:
                self.state = GameStates.PLAYING
                run = False

            surface.blit(background, (0, 0))
            pygame.draw.circle(surface, (0, 0, 0), (self.width // 2, self.height // 2), circle_radius)
            title.draw_centered(surface, 0, self.width)
            start_btn.draw_without_image(surface, pos)
            rules_btn.draw_without_image(surface, pos)
            quit_btn.draw_without_image(surface, pos)
            pygame.display.update()

    def rules(self, surface):
        """
        Handles the game state where rules are displayed
        :param surface: pygame.Surface - screen to draw on
        :return: None
        """
        run = True
        instructions = WordWrap("HOW TO PLAY \n - Use your mouse to create towers \n - Archers last about 1.4 minutes \n - Bombers last about 2 minutes \n - Coiners last about 2.7 minutes \n - Number of enemies increases each wave \n - 10 WAVES \n - Strategically place your towers using the radius drawing \n - Enemies gradually go faster", 200, self.width - 200, 35, "uroob", 35)

        back_btn = Button((255, 165, 0), self.width - 110, 10, 100, 50, "BACK")
        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    run = False
                    self.state = GameStates.PLAYING

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.is_over(pos):
                        run = False
                        self.state = GameStates.INTRO

            surface.fill((0, 0, 0))
            instructions.draw(surface, 100)
            back_btn.draw_without_image(surface, pos)
            pygame.display.update()

    def win(self, surface):
        """
        Handles the event in the case where the player wins
        :param surface: pygame.Surface - screen to draw on
        :return: None
        """
        run = True
        win_text = Text(font_name="uroob", size=45, text="YOU SURVIVED THE ATTACK!", color=(0, 0, 0), y=self.height // 3)
        home_btn = Button((155, 155, 155), self.width // 2 - 50, self.height * 13 // 25, 100, 50, "HOME")
        quit_btn = Button((210, 10, 15), self.width // 2 - 50, self.height * 17 // 25, 100, 50, "QUIT")
        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_btn.is_over(pos):
                        run = False
                        self.state = GameStates.INTRO
                    if quit_btn.is_over(pos):
                        run = False
                        self.running = False

            surface.fill((255, 255, 255))
            win_text.draw_centered(surface, 0, self.width)
            home_btn.draw_without_image(surface, pos)
            quit_btn.draw_without_image(surface, pos)
            pygame.display.update()

    def lose(self, surface):
        """
        Handles the event in the case where the player loses
        :param surface: pygame.Surface - screen to draw on
        :return: None
        """
        run = True
        lose_text = Text(font_name="uroob", size=45, text="THE MONSTERS DESTROYED YOU!", color=(0, 0, 0), y=self.height // 3)
        home_btn = Button((155, 155, 155), self.width // 2 - 50, self.height * 13 // 25, 100, 50, "HOME")
        quit_btn = Button((210, 10, 15), self.width // 2 - 50, self.height * 17 // 25, 100, 50, "QUIT")
        while run:
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if home_btn.is_over(pos):
                        run = False
                        self.state = GameStates.INTRO
                    if quit_btn.is_over(pos):
                        run = False
                        self.running = False

            surface.fill((255, 255, 255))
            lose_text.draw_centered(surface, 0, self.width)
            home_btn.draw_without_image(surface, pos)
            quit_btn.draw_without_image(surface, pos)
            pygame.display.update()