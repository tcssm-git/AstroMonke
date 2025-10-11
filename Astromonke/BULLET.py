import pygame
import math
import random

class Bullet:
    def __init__(self,_x,_y,_vx,_vy):
        self.x = _x
        self.y = _y
        self.vx = _vx
        self.vy = _vy
        self.id = random.randint(-999, 999)

       

    