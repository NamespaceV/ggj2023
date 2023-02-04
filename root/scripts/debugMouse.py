import pgzero, pygame

def minus(a,b):
    return (a[0]-b[0], a[1]-b[1])

class DebugMouse():
    def __init__(self):
        self.relative = (0, 0)
        
    def update(self):
       if pygame.mouse.get_pressed()[2]:
           self.relative = pygame.mouse.get_pos()
    
    def draw(self, screen):
        screen.draw.text(f'{minus(pygame.mouse.get_pos(),self.relative)}',\
                         (0,0),color="black", background="white")
        
