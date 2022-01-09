# Tappy Plane Game

import pygame as pg
import random

from pathlib import Path
from settings import *
from sprites import *


class Game:
    def __init__(self) -> None:
        # Initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.load_data()
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        
        
    def load_data(self):
        game_dir = Path(__file__).parent
        img_dir = game_dir / 'img'
        self.spritesheet = Spritesheet(img_dir, 
                                       img_dir / SPRITESHEET_PNG, 
                                       img_dir / SPRITESHEET_XML)
        self.player_anim = [pg.image.load(img_dir / img).convert_alpha() 
                       for img in PLAYER_IMAGES]
        self.background = self.spritesheet.load_image(BACKGROUND_IMG)
        self.background_rect = self.background.get_rect()
        

    def new(self):
        # Start a new game
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.grounds = pg.sprite.Group()
        self.player = Player(self, (3 * TILESIZE, 4 * TILESIZE))
        Ground(self)
        Ground(self)
        Ground(self)
    
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
         
        # Check for collision with obstacles
        hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
        for obstacle in hits:
            if pg.sprite.collide_mask(self.player, obstacle):
                self.quit()
        
        # Move screen
        for sprite in self.all_sprites:
            sprite.rect.x -= HORIZONTAL_SPEED
        
        # Spawn new.ground
        for ground in self.grounds:
            if WIDTH <= ground.rect.right <= SPAWN_DIST and Ground.spawn:
                Ground.next = ground.rect.bottomright
                Ground(self)
                Ground.spawn = False
        
        # Kill sprites that got of the screen
        for sprite in self.all_sprites:
            if sprite.rect.right < 0:
                Ground.spawn = True
                sprite.kill()
            
            
    def events(self): 
        # Game loop - events
        for event in pg.event.get():
            # check for closing window 
            if event.type == pg.QUIT:
                self.quit()
                
    def draw(self):
        # Show FPS
        pg.display.set_caption(f"{int(self.clock.get_fps())} FPS")
        # Game loop - draw
        self.screen.fill(BGCOLOR) 
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background, (self.background_rect.width, 0))
        self.all_sprites.draw(self.screen)
        #self.draw_grid()
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
    
    def quit(self):
        if self.playing:
            self.playing = False
        self.running = False
    
if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.run()
        g.show_go_screen()
    
    pg.quit()