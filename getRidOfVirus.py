
# import modules
import pygame, sys
from pygame.locals import *
import random, time
 
# initializing 
pygame.init()
 
# setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()
 
# creating colors
RED   = (245, 46, 46)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# other variables for use in the program
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 500 
SPEED = 5
SCORE = 0

TEMP = 0
RANDINT = 0

# setting up fonts
font = pygame.font.SysFont("impactttf", 50)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over" , True, RED)

background = pygame.image.load("media/background.jpg")
background = pygame.transform.scale(background, (DISPLAY_WIDTH,DISPLAY_HEIGHT))
 
# create a white screen 
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Get Rid of The Virus!")
 

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
    	super().__init__() 
    	image = pygame.image.load("media/virus.png")
    	self.image = pygame.transform.scale(image, (70, 70))
    	self.surf = pygame.Surface((70, 70))
    	self.rect = self.surf.get_rect(center = (random.randint(40, DISPLAY_WIDTH-40), 0))
    
    def move1(self):
        global SCORE
        self.rect.move_ip(0, SPEED)

        if self.rect.bottom > 600:
            SCORE += 1

    def move2(self):
        global SCORE
        self.rect.move_ip(0, -SPEED)

        if self.rect.top < (-100):
            SCORE += 1

    def move3(self):
        global SCORE
        self.rect.move_ip(SPEED, 0)

        if self.rect.right > 700:
            SCORE += 1

    def move4(self):
        global SCORE
        self.rect.move_ip(SPEED, 0)

        if self.rect.right < (-100):
            SCORE += 1
            
    def move(self):

        # 0: top to bottom (move 1)
        # 1: bottom to top (move 2)
        # 2: left to right (move 3)
        # 3: right to left (move 4)

        def generateRandInt():
            global RANDINT
            RANDINT = random.randint(0,2)
            if RANDINT == 0:
                self.rect.center = (random.randint(40, DISPLAY_WIDTH-40), 0)
                self.rect.top = 0
            elif RANDINT == 1:
                self.rect.center = (random.randint(40, DISPLAY_WIDTH-40), DISPLAY_HEIGHT)
                self.rect.bottom = DISPLAY_HEIGHT
            elif RANDINT == 2:
                self.rect.center = (0, random.randint(30, DISPLAY_HEIGHT-30))
                self.rect.left = 0
            elif RANDINT == 3:
                self.rect.center = (DISPLAY_WIDTH, random.randint(30, DISPLAY_HEIGHT-30))
                self.rect.left = DISPLAY_WIDTH

        def checking():
            global TEMP
            if TEMP != SCORE:
                generateRandInt()
                TEMP +=1    

        if RANDINT == 0:
            self.move1()
            checking()

        elif RANDINT == 1:
            self.move2()
            checking()

        elif RANDINT == 2:
            self.move3()
            checking()

        elif rRANDINT == 3:
            self.move4()
            checking()    
           
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        image = pygame.image.load("media/jack.png")
        self.image = pygame.transform.scale(image, (70, 70))
        self.surf = pygame.Surface((70, 70))
        self.rect = self.surf.get_rect(center = (150,455))
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -7)

        if self.rect.bottom < DISPLAY_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 7)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-7, 0)

        if self.rect.right < (DISPLAY_WIDTH):        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(7, 0)


def gameover_screen():
    bg_sound2.play()

    while True:
         for event in pygame.event.get():
        
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
	
         DISPLAYSURF.fill(BLACK)
         DISPLAYSURF.blit(game_over, (190, 180))
         DISPLAYSURF.blit(message, (160, 230))

         pygame.display.update()

         for entity in all_sprites:
            entity.kill()

         time.sleep(2)

         pygame.display.update()
         FramePerSec.tick(FPS)


# setting up sprites         
P1 = Player()
E1 = Enemy()

# creating sprites group
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# adding a new user event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# define sound effect and music
bg_sound = pygame.mixer.Sound('media/background.wav')
bg_sound2 = pygame.mixer.Sound('media/background2.wav')
cry = pygame.mixer.Sound('media/cry.wav')

bg_sound.play()

# game loop 
while True:     
	# cycles through all events occuring
    for event in pygame.event.get():   
    	if ((event.type == INC_SPEED) and (SPEED < 10)):
    		SPEED += 0.05      
    	if event.type == QUIT:
            pygame.quit()
            sys.exit() 

    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, WHITE)    
    DISPLAYSURF.blit(scores, (10,10))

    name1 = font.render("THE", True, BLACK)
    name2 = font.render("INCREDIBLES", True, RED)
    DISPLAYSURF.blit(name1, (270,180))
    DISPLAYSURF.blit(name2, (180,230))

    # move and re-draws all sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

	# to be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):

        message = font.render("Your Score: " + str(SCORE) , True, RED)

        cry.play()
        time.sleep(1)
        bg_sound.stop()
        gameover_screen()
    	
    pygame.display.update()
    FramePerSec.tick(FPS)
    




