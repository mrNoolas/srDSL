import random

class doMovements:
    def takeControl(self):
        return True
    
    def action(self):
        while (not self.suppressed) and self.active:       
            # random rotation in direction
            rot = random.randint(-6, 6) / 10
            #print(rot)
            result = self.m.safeRotate(rot, abs(rot))
            #print("saferotate result: " + str(result))
            
            if result == 1:
                # random forward unless collision
                dr = random.randint(5, 20) / 10
                self.m.forward(dr)
            else:
                self.m.backward(0.20) # 0.2 seems to be the ideal value here; it performs better than 0.15 and 0.25
            
        self.active = False
        
    def suppress(self):
        self.suppressed = True
    
    
    def __init__(self, vitals, movement):
        self.v = vitals
        self.m = movement
        
        self.suppressed = False
        self.active = False