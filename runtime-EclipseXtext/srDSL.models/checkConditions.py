#checkConditions.py

class checkConditions:        
    def takeControl(self):
        # check the list of movements
        for c in self.conditions:
            if c[0](**c[1]):
                self.conditions.remove(c)
                return True
            
        if len(self.conditions) == 0:
            self.isDone = True
        return False
                        
    def action(self):
        while (not self.suppressed) and self.active: 
            allDone = True
            for c in self.conditions:
                if not c[0](**c[1]):      
                    allDone = False
            if allDone:
                self.isDone = True           
            self.active = False
                
    def suppress(self):
        self.suppressed = True
    
    
    def __init__(self, conditions):
        self.conditions = conditions
        
        self.suppressed = False
        self.active = False
        self.isDone = False