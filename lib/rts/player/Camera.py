from bge import logic, events, render
from mathutils import Vector


class mouseScroll:
    
    def __init__ (self, cont):
        
        #get Dependencies
        self.cont = cont
        self.camera = cont.owner
        self.mouse = logic.mouse
        
        x = render.getWindowWidth()//2
        y = render.getWindowHeight()//2
        self.screen_center = (x, y)
        render.setMousePosition(x + 1, y + 1)
        #show Mouse
        render.showMouse(1)
        
    def main (self):
        
        
        #check for individual Mouse Position on Screen
        if self.mouse.position[1] <= 0.0:
            #print("Scroll Screen Foward")
            self._scrollY(0.5)
        if self.mouse.position[1] >= 1:
            #print("Scroll Screen Down")
            self._scrollY(-0.5)
        if self.mouse.position[0] <= 0.0:
            #print("Scroll Screen Left")
            self._scrollX(-0.5)
        if self.mouse.position[0] >= 1:
            #print("Scroll Screen Right")
            self._scrollX(0.5)
    
            
    def _scrollY (self, dir):
        
        #move Camera in Y axis
        self.camera.position.y += dir
        
    def _scrollX (self, dir):
        
        #move Camera in X axis
        self.camera.position.x += dir
       
       
       
class keyboardScroll:
    
    def __init__(self, cont):
        
        #get Dependencies
        self.cont = cont
        self.camera = cont.owner
        self.keyboard = logic.keyboard
        
    def main (self):
        
        #check for individual Keyboard Events
        if self.keyboard.events[events.UPARROWKEY] ==  logic.KX_INPUT_ACTIVE:
            #print("Activate Forward!")
            self._scrollY(0.1)
        if self.keyboard.events[events.DOWNARROWKEY] ==  logic.KX_INPUT_ACTIVE:
            #print("Activate Backward!")
            self._scrollY(-0.1)
        if self.keyboard.events[events.LEFTARROWKEY] ==  logic.KX_INPUT_ACTIVE:
            #print("Activate Left!")
            self._scrollX(-0.1)
        if self.keyboard.events[events.RIGHTARROWKEY] ==  logic.KX_INPUT_ACTIVE:
            #print("Activate Right!")
            self._scrollX(0.1)
            
    def _scrollY (self, dir):
        
        #move Camera in Y axis
        self.camera.position.y += dir
        
    def _scrollX (self, dir):
        
        #move Camera in X axis
        self.camera.position.x += dir


