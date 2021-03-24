import pygame

class WordWrap:
    """
    Creates a list of surfaces with strings
    That are word wrapped from left to right

    :param sentence: string - sentence that will be wrapped
    :param left: int - left margin
    :param right: int - right margin
    :param spacing: int - line spacing
    :param font_name: pygame.font.SysFont() - sys font name
    :param font_size: int - font size
    :param color: tuple() RGB color
    """
    def __init__(self, sentence, left, right, spacing, font_name, font_size, color=(255, 255, 255)):
        self.left = left
        self.spacing = spacing
        self.surfaces = []
        # format string to list of strings and keep \n characters
        words = sentence.strip().split(" ")

        font = pygame.font.SysFont(font_name, font_size)
        words_so_far = ""  # keeps track of words that have been added
        words_idx_blw = ""  # has one word fewer than words_so_far
        text = None
        space_btwn = right - self.left  # width for word wrap


        for i in range(len(words)):
            word = words[i]
            if word == "\n":
                # creates a new line
                text = font.render(words_so_far, 1, color)
                self.surfaces.append(text)
                words_so_far = ""
                continue
            # concatenates a new word
            words_so_far += word + " "

            # if the text is still too small
            if font.render(words_so_far, 1, color).get_width() < space_btwn:
                text = font.render(words_so_far, 1, color)
                words_idx_blw = words_so_far

            else:
                # the text is
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
        :param start_y: int - start y coordinate for text
        """
        for idx, text_surface in enumerate(self.surfaces):
            surface.blit(text_surface, (self.left, start_y + idx * self.spacing))