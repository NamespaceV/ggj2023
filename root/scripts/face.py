from pgzero.actor import Actor
from pygame.rect import Rect
from .button import Button, ButtonSmall
from .text import Text

from .data import people
import pygame

rects = [
    ( -60, -80, 50, 50),#eyeL
    ( -10, -80, 50, 50),#eyeR
    ( -30, -34, 50, 50),#nose
    ( -70, +10, 50, 50),#mouth
]

class Face():
    def __init__(self, scene, name, xy, setFamily):
        self.scene = scene
        self.xy = xy
        self.data = people[name] if name in people else None
        self.focusRect = None
        self.wasMouseDown = False
        self.inFocus = False
        self.updateables = []
        
        if self.data == None:
            return
        addChild = self.updateables.append

        y = xy[1]-160
        x = xy[0]- 50

        for g in self.data.parents:
            if g == None:
                addChild(Text("unknown",(x,y)))
            else:
                def setFamilyInternal(family = g):
                    setFamily(family)
                addChild(ButtonSmall(g,(x,y), setFamilyInternal))
            x += 10+100

        
    def getRect(self, xy):
        xy = (xy[0] - self.xy[0], xy[1] - self.xy[1])
        for i in range(len(rects)):
            if (xy[0] >= rects[i][0] and xy[0] <= rects[i][0]+rects[i][2]
                and xy[1] >= rects[i][1] and xy[1] <= rects[i][1]+rects[i][3]):
                return i
        return None
 
    def update(self):
        if self.data == None:
            return
        for u in self.updateables:
            u.update()
        isMouseDown = pygame.mouse.get_pressed()[0]
        currRect = self.getRect(pygame.mouse.get_pos())
        if currRect == None:
            self.inFocus = False
        elif isMouseDown:
            if self.wasMouseDown == False:
                self.focusRect = currRect
                self.inFocus = True
            elif self.focusRect != currRect:
                self.inFocus = False
        elif self.wasMouseDown:
            if self.focusRect == currRect:
                self.clickRect(currRect)
        
        self.wasMouseDown = isMouseDown
    
    def clickRect(self, rectId):
#         print("cccc",rectId)
        if rectId == 0:
            rectId += 1
        rectId -= 1
        result = self.data.updateGene(rectId)
        if result == False:
            self.scene.geneModFailed()
    
    def draw(self, screen):
        if self.data == None:
            return
        for u in self.updateables:
            u.draw(screen)
        x, y = self.xy
#             screen.draw.rect(Rect(x-60,y-80,50,50), "red")
        screen.blit("face", (x-105,y-125))
        screen.blit("eye"+str(self.data.genes[0]), (x-60,y-80))
        screen.blit("eye"+str(self.data.genes[0]), (x-10,y-80))
        screen.blit("nose"+str(self.data.genes[1]), (x-30,y-34))
        screen.blit("mouth"+str(self.data.genes[2]), (x-70,y+10))
        
        screen.draw.text(self.data.displayName,(x-50,y+100),color="black", background="white")

