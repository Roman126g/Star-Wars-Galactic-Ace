import pygame
import random

class Ship (pygame.sprite.Sprite):
    """Class representing a ship in the game."""

    def __init__(self,screen,image):
        super(Ship, self).__init__()
        self.screen = screen  ###
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, 
                                            (self.image.get_width() - 20, 
                                            self.image.get_height() - 20))
        self.rect = self.image.get_rect()
        
        self.screen_rect = screen.get_rect()  # рект екрану 
        self.rect.centerx = self.screen_rect.centerx 
        self.rect.centery = self.screen_rect.centery


    def draw(self):
        """ Draws the ship on the screen """

        self.screen.blit(self.image,self.rect)
    



class X_wing(Ship):
    """ Class representing the player's ship in the game """

    def __init__(self, screen, image):
        super(X_wing, self).__init__(screen, image)
        self.rect.centery = self.screen_rect.bottom - 100
        self.mRight = False
        self.mLeft = False
        self.mUp = False
        self.mDown = False
        
        self.life = 3
        self.damage_received = False
        self.alpha = 255

    def update_position(self):
        """ Updates the player's position based on the user input """

        if self.mRight and self.rect.right < self.screen_rect.right:
            self.rect.centerx += 7
        if self.mLeft and self.rect.left > 0:
            self.rect.centerx -= 7
        if self.mUp and self.rect.top > 0:
            self.rect.centery -= 5
        if self.mDown and self.rect.bottom < self.screen_rect.bottom:
            self.rect.centery += 5

        if self.damage_received:
            self.alpha -= 2
            if self.alpha < 0:
                self.alpha = 0
                self.damage_received = False
                
                self.alpha = 255
        self.image.set_alpha(self.alpha)
        
 
class TIE_Fighter(Ship):
    """ A class to represent a TIE Fighter enemy ship in the game."""

    def __init__(self, screen, image):
        super(TIE_Fighter, self).__init__(screen, image)
        self.rect.inflate_ip(0, -15)
        self.rect.centery = self.screen_rect.top - random.randrange(50, 300, 50)
        self.rect.centerx = random.randrange(0, 800, 100)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.speed_x = random.choice([2.5, -2.5, 0])
        self.speed_y = 2

    def update(self):
        """ Updates the enemy position on screen"""

        if self.speed_x == 0:
             self.y += 2
        else:
            self.y += 0.5
        self.rect.y = self.y

        self.x += self.speed_x
        self.rect.x =  self.x
        if self.rect.centerx < self.screen_rect.left - 50:
            self.speed_x = self.speed_x * -1
        elif self.rect.centerx> self.screen_rect.right + 50:          
            self.speed_x = self.speed_x * -1
