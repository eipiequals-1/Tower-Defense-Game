import pygame

class WordWrap:
    def __init__(self, sentence, left, right, spacing, font_name, font_size, color=(255, 255, 255)):
        """
        Creates a list of surfaces with strings
        That are word wrapped from left to right

        :param sentence: string
        :param left: left margin
        :param right: right margin
        :param spacing: line spacing
        :param font_name: sys font name
        :param font_size: int of font size
        :param color: RGB color tuple
        """
        self.left = left
        self.spacing = spacing
        self.surfaces = []
        # format string to list of strings and keep \n characters
        words = sentence.strip().split(" ")

        font = pygame.font.SysFont(font_name, font_size)
        words_so_far = ""
        words_idx_blw = ""
        text = None
        space_btwn = right - self.left


        for i in range(len(words)):
            word = words[i]
            if word == "\n":
                text = font.render(words_so_far, 1, color)
                self.surfaces.append(text)
                words_so_far = ""
                continue
            words_so_far += word + " "

            if font.render(words_so_far, 1, color).get_width() < space_btwn:
                text = font.render(words_so_far, 1, color)
                words_idx_blw = words_so_far

            else:
                text = font.render(words_idx_blw, 1, color)
                self.surfaces.append(text)
                words_so_far = ""

            if i == len(words) - 1:
                text = font.render(words_idx_blw, 1, color)
                self.surfaces.append(text)                
        

    def draw(self, surface, start_y):
        """
        Draws the list of surfaces onto the pygame main surface
        :param surface: pygame screen
        :param start_y: start_y for text
        """
        for idx, text_surface in enumerate(self.surfaces):
            surface.blit(text_surface, (self.left, start_y + idx * self.spacing))