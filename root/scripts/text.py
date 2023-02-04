import pygame

class Text():
    def __init__(self, text, xy):
        self.text = text
        self.xy = (xy[0]-50, xy[1]-25)
        self.w, self.h = (100,50)
        
    def update(self):
        pass

    def draw(self, screen):
        screen.draw.text(self.text,(self.xy[0]+10,self.xy[1]+10),color="black", background="white")
