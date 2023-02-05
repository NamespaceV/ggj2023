import pgzero, pgzrun, pygame
import sys, math, random

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

attacks = []

class Particle():
    def __init__(self, loc, color="red"):
        self.loc = loc
        self.time = 60
        self.vy = -10
        self.vx = random.uniform(-2,2)
        self.color = color
    def update(self):
        self.time -= 1
        l = self.loc
        self.vy += 1
        self.loc = (l[0]+self.vx, l[1]+self.vy)
        if (self.loc[1] > 480+5):
            self.time = 0
        pass
    def draw(self, screen):
        screen.draw.circle(self.loc,5,self.color)
        

class Particles():
    def __init__(self):
        self.particles = []
    def hitHero(self, loc):
        if (len(self.particles) > 200):
            return
        self.particles.append(Particle(loc))
    def hitBoss(self, loc):
        if (len(self.particles) > 200):
            return
        self.particles.append(Particle(loc, "green"))
    def update(self):
        for p in self.particles:
            p.update()
        self.particles = list(filter( lambda p: p.time > 0, self.particles))
    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
    def clear(self):
        self.particles = []
    
    
particles = Particles()

class Attack(Actor):
    def __init__(self):
        Actor.__init__(self, "attack", (hero.x, hero.y))
        self.lifetime = 30
        
    def update(self):
        self.angle -= 25
        self.lifetime -= 1

def lerp(pct, a, b):
    return (a[0]*(1.0-pct)+b[0]*pct, a[1]*(1.0-pct)+b[1]*pct)

def lerpf(pct, a, b):
    return a*(1.0-pct)+b*pct

SPEED = 3.5

class Hero(Actor):
    def __init__(self):
        Actor.__init__(self,"hero")
        self.wasAtt = False
        self.v = 0
        self.timeFly = 0

    def update(self):
        if self.timeFly > 0:
            self.x -= SPEED
            self.timeFly -= 1
        else:
            if keyboard.a or keyboard.left:
                self.x -= SPEED
            if keyboard.d or keyboard.right:
                self.x += SPEED
            if (keyboard.space or keyboard.w or keyboard.up) and hero.y >= LAND_LEVEL:
                self.v = -15
        self.v += 1
        self.y += self.v
        if (self.y > LAND_LEVEL):
            self.y = LAND_LEVEL
            self.v = 0
        isAtt = keyboard.kp5 or keyboard.k or keyboard.z or keyboard.x or keyboard.c
        if isAtt and not self.wasAtt:
            attacks.append(Attack())
        self.wasAtt = isAtt
        if self.x > 400:
            self.timeFly = 60
            self.v = -30


hero = Hero()
hero.y = LAND_LEVEL

heroHp = 100
bossHp = 100

timescore = 0

def inRange(r, a, b ):
    x = a[0]-b[0]
    y = a[1]-b[1]
    return x*x + y*y < r*r

def checkCollisions(loc, r):
    global bossHp, heroHp
    if heroHp < 0 or bossHp < 0:
        return

    attack_r=30
    hero_r = 7
#     screen.draw.circle((hero.x, hero.y), hero_r, "red")
#     screen.draw.circle((hero.x, hero.y+20), hero_r, "red")
#     screen.draw.circle((hero.x, hero.y-30), hero_r, "red")
    hit = False
    if inRange(r+hero_r, (hero.x, hero.y), loc):
        hit = True
        particles.hitHero((hero.x, hero.y))
    elif inRange(r+hero_r, (hero.x, hero.y+20), loc):
        hit = True
        particles.hitHero((hero.x, hero.y+20))
    elif inRange(r+hero_r, (hero.x, hero.y-30), loc):
        hit = True
        particles.hitHero((hero.x, hero.y-30))
    if hit:
        heroHp -= 0.1
    for a in attacks:
#         screen.draw.circle((a.x, a.y), attack_r, "white")
        if inRange(r+attack_r, (a.x, a.y), loc):
            bossHp -= 0.01
            particles.hitBoss(loc)


class Root():
    def __init__(self):
        self.a = (150, 400)
        self.b = (416, 176)
        self.c = (400, 400)
        self.lastPhase = 0
    
    def update(self):
        if heroHp < 0 or bossHp < 0:
            phase = self.lastPhase
        else:
            phase = pygame.time.get_ticks()* 2.0 / 1000.0
            self.lastPhase = phase
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
            pos = lerp(pct, a1, a2)
            r = int(lerpf(pct, 3, 15))
            checkCollisions(prev, r)
            prev = pos
#         if pygame.mouse.get_pressed()[0]:
#             self.b = pygame.mouse.get_pos()
#         if pygame.mouse.get_pressed()[2]:
#             self.a = pygame.mouse.get_pos()

    def draw(self, screen):
        if heroHp < 0 or bossHp < 0:
            phase = self.lastPhase
        else:
            phase = pygame.time.get_ticks()* 2.0 / 1000.0
            self.lastPhase = phase
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
            pos = lerp(pct, a1, a2)
            screen.draw.line(prev, pos, "brown")
            r = int(lerpf(pct, 3, 15))
            screen.draw.filled_circle(prev, r, "brown")
            prev = pos
            
#         screen.draw.circle(self.a, 10, "red")
#         screen.draw.circle(self.b, 8, "green")
#         screen.draw.circle(self.c, 10, "red")
#         print("==[", self.b, "]==>", self.a);
    
root1 = Root()

def restart():
    global heroHp, bossHp, attacks, timescore
    timescore = 0
    heroHp = 100
    bossHp = 100
    hero.y = LAND_LEVEL
    hero.x = 0
    particles.clear()
    attacks = []
    
def update():
    global timescore
#     print(heroHp , "--", bossHp)
    if heroHp < 0 or bossHp < 0:
        if keyboard.r:
            restart()
        return
    timescore += 1
    hero.update()

    global attacks
    for a in attacks:
        a.update()
    attacks = list(filter( lambda a : a.lifetime > 0, attacks))
    
    root1.update()
    particles.update()

def draw():
    screen.fill("white")
    screen.blit("bg", (0,0))
    hero.draw()
    for a in attacks:
        a.draw()
    root1.draw(screen)
    particles.draw(screen)
#             print(bossHp, "VS", heroHp)
    screen.draw.filled_rect(Rect(10,10,620,10), "white")
    down = int(620*max(1.0-(bossHp/100), 0))
    screen.draw.filled_rect(Rect(10+down,10,620-down,10), "brown")
    screen.draw.text("Tree", (10,20), color="White")

    screen.draw.filled_rect(Rect(10,460,620,10), "red")
    down = int(620*max(1.0-(heroHp/100), 0))
    screen.draw.filled_rect(Rect(10+down,460,620-down,10), "black")
    screen.draw.text("Lumberjack", (10,435), color="Red")
    
    resetText = False
    if bossHp < 0:
        screen.blit("won", (0,0))
        screen.draw.text(f'Time used: {timescore} hp left {heroHp:.1f}', (250,300), color="black", background="white")
        resetText = True
    elif heroHp < 0:
        screen.blit("lost", (0,0))
        resetText = True
    if resetText and pygame.time.get_ticks() % 1000 > 500:
        screen.draw.text("Press R to restart", (250,280), color="black", background="white")



pgzrun.go()
