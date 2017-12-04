from bge import logic,types


class Map(types.KX_GameObject):
    
    def __init__(self, own):
        
        self.owner = own
        self.cont = logic.getCurrentController()
        
        self.main = self._idle
        
    def _idle(self):
        
        pass 