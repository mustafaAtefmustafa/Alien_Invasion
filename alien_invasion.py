import sys
import pygame as p
from settings import Settings
from ship import Ship


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

    def run_game(self):
        """"Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            for event in p.event.get():
                if event.type == p.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            # Put the ship in the mid bottom of the screen.
            self.ship.blitme()

            # Make the most recently drawn screen visible
            p.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
