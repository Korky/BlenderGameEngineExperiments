from bge import logic, types, render
from mathutils import Vector, Quaternion
from math import pi, atan2, degrees

class Bot(types.KX_GameObject):
    
    def __init__(self, own):
        
        #backword compatibility self.scene defined by default in later blender versions
        #self.scene = logic.getCurrentScene()
        
        #set Bot Properties
        self.owner = own
        self.cont = logic.getCurrentController()
        self.markerFlag = 0
        self.track_point = None
        self.track_obj = None
        self.terrain_pos = None
        self.team = 0               #use 0 for neutral bots
        self.speed = 2
        self.hp = 1
        self.status = "alive"
        #self.tracker.worldPositon = self.worldPosition
        
        #self.scene.addObject("TrackMarker")
        #print(self.scene.objects)
        #unused Properties for future versions
        #self.lookingAt = self.worldOrientation.to_euler()
        if "Move" in self.cont.actuators:
            self.pathFind = self.cont.actuators["Move"]
        else:
            self.pathFind = None
        
        if "TrackMarker" in self.scene.objects:       
            self.tracker = self.scene.objects["TrackMarker"]
            self.tracker.setVisible(False)
        else:
            self.tracker = None    
        #sMacros overwrite
        #if "team" in self.owner:
        #    self.team = self.owner["team"]
        
        #set the Initial State
        self.main = self._idle
        
        
         
    # Public
    def holdPosition(self):
        self.main = self._hold
        
    def damage(self,amnt):
        self.hp -= amnt
        if self.hp == 0:
            self.status = "dead"
             
    def select(self):
        self.main = self._selected
        self.markerFlag = 1
    
    def deselect(self):
        self.markerFlag = 0
        
    def setTrackPoint(self, point):
        self.track_point = point
    
    def move(self):
        self.main = self._moving
    
    def setTeam(self, player):
        self.team = player   
    
    def lookAt(self):
        
        #delta = self.track_point - self.worldPosition
        #delta.normalize()
        
        #angle = atan2(delta.x,delta.y)
        #print(angle)
        #self.lookingAt = self.worldOrientation.to_euler()
        #print(self.lookingAt)
        #self.actuators["lookingat"].navmesh = self.scene.objects["Terrain"]
        #self.actuators["lookingat"].target = self.scene.objects["Terrain"]
        
        #print(self.actuators["lookingat"].target)
        #angle *= degrees(angle)
        #rotation = Vector((0,0,angle))
        #self.applyRotation(rotation)
        pass    
        
    # States
    def _hold(self):
        
        self._drawMarker()
        self.track_point = self.worldPosition
        delta = self.track_point - self.worldPosition
        delta.magnitud = self.speed
        self.setLinearVelocity(delta)
        
    def _moving(self):
        
        #check for selected_flag and draw marker if needed
        self._drawMarker()
        
        
        #check for track_point
        if self.track_point:
            
            ### OLD CODE FOR FUTURE BLENDER INDEPENDENT PATH FINDING           
            #delta = self.track_point - self.worldPosition
            #delta.magnitude = self.speed
            
            #angle = atan2(delta.x,delta.y)
            #angle *= degrees(angle)
            #rotation = Vector((0,0,angle))
            #self.applyRotation(rotation)
            ### OLD CODE FOR FUTURE BLENDER INDEPENDENT PATH FINDING
            
            
            #set track_point value, set to Visible and activate Path Finding Actuator
            if self.tracker:
                self.tracker.localPosition = self.track_point
                self.tracker.setVisible(True)
            #self["isTrackPoint"] = True
            
            #get comparison points
            self.terrain_pos = (round(self.worldPosition.x,0), round(self.worldPosition.y,0))
            compare_point = (round(self.track_point.x,0), round(self.track_point.y,0))
            
            #compare current Object's Position with track_point's Position
            if not self.terrain_pos == compare_point:
                
                #Code happening during movement ...
                #use for future since Path Finding Actuator is in use 
                #no movment code nessesary              
                #self.setLinearVelocity(delta)
                if self.pathFind:
                    self.cont.activate(self.pathFind)   
                pass
            
            else:
                
                #deavtivate Path Finding Actuator & release track_point when track_point reached
                #self["isTrackPoint"] = False
                if self.pathFind:
                    self.cont.deactivate(self.pathFind) 
                
                self.track_point = None
                
                
        
        elif self.track_obj:
            if self.pathFind:
                self.pathFind.target  = self.track_obj
            
           
                
        else:
            
            #set tracker to invisible & change Object's State
            if self.tracker:
                self.tracker.setVisible(False)
            self.main = self._idle  
            
    def _idle(self):
        
        #check for selected_flag and draw marker if needed
        self._drawMarker()    
        pass
    
    def _selected(self):
        
        #check for selected_flag and draw marker if needed
        self._drawMarker()
    
        
    # Facilitating methods
    def _drawMarker(self):
        
        #check for selected_flag and draw marker if needed
        if self.markerFlag:
            delta = Vector((0,0,1))
            delta.magnitude = 2.5
            render.drawLine(self.worldPosition, self.worldPosition + delta, [255, 0, 0])



class Worker(Bot):
    
    def __init__(self, own):
        
        
        self.MAX_HOLD = 5
        
        self.minerals = 0
        self.mineralPatch = None
        
        Bot.__init__(self,own)
    
    #States    
    def _gather(slef):
        
        pass
    
class Melee(Bot):
    
    
    def __init__(self, own):
        
        self.target = None
        
        Bot.__init__(self,own) 


class Range(Bot):
    
    
    def __init__(self, own):
        
        #Constant Properties
        self.MAX_RANGE = 0      # set 0 for infinite
        self.FIRE_SPEED = 10    # speed which bullets move
        
        #Object Properties
        self.target = None      # will not implement for this demo
        self.amuQty = 0
        
        #call super class to init States
        Bot.__init__(self,own)
        
  
      
    def collect_amu(self, qty):
        self.amuQty += qty   
    
            
                
