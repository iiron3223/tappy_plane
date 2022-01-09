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


# Game settings
TITLE = "Tappy Plane"
WIDTH = 1024  # 16 x 64 or 32 x 32 or 64 x 16 
HEIGHT = 480  # 32 x 16 or 32 x 16 or 64 x 8
FPS = 60
BGCOLOR = DARKGREY
SPRITESHEET_PNG = 'sheet.png'
SPRITESHEET_XML = 'sheet.xml'
BACKGROUND_IMG = 'background.png'

# Game properties
TILESIZE = 64
GRID_WIDTH = WIDTH / TILESIZE
GRID_HEIGHT = HEIGHT / TILESIZE
SPAWN_DIST = WIDTH + 200


# Player settings
PLAYER_IMAGES = ['planeRed1.png', 'planeRed2.png', 'planeRed3.png']
FLAP_POWER = -300
FLAP_INTERVAL = 500
GRAVITY = 600
HORIZONTAL_SPEED = 2


# Obstacles settings
GROUND_IMG = 'groundGrass.png'

