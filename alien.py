import pygame
import math
import random
import tim
import utils

pygame.mixer.init()
screen_width = 1920
screen_height = 1020
size = 2
damageNoise = pygame.mixer.Sound("Damage.wav")

# Set True to draw collision rect (sprite bounds = bullet + ship hit area)
SHOW_ALIEN_HITBOX = False

base_speed = 2  # Aliens move 2 pixels per frame
jimboomimage = pygame.transform.scale(pygame.image.load("Big_BOOM_temp.png"), (500, 500)) #BOOM

class AlienCube:
    def __init__(self, shipx, shipy, alienSize):
        self.vx = 0
        self.vy = 0
        self.x = 0
        self.y = 0
        self.expired = False
        size = alienSize

        e = random.randint(0, 3)

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

        utils.buttonDelay = 0

        self.expired = False

        spriteSheetImageJim = pygame.image.load("Monke alien-sheet.png").convert_alpha() #alien sprite
        spriteSheetJim = tim.Tim(spriteSheetImageJim)

        BLACK = (0, 0, 0)

        jimFrame1 = spriteSheetJim.get_image(0, 50, 50, 1.7 * size, BLACK).convert_alpha() #alien animation
        jimFrame2 = spriteSheetJim.get_image(1, 50, 50, 1.7 * size, BLACK).convert_alpha()

        self.jimFrames = [jimFrame1, jimFrame2]
        self.jimMasks = [pygame.mask.from_surface(f) for f in self.jimFrames]
        self.currentJimFrame = 0
        self.jimFrameDelay = 600
        self.lastJimSwitch = pygame.time.get_ticks()

        self.now = pygame.time.get_ticks()

    def blit(self, screen):
        self.now = pygame.time.get_ticks()
        if self.now - self.lastJimSwitch > self.jimFrameDelay:
            self.currentJimFrame = (self.currentJimFrame + 1) % len(self.jimFrames)
            self.lastJimSwitch = self.now
        image_rect = self.jimFrames[self.currentJimFrame].get_rect()
        image_rect.x = self.x
        image_rect.y = self.y
        screen.blit(self.jimFrames[self.currentJimFrame], image_rect)
        if SHOW_ALIEN_HITBOX:
            r = self._hit_rect()
            my_mask = self.jimMasks[self.currentJimFrame]
            outline = my_mask.outline()
            if len(outline) > 2:
                points = [(p[0] + r.left, p[1] + r.top) for p in outline]
                pygame.draw.polygon(screen, (0, 220, 255), points, 2)

    def _hit_rect(self):
        """Sprite bounds — same rect used for bullet and ship collision."""
        surf = self.jimFrames[self.currentJimFrame]
        return surf.get_rect(topleft=(int(self.x), int(self.y)))

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

    def detectCollision(self, bullets_data, bullets_list):
        damageNoise.play
        my_rect = self._hit_rect()
        my_mask = self.jimMasks[self.currentJimFrame]

        for b_data in bullets_data[:]:
            b_rect, b_mask, b_tuple = b_data
            if my_rect.colliderect(b_rect):
                offset = (b_rect.left - my_rect.left, b_rect.top - my_rect.top)
                if my_mask.overlap(b_mask, offset):
                    self.expired = True
                    utils.kills = utils.kills + 1
                    utils.needFirstKill = False  
                    utils.totalkills = utils.totalkills + 1
                    if b_tuple in bullets_list:
                        bullets_list.remove(b_tuple)
                    bullets_data.remove(b_data)
                    return

    def detectShipCollision(self, ship_rect, ship_mask, health):
        my_rect = self._hit_rect()
        my_mask = self.jimMasks[self.currentJimFrame]
        if my_rect.colliderect(ship_rect):
            offset = (ship_rect.left - my_rect.left, ship_rect.top - my_rect.top)
            if my_mask.overlap(ship_mask, offset):
                self.expired = True
                damageNoise.play()
                return health - 5, True

        return health, False
    
    def jimExplode(self, screen):
        screen.blit(jimboomimage, (self.x, self.y))
        self.expired = True
