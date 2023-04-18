import pygame

pygame.init()

def draw_text(screen, text, font, text_color, x, y):
    """Draws text onto the screen using the
        provided font and color at the given location"""

    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

text_font1 = pygame.font.Font(None, 140)
text_font2 = pygame.font.Font(None, 40)
text_font3 = pygame.font.Font(None, 100)

# all sounds on game
sound_explosion = pygame.mixer.Sound('sounds/explosion.mp3')
sound_explosion.set_volume(0.5)

sound_rb = pygame.mixer.Sound('sounds/red-blaster.mp3')
sound_rb.set_volume(0.3)

sound_gb = pygame.mixer.Sound('sounds/green-blaster.mp3')
sound_gb.set_volume(0.2)

sound_them = pygame.mixer.Sound('sounds/The-Force-Them.mp3')
sound_them.set_volume(0.2)


