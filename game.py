import pygame
from background import Background


class Game:
    def __init__(self):
        self.width = 1250
        self.height = 750
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tower Defense")
        pygame.init()
        self.clock = pygame.time.Clock()
        self.state = "playing"
        self.running = True

    def run(self):
        #music = pygame.mixer.music.load("assets/music.mp3")
        #pygame.mixer.music.play(-1)
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

                background.handle_user_events(event, pos)

            if background.get_game_over():
                run = False
                self.state = "win"

            background.draw(surface, pos)  
            background.update()
            pygame.display.update()

    def menu(self, surface):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.running = False

            surface.fill((245, 234, 21))
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
