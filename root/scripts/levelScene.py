from .button import ButtonSmall, Button
from .familyView import FamilyView
from .helpView import HelpView
from .debugMouse import DebugMouse
from .data import loadLevel, DorothyVampireLevel, BibleLevel

class LevelScene():
    def __init__(self, music, levelName = None):
        self.state = "help"
        self.familyView = None
        self.debugMouse = DebugMouse()
        self.music = music
        self.geneModFailedCounter = 0
        global familyView
        if levelName == None:
            self.levelData = DorothyVampireLevel()
        else:
            self.levelData = BibleLevel()
        loadLevel(self.levelData)
        self.familyView = FamilyView(self, self.levelData.startId)
        self.helpView = HelpView(self, self.levelData.help)
        try:
            #music.play("awaken-136824")
            music.set_volume(0.3)
        except:
            print("music failed")
            pass

    def update(self):
        self.debugMouse.update()
        if self.state == "help":
            self.helpView.update()
            return
        if self.state == "win":
            return

        self.familyView.update()
        if self.geneModFailedCounter > 0:
            self.geneModFailedCounter -= 1
        if self.familyView.loadNextFamily != None:
            self.familyView = FamilyView(self, self.familyView.loadNextFamily)
        if self.levelData.checkWinCon(self.familyView.getCharactersOnScreen()):
            self.state = "win"
        
    def draw(self, screen):
        if self.state == "help":
            self.helpView.draw(screen)
            self.debugMouse.draw(screen)
            return
        if self.state == "win":
            screen.blit(self.levelData.win, (0,0))
            return

        self.familyView.draw(screen)
        self.debugMouse.draw(screen)
        if self.geneModFailedCounter > 0:
            screen.draw.text(f'You have to modify parents genes. ({self.geneModFailedCounter})',\
                         (0,0),color="black", background="white")
    
    def geneModFailed(self):
        self.geneModFailedCounter = 3*60
        
    def showHelp(self):
        self.state = "help"
        
    def closeHelp(self):
        self.state = ""
    

        