import pygame
import random
import os
from pygame.constants import QUIT,K_DOWN,K_UP,K_LEFT,K_RIGHT,K_SPACE, K_ESCAPE

pygame.init()
FPS= pygame.time.Clock()

HEIGHT=800
WIDTH=1200

POS_SP= 650
POS_SC=-100
POS_FINISH=1500
POS_ESC=1500
POS_TOTALY=1500
POS_TOTAL=1500
start= False
GOOSE=True

ENEMY_MOVE_X = -8 
ENEMY_MOVE_XX= -4

BONUS_MOVE_Y = 3
BONUS_MOVE_YY= 6

BOOM_X=-500
BOOM_Y=-500
XY_ENEMY=()

FONT= pygame.font.SysFont('Verdana',36)
FONT2= pygame.font.SysFont('Verdana',40)
FONT3= pygame.font.SysFont('Verdana',30) 
FONT4= pygame.font.SysFont('Verdana',100)
 
score= 0
text= ' SCORE: '
text_start=' START '
text_push='- push spase -' 
TEXT_FINISH ='Complete ZERO !'

text_esc='For restart game, push "ESC'
text_totaly='Total score:'
text_total=0
bonuses=[]
enemies=[]

 
image_index = 0 
main_display=pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'),(WIDTH,HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3
  
IMAGE_PATH= "Goose"
PLAYER_IMAGES= os.listdir(IMAGE_PATH)

player_size=(40, 20)
bonus_size=(40, 40)
enemy_size=(60, 15)
boom_size=(150,80)
logo_size=(450,250)
scoreLogo_size=(100,50)
backSc_sise=(122,40)
COLOR_BACKSC=(245,0, 55)
board_size=(160 ,80 )
  
COLOR_BONUS=(0, 0, 0)

boom=pygame.transform.scale(pygame.image.load('boom.png').convert_alpha(),(400,300)) 
boom_rect = boom.get_rect(center=(BOOM_X,BOOM_Y))  
   
player=pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(),(150,75))  
player_rect = player.get_rect(center=(150,400)) 

logo=pygame.transform.scale(pygame.image.load('start.png').convert_alpha(),(450,200))  
logo_rect = logo.get_rect(center=(580,540)) 

scoreLogo=pygame.transform.scale(pygame.image.load('score.png').convert_alpha(),(150,50))  
scoreLogo_rect = scoreLogo.get_rect(center=(510,40)) 
scoreLogo2=pygame.transform.scale(pygame.image.load('score.png').convert_alpha(),(150,50))  
scoreLogo2_rect = scoreLogo2.get_rect(center=(690,40)) 

backSc=pygame.Surface(backSc_sise)
backSc.fill(COLOR_BACKSC)
backSc_rect=backSc.get_rect(center=(690,40)) 

board=pygame.transform.scale(pygame.image.load('board.png').convert_alpha(),(1392,1660)) 
board_rect = board.get_rect(center=(600,390) )
 
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_rigth = [4, 0]
player_move_left = [-4, 0]
 
def create_bonus(): 
    bonus=pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(),(75,100)) 
    bonus_rect=pygame.Rect(random.randint(100, WIDTH - 100), 0, *bonus_size)
    bonus_move=[0, random.randint (BONUS_MOVE_Y,BONUS_MOVE_YY)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = pygame.USEREVENT +2
pygame.time.set_timer(CREATE_BONUS, 2000)

def create_enemy(): 
    enemy = pygame.transform.scale(pygame.image.load("enemy.png").convert_alpha(),(120,30)) 
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT -100), *enemy_size)
    enemy_move=[random.randint(ENEMY_MOVE_X,ENEMY_MOVE_XX), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CHANGE_IMAGE= pygame.USEREVENT +3
pygame.time.set_timer(CHANGE_IMAGE,200)
 
playing=True 
while playing:
    FPS.tick(120)
    for event in pygame.event.get(): 

        if event.type==pygame.QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type==CHANGE_IMAGE:
            if GOOSE:
                player=pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
                image_index+=1
                if image_index>=len(PLAYER_IMAGES):
                    image_index=0
 
    bg_X1-=bg_move
    bg_X2-=bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
    
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg,(bg_X1,0))
    main_display.blit(bg,(bg_X2,0))
 
    keys = pygame.key.get_pressed() 
    if keys[K_SPACE]:
        POS_SC=16
        POS_SP=1400
        POS_ST=1400
        start= True

    if keys[K_ESCAPE]:
        player=False
    if GOOSE and start:
        if keys[K_DOWN] and player_rect.bottom< HEIGHT: 
            player_rect=player_rect.move(player_move_down)

        if keys[K_UP] and player_rect.top > 0:
            player_rect=player_rect.move(player_move_up)

        if keys[K_RIGHT] and player_rect.right<WIDTH:
            player_rect = player_rect.move(player_move_rigth)

        if keys[K_LEFT]  and player_rect.left > 0:
            player_rect= player_rect.move(player_move_left)

    
    for enemy in enemies:
        enemy[1]= enemy[1].move(enemy[2])
        main_display.blit(enemy[0],enemy[1])

        if start:
            if player_rect.colliderect(enemy[1]):
                POS_FINISH=150 
                POS_ESC=175
                POS_TOTALY=150
                POS_TOTAL=750
                start=False
                POS_SC=-100
                XY_ENEMY=enemy[1]
                BOOM_X=int(XY_ENEMY[0])
                BOOM_Y=int(XY_ENEMY[1])
                GOOSE=False
                boom_rect = boom.get_rect(center=(BOOM_X,BOOM_Y))
    
    for bonus in bonuses:
        bonus[1]= bonus[1].move(bonus[2])
        main_display.blit(bonus[0],bonus[1])
        if start:
            if player_rect.colliderect(bonus[1]):
                score+=1 
                ENEMY_MOVE_X-=2
                ENEMY_MOVE_XX-=2 

                if score <= 5: 
                    TEXT_FINISH='You are a loser !' 
                elif score <=10: 
                    BONUS_MOVE_Y += 1
                    BONUS_MOVE_YY += 1
                    TEXT_FINISH='Good work !'
                elif score <=15: 
                    TEXT_FINISH='You are a proff !'
                else : 
                    TEXT_FINISH='You are a genius !'
                text_total=score
                bonuses.pop(bonuses.index(bonus)) 
     
    main_display.blit(FONT3.render(str(text_push),True, (220, 20, 60) ), (490, POS_SP))

    if not start and GOOSE:
        main_display.blit(logo, (logo_rect)) 
        
    if start: 
        main_display.blit(scoreLogo,(scoreLogo_rect))
        main_display.blit(scoreLogo2,(scoreLogo2_rect))
        main_display.blit(backSc,(backSc_rect))
 
    main_display.blit(FONT.render(str(score),True, COLOR_BONUS ), (680 , POS_SC))

    main_display.blit(FONT4.render(str(TEXT_FINISH),True, (220, 20, 60) ), (POS_FINISH, 350))
    main_display.blit(FONT.render(str(text_esc),True, (220, 20, 60) ), (POS_ESC, 475))

    main_display.blit(FONT4.render(str(text_totaly),True, (0, 0, 255) ), (POS_TOTALY, 225))
    main_display.blit(FONT4.render(str(text_total),True, (0, 0, 255) ), (POS_TOTAL, 225))
 
    main_display.blit(player, (player_rect))  
    main_display.blit(boom, (boom_rect))
   
    main_display.blit(board,(board_rect))
    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
 
    for bonus in bonuses:
        if bonus[1].bottom >= HEIGHT:
            bonuses.pop(bonuses.index(bonus))
