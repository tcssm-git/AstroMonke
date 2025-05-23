import pygame
import math
import random

screen_width = 1600
screen_height = 1000

base_speed = random.uniform(1.0, 3.0)  # Aliens move between 1 and 3 pixels per frame

class AlienCube:
    def __init__(self, shipx, shipy):
        self.vx = 0
        self.vy = 0

        e = random.randint(0,3)
        if e == 0:#bottom
            self.x = random.randint(0, screen_width)
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
        #angle = random.uniform(0, 2 * math.pi)  # Random direction in radians
        angle = 2 * math.pi * random.random()

        #self.vx = random.randint(-10, 10)/10
        #self.vy = random.randint(-10, 10)/10
 

        #print(f'X Velocity: {self.vx}, Y Velocity: {self.vy}')
        self.jontcoobimage = pygame.transform.scale(pygame.image.load("Jont coob alien.png"), (80, 60))
        self.expired = False
        #while math.sqrt(((shipx - self.x) ** 2) + ((shipy - self.y) ** 2)) < 100:
            #self.expired = True

    def blit(self, screen):
        image_rect = self.jontcoobimage.get_rect()
        image_rect.x = self.x
        image_rect.y = self.y
        screen.blit(self.jontcoobimage, image_rect)

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
            if math.sqrt(((b[0] - self.x-40) ** 2) + ((b[1] - self.y-30) ** 2)) < 25:
                self.expired = True

               