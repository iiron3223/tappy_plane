from __future__ import annotations
import pygame as pg
import xml.etree.ElementTree as ET
import random
from main import Game
from settings import *

vector = pg.math.Vector2

class Spritesheet:
    """Utility class for loading and parsing spritesheets"""
    
    def __init__(self, img_dir, spritesheet, xml):
        self.spritesheet = pg.image.load(spritesheet).convert()
        with open(img_dir / SPRITESHEET_XML) as f:
            self.root = ET.parse(f).getroot()
    
    def get_image(self, x, y, width, height):
        """Grab an image out of a larger spritesheet"""
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image.convert_alpha()
    
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
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.image = self.game.player_anim[self.current_frame]
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.center = self.pos
        self.vel = vector(0, 0)
        self.acc = vector(0, GRAVITY)
        self.rot = 0
        self.last_flap = 0
        
        
        
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            self.flap()
    
    def animate(self):
        now = pg.time.get_ticks()
        if  now - self.last_update >= PLAYER_ANIM_RATE:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(PLAYER_IMAGES)
            center = self.rect.center
            self.image = self.game.player_anim[self.current_frame]
            vel = vector(self.vel.x * 100, self.vel.y * 0.005)
            self.rot = vel.angle_to(vector(1, 0))
            self.image = pg.transform.rotate(self.image, self.rot)
            self.rect.center = center
        
    def update(self):
        self.get_keys()
        self.animate()
        self.vel.y += self.acc.y * self.game.dt
        self.vel.x = HORIZONTAL_SPEED * self.game.dt
        if self.pos.y < 0:
            self.vel.y += 3* self.acc.y * self.game.dt
        self.rect = self.image.get_rect()
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.rect.center = self.pos

    def flap(self):
        """Apply upward force to player."""
        #if (now := pg.time.get_ticks()) - self.last_flap > FLAP_INTERVAL:
        #    self.last_flap = now
        if self.pos.y > 0:
            self.vel.y += FLAP_POWER
    

class Ground(pg.sprite.Sprite):
    next = (0, HEIGHT)
    spawn = False
    
    def __init__(self, game: Game):
        self._layer = GROUND_LAYER
        self.groups = game.all_sprites, game.obstacles, game.grounds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = self.next
        self.image = self.game.spritesheet.load_image(GROUND_IMG)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos
        Ground.next = self.rect.bottomright
    
    @classmethod
    def reset(cls):
        cls.next = (0, HEIGHT)
        spawn = False


class Rock(pg.sprite.Sprite):
    def __init__(self, game: Game, pos: tuple(int, int), up: bool = True):
        self._layer = ROCK_LAYER
        self.groups = game.all_sprites, game.obstacles, game.rocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.up = up
        self.x, self.y = pos
        if self.up:
            self.image = self.game.spritesheet.load_image(ROCK)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = self.x, self.y + random.randint(int(TILESIZE/3*2), ROCK_VAR)
        else:
            self.image = self.game.spritesheet.load_image(ROCK_DOWN)
            self.rect = self.image.get_rect()
            self.rect.topleft = self.x, self.y - random.randint(int(TILESIZE/3*2), ROCK_VAR)