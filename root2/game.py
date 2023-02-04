import pgzero, pgzrun, pygame
import sys

from enum import Enum

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
TITLE = "Root 2"

class TileType(Enum):
    GROUND = 0
    ROCK   = 1
    ROOT_L = 2
    ROOT_R = 3
    ROOT_U = 4
    ROOT_D = 5
    ROOT_H = 6
    ROOT_V = 7
    ROOT_X = 8
    WATER  = 9
    POISON = 10
    ROCK_LU = 11
    ROCK_LD = 12
    ROCK_RU = 13
    ROCK_RD = 14

def getGraphic(t):
    if t == TileType.ROCK:       
        return "tile_rock"
    if t == TileType.ROOT_U:       
        return "tile_root_u"
    if t == TileType.ROOT_D:       
        return "tile_root_d"
    if t == TileType.ROOT_L:       
        return "tile_root_l"
    if t == TileType.ROOT_R:       
        return "tile_root_r"
    if t == TileType.ROOT_H:       
        return "tile_root_h"
    if t == TileType.ROOT_V:       
        return "tile_root_v"
    if t == TileType.ROOT_X:       
        return "tile_root_x"
    if t == TileType.WATER:       
        return "tile_water"
    if t == TileType.POISON:       
        return "tile_poison"
    if t == TileType.ROCK_LU:       
        return "tile_rock_lu"
    if t == TileType.ROCK_LD:       
        return "tile_rock_ld"
    if t == TileType.ROCK_RU:       
        return "tile_rock_ru"
    if t == TileType.ROCK_RD:       
        return "tile_rock_rd"
    return "tile_ground"

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

TILE_W = 50
TILE_H = 50

BOARD_W = int(WIDTH/TILE_W)
BOARD_H = int(HEIGHT/TILE_H)-3

state = "play"

def checkCircle(mouse, xy, r):
    x,y = xy
    mx, my = mouse
    return (mx-x)*(mx-x)+(my-y)*(my-y) < r * r

class Tool:
    def __init__(self, xy, r, tileType):
        self.xy = xy
        self.r = r
        self.tileType = tileType

    def draw(self, screen, selected):
        screen.draw.circle(self.xy, self.r, "red" if selected else "blue")
    
    def checkClick(self, mx, my):
        return checkCircle((mx, my), self.xy, self.r)
   
tools = [
    Tool((75, 362), 20, TileType.ROOT_U),
    Tool((34, 388), 20, TileType.ROOT_L),
    Tool((128,400), 20, TileType.ROOT_R),
    Tool((77, 418), 20, TileType.ROOT_D),
    Tool((260, 401), 20, TileType.ROCK),
    Tool((393, 354), 20, TileType.GROUND),
    Tool((363, 420), 20, TileType.WATER),
    Tool((445, 415), 20, TileType.POISON),
    Tool((226, 349), 20, TileType.ROCK_LU),
    Tool((225, 386), 20, TileType.ROCK_LD),
    Tool((300, 360), 20, TileType.ROCK_RU),
    Tool((298, 391), 20, TileType.ROCK_RD),
    Tool((560, 380), 40, "simulation"),
]

selectedToolId = 0

tiles = []

def saveLevel():
    level = ""
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            level += "+" + hex(getTile(x,y).value)
        level += '\n'
#     print(level)
    file = open("levels/test.txt", "w")
    file.write(level)
    file.close()

def loadLevel(no=None):
    if no == None:
        file = "levels/test.txt"
    else:
        file = "levels/level"+str(no)+".txt"
    
    file = open(file, "r")
    level = file.read()
    file.close()
    level = level.split("\n")

    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            t = level[y].split("+")[x+1]
            #print (">>", t)
            setTile(x,y, TileType(int(t, 0)))
    

def reset():
    global tiles, stepTimer, selectedToolId, state
    tiles = []
    for i in range(BOARD_H):
        tiles.append([TileType.GROUND]*BOARD_W)
    stepTimer = -1
    selectedToolId = 0
    state = "play"
    loadLevel()

def gridToScreen(x, y):
    return (20+x * TILE_W, 10+y * TILE_H)

def screenToGrid(x, y):
    return (int((-20+x)/TILE_W), int((-10+y) / TILE_H))

def getTile(x, y):
    return tiles[y][x]

def setTile(x, y, v):
    tiles[y][x] = v
    
def clickedTile(x, y):
    setTile(x,y,tools[selectedToolId].tileType)
    
