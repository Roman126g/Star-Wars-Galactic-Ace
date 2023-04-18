import pygame

class Blaster(pygame.sprite.Sprite):
    """A class for displaying a blaster projectile"""

    def __init__(self, SCREEN, fighter):
        super(Blaster, self).__init__()
        self.SCREEN = SCREEN
        self.rect = pygame.Rect(0, 0, 4, 30)
        self.color = 0, 255 , 0
        self.speed = 9
        self.rect.centerx = fighter.rect.centerx
        self.rect.top = fighter.rect.top
        self.y = float(self.rect.y)

    def update(self):
        """Update the position of the blaster on the screen."""
        self.y -= self.speed
        self.rect.y = self.y
    
    def draw_blaster(self):
        """Draw the blaster on the screen."""
        
        pygame.draw.rect(self.SCREEN, self.color, self.rect)


class Friendly_blaster(Blaster):
    """A class for displaying an player blaster projectile"""
    def __init__(self, screen, fighter):
        super(Friendly_blaster, self).__init__(screen, fighter)
        self.color = 255, 0, 0


class Enemy_blaster(Blaster):
    """A class for displaying an ememy blaster projectile"""

    def __init__(self, screen, fighter):
        super(Enemy_blaster, self).__init__(screen, fighter)
        self.rect.top = fighter.rect.centery
        self.y = float(self.rect.y)
        
    def update(self):
        """Update the position of the enemy blaster on the screen."""

        self.y += self.speed
        self.rect.y = self.y