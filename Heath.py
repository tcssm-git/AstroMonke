import pygame
import math
import random
import tim
import utils

pygame.mixer.init()
screen_width = 1920
screen_height = 1020
size = 2
heathNoise = pygame.mixer.Sound("Heal.wav")
damageNoise = pygame.mixer.Sound("Damage.wav")

# Set True to draw the collision rect (same as bullet/ship checks)
SHOW_HEATH_HITBOX = False

class Heath:
    def __init__(self, heathSize):
        size = heathSize

        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)

        spriteSheetImageHeath = pygame.image.load("Heath-sheet.png").convert_alpha()
        spriteSheetHeath = tim.Tim(spriteSheetImageHeath)

        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)

        heathFrame1 = spriteSheetHeath.get_image(0, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame2 = spriteSheetHeath.get_image(1, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame3 = spriteSheetHeath.get_image(2, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame4 = spriteSheetHeath.get_image(3, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame5 = spriteSheetHeath.get_image(4, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame6 = spriteSheetHeath.get_image(5, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame7 = spriteSheetHeath.get_image(6, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame8 = spriteSheetHeath.get_image(7, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame9 = spriteSheetHeath.get_image(8, 30, 30, 1.5 * size, WHITE).convert_alpha()
        heathFrame10 = spriteSheetHeath.get_image(9, 30, 30, 1.5 * size, WHITE).convert_alpha()

        self.heathFrames = [heathFrame1, heathFrame2, heathFrame3, heathFrame4, heathFrame5, heathFrame6, heathFrame7, heathFrame8, heathFrame9, heathFrame10]
        self.currentHeathFrame = 0
        self.isAnimaniting = True
        self.now = pygame.time.get_ticks()
        self.heathMasks = [pygame.mask.from_surface(f) for f in self.heathFrames]

        self.expired = False

    def blit(self, screen):
        if self.isAnimaniting == True:
            self.currentHeathFrame += 0.05
            if int(self.currentHeathFrame) == len(self.heathFrames)-1:
                self.isAnimaniting = False
            else:
                image_rect = self.heathFrames[int(self.currentHeathFrame)].get_rect()
                image_rect.x = self.x
                image_rect.y = self.y
                screen.blit(self.heathFrames[int(self.currentHeathFrame)], image_rect)
        else:
            image_rect = self.heathFrames[9].get_rect()
            image_rect.x = self.x
            image_rect.y = self.y
            screen.blit(self.heathFrames[9], image_rect)
            
             




        if SHOW_HEATH_HITBOX:
            hitbox = self.heathImage.get_rect(topleft=(self.x, self.y))
            outline = self.heathMask.outline()
            if len(outline) > 2:
                points = [(p[0] + hitbox.left, p[1] + hitbox.top) for p in outline]
                pygame.draw.polygon(screen, (0, 255, 0), points, 2)
    
#bullet collision detection
    def detectCollision(self, bullets_data, bullets_list):
        my_rect = self.heathFrames[int(self.currentHeathFrame)].get_rect(topleft=(self.x, self.y))
        my_mask = self.heathMasks[int(self.currentHeathFrame)]
        
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
        my_rect = self.heathFrames[int(self.currentHeathFrame)].get_rect(topleft=(self.x, self.y))
        my_mask = self.heathMasks[int(self.currentHeathFrame)]

        if my_rect.colliderect(ship_rect):
            self.expired = True
            heathNoise.play()
            if health <= 100-12:
                return health + 12, True
            else:
                return 100, True
        return health, False