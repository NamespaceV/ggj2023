import pgzero, pgzrun, pygame
import sys

from scripts.levelScene import LevelScene

if sys.version_info < (3,5):
    print("This game requires at least version 3.5 of Python. Please download it from www.python.org")
    sys.exit()

pgzero_version = [int(s) if s.isnumeric() else s for s in pgzero.__version__.split('.')]
if pgzero_version < [1,2]:
    print("This game requires at least version 1.2 of Pygame Zero. You have version {0}. Please upgrade using the command 'pip3 install --upgrade pgzero'".format(pgzero.__version__))
    sys.exit()

# Set up constants
WIDTH = 640
HEIGHT = 480
TITLE = "Root"

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

updateable = LevelScene(music)

def update():
    global updateable
    updateable.update()
    if keyboard.o:
        updateable = LevelScene(music)
    if keyboard.p:
        updateable = LevelScene(music, "2")

def draw():
    screen.fill("white")
    updateable.draw(screen)

pgzrun.go()

