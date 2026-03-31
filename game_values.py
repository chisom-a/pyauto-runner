from enum import Enum, auto

class State(Enum):
    MAIN_MENU = auto()
    GAME_OVER = auto()
    EDITOR = auto()
    GAMEPLAY = auto()
    WON_LEVEL = auto()

#Game variables
GAME_WIDTH = 832
GAME_HEIGHT = 512
OUTER_MARGIN_WIDTH = 0
OUTER_MARGIN_HEIGHT = 128

#Game colors
BKG_COLOR = (144, 213, 255) #Light Blue (#90D5FF)
MOUSE_TILE_COLOR = (0, 128, 0) #Standard Green (#008000)
USER_TILE_COLOR_RGBA = (0, 79, 0, 80)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#Game tile info
TILE_SIZE = 64 #Tiles will be used in a 832x512 area (tiles will form 13x8 grid)
TILES_PER_ROW = GAME_WIDTH // TILE_SIZE
TILES_PER_COL = GAME_HEIGHT // TILE_SIZE

PLAYER_DEFAULT_X_POS = 100
PLAYER_DEFAULT_Y_POS = GAME_HEIGHT - (2 * TILE_SIZE)

SCREEN_WIDTH = GAME_WIDTH + OUTER_MARGIN_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT + OUTER_MARGIN_HEIGHT
FPS = 60 #Max number of fps game should run
GAME_TITLE = "PyAuto Runner"
MAX_LEVELS = 2

#Game tile info
TILES_PER_ROW = GAME_WIDTH // TILE_SIZE
TILES_PER_COL = GAME_HEIGHT // TILE_SIZE
