# Flappy Game

import pygame as pg
import random
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self) -> None:
        # Initialize game window
        pg.init()
        pg.mixer.init()
        self.load_data()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        
        
    def load_data(self):
        game_dir = path.dirname(__file__)
        
    def new(self):
        # Start a new game
        self.all_sprites = pg.sprite.Group()
        self.player = Player(self, (3 * TILESIZE, 4 * TILESIZE))
        
    
    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def update(self):
        # Game loop - update
        self.all_sprites.update()

    def events(self):
        # Game loop - events
        for event in pg.event.get():
            # check for closing window 
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    
    def draw(self):
        # Game loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        # double bufffering = after drawing everything flip the display
        pg.display.flip()
        
        
    def draw_grid(self):
        """Draw grid using TILESIZE on the screen."""
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y), 1)
            
            
            
    def show_start_screen(self):
        # Game splash/start screen
        pass
    
    def show_go_screen(self):
        # Game over/continue
        pass
    
if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.run()
        g.show_go_screen()
    
    pg.quit()