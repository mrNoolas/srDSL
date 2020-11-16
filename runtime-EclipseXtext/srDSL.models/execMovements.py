#execFunctions.py    
        
class execMovements:        
    def takeControl(self):
        # check the list of movements
        if len(self.actions) > 0:
            return True
        else:
            self.isDone = True
            return False
                        
    def action(self):
        while (not self.suppressed) and self.active:   
            if self.actions[0][2]: # keep looping this action    
                action = self.actions[0] #i.e. don't pop, just do
            else: # don't loop          
                action = self.actions.pop(0)
            
            action[0](**action[1])
                
            self.active = False
                
    def suppress(self):
        self.suppressed = True
    
    
    def __init__(self, actions):
        self.actions = actions
        self.suppressed = False
        self.active = False
        self.isDone = False