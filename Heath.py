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
        self.heathImage = pygame.transform.scale(pygame.image.load("Heath_Ledger_(2).jpg"), (30, 60))

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
        hitbox = self.heathImage.get_rect(topleft=(self.x, self.y))
        for b in list[:]: 
            bullet_rect = pygame.Rect(b[0], b[1], 10, 10)
            if hitbox.colliderect(bullet_rect):
                self.expired = True
                if b in list:
                    list.remove(b)
                return

#ship collision detection
    def detectShipCollision(self, shipx, shipy, health, list):
        hitbox = self.heathImage.get_rect(topleft=(self.x, self.y))
        ship_size_approx = 50 * 1.7 * size
        ship_rect = pygame.Rect(shipx, shipy, ship_size_approx, ship_size_approx)

        if hitbox.colliderect(ship_rect):
            self.expired = True
            if health <= 100-12:
                return health + 12, True
            else:
                return 100, True
        return health, False