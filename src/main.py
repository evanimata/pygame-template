"""Main file to run a Pygame."""
from __future__ import annotations
import pygame as pg

from sprites import Ball, Group, Paddle


class GameState:
    """GameState class to manage the entire game."""
    running = True
    centering = True

    def __init__(self) -> None:
        """Initiate Pygame constants and variables."""
        # Press the on-button for Pygame.
        pg.init()

        # BUILD the game window.
        self.window = Window(game=self,
                             width=800,
                             height=600,
                             background_color="black",
                             title="My Pygame",
                            )

        # DEFINE time-keeping variables.
        self.clock = pg.time.Clock()
        self.fps = 60

        # Initialize the main sprite group.
        self.sprites = Group(self)
        self.create_sprites()

    def create_sprites(self) -> None:
        """Build sprites and sprite groups."""
        player1 = Paddle(game=self,
                         player=1,
                         x=self.window.width / 6,
                         y=self.window.height / 2,
                         width=self.window.width / 32,
                         height=self.window.height / 3.5,
                         color="white")

        player2 = Paddle(game=self,
                         player=2,
                         x=self.window.width * (5 / 6),
                         y=self.window.height / 2,
                         width=self.window.width / 32,
                         height=self.window.height / 3.5,
                         color="white")

        ball = Ball(game=self,
                      x=self.window.width / 2,
                      y=self.window.height / 2,
                      radius=self.window.width / 48,
                      color="white")
        
        self.sprites.add(player1, player2, ball)

    def check_game_events(self) -> None:
        """DEFINE a for loop to check all Pygame events."""
        # Loop through all game events (e.g.: mouse clicks, key buttons, etc.).
        keys = pg.key.get_pressed()
        self.sprites.key_hold(keys)
        for event in pg.event.get():
            # Screen is resized by user.
            if event.type == pg.VIDEORESIZE:
                print("RESIZE.")

            # Top-left corner x-button.
            if event.type == pg.QUIT:
                self.quit()

            # Key pressing / key pressed down sensing.
            if event.type == pg.KEYDOWN:
                self.sprites.key_press(event)
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def play(self) -> None:
        """Main Pygame while loop."""
        while self.running:
            # Set the game frames-per-second.
            self.clock.tick(self.fps)

            # Call the for loop method to check all game events.
            self.check_game_events()

            # Sprite group updates.
            self.sprites.update()

            # Window & screen updates.
            self.window.fill(self.window.background_color)
            self.sprites.draw(self.window.screen)
            pg.display.update()

    def quit(self) -> None:
        """Exit the Pygame program."""
        self.running = False
        print("\n" + "-"*30 + "\nGAME EXITING, HAVE A GOOD DAY.")


class Window:
    """DEFINE the Pygame window & screen."""
    def __init__(self, game: GameState,
                 width: int | float,
                 height: int | float,
                 background_color: str | tuple | list="black",
                 title: str="Pygame") -> None:
        """Create a screen object."""
        self.game = game

        # Window attributes.
        self.width = width
        self.height = height
        self.background_color = background_color

        # BUILD the Pygame screen. DO NOT EDIT.
        self.dimensions = (self.width, self.height)
        self.screen = pg.display.set_mode(self.dimensions, pg.RESIZABLE)
        pg.display.set_caption(title)
        self.fill(self.background_color)

    def fill(self, color: str | tuple | list) -> None:
        """Update the display, fill the screen with a color."""
        self.screen.fill(color)


# RUN THE GAME.
if __name__ == "__main__":
    game = GameState()
    try:
        game.play()
    except KeyboardInterrupt:
        pass
