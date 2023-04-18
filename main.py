import pygame
from pygame.sprite import Group
from ships import*
from blaster import *
from text_sounds import *

FPS = 60
MENU = True
GAME_PLAY = False
RUN = True
number_TIE_group = 4
min_shot_delay = 50
shot_delay = 500 

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Star Wars: Galactic Ace")
icon = pygame.image.load('img/icon-xwing.jpg')
pygame.display.set_icon(icon)

background_main = pygame.image.load('img/space-stars.jpg')
background_menu = pygame.image.load('img/x-wing-firepower.jpg')

red_blaster_group = Group()  
tie_figter = TIE_Fighter(screen, 'img/TIE-fighter.png')
TIE_group = Group()
green_blaster_group = Group()
next_shot_time = pygame.time.get_ticks() + random.randint(min_shot_delay,shot_delay)

def armu():
    """creates a group of enemies"""
    
    for enemy in range(number_TIE_group):
        tie_figter =  TIE_Fighter(screen, 'img/TIE-fighter.png')
        TIE_group.add(tie_figter)

sound_them.play(-1)

while RUN:

    if MENU:

        screen.blit(background_menu, (-50, -100))
        
        SCORE = 0
        with open('score.txt', 'r') as f:
            best_score = str(f.read())

        draw_text(screen, "W,A,S,D - move", text_font2, (0,0,0),580, 10)
        draw_text(screen, " SPASE - shoot", text_font2, (0,0,0),580, 50)
        draw_text(screen, f"Best Score:{best_score}", text_font3, (255,255,150),160, 450)
        play_game_text = text_font1.render("PLAY GAME", True, (255,255,0))
        play_game_text_rect = play_game_text.get_rect()
        play_game_text_rect.x = 120
        play_game_text_rect.y = 250
        screen.blit(play_game_text, play_game_text_rect)

        mouse_pos = pygame.mouse.get_pos()
        if play_game_text_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            xwing = X_wing(screen, 'img/X-wing.png') 
            GAME_PLAY = True
            MENU = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

    elif GAME_PLAY or xwing.damage_received:
        
        screen.blit(background_main, (0, -200))
        xwing.draw()
        for red_blaster in red_blaster_group.sprites(): 
            red_blaster.draw_blaster()

        if len(TIE_group.sprites()) < number_TIE_group: 
            armu()
        TIE_group.draw(screen)
        
        current_time = pygame.time.get_ticks()
        if current_time > next_shot_time:
            # find a random TIE Fighter from the TIE_group
            random_tie = random.choice(TIE_group.sprites())
            new_enemy_blaster = Enemy_blaster(screen, random_tie)
            green_blaster_group.add(new_enemy_blaster)
            if new_enemy_blaster.rect.top > -50:
                sound_gb.play()
            # updating the time for the next shot
            next_shot_time = current_time + random.randint(min_shot_delay, shot_delay)
        for green_blaster in green_blaster_group.sprites(): 
            green_blaster.draw_blaster()

        # main control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    xwing.mRight = True
                elif event.key == pygame.K_a:
                    xwing.mLeft = True
                elif event.key == pygame.K_w:
                    xwing.mUp = True
                elif event.key == pygame.K_s:
                    xwing.mDown = True
            
                elif event.key == pygame.K_SPACE:     
                    new_red_blaster = Friendly_blaster(screen, xwing)
                    red_blaster_group.add(new_red_blaster)
                    sound_rb.play()
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    xwing.mRight = False
                elif event.key == pygame.K_a:
                    xwing.mLeft = False
                elif event.key == pygame.K_w:
                    xwing.mUp = False
                elif event.key == pygame.K_s:
                    xwing.mDown = False 

        #all collisions in game
        collision1 = pygame.sprite.groupcollide(red_blaster_group, TIE_group, True, True)
        if collision1:
            SCORE += 1

        collisions2 = [blaster for blaster in green_blaster_group 
                    if xwing.rect.colliderect(blaster.rect)]
        if collisions2 and not xwing.damage_received:
            for blaster in collisions2:
                blaster.kill()
            xwing.life -= 1
            sound_explosion.play()
            xwing.damage_received = True

        collisions3 = [tie_figter for tie_figter in TIE_group 
                if xwing.rect.colliderect(tie_figter.rect)]
        if collisions3 and not xwing.damage_received:
            for tie_figter in collisions3:
                tie_figter.kill()
            xwing.life -= 1
            sound_explosion.play()
            xwing.damage_received = True

        draw_text(screen, f'score:{SCORE}', text_font2, (240,240,240), 20,10)
        draw_text(screen, f'life: {xwing.life}', text_font2, (240,240,240), 710,10)

        # updating objects
        xwing.update_position()
        red_blaster_group.update() 
        for red_blaster in red_blaster_group.sprites():
            if red_blaster.rect.bottom <= 0:
                red_blaster.kill()

        TIE_group.update()
        for tie_figter in TIE_group.sprites():
            if tie_figter.rect.top > 800:
                tie_figter.kill()

        green_blaster_group.update()
        for green_blaster in green_blaster_group.sprites():
            if green_blaster.rect.bottom <= -50 or green_blaster.rect.bottom > 800:
                green_blaster.kill()

        # losing condition
        if xwing.life <= 0:
            GAME_PLAY = False


    else:
        xwing.kill()

        draw_text(screen, "GAME OVER", text_font1, (240,240,100),100, 250)
        
        restart_text = text_font1.render("RESTART", True, (240,240,240))
        restart_text_rect = restart_text.get_rect()
        restart_text_rect.x = 170
        restart_text_rect.y = 450
        screen.blit(restart_text, restart_text_rect)

        # record save
        with open('score.txt', 'r') as f:
            number = int(f.read())
        if number < SCORE:
            with open('score.txt', 'w') as f:
                f.write(str(SCORE))

        mouse_pos = pygame.mouse.get_pos()
        if restart_text_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
           
           # updatind game
            for sprite in TIE_group.sprites():
                sprite.kill()
            for sprite in green_blaster_group.sprites():
                sprite.kill()
            for sprite in red_blaster_group.sprites():
                sprite.kill()

            MENU = True 
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
           
     

    pygame.display.flip()
    clock.tick(FPS) 

    
pygame.quit()



'''
print(len(red_blaster_group.sprites()))
print(len(green_blaster_group.sprites()))
print(len(TIE_group.sprites()))
'''

