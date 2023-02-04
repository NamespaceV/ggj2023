from .button import Button, ButtonSmall

class HelpView:
    def __init__(self, scene, helpBg):
        self.bg = helpBg
        def deactivate():
            scene.closeHelp()
        self.closeButton = ButtonSmall("X", (570,450), deactivate)

    def update(self):
        self.closeButton.update()

    def draw(self, screen):
        screen.blit(self.bg, (0,0))
        self.closeButton.draw(screen)
    
        