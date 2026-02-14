#  ͡( ͡° ͜ʖ ͡°)   <---- Lord Lenny

import pygame
import math
import random
import alien as aln
import tim
import time
import utils

screen_width = 1920
screen_height = 1020
damaged_screen = pygame.Surface((screen_width, screen_height))
damaged_screen.fill((255, 0, 0))
alpha = 0
fade_speed = 2
size = 2
wave = 0
fading = False
fade_direction = 1
gameover = False
damageTaken = False
screen = pygame.display.set_mode((screen_width, screen_height))
bulletimage = pygame.transform.scale(pygame.image.load("BULLET.png"), (10, 10))
thumbimage = pygame.image.load("thumb-1920-825785.jpg") #background image
ubededimage = pygame.transform.scale(pygame.image.load("Untitled_Presentation.png"), (screen_width, screen_height)) #deathscreen
ubegonnarespawnimage = pygame.transform.scale(pygame.image.load("Respawn_pressed.png"), (screen_width, screen_height)) #respawn button pressed
ubegonnaexitimage = pygame.transform.scale(pygame.image.load("Exit_pressed.png"), (screen_width, screen_height)) #exit button pressed
ubegoimage = pygame.transform.scale(pygame.image.load("Start screen.png"), (screen_width, screen_height)) #startscreen
ubegonowimage = pygame.transform.scale(pygame.image.load("Start screen pressed.png"), (screen_width, screen_height)) #startscreen but pressed

def player_takes_damage():
    global fading, fade_direction, alpha
    fading = True 
    fade_direction = 1
    alpha = 0
    damageTaken = False

#player sprite sheet
spriteSheetImageTim = pygame.image.load("Monke ship-Sheet.png").convert_alpha()
spriteSheetTim = tim.Tim(spriteSheetImageTim)

#player moving sprite sheet
spriteSheetImageTimFire = pygame.image.load("Monke_ship_fire-Sheet.png").convert_alpha()
spriteSheetTimFire = tim.Tim(spriteSheetImageTimFire)

#bullet sprite sheet
spriteSheetImageBullet = pygame.image.load("Monke bullet-Sheet.png").convert_alpha()
spriteSheetBullet = tim.Tim(spriteSheetImageBullet)

BLACK = (0, 0, 0)

#player anim frames
timFrame1 = spriteSheetTim.get_image(0, 50, 50, 1.7 * size, BLACK).convert_alpha()
timFrame2 = spriteSheetTim.get_image(1, 50, 50, 1.7 * size, BLACK).convert_alpha()

#palyer moving anim frames
timFireFrame1 = spriteSheetTimFire.get_image(0, 50, 50, 1.7 * size, BLACK).convert_alpha()
timFireFrame2 = spriteSheetTimFire.get_image(1, 50, 50, 1.7 * size, BLACK).convert_alpha()
timFireFrame3 = spriteSheetTimFire.get_image(2, 50, 50, 1.7 * size, BLACK).convert_alpha()
timFireFrame4 = spriteSheetTimFire.get_image(3, 50, 50, 1.7 * size, BLACK).convert_alpha()

#bullet anim frames
bulletFrame1 = spriteSheetBullet.get_image(0, 10, 10, 3 * size, BLACK).convert_alpha()
bulletFrame2 = spriteSheetBullet.get_image(1, 10, 10, 3 * size, BLACK).convert_alpha()
bulletFrame3 = spriteSheetBullet.get_image(2, 10, 10, 3 * size, BLACK).convert_alpha()
bulletFrame4 = spriteSheetBullet.get_image(3, 10, 10, 3 * size, BLACK).convert_alpha()
bulletFrame5 = spriteSheetBullet.get_image(4, 10, 10, 3 * size, BLACK).convert_alpha()
bulletFrame6 = spriteSheetBullet.get_image(5, 10, 10, 3 * size, BLACK).convert_alpha()
bulletFrame7 = spriteSheetBullet.get_image(6, 10, 10, 3 * size, BLACK).convert_alpha()
bulletFrame8 = spriteSheetBullet.get_image(7, 10, 10, 3 * size, BLACK).convert_alpha()

