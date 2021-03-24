import os
import pygame
from .enemy import Enemy

class Crow(Enemy):
    def __init__(self, x):
        super().__init__(x, 30, 56, len(os.listdir("assets/crow")), "crow/", 230)