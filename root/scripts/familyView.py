from pgzero.actor import Actor
from .button import Button, ButtonSmall
from .face import Face
from .text import Text
from .data import loadFamily

class FamilyView():
    def __init__(self, scene, initPersonId):
        self.updateables = []
        self.data = loadFamily(initPersonId)
        self.loadNextFamily = None

        addChild = self.updateables.append
        addChild(Face(scene, self.data.left, (200,200), self.setFamily))
        addChild(Face(scene, self.data.right, (450,200), self.setFamily))

        y = 380+50/2
        x = 50+100/2
        for c in self.data.children:
            def setFamily(family = c):
                self.loadNextFamily = family
            addChild(ButtonSmall(c,(x,y), setFamily))
            x += 10+100
            
        def showHelp():
            scene.showHelp()
        addChild(ButtonSmall("help",(550,40), showHelp))

            
    def setFamily(self, family):
        self.loadNextFamily = family        

    def update(self):
        for c in self.updateables:
            c.update()

    def draw(self, screen):
        if len(self.data.children) == 0:
            screen.draw.text("no children",(60,395),color="black", background="white")
        for c in self.updateables:
            c.draw(screen)
            
    def getCharactersOnScreen(self):
        result = [self.data.left]
        if self.data.right != None:
            result.append(self.data.right)
        return result