def getNextCellAndType(x,y,t):
    global state
    nx = x
    ny = y
    if t == TileType.ROOT_U:
          ny -= 1  
    elif t == TileType.ROOT_D:
          ny += 1  
    elif t == TileType.ROOT_L:
          nx -= 1  
    elif t == TileType.ROOT_R:
          nx += 1
    
    if not Rect(0,0,BOARD_W, BOARD_H).collidepoint(nx,ny):
        return None
    prevT = getTile(nx,ny)
    if (prevT == TileType.ROCK_LU and t == TileType.ROOT_R):
        return getNextCellAndType(nx, ny, TileType.ROOT_U)
    if (prevT == TileType.ROCK_LU and t == TileType.ROOT_D):
        return getNextCellAndType(nx, ny, TileType.ROOT_L)
    if (prevT == TileType.ROCK_RU and t == TileType.ROOT_L):
        return getNextCellAndType(nx, ny, TileType.ROOT_U)
    if (prevT == TileType.ROCK_RU and t == TileType.ROOT_D):
        return getNextCellAndType(nx, ny, TileType.ROOT_R)
    if (prevT == TileType.ROCK_LD and t == TileType.ROOT_R):
        return getNextCellAndType(nx, ny, TileType.ROOT_D)
    if (prevT == TileType.ROCK_LD and t == TileType.ROOT_U):
        return getNextCellAndType(nx, ny, TileType.ROOT_L)
    if (prevT == TileType.ROCK_RD and t == TileType.ROOT_L):
        return getNextCellAndType(nx, ny, TileType.ROOT_D)
    if (prevT == TileType.ROCK_RD and t == TileType.ROOT_U):
        return getNextCellAndType(nx, ny, TileType.ROOT_R)
    if not (prevT == TileType.GROUND or prevT == TileType.WATER):
        if prevT == TileType.POISON:
#             print("LOST")
            state = "lost"
        return None
    
    return (nx, ny, t) 

def simulateStep():
    roots = []
    newRoots = []
    rootCollisions = []
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            t = getTile(x,y)
            if (t.value >=2 and t.value <= 5):
                roots.append((x,y,t))
    for r in roots:
        x, y, t = r
        nxyt = getNextCellAndType(x,y,t)
        setTile(x, y, TileType.ROOT_H if (t.value >=2 and t.value <= 3) else TileType.ROOT_V)
        if nxyt != None:
            newRoots.append((nxyt[0], nxyt[1], nxyt[2]))
    for nr in newRoots:
        x, y, t = nr
        setTile(x, y, t if getTile(x,y) == TileType.GROUND else TileType.ROOT_X)
    if len(roots) == 0:
        checkWinCon()
        
def checkWinCon():
    global state
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            t = getTile(x,y)
            if t == TileType.WATER:
                state = "lost"
                return
    state = "won"


reset()
wasMouseDown = False
stepTimer = -1

def simulationActive():
    return stepTimer != -1

def update():
    global wasMouseDown, selectedToolId, stepTimer
    if keyboard.r:
        reset()
    if keyboard.s:
        saveLevel()
    if keyboard.l:
        loadLevel()
    if keyboard.k_1:
        loadLevel(1)
    if keyboard.k_2:
        loadLevel(2)
    if keyboard.k_3:
        loadLevel(3)
    if keyboard.k_4:
        loadLevel(4)
    if keyboard.k_5:
        loadLevel(5)
    isMouseDown = pygame.mouse.get_pressed()[0]
    if state == "lost" or state == "won":
        if isMouseDown and not wasMouseDown:
            reset()
        wasMouseDown = isMouseDown
        return
    if simulationActive():
        stepTimer -= 1
        if stepTimer == 0:
            stepTimer = 60
            simulateStep()
        return
    if isMouseDown and not wasMouseDown:
        print(pygame.mouse.get_pos())
        mx, my = pygame.mouse.get_pos()
        gx, gy = screenToGrid(mx, my)
        if Rect(0,0,BOARD_W, BOARD_H).collidepoint(gx,gy):
            clickedTile(gx,gy)
        for toolId in range(len(tools)):
            if tools[toolId].checkClick(mx, my):
               selectedToolId = toolId
        if tools[selectedToolId].tileType == "simulation":
            stepTimer = 60
            saveLevel()
    wasMouseDown = isMouseDown

def draw():
    screen.fill("white")
    screen.blit("bg" if not simulationActive() else "bg_growing", (0,0))
    for y in range(len(tiles)):
        for x in range(len(tiles[y])):
            screen.blit(getGraphic(tiles[y][x]), gridToScreen(x,y))
    if (not simulationActive()):
        for toolId in range(len(tools)):
            tools[toolId].draw(screen, toolId == selectedToolId)
    if state == "lost":
        screen.blit("lost", (0,0))
    if state == "won":
        screen.blit("won", (0,0))


pgzrun.go()
