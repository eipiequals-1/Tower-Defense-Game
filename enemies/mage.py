import os
import pygame
from .enemy import Enemy

class Mage(Enemy):
    def __init__(self, x):
        super().__init__(x, 30, 50, len(os.listdir("assets/mage")), "mage/", 300)