#player anim variables
timFrames = [timFrame1, timFrame2]
currentTimFrame = 0
timFrameDelay = 600
lastTimSwitch = pygame.time.get_ticks()

#player moving anim variables
timFireFrames = [timFireFrame1, timFireFrame2, timFireFrame3, timFireFrame4]
currentTimFireFrame = 0
timFireFrameDelay = 200
lastTimFireSwitch = pygame.time.get_ticks()

#player anim variables
bulletFrames = [bulletFrame1, bulletFrame2, bulletFrame3, bulletFrame4, bulletFrame5, bulletFrame6, bulletFrame7, bulletFrame8]
currentBulletFrame = 0
bulletFrameDelay = 100
lastBulletSwitch = pygame.time.get_ticks()

#Timer system for 60fps
clock = pygame.time.Clock()

# Initialize Pygame
pygame.init()

font = pygame.font.SysFont(None , 50)
health = 100
decimalHealth = health/100

textColor = (255, 255, 255)

hptxt = f"Health: {int(decimalHealth*100)}"
txtsfs = font.render(hptxt, True, textColor)  
hptxtRect = txtsfs.get_rect()
hptxtRect.topright = (screen_width - 10, 55)

wavetxt = f"Wave: {str(wave)}"
txtswing = font.render(wavetxt, True, textColor)  
wavetxtRect = txtswing.get_rect()
wavetxtRect.topleft = (50, 55)

killstxt = f"Kills: {str(utils.kills)}"
txtshipK = font.render(killstxt, True, textColor)  
killstxtRect = txtshipK.get_rect()
killstxtRect.topleft = (250, 55)

#screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("Minimal Pygame Example")

def ship(i,j,a,whichFrame):
    image_rect = whichFrame.get_rect()
    image_rect.x = i
    image_rect.y = j
    if health > 0:
        screen.blit(pygame.transform.rotate(whichFrame, a), image_rect)
        screen.blit(txtsfs, hptxtRect)
        screen.blit(txtswing, wavetxtRect)

def bullet(i,j, whichFrame):
    image_rect = bulletimage.get_rect()
    image_rect.x = i
    image_rect.y = j
    if health > 0:
        #screen.blit(bulletimage, image_rect)
        #pygame.draw.circle(screen, (247, 151, 7), (i, j), 5)
        screen.blit(whichFrame, image_rect)
        #screen.blit(txtsfs, hptxtRect)

#We couldn't agree on a name, so I wrote "the name that we cant agree on", and turned that into the acronym "tntwcao" and that looked like "tntcacao", so that is the name of the variable. It is the rectangle for the healthbar
def tntcacao():
    if decimalHealth > 0:
       pygame.draw.rect(screen, (255-decimalHealth*255, decimalHealth*255, 255), (10, 10, (screen_width-20)*decimalHealth, 25), width = 0)

def tntcacaobelow():
    if health > 0:
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, screen_width, 45), width = 0)   

def textRect():
    if health > 0:
        pygame.draw.rect(screen, (67, 67, 67), (0, 45, screen_width, 55), width = 0) 

def totch(): 
    hptxt = f"Health: {decimalHealth*100}"
    txtsfs = font.render(hptxt, True, textColor)
    wavetxt = f"Wave: {str(wave)}"
    txtswing = font.render(wavetxt, True, textColor)
    #hptxtRect = txtsfs.get_rect()

bullets = []
aliens = []

#                                                      w.|W.w|w
#                                                      / . , .\
#                                  Ferdinand --->      \ __o_ /
#                                                       __| |__
#                                                      |   v   |
#                                                      |_|   |_|
#                                                       W|___|W
#                                                        | | |
#                                                        |_|_|
#                                                        |=|=|

timer = 0
wave = 0
x = screen_width/2
y = screen_height/2
oldX = 0
oldY = 0
angle = 0.01
s = 5
u = 0
dx = 0
dy = 0
dxx = 442
dyy = 145
running = True
gamestarted = False

buttonPresssed = False
buttonDelay = 0

endButtonPressed = False
# Game loop
    
#screen.blit(ubegoimage, (0,0))
if gamestarted == False and buttonPresssed == False:
    screen.blit(ubegoimage, (0,0))

