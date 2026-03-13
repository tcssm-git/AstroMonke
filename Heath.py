import pygame
import math
import random
import tim
import utils

screen_width = 1920
screen_height = 1020
size = 2

class Heath:
    def __init__(self, heathSize):
        size = heathSize

        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)

        self.heathImage = pygame.image.load("Heath_Ledger_(2).jpg").convert_alpha() #alien sprite

        BLACK = (0, 0, 0)

        self.now = pygame.time.get_ticks()

        self.expired = False

    def blit(self, screen):
        image_rect = self.heathImage.get_rect()
        image_rect.x = self.x
        image_rect.y = self.y
        screen.blit(self.heathImage, image_rect)
    


#bullet collision detection
    def detectCollision(self, list):
        for b in list[:]: 
            if math.sqrt(((b[0] - self.x-40 * size) ** 2) + ((b[1] - self.y-30 * size) ** 2)) < 50 * size:
                self.expired = True
                if b in list:
                    list.remove(b)
                return

#ship collision detection
    def detectShipCollision(self, shipx, shipy, health, list):
        if math.sqrt(((shipx+37 * size - self.x-40 * size) ** 2) + ((shipy+37 * size - self.y-30) ** 2)) < 60 * size:
            self.expired = True
            if health < 100:
                return health + 5, True


        return health, False