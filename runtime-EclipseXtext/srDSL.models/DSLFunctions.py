# DSLFunctions.py

class DSLFunctions:
    # =============== Actions ===============
    def forwardForMove(self, distance, unit):
        if unit == "rotations" and distance > 0:
            self.m.forward(distance)
    
    def forwardMove(self):
        while True:
            self.m.forward(0.2)
            
    def backwardForMove(self, distance, unit):
        if unit == "rotations" and distance > 0:
            self.m.forward(distance)
        
    def backwardMove(self):
        while True:
            self.m.backward(0.2)
        
    def leftForMove(self, angle, unit):
        if unit == "rotations":
            self.m.safeRotate(-1, angle)
        elif unit == "seconds":
            # TODO: implement
            return
        
    def leftMove(self):
        while True:
            self.m.safeRotate(-1, 0.2)
        
    def rightForMove(self, angle, unit):
        if unit == "rotations":
            self.m.safeRotate(1, angle)
        elif unit == "seconds":
            # TODO: implement
            return
        
    def rightMove(self):
        while True:
            self.m.safeRotate(1, 0.2)
        
    def randomMove(self):
        self.m.randomStep()
        
    def randomWalk(self):
        while True:
            self.m.randomStep()
            
            
    # =============== Conditions ===============
    def colorCondition (self, shouldFind):
        color = self.u.lastColor
        if color != self.lastColor and color in shouldFind: 
            self.lastColor = color
            self.foundColours.append(color)
            
            if (all(c in self.foundColours for c in shouldFind)):
                shouldFind = [] # reset the list for the next task
                return True
        return False
         
        
    def distanceCondition (self, comparator, distance):
        if comparator == "lt":
            return self.u.checkDistance() <= distance 
        elif comparator == "gt":
            return self.u.checkDistance() >= distance
        return False
            
        
    def touchCondition (self, comparator, value):
        if comparator == "left":
            return self.u.checkTouchL()
        elif comparator == "right":
            return self.u.checkTouchR()
        elif comparator == "both":
            return self.u.checkTouchL() and self.u.checkTouchR()
        return False
    
    def buttonPressCondition(self):
        # TODO: implement
        return
    
    def init(self, movement, utils):
        self.m = movement
        self.u = utils
    
        self.foundColours = []