while running:
    now = pygame.time.get_ticks()
    clock.tick(125)

    if gamestarted == False:
        # Draw the menu background every frame while in menu mode
        if not buttonPresssed:
            screen.blit(ubegoimage, (0,0))
        else:
            screen.blit(ubegonowimage, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    buttonPresssed = True
            
        if buttonPresssed:
            buttonDelay += 1
            if buttonDelay > 25:
                gamestarted = True
        
        pygame.display.flip() # Keep the menu updating
        if buttonPresssed:   #for play button
            buttonDelay += 1
        if buttonDelay > 25:
            gamestarted = True
    else:

        if gameover == True:
            aliens = []
            if endButtonPressed == False:
                screen.blit(ubededimage, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    m_x, m_y = pygame.mouse.get_pos()
                    if(m_x > (166) and m_x < (166 + dxx)) and (m_y > (698) and m_y < (698 + dyy)): #respawn
                        health = 100
                        gameover = False
                        endButtonPressed = False                  
                        aliens = []
                        bullets = []
                        angle = 0.01
                        x, y = screen_width/2, screen_height/2 
                        size = 2
                    if(m_x > (1100) and m_x < (1100 + dxx)) and (m_y > (698) and m_y < (698 + dyy)): #exit to menu
                        gamestarted = False
                        buttonPresssed = False
                        buttonDelay = 0
                        
                        health = 100
                        decimalHealth = 1.0
                        gameover = False
                        endButtonPressed = False
                        bullets = []
                        aliens = []
                        angle = 0.01
                        x, y = screen_width/2, screen_height/2                                                                      

        if gameover==False:
            screen.blit(thumbimage, (0,0))

        timMoving = False

        if health <= 0:
            gameover = True

        #player anim frames
        timFrame1 = spriteSheetTim.get_image(0, 50, 50, 1.7 * size, BLACK).convert_alpha()
        timFrame2 = spriteSheetTim.get_image(1, 50, 50, 1.7 * size, BLACK).convert_alpha()

        #palyer moving anim frames
        timFireFrame1 = spriteSheetTimFire.get_image(0, 50, 50, 1.7 * size, BLACK).convert_alpha()
        timFireFrame2 = spriteSheetTimFire.get_image(1, 50, 50, 1.7 * size, BLACK).convert_alpha()
        timFireFrame3 = spriteSheetTimFire.get_image(2, 50, 50, 1.7 * size, BLACK).convert_alpha()
        timFireFrame4 = spriteSheetTimFire.get_image(3, 50, 50, 1.7 * size, BLACK).convert_alpha()

        #bullet anim frames
        bulletFrame1 = spriteSheetBullet.get_image(0, 10, 10, 3 * size, BLACK).convert_alpha()
        bulletFrame2 = spriteSheetBullet.get_image(1, 10, 10, 3 * size, BLACK).convert_alpha()
        bulletFrame3 = spriteSheetBullet.get_image(2, 10, 10, 3 * size, BLACK).convert_alpha()
        bulletFrame4 = spriteSheetBullet.get_image(3, 10, 10, 3 * size, BLACK).convert_alpha()
        bulletFrame5 = spriteSheetBullet.get_image(4, 10, 10, 3 * size, BLACK).convert_alpha()
        bulletFrame6 = spriteSheetBullet.get_image(5, 10, 10, 3 * size, BLACK).convert_alpha()
        bulletFrame7 = spriteSheetBullet.get_image(6, 10, 10, 3 * size, BLACK).convert_alpha()
        bulletFrame8 = spriteSheetBullet.get_image(7, 10, 10, 3 * size, BLACK).convert_alpha()

        timFrames = [timFrame1, timFrame2]
        timFireFrames = [timFireFrame1, timFireFrame2, timFireFrame3, timFireFrame4]
        bulletFrames = [bulletFrame1, bulletFrame2, bulletFrame3, bulletFrame4, bulletFrame5, bulletFrame6, bulletFrame7, bulletFrame8]

        if now - lastBulletSwitch > bulletFrameDelay:
            currentBulletFrame = (currentBulletFrame + 1) % len(bulletFrames)
            lastBulletSwitch = now
    
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append((x+37*size,y+37*size,dx*s,dy*s))
       
        if fading:
            alpha += fade_speed * fade_direction

            if fade_direction == 1 and alpha >= 30:
                alpha = 30
                fade_direction = -1
            elif fade_direction == -1 and alpha <= 0:
                alpha = 0
                fading = False

            damaged_screen.set_alpha(alpha)
            screen.blit(damaged_screen, (0, 0))

        keys=pygame.key.get_pressed()
                        
        if keys[pygame.K_d]:
            angle = angle - 1.7    

        if keys[pygame.K_a]:
            angle = angle + 1.7
                    
        dx = -math.cos(math.radians(angle-90))*2
        dy = math.sin(math.radians(angle-90))*2

        if keys[pygame.K_w]:
            timMoving = True

            if y<50 and dy>0:
                y = y + dy
            elif y>screen_height-120 and dy < 0:
                y = y + dy
            elif y>50 and y < screen_height-120:
                y = y + dy
            
            if x<50 and dx>0:
                x = x + dx
            elif x>screen_width-120 and dx < 0:
                x = x + dx
            elif x>50 and x < screen_width-120:
                x = x + dx   
        
        if now - lastTimSwitch > timFrameDelay:
            currentTimFrame = (currentTimFrame + 1) % len(timFrames)
            lastTimSwitch = now

        if now - lastTimFireSwitch > timFireFrameDelay:
            currentTimFireFrame = (currentTimFireFrame + 1) % len(timFireFrames)
            lastTimFireSwitch = now

        if timMoving:
            ship(x,y,angle,timFireFrames[currentTimFireFrame])
        else:
            ship(x,y,angle,timFrames[currentTimFrame])

        b = 0
        while((b)<len(bullets)):
            bullets[b] = (bullets[b][0]+bullets[b][2], bullets[b][1]+bullets[b][3], bullets[b][2], bullets[b][3])
            bullet(bullets[b][0], bullets[b][1], bulletFrames[currentBulletFrame])
            b = b + 1

        if u%100 * size == 0 and not gameover:
            if utils.kills >= 10:
                utils.kills=0
                size = size - 0.05          
            a = aln.AlienCube(oldX, oldY, size)
            aliens.append(a) 
            a = aln.AlienCube(oldX, oldY, size)
            aliens.append(a) 
        
        for a in aliens:
            a.move()
            a.detectCollision(bullets)
            a.blit(screen)
            health, damageTaken = a.detectShipCollision(x,y, health)
            if damageTaken: 
                player_takes_damage()
            
        aliens[:] = [a for a in aliens if not a.isExperied()] 

        o = 0
        while(o<len(bullets)-1):
            if bullets[o][0] < 0:
                _ = bullets.pop(o)
            elif bullets[o][0] > screen_width:
                _ = bullets.pop(o)      
            elif bullets[o][1] < 0:
                _ = bullets.pop(o)
            elif bullets[o][1] > screen_height:
                _ = bullets.pop(o) 
            else:
                o = o + 1

        if decimalHealth >= 0:
            hptxt = f"Health: {int(decimalHealth*100)}"
        else:
            hptxt = f"Health: {int(0)}"
            
        killstxt = f"Kills: {str(utils.kills)}"
        txtsfs = font.render(hptxt, True, textColor)  
        txtswing = font.render(wavetxt, True, textColor) 
        txtshipK = font.render(killstxt, True, textColor) 
        hptxtRect = txtsfs.get_rect()
        wavetxtRect = txtswing.get_rect()
        killstxtRect = txtshipK.get_rect()
        hptxtRect.topright = (screen_width - 50, 55)
        wavetxtRect.topleft = (50, 55)
        killstxtRect.topleft = (250, 55)
        tntcacaobelow()
        textRect()
        screen.blit(txtswing, wavetxtRect)
        screen.blit(txtsfs, hptxtRect)
        screen.blit(txtshipK, killstxtRect)
        tntcacao()
        totch()
        
        oldY = y
        oldX = x
    
            # Update the display   
        pygame.display.flip()
        u = u + 1

        decimalHealth = health/100
    
# Quit Pygame
pygame.quit()
