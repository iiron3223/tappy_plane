# Tappy Plane Game

import pygame as pg
import random

from pathlib import Path

from pygame.font import Font
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
        self.font = img_dir / FONT
        self.font_thin = img_dir /FONT_THIN
        

    def new(self):
        # Start a new game
        Ground.reset()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.obstacles = pg.sprite.Group()
        self.grounds = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.player = Player(self, START_POSITION)
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
            if self.playing:
                self.draw()
    
    def update(self):
        # Game loop - update
        self.all_sprites.update()
         
        # Check for collision with obstacles
        hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
        for obstacle in hits:
            if pg.sprite.collide_mask(self.player, obstacle):
                self.playing = False
                self.show_go_screen()
        
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
        
        # Spawn rocks
        if len(self.rocks) < ROCKS_NUMBER:
            x = random.randrange(WIDTH, WIDTH * 2)
            y = random.choice((0, HEIGHT))
            up = bool(y)
            Rock(self, (x, y), up)
            
            
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
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background, (self.background_rect.width, 0))
        self.draw_text(TITLE, self.font, 105, DARK_BLUE, 
                       WIDTH / 2, HEIGHT / 2, align="s")
        self.draw_text("Press any key to start", self.font_thin, 32, STEEL_BLUE,
                        WIDTH / 2, HEIGHT * 3 / 4, align="s")
        self.draw_text("Tap space to fly", self.font_thin, 32, STEEL_BLUE,
                        WIDTH / 2, HEIGHT * 5 / 6, align="s")
        pg.display.flip()
        self.wait_for_key()
    
    def show_go_screen(self):
        # Game over/continue
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background, (self.background_rect.width, 0))
        self.draw_text("GAME OVER", self.font, 105, DARK_BLUE, 
                       WIDTH / 2, HEIGHT / 2, align="s")
        self.draw_text("Press any key to restart", self.font_thin, 32, STEEL_BLUE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="s")
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    
    def quit(self):
        if self.playing:
            self.playing = False
        self.running = False
    
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        
        
if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.show_start_screen()
        g.new()
        g.run()
    
    pg.quit()