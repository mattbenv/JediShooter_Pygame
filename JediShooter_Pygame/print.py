import pygame
import os

pygame.font.init()
pygame.mixer.init()

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',75)

WIDTH, HEIGHT = 1100, 800
WIDTH_BULLET, HEIGHT_BULLET = 10, 5
WIDTH_ROCKET, HEIGHT_ROCKET = 20, 10
BORDER_WIDTH = 10
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STARWARSSSS")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 50, 40
FPS = 60
VEL = 10
BULLET_VEL = 10
ROCKET_VEL = 15
MAX_BULLETS = 5
MAX_ROCKETS = 1

YELLOW_HIT = pygame.USEREVENT + 1 # number represents unique event.
RED_HIT = pygame.USEREVENT + 2 # number represents unique event id

BORDER = pygame.Rect(WIDTH/2-BORDER_WIDTH/2,0,BORDER_WIDTH,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound("assets/Assets_Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("assets/Assets_Gun+Silencer.mp3")
WINNER = pygame.mixer.Sound("assets/Dababy-lets-go-adlibs-sound-effect.mp3")
INITIALIZER = pygame.mixer.Sound("assets/Are-You-Ready.mp3")


YELLOW_SPACESHIP_IMAGE = pygame.image.load("assets/spaceship_yellow.png")
RED_SPACESHIP_IMAGE = pygame.image.load("assets/spaceship_red.png")
SPACE_IMAGE = pygame.image.load("assets/space.png")
LUKE_IMAGE = pygame.image.load("assets/luke.png")
KYLO_IMAGE = pygame.image.load("assets/kylo.png")
SPACE_IMAGE2 = pygame.image.load("assets/darkspace.jpg")
ROCKET_IMAGE = pygame.image.load("assets/rocket.png")

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)
SPACE = pygame.transform.scale(SPACE_IMAGE,(WIDTH,HEIGHT))
LUKE = pygame.transform.scale(LUKE_IMAGE,(WIDTH//2,HEIGHT//2))
KYLO = pygame.transform.scale(KYLO_IMAGE,(WIDTH//2,HEIGHT//2))
SPACE2 = pygame.transform.scale(SPACE_IMAGE2,(WIDTH,HEIGHT))
RED_ROCKET = pygame.transform.scale(ROCKET_IMAGE,(WIDTH_ROCKET, HEIGHT_ROCKET))


def draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health, red_rockets,yellow_rockets):
    WIN.fill(WHITE)
    WIN.blit(SPACE,(0,0))
    WIN.blit(LUKE,(0,0))
    WIN.blit(KYLO,(WIDTH//2,0))

    red_health_text=HEALTH_FONT.render("Health: "+str(red_health),True, WHITE)
    yellow_health_text=HEALTH_FONT.render("Health: "+str(yellow_health),True, WHITE)
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))

    WIN.blit(SPACE2,(WIDTH, HEIGHT))
    pygame.draw.rect(WIN,BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for rocket in red_rockets:
        pygame.draw.rect(WIN, RED_ROCKET, rocket)
    for rocket in yellow_rockets:
        pygame.draw.rect(WIN,YELLOW, rocket)
    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
    #w,a,s,d: set for the yellow spaceship
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0: #left key
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width<BORDER.x: #right key
        yellow.x +=VEL
    if keys_pressed[pygame.K_w] and yellow.y-VEL>0:
        yellow.y -=VEL
    if keys_pressed[pygame.K_s] and yellow.y+VEL+yellow.height<HEIGHT-5:
        yellow.y +=VEL

def red_handle_movement(keys_pressed,red):
    #arrows: set for the red spaceship
    if keys_pressed[pygame.K_LEFT] and red.x-VEL>BORDER.x+BORDER.width:
        red.x -=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+VEL+red.width<WIDTH:
        red.x +=VEL
    if keys_pressed[pygame.K_UP] and red.y-VEL>0:
        red.y -=VEL
    if keys_pressed[pygame.K_DOWN] and red.y+VEL+red.height<HEIGHT-15:
        red.y +=VEL

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            #post an an event so that you can add score, remove health.
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            #post an an event so that you can add score, remove health.
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
def handle_rockets(yellow_rockets,red_rockets,yellow,red):
    for rocket in yellow_rockets:
        rocket.x += ROCKET_VEL
        if red.colliderect(rocket):
            #post an an event so that you can add score, remove health.
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_rockets.remove(rocket)
        elif rocket.x > WIDTH:
            yellow_rockets.remove(rocket)

    for rocket in red_rockets:
        rocket.x -= ROCKET_VEL
        if yellow.colliderect(rocket):
            #post an an event so that you can add score, remove health.
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_rockets.remove(rocket)
        elif rocket.x < 0:
            red_rockets.remove(rocket)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    #RECT(x,y,width,height)
    red=pygame.Rect(600,350,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,350,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_rockets = []
    yellow_rockets = []

    red_health = 20
    yellow_health = 20

    clock = pygame.time.Clock()

    run = True
    INITIALIZER.play()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
                pygame.quit()
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x+yellow.width, yellow.y+yellow.height//2-WIDTH_BULLET//2,WIDTH_BULLET,HEIGHT_BULLET )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_BACKSPACE and len(red_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(red.x,red.y+red.height//2-WIDTH_BULLET//2,WIDTH_BULLET,HEIGHT_BULLET)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_v and len(yellow_rockets)<MAX_ROCKETS:
                    rocket = pygame.Rect(yellow.x+yellow.width, yellow.y+yellow.height//2-WIDTH_ROCKET//2,WIDTH_ROCKET,HEIGHT_ROCKET )
                    yellow_rockets.append(rocket)
                if event.key == pygame.K_DELETE and len(red_rockets)<MAX_ROCKETS:
                    rocket = pygame.Rect(red.x,red.y+red.height//2-WIDTH_ROCKET//2,WIDTH_ROCKET,HEIGHT_ROCKET)
                    red_rockets.append(rocket)

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text=""
        if red_health <= 0:
            winner_text="Matt ALWAYS WINS"
            WINNER.play()
        if yellow_health <= 0:
            winner_text= "LEXI LOSES"
            WINNER.play()
        if winner_text !="":
            draw_winner(winner_text) #someone won
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        handle_rockets(yellow_rockets,red_rockets,yellow,red)

        draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health, red_rockets, yellow_rockets)
    main()

if __name__ =="__main__":
    main()