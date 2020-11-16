#checkConditions.py

class checkConditions:        
    def takeControl(self):
        # check the list of movements
        for c in self.conditions:
            if c[0](**c[1]):
                self.conditions.remove(c)
        return len(self.actions) > 0
                        
    def action(self):
        while (not self.suppressed) and self.active: 
            self.isDone = True
            for c in self.conditions:
                if not c[0](**c[1]):      
                    self.isDone = False                
            self.active = False
                
    def suppress(self):
        self.suppressed = True
    
    
    def __init__(self, conditions):
        self.conditions = conditions
        
        self.suppressed = False
        self.active = False
        self.isDone = False