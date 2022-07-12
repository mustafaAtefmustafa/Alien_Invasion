import pygame as p


class Ship():
    """A class to manage the ship"""

    def __init__(self, ai_game):
        """Initialize ship and set its starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        # Movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Load the ship image and get its rect.
        self.image = p.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom


    def update(self):
        """Update the ship's position based on movement flag."""
        if self.moving_right == True:
            self.rect.x += 1
        if self.moving_left == True:
            self.rect.x -= 1
        if self.moving_up == True:
            self.rect.y -= 1
        if self.moving_down == True:
            self.rect.y += 1

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)


