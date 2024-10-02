import pygame
import os
pygame.font.init()

WIDTH,HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AISES Game")

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0,0,0)
RED_COLOR = (255,0,0)
YELLOW_COLOR = (255,255,0)
FPS = 60
VEL = 2
BULLET_VEL = 7 # I Want this to be faster than the characters and harder
IMAGE_WIDTH_UHK, IMAGE_HEIGHT_UHK = 55, 40
IMAGE_WIDTH_TLAN, IMAGE_HEIGHT_TLAN = 90, 80
MAX_BULLETS = 3

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

WOODS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'smokymountains.jpg')), (WIDTH, HEIGHT))

UHKTENA_HIT = pygame.USEREVENT + 1
TLANUWHA_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect((WIDTH//2 -5), 0, 10, HEIGHT) # position x, position y, width, height

UHKTENA_IMAGE = pygame.image.load(os.path.join('Assets', 'uhktena.png'))
UHKTENA_IMAGE_RESIZED = pygame.transform.scale(UHKTENA_IMAGE, (IMAGE_WIDTH_UHK, IMAGE_HEIGHT_UHK))
TLANUWHA_IMAGE = pygame.image.load(os.path.join('Assets', 'tlanuwha.png'))
TLANUWHA_IMAGE_RESIZED = pygame.transform.scale(TLANUWHA_IMAGE, (IMAGE_WIDTH_TLAN, IMAGE_HEIGHT_TLAN))

def draw_window(uhktena, tlanuwha, uhktena_bullets, tlanuwha_bullets, uhktena_health, tlanuwha_health):
    WIN.blit(WOODS, (0,0))
    pygame.draw.rect(WIN, BLACK_COLOR, BORDER) #surface, colorvalue, object
    
    uhktena_health_text = HEALTH_FONT.render("Health: " + str(uhktena_health), 1, WHITE_COLOR)
    tlanuwha_health_text = HEALTH_FONT.render("Health: " + str(tlanuwha_health), 1, WHITE_COLOR)
    WIN.blit(tlanuwha_health_text, ((WIDTH-tlanuwha_health_text.get_width()-10), 10)) #padding 10 from right and top
    WIN.blit(uhktena_health_text, (10, 10)) #padding 10 from right and top
    
    WIN.blit(UHKTENA_IMAGE_RESIZED, (uhktena.x, uhktena.y))
    WIN.blit(TLANUWHA_IMAGE_RESIZED,(tlanuwha.x,tlanuwha.y))
    
    for bullet in uhktena_bullets:
        pygame.draw.rect(WIN, YELLOW_COLOR, bullet)
        
    for bullet in tlanuwha_bullets:
        pygame.draw.rect(WIN, RED_COLOR, bullet)
    #use blit when u want to bring surfaces onto the screen (ie text or images)
    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE_COLOR)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    
def uhktena_handle_movement(keys_pressed, uhktena):
        # Uhktena movements
        if keys_pressed[pygame.K_a] and uhktena.x - VEL > 0: #LEFT
            uhktena.x -= VEL
        if keys_pressed[pygame.K_d] and uhktena.x + VEL + uhktena.width < BORDER.x: #RIGHT
            uhktena.x += VEL
        if keys_pressed[pygame.K_w]and uhktena.y - VEL > 0: #UP
            uhktena.y -= VEL
        if keys_pressed[pygame.K_s] and uhktena.y + VEL + uhktena.height < HEIGHT: #DOWN
            uhktena.y += VEL   
            
def tlanuwha_handle_movement(keys_pressed, tlanuwha):
        # Uhktena movements
        if keys_pressed[pygame.K_LEFT] and tlanuwha.x - VEL > BORDER.x + BORDER.width: #LEFT
            tlanuwha.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and tlanuwha.x + VEL + tlanuwha.width < WIDTH: #RIGHT
            tlanuwha.x += VEL
        if keys_pressed[pygame.K_UP] and tlanuwha.y - VEL > 0: #UP
            tlanuwha.y -= VEL
        if keys_pressed[pygame.K_DOWN] and tlanuwha.y + VEL + tlanuwha.width < HEIGHT: #DOWN
            tlanuwha.y += VEL   

def handle_bullets(uhktena_bullets, tlanuwha_bullets, uhktena, tlanuwha):
    #loop thru the uhktena's bullets and see if they are off the screen or collide with tlanuwha
    for bullet in uhktena_bullets:
        #since bullet comes from left it needs to move right
        bullet.x += BULLET_VEL
        if tlanuwha.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TLANUWHA_HIT))
            uhktena_bullets.remove(bullet)
        elif (bullet.x > WIDTH):
            uhktena_bullets.remove(bullet)
    
    for bullet in tlanuwha_bullets:
        #since bullet comes from right player it needs to move left
        bullet.x -= BULLET_VEL
        if uhktena.colliderect(bullet):
            pygame.event.post(pygame.event.Event(UHKTENA_HIT))
            tlanuwha_bullets.remove(bullet)
        elif (bullet.x < 0):
            tlanuwha_bullets.remove(bullet)

def main():
    # create rectangle to represent where my uhktena moves
    uhktena = pygame.Rect(100, 300, IMAGE_WIDTH_UHK, IMAGE_HEIGHT_UHK)
    tlanuwha = pygame.Rect(700,300, IMAGE_WIDTH_TLAN, IMAGE_HEIGHT_TLAN)
    
    #list all the bullets for the uhktena
    uhktena_bullets = []
    #list all the bullets for hte tlanuwha
    tlanuwha_bullets = []
    
    uhktena_health = 10
    tlanuwha_health = 10
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(uhktena_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(uhktena.x + uhktena.width, uhktena.y + uhktena.height//2 - 2 , 10, 5)
                    uhktena_bullets.append(bullet)
                if event.key == pygame.K_RSHIFT and len(tlanuwha_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(tlanuwha.x, tlanuwha.y + tlanuwha.height//2 - 2 , 10, 5)
                    tlanuwha_bullets.append(bullet)
                    
            if event.type == TLANUWHA_HIT:
                tlanuwha_health -= 1
                
            if event.type == UHKTENA_HIT:
                uhktena_health -= 1
        
        winner_text = ""
        if tlanuwha_health <= 0:
           winner_text = "UHKTENA WINS!" 
           
        if uhktena_health <= 0:
           winner_text = "TLANUWHA WINS!" 
        
        if winner_text != "":
            draw_winner(winner_text)
            break
           
        handle_bullets(uhktena_bullets, tlanuwha_bullets, uhktena, tlanuwha)
        
        # every time we run this loop  and we reach this line (ie 60 times per second) we will get what keys are pressed 
        keys_pressed = pygame.key.get_pressed()
        
        uhktena_handle_movement(keys_pressed, uhktena)
        tlanuwha_handle_movement(keys_pressed, tlanuwha)
            
        draw_window(uhktena, tlanuwha, uhktena_bullets, tlanuwha_bullets, uhktena_health, tlanuwha_health)    
    pygame.quit()
    
if __name__ == "__main__":
    main()