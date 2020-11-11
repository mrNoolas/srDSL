
class checkColor:
    def takeControl(self):
        color = self.u.lastColor
        if color != self.lastColor and (color == 2 or color == 4 or color == 5): #Blue, yellow or red  
            #print("Color read: " + str(color))
            self.lastColor = color
            return True
        else: return False 
        
    def action(self):
        if not self.suppressed:
            if self.lastColor in self.colorsToFind:
                self.readyToSend = True
                self.colorsToFind.remove(self.lastColor)
                print(self.colorsToFind)
            self.u.playDebugSound = True
            #self.u.mBeep()
            self.u.int2SpeakColor(self.lastColor)
            self.u.playDebugSound = False
            if len(self.colorsToFind) == 0:
                self.u.mSpeak("Found all colors!")
                self.foundAllColors = True
        self.active = False
    
    def suppress(self):
        self.suppressed = True

        
    def __init__(self, utils):
        self.u = utils
        self.lastColor = self.u.lastColor
        
        self.colorsToFind = [2,4,5]
        
        self.readyToSend = False
        
        self.foundAllColors = False
        self.active = False
        self.suppressed = False

        