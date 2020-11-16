#execFunctions.py    
        
class execMovements:        
    def takeControl(self):
        # check the list of movements
        return len(self.actions) > 0
                        
    def action(self):
        while (not self.suppressed) and self.active:       
            action = self.actions.pop(0)
            action[0](**action[1])
                
            self.active = False
                
    def suppress(self):
        self.suppressed = True
    
    
    def __init__(self, actions):
        self.actions = actions
        self.suppressed = False
        self.active = False