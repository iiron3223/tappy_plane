from __future__ import annotations
import pygame as pg
import xml.etree.ElementTree as ET
from main import Game
from settings import *

vector = pg.math.Vector2

class Spritesheet:
    """Utility class for loading and parsing spritesheets"""
    
    def __init__(self, img_dir, spritesheet, xml):
        self.spritesheet = pg.image.load(spritesheet).convert_alpha()
        with open(img_dir / SPRITESHEET_XML) as f:
            self.root = ET.parse(f).getroot()
    
    def get_image(self, x, y, width, height):
        """Grab an image out of a larger spritesheet"""
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image
    
    def load_image(self, name):
        """Load an sprite image from a spritesheet."""
        for c in self.root:
            if c.attrib['name'] == name:
                return self.get_image(int(c.attrib['x']), 
                                      int(c.attrib['y']), 
                                      int(c.attrib['width']), 
                                      int(c.attrib['height']))
        

class Player(pg.sprite.Sprite):
    def __init__(self, game: Game, pos: tuple(int, int)):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.center = self.pos
        self.vel = vector(HORIZONTAL_SPEED, 0)
        self.acc = vector(0, GRAVITY)
        self.last_flap = 0
        
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.flap()
        
    def update(self):
        self.get_keys()
        self.vel.y += self.acc.y * self.game.dt
        self.vel.x = HORIZONTAL_SPEED * self.game.dt
        #self.vel.y += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.rect.center = self.pos

    def flap(self):
        """Apply upward force to player, simulating wings flapping."""
        if (now := pg.time.get_ticks()) - self.last_flap > FLAP_INTERVAL:
            self.last_flap = now
            self.vel.y = FLAP_POWER
    

class Ground(pg.sprite.Sprite):
    previous = (0, HEIGHT)
    
    def __init__(self, game: Game):
        self.groups = game.all_sprites, game.obstacles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = self.previous
        self.image = self.game.spritesheet.load_image(GROUND_IMG)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos
        Ground.previous = self.rect.bottomright