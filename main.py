# Tappy Plane Game

import pygame as pg  # type: ignore
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
        self.game_dir = Path(__file__).parent
        # Load graphics
        img_dir = self.game_dir / 'img'
        self.spritesheet = Spritesheet(img_dir / SPRITESHEET_PNG, 
                                       img_dir / SPRITESHEET_XML)
        self.player_anim = [pg.image.load(img_dir / img).convert_alpha() 
                       for img in PLAYER_IMAGES]
        self.background = self.spritesheet.load_image(BACKGROUND_IMG)
        self.background_rect = self.background.get_rect()
        self.crash_img = self.spritesheet.load_image(CRASH_IMG)
        self.crash_rect = self.crash_img.get_rect()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.font_big = pg.font.Font(img_dir / FONT, 100)
        self.font_med = pg.font.Font(img_dir / FONT, 42)
        self.font_thin = pg.font.Font(img_dir /FONT_THIN, 32)
        # Load sound
        self.snd_dir = self.game_dir / 'snd'
        self.propeler_snd = pg.mixer.Sound(self.snd_dir / PROPELER_SOUND)
        #self.propeler_snd.set_volume(0.7)
        self.star_pickup_snd = pg.mixer.Sound(self.snd_dir / STAR_PICKUP_SND)
        self.star_pickup_snd.set_volume(0.7)
        self.crash_snd = pg.mixer.Sound(self.snd_dir / CRASH_SND)
        #self.crash_snd.set_volume(0.7)
        self.wind_snd = pg.mixer.Sound(self.snd_dir / WIND_SND)
        # Load highscore
        with open(self.game_dir / SCORE, 'r') as f:
            self.highscore = f.read()
        
    def new(self):
        # Start a new game
        Ground.reset()
        pg.mixer.music.load(self.snd_dir / BACKGROUND_MUSIC, )
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops=-1)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.obstacles = pg.sprite.Group()
        self.grounds = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.player = Player(self, START_POSITION)
        self.score = 0
        Ground(self)
        Ground(self)
        Ground(self) 
        self.paused = False
    
    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
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
                self.screen.blit(self.crash_img, self.player.rect.center)
                pg.display.flip()
                self.player.kill()
                self.playing = False
                self.propeler_snd.fadeout(50)
                self.wind_snd.fadeout(100)
                pg.mixer.music.fadeout(500)
                self.crash_snd.play()
                self.show_go_screen()
                
        # Check for collisions with stars
        hits = pg.sprite.spritecollide(self.player, self.stars, True)
        for star in hits:
            self.score += STAR_POINTS
            self.star_pickup_snd.play()
        
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
        
        # Spawn stars
        if len(self.stars) < STAR_NUMBER:
            x = random.randint(WIDTH, 2*WIDTH)
            y = random.randint(0, HEIGHT)
            for i in range(3):
                Star(self, (x + i * STAR_SPREAD, y))
        
        if not self.wind_snd.get_num_channels():
            self.wind_snd.play()
        
        pg.sprite.groupcollide(self.stars, self.obstacles, True, False) 
           
    def events(self): 
        # Game loop - events
        for event in pg.event.get():
            # check for closing window 
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused
    def draw(self):
        # Show FPS
        # pg.display.set_caption(f"{int(self.clock.get_fps())} FPS")
        # Game loop - draw
        self.screen.fill(pg.Color("grey30")) 
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background, (self.background_rect.width, 0))
        self.all_sprites.draw(self.screen)
        #self.draw_grid()
        # Draw HUD
        self.draw_text(f"{self.score}", self.font_thin, STEEL_BLUE,
                       20, 20, align="nw")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.font_big, pg.Color("white"),
                           WIDTH / 2, HEIGHT /2, align="center")
        pg.display.flip()
        
    def draw_grid(self):
        """Draw grid using TILESIZE on the screen."""
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, pg.Color("gray60"), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, pg.Color("gray60"), (0, y), (WIDTH, y), 1)
            
    def show_start_screen(self):
        pg.mixer.music.load(self.snd_dir / MENU_MUSIC)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background, (self.background_rect.width, 0))
        self.draw_text(TITLE, self.font_big, DARK_BLUE, 
                       WIDTH / 2, HEIGHT / 2, align="s")
        self.draw_text("Press any key to start", self.font_thin, STEEL_BLUE,
                        WIDTH / 2, HEIGHT * 3 / 4, align="s")
        self.draw_text("Tap space to fly", self.font_thin, STEEL_BLUE,
                        WIDTH / 2, HEIGHT * 5 / 6, align="s")
        pg.display.flip()
        self.wait_for_key()
    
    def show_go_screen(self):
        # Game over/continue
        pg.mixer.music.load(self.snd_dir / MENU_MUSIC)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.background, (self.background_rect.width, 0))
        self.draw_text("GAME OVER", self.font_big, DARK_BLUE, 
                       WIDTH / 2, HEIGHT / 2, align="s")
        if self.score <= int(self.highscore):
            self.draw_text(f"YOUR SCORE: {self.score}", self.font_med, DARK_BLUE, 
                        WIDTH / 2, HEIGHT * 3 / 5, align="s")
            self.draw_text(f"Highscore: {self.highscore}", self.font_thin, DARK_BLUE, 
                        WIDTH / 2, HEIGHT * 5 / 7, align="s")
        else:
            self.draw_text(f"NEW HIGHSCORE! {self.score}", self.font_med, DARK_BLUE, 
                        WIDTH / 2, HEIGHT * 3 / 5, align="s")
            self.draw_text(f" Previous Highscore: {self.highscore}", self.font_thin, DARK_BLUE, 
                        WIDTH / 2, HEIGHT * 5 / 7, align="s")
            self.highscore = str(self.score)
            with open(self.game_dir / SCORE, 'w') as f:
                f.write(self.highscore)
        self.draw_text("Press any key to restart", self.font_thin, STEEL_BLUE,
                       WIDTH / 2, HEIGHT * 7 / 8, align="s")
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
    
    def draw_text(self, 
                  text: str, 
                  font: pg.font.Font, 
                  color: tuple[int, int, int], 
                  x: int,
                  y: int, 
                  align: str="nw"):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        elif align == "ne":
            text_rect.topright = (x, y)
        elif align == "sw":
            text_rect.bottomleft = (x, y)
        elif align == "se":
            text_rect.bottomright = (x, y)
        elif align == "n":
            text_rect.midtop = (x, y)
        elif align == "s":
            text_rect.midbottom = (x, y)
        elif align == "e":
            text_rect.midright = (x, y)
        elif align == "w":
            text_rect.midleft = (x, y)
        elif align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        
        
if __name__ == '__main__':
    g = Game()
    g.show_start_screen()
    while g.running:
        g.new()
        g.run()
    
    pg.quit()