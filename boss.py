import pygame
import math
import random
import tim
import utils

screen_width = 1920
screen_height = 1020
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Him:
    def __init__(self, alienSize):
        self.vx = 0
        self.vy = 0
        self.x = screen_width/2
        self.y = -200
        self.now = pygame.time.get_ticks()
        self.currentHimFrame = 0
        self.lastHimSwitch = self.now
        self.base_speed = alienSize
        self.currentMoveChip = 0
        self.himFrameDelay = 600

        moveChip1 = ((4/8)*screen_width,(0/6)*screen_height)
        moveChip2 = ((0/8)*screen_width,(4/6)*screen_height)
        moveChip3 = ((6/8)*screen_width,(2/6)*screen_height)
        moveChip4 = ((0/8)*screen_width,(0/6)*screen_height)
        moveChip5 = ((6/8)*screen_width,(0/6)*screen_height)
        moveChip6 = ((4/8)*screen_width,(4/6)*screen_height)
        moveChip7 = ((0/8)*screen_width,(2/6)*screen_height)
        moveChip8 = ((2/8)*screen_width,(0/6)*screen_height)
        moveChip9 = ((6/8)*screen_width,(4/6)*screen_height)
        moveChip10 = ((2/8)*screen_width,(4/6)*screen_height)
        #https://www.youtube.com/watch?v=WIRK_pGdIdA
        self.moveChips = [moveChip1,moveChip2,moveChip3,moveChip4,moveChip5,moveChip6,moveChip7,moveChip8,moveChip9,moveChip10]

        spriteSheetImageHim = pygame.image.load("himothonger XIV Sr. Sr..png").convert_alpha() #1st boss sprite
        spriteSheetHim = tim.Tim(spriteSheetImageHim)

        himFrame1 = spriteSheetHim.get_image(0, 415, 415, 0.75 * utils.size, GREEN).convert_alpha() #1st boss animation

        self.himFrames = [himFrame1]
        
    def blit(self, screen):
        self.now = pygame.time.get_ticks()
        if self.now - self.lastHimSwitch > self.himFrameDelay:
            self.currentHimFrame = (self.currentHimFrame + 1) % len(self.himFrames)
            self.lastHimSwitch = self.now
        image_rect = self.himFrames[self.currentHimFrame].get_rect()
        image_rect.x = self.x
        image_rect.y = self.y
        screen.blit(self.himFrames[self.currentHimFrame], image_rect)

    def move(self):

        x,y = self.moveChips[self.currentMoveChip]

        if self.x > x - 50 and self.x < x + 50:
            self.currentMoveChip = (self.currentMoveChip + 1) % len(self.moveChips)

        self.vx = self.base_speed*((x - self.x)/(math.sqrt((y - self.y)**2+(x - self.x)**2)))*5
        self.vy = self.base_speed*((y - self.y)/(math.sqrt((y - self.y)**2+(x - self.x)**2)))*5


        self.x = self.x + self.vx
        self.y = self.y + self.vy