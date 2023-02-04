from pgzero.actor import Actor

import pygame

class Button(Actor):
    def __init__(self, text, xy, onClick):
        if not hasattr(self, "images"):
            self.images = ["btn", "btn_click", "btn_hover"]
        Actor.__init__(self, self.images[0], xy)
        self.text = text
        self.onClick = onClick
        self.wasMouseDown = False
        self.inFocus = False
        self.w, self.h = self._surf.get_size()
        
    def update(self):
        mx,my = pygame.mouse.get_pos()
        isMouseDown = pygame.mouse.get_pressed()[0]
        if (mx < self.left or my < self.top
            or mx > self.left + self.w or my > self.top + self.h):
            self.image = self.images[0]
            self.inFocus = False
        elif isMouseDown:
            if self.wasMouseDown == False:
                self.image = self.images[1]
                self.inFocus = True
        else:
            self.image = self.images[2]
            if self.inFocus:
                self.onClick()
        self.wasMouseDown = isMouseDown

    def draw(self, screen):
        Actor.draw(self)
        screen.draw.text(self.text,(self.left+10,self.top+10),color="black")
        
class ButtonSmall(Button):
    def __init__(self, text, xy, onClick):
        self.images = ["btn_small", "btn_small_click", "btn_small_hover"] 
        Button.__init__(self, text, xy, onClick)
