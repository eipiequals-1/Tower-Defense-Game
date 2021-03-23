import math

import pygame


class Utility:
    
    @staticmethod
    def get_img(img, w, h):
        """
        A reusable method that returns a image scaled to the desired size

        :param img: path to image in .png or .jpeg form
        :param w: width
        :param h: height
        :return surface: surface that user wants
        """
        return pygame.transform.scale(pygame.image.load(img).convert_alpha(), (w, h))

    @staticmethod
    def pyth_dis(x1, y1, x2, y2):
        """
        Return pythagorean distance between two objects

        :param x1: x_coord of first object
        :param y1: y_coord of first object
        :param x2: x_coord of second object
        :param y2: y_coord of second object
        :return: float
        """
        return float(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))