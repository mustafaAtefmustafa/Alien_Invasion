"""This entire project was built following Eric Matthes PCC Book."""

import sys
from time import sleep

import pygame as p
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button


class AlienInvasion:
    """Class to manage game assets and behaviour"""

    def __init__(self):
        """Initialize the game and create game resources"""
        p.init()
        self.settings = Settings()
        self.screen = p.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        p.display.set_caption("Alien Invasion")

        # Create an instance to store game stats.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = p.sprite.Group()
        self.aliens = p.sprite.Group()
        self._create_fleet()

        # Make the play button.
        self.play_button = Button(self,"Play")
        

    def run_game(self):
        """"Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
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
            elif event.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game stats.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            p.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Responds to keypresses."""
        if event.key == p.K_RIGHT:
            # Move the ship to the right
            self.ship.moving_right = True
        elif event.key == p.K_LEFT:
            # Move the ship to the left
            self.ship.moving_left = True
        elif event.key == p.K_UP:
            # Move the ship up
            self.ship.moving_up = True
        elif event.key == p.K_DOWN:
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


    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens
        # Spacing between each alien is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        # Create the full fleet
        for row_number in range(number_rows):
            # Create the first row of aliens
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien.rect.height + 2 * alien_height * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """Respond when any alien hits the screen edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_directions()
                break

    def _change_fleet_directions(self):
        """Drop the entire fleet and change direction."""
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        """Creat new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        self.bullets.update()

        # Check for collisions between bullets and aliens
        self._check_bullet_alien_collisions()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))



    def _update_aliens(self):
        """
        Check if the fleet is at edge,
            then Update the positions of all aliens in the fleet.
        """
        for alien in self.aliens.sprites():
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = alien.y
        self._check_fleet_edges()
        self.aliens.update()

        # Check for collisions between aliens and ship.
        if p.sprite.spritecollideany(self.ship, self.aliens):
           self._ship_hit()

        # Check for aliens reached the bottom of the screen.
        self._check_aliens_bottom()

    
    def _ship_hit(self):
        """Respond to alien-ship collisions."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1

            # Remove all aliens and bullets left.
            self.bullets.empty()
            self.aliens.empty()

            # Create new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            p.mouse.set_visible(True)



    def _check_aliens_bottom(self):
        """Checks if any alien reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Do the same as ship hit.
                self._ship_hit()
                break



    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collision"""
        # Then remove both of them.
        collisions = p.sprite.groupcollide(self.bullets, self.aliens,
        True, True)
        
        # When the entire fleet dies, remove bullets and create new fleet.
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the play button when the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        p.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
