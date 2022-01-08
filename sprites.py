from __future__ import annotations
import pygame as pg
from main import Game
from settings import *




class Player(pg.sprite.Sprite):
    def __init__(self, game: Game, pos: tuple(int, int)):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottomright = pos
        
    def update(self):
        pass