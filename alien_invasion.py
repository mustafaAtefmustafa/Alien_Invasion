"""This entire project was built following Eric Matthes PCC Book."""

import sys
import pygame as p
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game and create game resources"""
        p.init()
        self.settings = Settings()
        self.screen = p.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        p.display.set_caption("Alien Invasion")
        self.ship = Ship(self)
        self.bullets = p.sprite.Group()
        self.aliens = p.sprite.Group()

        self._create_fleet()


    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens 
        # Spacing between each alien is one alien width
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Create the first row of aliens
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row
            alien = Alien(self)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien)


    def run_game(self):
        """"Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()


    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in p.event.get():
            if event.type == p.QUIT:
                sys.exit()
            elif event.type == p.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == p.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Responds to keypresses."""
        if event.key == p.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key ==p.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key ==p.K_UP:
            # Move the ship up
            self.ship.moving_up = True
        elif event.key ==p.K_DOWN:
            # Move the ship down
            self.ship.moving_down = True
        elif event.key == p.K_q:
            sys.exit()
        elif event.key == p.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """Responds to key releases."""
        if event.key == p.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == p.K_LEFT:
            self.ship.moving_left = False
        elif event.key == p.K_UP:
            self.ship.moving_up = False
        elif event.key == p.K_DOWN:
            self.ship.moving_down = False


    def _fire_bullet(self):
        """Creat new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        p.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
