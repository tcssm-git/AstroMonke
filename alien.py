import pygame
import math
import random
import tim
import utils

screen_width = 1920
screen_height = 1020
size = 2

base_speed = 2  # Aliens move 2 pixels per frame

class AlienCube:
    def __init__(self, shipx, shipy, alienSize):
        self.vx = 0
        self.vy = 0
        size = alienSize

        e = random.randint(0,3)
        if e == 0:#bottom
            self.x = random.randint(0, screen_width) #Alien spawning mechanics
            self.y = screen_height
            self.vx = math.cos(random.uniform((4*math.pi)/3, (5*math.pi)/3)) * base_speed
            self.vy = math.sin(3*math.pi/2) * base_speed 
        elif e == 1:#top
            self.x = random.randint(0, screen_width)
            self.y = 0
            self.vx = math.cos(random.uniform((4*math.pi)/3, (5*math.pi)/3)) * base_speed
            self.vy = math.sin(math.pi/2) * base_speed
        elif e == 2:#right
            self.y = random.randint(0, screen_height)
            self.x = screen_width-50
            self.vx = math.cos(math.pi) * base_speed
            self.vy = math.sin(random.uniform((5*math.pi)/6,(7*math.pi)/6)) * base_speed
        else:#left
            self.y = random.randint(0, screen_height) 
            self.x = 0
            self.vx = math.cos(0) * base_speed
            self.vy = math.sin(random.uniform((5*math.pi)/6,(7*math.pi)/6)) * base_speed                                                       
        angle = 2 * math.pi * random.random()

        self.expired = False

        spriteSheetImageJim = pygame.image.load("Monke alien-sheet.png").convert_alpha() #alien sprite
        spriteSheetJim = tim.Tim(spriteSheetImageJim)

        BLACK = (0, 0, 0)

        jimFrame1 = spriteSheetJim.get_image(0, 50, 50, 1.7 * size, BLACK).convert_alpha() #alien animation
        jimFrame2 = spriteSheetJim.get_image(1, 50, 50, 1.7 * size, BLACK).convert_alpha()

        self.jimFrames = [jimFrame1, jimFrame2]
        self.currentJimFrame = 0
        self.jimFrameDelay = 600
        self.lastJimSwitch = pygame.time.get_ticks()

        self.now = pygame.time.get_ticks()

    def blit(self, screen):
        self.now = pygame.time.get_ticks()
        if self.now - self.lastJimSwitch > self.jimFrameDelay:
            self.currentJimFrame = (self.currentJimFrame + 1) % len(self.jimFrames)
            self.lastJimSwitch = self.now
        #print(self.now)
        image_rect = self.jimFrames[self.currentJimFrame].get_rect()
        image_rect.x = self.x
        image_rect.y = self.y
        screen.blit(self.jimFrames[self.currentJimFrame], image_rect)

    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

        if self.x < 0:
            self.expired = True
        elif self.x > screen_width:
            self.expired = True    
        elif self.y < 0:
            self.expired = True
        elif self.y > screen_height:
            self.expired = True


    def isExperied(self):
        return self.expired

    def detectCollision(self, list):
        for b in list: 
            if math.sqrt(((b[0] - self.x-40 * size) ** 2) + ((b[1] - self.y-30 * size) ** 2)) < 50 * size:
                self.expired = True
                utils.kills = utils.kills + 1
                utils.totalkills = utils.totalkills + 1

    def detectShipCollision(self, shipx, shipy, health):
        if math.sqrt(((shipx+37 * size - self.x-40 * size) ** 2) + ((shipy+37 * size - self.y-30) ** 2)) < 60 * size:
            self.expired = True
            return health - 5, True

        return health, False
    


               