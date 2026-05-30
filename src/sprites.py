"""Define all Pygame objects."""
from __future__ import annotations
import pygame as pg
import random

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameState


class Group(pg.sprite.Group):
    """Custom Pygame Group."""
    def __init__(self, game: GameState) -> None:
        """Initialize a custom group."""
        super().__init__()
        self.game = game

    def key_press(self, event: pg.event) -> None:
        """Call key press method for all sprites in group."""
        for sprite in self.sprites():
            sprite.key_press(event)

    def key_hold(self, keys: pg.key.ScancodeWrapper) -> None:
        """Call key hold method for all sprites in group."""
        for sprite in self.sprites():
            sprite.key_hold(keys)


class Sprite(pg.sprite.Sprite):
    """Custom Pygame Sprite."""
    def __init__(self) -> None:
        """Initialize a custom sprite."""
        super().__init__()
    
    def key_press(self, event: pg.event.Event) -> None:
        """Key pressing and sensing method."""

    def key_hold(self, keys: pg.key.ScancodeWrapper) -> None:
        """Key pressing and sensing method."""

    def set_velocity(self, x_velocity: int | float, y_velocity: int | float) -> None:
        """Set the x and y velocities of the character."""
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def update(self) -> None:
        """Make rect attribute coordinates match x and y coordinate attributes."""
        if self.game.centering:
            self.rect.center = (self.x, self.y)
        else:
            self.rect.x = self.x
            self.rect.y = self.y


class Paddle(Sprite):
    """Rectangle sprite."""
    def __init__(self,
                 game: GameState,
                 player: int,
                 x: int | float,
                 y: int | float,
                 width: int | float,
                 height: int | float,
                 color: str) -> None:
        """DEFINE the Rectangle sprite."""
        super().__init__()
        self.game = game
        self.player = player

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dimensions = (self.width, self.height)
        self.color = color

        self.image = pg.Surface(self.dimensions, pg.SRCALPHA)
        self.image.fill(self.color)
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.set_velocity(x_velocity=5,
                          y_velocity=5)

    def key_hold(self, keys: pg.key.ScancodeWrapper) -> None:
        """Move sprite with key presses."""
        if self.player == 1:
            if keys[pg.K_w]:
                self.y -= self.y_velocity
            if keys[pg.K_s]:
                self.y += self.y_velocity

        if self.player == 2:
            if keys[pg.K_UP]:
                self.y -= self.y_velocity
            if keys[pg.K_DOWN]:
                self.y += self.y_velocity


class Ball(Sprite):
    """Rectangle sprite."""
    def __init__(self,
                 game: GameState,
                 x: int | float,
                 y: int | float,
                 radius: int | float,
                 color: str) -> None:
        """DEFINE the Circle sprite."""
        super().__init__()
        self.game = game

        self.x = x
        self.y = y
        self.radius = radius
        self.diameter = self.radius * 2
        self.dimensions = (self.diameter, self.diameter)
        self.color = color

        self.image = pg.Surface(self.dimensions, pg.SRCALPHA)
        pg.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.randomize_velocity()
        
        self.cooldown = self.game.fps * 2
        self.starting_cooldown = self.cooldown

    def randomize_velocity(self) -> None:
        velocity_choices = [-5, -4, -3, 3, 4, 5]
        self.set_velocity(x_velocity=random.choice(velocity_choices),
                          y_velocity=random.choice(velocity_choices))

    def return_to_center(self) -> None:
        self.x = self.game.window.width / 2
        self.y = self.game.window.height / 2

        self.randomize_velocity()
        self.cooldown = self.starting_cooldown
        
    def update(self) -> None:
        """Make ball move on its own."""
        super().update()

        # Update cooldown.
        if self.cooldown > 0:
            self.cooldown -= 1
            return None

        # Continuous movement.
        self.x += self.x_velocity
        self.y += self.y_velocity

        # Top and bottom wall bouncing.
        if self.y + self.radius > self.game.window.height or self.y - self.radius < 0:
            self.y_velocity *= -1

        if self.x - self.radius > self.game.window.width or self.x + self.radius < 0:
            self.return_to_center()
