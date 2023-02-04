import pgzero, pgzrun, pygame
import sys, math

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
TITLE = "Root 3"

LAND_LEVEL = 400

hero = Actor("hero")
hero.y = LAND_LEVEL

actorV = 0

attacks = []

SPEED = 3.5

wasAtt = False

class Attack(Actor):
    def __init__(self):
        Actor.__init__(self, "attack", (hero.x, hero.y))
        self.lifetime = 45
        
    def update(self):
        self.angle -= 15
        self.lifetime -= 1

def lerp(pct, a, b):
    return (a[0]*(1.0-pct)+b[0]*pct, a[1]*(1.0-pct)+b[1]*pct)

def lerpf(pct, a, b):
    return a*(1.0-pct)+b*pct

class Root():
    def __init__(self):
        self.a = (100, 400)
        self.b = (416, 176)
        self.c = (400, 400)
    
    def update(self):
        pass
#         if pygame.mouse.get_pressed()[0]:
#             self.b = pygame.mouse.get_pos()
#         if pygame.mouse.get_pressed()[2]:
#             self.a = pygame.mouse.get_pos()

    def draw(self, screen):
        phase = pygame.time.get_ticks()* 2.0 / 1000.0
        phaseB = phase + math.pi/2
        alfa = (1 + math.sin(phase))/2
        alfaB = (1 + math.sin(phaseB))/2
        self.a = lerp(alfa, (46, 404), (429, 154))
        self.b = lerp(alfaB, (46, 404), (429, 154))
        prev = self.a
        pct = 0
        SEGMENTS = 30
        for i in range(SEGMENTS):
            pct += 1.0/SEGMENTS
            a1 = lerp(pct, self.a, self.b)
            a2 = lerp(pct, self.b, self.c)
            r = lerp(pct, a1, a2)
            screen.draw.line(prev, r, "brown")
            screen.draw.filled_circle(prev, int(lerpf(pct, 3, 15)), "brown")
            prev = r
            
#         screen.draw.circle(self.a, 10, "red")
#         screen.draw.circle(self.b, 8, "green")
#         screen.draw.circle(self.c, 10, "red")
#         print("==[", self.b, "]==>", self.a);
    
root1 = Root()
    
def update():
    global wasAtt, actorV, attacks
    if keyboard.a:
        hero.x -= SPEED
    if keyboard.d:
        hero.x += SPEED
    if (keyboard.space or keyboard.w) and hero.y >= LAND_LEVEL:
        actorV = -15
    actorV += 1
    hero.y += actorV
    
    if (hero.y > LAND_LEVEL):
        hero.y = LAND_LEVEL
        actorV = 0
    isAtt = keyboard.kp5 or keyboard.k
    if isAtt and not wasAtt:
        attacks.append(Attack())
    wasAtt = isAtt
    for a in attacks:
        a.update()
    attacks = list(filter( lambda a : a.lifetime > 0, attacks))
    root1.update()   

def draw():
    screen.fill("white")
    screen.blit("bg", (0,0))
    hero.draw()
    for a in attacks:
        a.draw()
    root1.draw(screen)

pgzrun.go()
