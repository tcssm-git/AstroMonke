import pygame
import math
import random
import tim
import utils

screen_width = 1920
screen_height = 1020
size = 2

# Set True to draw the collision rect (same as bullet/ship checks)
SHOW_HEATH_HITBOX = False

class Heath:
    def __init__(self, heathSize):
        size = heathSize

        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)

        self.heathImage = pygame.image.load("Heath_Ledger_(2).jpg").convert_alpha() #alien sprite
        self.heathImage = pygame.transform.scale(pygame.image.load("Heath_Ledger_(2).jpg"), (30, 60))
        self.heathMask = pygame.mask.from_surface(self.heathImage)

        BLACK = (0, 0, 0)

        self.now = pygame.time.get_ticks()

        self.expired = False

    def blit(self, screen):
        image_rect = self.heathImage.get_rect()
        image_rect.x = self.x
        image_rect.y = self.y
        screen.blit(self.heathImage, image_rect)
        if SHOW_HEATH_HITBOX:
            hitbox = self.heathImage.get_rect(topleft=(self.x, self.y))
            outline = self.heathMask.outline()
            if len(outline) > 2:
                points = [(p[0] + hitbox.left, p[1] + hitbox.top) for p in outline]
                pygame.draw.polygon(screen, (0, 255, 0), points, 2)
    
#bullet collision detection
    def detectCollision(self, bullets_data, bullets_list):
        my_rect = self.heathImage.get_rect(topleft=(self.x, self.y))
        my_mask = self.heathMask
        
        for b_data in bullets_data[:]:
            b_rect, b_mask, b_tuple = b_data
            if my_rect.colliderect(b_rect):
                offset = (b_rect.left - my_rect.left, b_rect.top - my_rect.top)
                if my_mask.overlap(b_mask, offset):
                    self.expired = True
                    if b_tuple in bullets_list:
                        bullets_list.remove(b_tuple)
                    bullets_data.remove(b_data)
                    return

#ship collision detection
    def detectShipCollision(self, ship_rect, ship_mask, health):
        my_rect = self.heathImage.get_rect(topleft=(self.x, self.y))
        my_mask = self.heathMask

        if my_rect.colliderect(ship_rect):
            offset = (ship_rect.left - my_rect.left, ship_rect.top - my_rect.top)
            if my_mask.overlap(ship_mask, offset):
                self.expired = True
                if health < 100:
                    return health + 5, True
        return health, False