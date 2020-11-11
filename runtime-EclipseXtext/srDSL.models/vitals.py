from utils import utils

class vitals:           
    def onBorder(self):
        color = self.u.checkColor()
        return color == 1 or color == 0        
    
    def isColliding(self):
        isColliding = self.u.checkTouchL() or self.u.checkTouchR()
        return isColliding
    
    def isCloseToColliding(self):
        distance = self.u.checkDistance()
        if distance < 280:
            self.u.mSpeak('Collision threat in the front!')
            return True

        return False
        
                
    def __init__(self, utils):
        # Hello!  
        self.u = utils