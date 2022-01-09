from __future__ import annotations
import pygame as pg
from main import Game
from settings import *

vector = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game: Game, pos: tuple(int, int)):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.bottomright = self.pos
        self.vel = vector(HORIZONTAL_SPEED, 0)
        self.acc = vector(0, GRAVITY)
        self.last_flap = 0
        
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.flap()
        
    def update(self):
        self.get_keys()
        self.vel += self.acc
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.rect.bottomright = self.pos

    def flap(self):
        """Apply upward force to player, simulating wings flapping."""
        if (now := pg.time.get_ticks()) - self.last_flap > FLAP_INTERVAL:
            self.last_flap = now
            self.vel.y = FLAP_POWER
    

class Ground(pg.sprite.Sprite):
    def __init__(self, game: Game, pos: tuple(int, int)):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = pos
        self.image = pg.Surface((12 * TILESIZE, 1 * TILESIZE))
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos