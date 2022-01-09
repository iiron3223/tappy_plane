# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
STEEL_BLUE = (70, 130, 180)
DARK_BLUE = (74, 88, 112)


# Game settings
TITLE = "Tappy Plane"
WIDTH = 1024  # 16 x 64 or 32 x 32 or 64 x 16 
HEIGHT = 480  # 32 x 16 or 32 x 16 or 64 x 8
FPS = 60
BGCOLOR = DARKGREY
SPRITESHEET_PNG = 'sheet.png'
SPRITESHEET_XML = 'sheet.xml'
BACKGROUND_IMG = 'background.png'
FONT = 'kenvector_future.ttf'
FONT_THIN = 'kenvector_future_thin.ttf'


# Game properties
TILESIZE = 64
GRID_WIDTH = WIDTH / TILESIZE
GRID_HEIGHT = HEIGHT / TILESIZE
SPAWN_DIST = WIDTH + 200


# Player settings
PLAYER_IMAGES = ['planeRed1.png', 'planeRed2.png', 'planeRed3.png']
PROPELER_SOUND = 'airplane_prop.ogg'
CRASH_SND = 'crash.wav'
PLAYER_ANIM_RATE = 30
FLAP_POWER = -30
FLAP_INTERVAL = 500
GRAVITY = 600
HORIZONTAL_SPEED = 2
START_POSITION = (3 * TILESIZE, 2 * TILESIZE)


# Obstacles settings
GROUND_IMG = 'groundGrass.png'
ROCK = 'rockGrass.png'
ROCK_DOWN = 'rockDown.png'
ROCK_VAR = 100
ROCKS_NUMBER = 10


# Stars settings
STAR_IMG = 'starGold.png'
STAR_PICKUP_SND = 'pickupStar.wav'
STAR_BOB_RANGE = 25
STAR_BOB_SPEED = 0.5
STAR_POINTS = 10
STAR_NUMBER = 6
STAR_SPREAD = 64

# Sprite layers
ROCK_LAYER = 1
GROUND_LAYER = 2
STAR_LAYER = 3
PLAYER_LAYER = 4


