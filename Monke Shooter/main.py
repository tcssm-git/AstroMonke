import pygame
import math
import random
import alien as aln


shipimage = pygame.transform.scale(pygame.image.load("ship.png"), (80, 80))
bulletimage = pygame.transform.scale(pygame.image.load("BULLET.png"), (10, 10))
thumbimage = pygame.image.load("thumb-1920-825785.jpg")


#Timer system for 60fps
clock = pygame.time.Clock()


# Initialize Pygame
pygame.init()

font = pygame.font.SysFont(None , 48)
health = 100
decimalHealth = health/100

hptxt = f"Health: {decimalHealth*100}"
textColor = (255, 255, 255)




# Set window dimensions
screen_width = 1600
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window title
pygame.display.set_caption("Minimal Pygame Example")

def ship(i,j,a):
    image_rect = shipimage.get_rect()

    image_rect.x = i
    image_rect.y = j
    screen.blit(pygame.transform.rotate(shipimage, a), image_rect)
    screen.blit(txtsfs, hptxtRect)

def bullet(i,j):
    image_rect = bulletimage.get_rect()
    image_rect.x = i
    image_rect.y = j
    #screen.blit(bulletimage, image_rect)
    pygame.draw.circle(screen, (247, 151, 7), (i, j), 5)

#We couldn't agree on a name, so I wrote "the name that we cant agree on", and turned that into the acronym "tntwcao" and that looked like "tntcacao", so that is the name of the variable. It is the red rectangle for the healthbar
def tntcacao(health):
   
    pygame.draw.rect(screen, (255-255*decimalHealth, 255*decimalHealth, 255), (10, 10, 1580*decimalHealth, 25), width = 0)

def tntcacaobelow():
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, 1600, 45), width = 0)   

def textRect():
    pygame.draw.rect(screen, (50, 50, 50), (1350, 45, 1600, 55), width = 0) 

txtsfs = font.render(hptxt, True, textColor)  
hptxtRect = txtsfs.get_rect()
hptxtRect.topright = (1590, 50)

def totch():
    hptxt = f"Health: {health}"


bullets = []
aliens = []

#                                                      W.|W.w|w
#                                                      / . , .\
#                                  Ferdinand --->      \ _O___/
#                                                       __| |__
#                                                      |   v   |
#                                                      |_|   |_|
#                                                       W|___|W
#                                                        | | |
#                                                        |_|_|
#                                                        |=|=|

x = 750
y = 450
oldX = 0
oldY = 0
angle = 0
s = 5
u = 0

# Game loop
running = True
while running:
    clock.tick(125)  # Limit FPS to 60
  
    screen.blit(thumbimage, (0,0))

   
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append((x+40,y+40,dx*s,dy*s))
 

    keys=pygame.key.get_pressed()

    
                        
    if keys[pygame.K_d]:
        angle = angle - 1.7    

    if keys[pygame.K_a]:
        angle = angle + 1.7
            
    dx = -math.cos(math.radians(angle-90))*2
    dy = math.sin(math.radians(angle-90))*2

    if keys[pygame.K_w]:
        if y<40 and dy>0:
            y = y + dy
        elif y>screen_height-120 and dy < 0:
            y = y + dy
        elif y>40 and y < screen_height-120:
            y = y + dy
        
        if x<40 and dx>0:
            x = x + dx
        elif x>screen_width-120 and dx < 0:
            x = x + dx
        elif x>40 and x < screen_width-120:
            x = x + dx   
        

    # if(dx == 0 and dy != 0):
    #     if(dy > 0):
    #         angle = 180
    #     else:
    #         angle = 0
    # elif(dy == 0 and dx != 0):
    #     if(dx > 0):
    #         angle = 270
    #     else:
    #         angle = 90
    # elif(dy != 0 and dx != 0):
    #     angle = math.degrees(math.atan2(-dy, dx)) - 90
    
    

    ship(x,y,angle)
    b = 0
    while((b)<len(bullets)):
        bullets[b] = (bullets[b][0]+bullets[b][2], bullets[b][1]+bullets[b][3], bullets[b][2], bullets[b][3])
        bullet(bullets[b][0], bullets[b][1])
        b = b + 1

    #print(aliens)

    if u%100 == 0:
        a = aln.AlienCube(oldX, oldY)
        aliens.append(a) 
        a = aln.AlienCube(oldX, oldY)
        aliens.append(a) 
    
    for a in aliens:
        a.move()
        a.detectCollision(bullets)
        a.blit(screen)
        
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

    tntcacaobelow()
    textRect()
    screen.blit(txtsfs, hptxtRect)
    tntcacao(health)
    #totch()

    oldY = y
    oldX = x
   
        # Update the display   
    pygame.display.flip()
    u = u + 1

    health = health - 0.01
    
    
        

# Quit Pygame
pygame.quit()