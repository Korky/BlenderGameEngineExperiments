from bge import logic, types, render, events
from mathutils import Vector, geometry
import bgl

class Selector(types.KX_GameObject):
    
    def __init__(self, own):
        
        #self.scene = logic.getCurrentScene() # defined by default in later blender versions
        self.owner = own
        
        #get Scene Object Dependencies 
        self.camera = self.scene.objects["Camera"]
        
                
        #get the Controller Running this code
        cont = self.controllers["Main"]
        
         
        #get Sensors Dependencies
        self.mouseLclick = cont.sensors["mouseLclick"]
        self.mouseRclick = cont.sensors["mouseRclick"]
        self.mouseover = cont.sensors["mouseover"]
        self.keyboard = logic.keyboard
        #set Selector's Properties
        #selection_box
        self.box_coords = [None, None]
        self.build_flag = False
        
        #Selection List
        self.selected = []
        
        #set Initial State
        self.main = self._idle
        
    # States
    
    def _idle(self):
        
        #check build flag triggers
        if self.keyboard.events[events.BKEY] ==  logic.KX_INPUT_JUST_ACTIVATED:
            self.build_flag = True
            self.scene.addObject("basic_building",self.scene.objects["build_tracker"])
        elif self.build_flag and self.keyboard.events[events.QKEY] ==  logic.KX_INPUT_JUST_ACTIVATED:
            self.build_flag = False
            
        if self.build_flag:
            self.scene.objects["build_tracker"].worldPosition = self.mouseover.hitPosition
            
            
        #check each Sensor's Activity
        if self.mouseLclick.positive and not self.build_flag:
            #set first selection_box cordinates and change State
            self.box_coords[0] = logic.mouse.position
            self.main = self._select
        if self.mouseRclick.positive and not self.build_flag:
            #set an action to selected Objects
            self._dispatchSelected()   
    
    def _select(self):
        
        #update selection_box cordinate and render
        self.box_coords[1] = logic.mouse.position
        self.scene.post_draw = [self._drawSelectionBox]
        
        #check for mouse release action
        if not self.mouseLclick.positive:
            
            #check Multiple or Single Selection
            if self.box_coords[0] != self.box_coords[1]:
                self._selectObjects()
            else:
                self._dispatchSelected()
                #self._selectObject()
            
            #release Post-Renedered Data
            self.scene.post_draw.pop()
            self.main = self._idle
            
    # Facilitating methods
    
    def _whatGotClicked(self): 
        
        #return the object clicked by the mouse in the 3D World
        point = Vector(self.camera.getScreenPosition(self.mouseover.hitPosition))
        return self.camera.getScreenRay(point.x, point.y, 1000)
    
    def _dispatchSelected(self):
        
        #check if Cursor is over Game Screen
        if self.mouseover.positive:
            
            #get cordinates of the Cursor relative to the 3D World and get the Object that got clicked
            hit_pos = self.mouseover.hitPosition
            hit_obj = self._whatGotClicked()
            
            #check if what you clicked is not a Unit then give all selected objects an action
            if not "UnitType" in hit_obj:
                for obj in self.selected:
                    obj.setTrackPoint(hit_pos)
                    obj.move()
    
    def _selectObject(self,hit_obj):
        
        #check if going to [Apend to] or [Create a new] Selection List 
        if not logic.keyboard.events[events.LEFTSHIFTKEY] ==  logic.KX_INPUT_ACTIVE or not logic.keyboard.events[events.RIGHTSHIFTKEY] ==  logic.KX_INPUT_ACTIVE:
            for obj in self.selected:
                obj.deselect()
            self.selected = []
        
        #check if hit Object is a Unit       
        if "UnitType" in hit_obj:
            
            #set Object slelected property and Apend it to the Selection List
            hit_obj.select()
            self.selected.append(hit_obj)
                
                
    def _selectObjects(self):
        
        #get selection_box
        quad = self._getScreenQuad()
        
        #check if going to [Apend to] or [Create a new] Selection List
        if not logic.keyboard.events[events.LEFTSHIFTKEY] ==  logic.KX_INPUT_ACTIVE or not logic.keyboard.events[events.RIGHTSHIFTKEY] ==  logic.KX_INPUT_ACTIVE:
            for obj in self.selected:
                obj.deselect()
            self.selected = []
        
        #get all Objects in and ccheck if they are Units
        for obj in self.scene.objects:
            if "UnitType" in obj:
                
                #get the Object's 3D World Position relative to the screen and check if it intersects with 2D selection_box
                point = Vector(self.camera.getScreenPosition(obj.worldPosition))
                test = [point] + quad
                in_quad = geometry.intersect_point_quad_2d(*test)
                
                #if it intersects set Object selected property and Apend it to the Selection Lis
                if in_quad:
                    
                    hit_obj = self.camera.getScreenRay(point.x, point.y, 1000)
                    if hit_obj == obj:
                        obj.select()
                        self.selected.append(obj)
    
    def _getScreenQuad(self):
        
        vec_A = Vector(self.box_coords[0])
        vec_B = Vector(self.box_coords[1])
        
        delta = vec_B - vec_A
        
        vec_a = vec_A.copy()
        vec_a.x += delta.x
        
        vec_b = vec_B.copy()
        vec_b.x -= delta.x
        
        return [vec_A, vec_a, vec_B, vec_b]
    
    
    def _drawSelectionBox(self):
        
        quad = self._getScreenQuad()
        
        bgl.glMatrixMode(bgl.GL_PROJECTION)
        bgl.glLoadIdentity()
        bgl.gluOrtho2D(0, 1, 1, 0)
        
        bgl.glMatrixMode(bgl.GL_MODELVIEW)
        bgl.glLoadIdentity()
     
        bgl.glColor3f(1, 0, 0)
        bgl.glBegin(bgl.GL_LINE_LOOP)
        for p in quad:
            bgl.glVertex2f(p.x, p.y)
        bgl.glEnd()
        
        


