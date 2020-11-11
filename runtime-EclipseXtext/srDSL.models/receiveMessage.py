
class receiveMessage:

    def takeControl(self):
        return self.receivedMessage
    
    def action(self):
        print(self.user + " RECEIVED A MESSAGE")
        while (not self.suppressed) and self.active:       
            if self.receivedColor in self.c.colorsToFind:
                self.c.colorsToFind.remove(self.receivedColor)
                print(self.user + ": " + str(self.c.colorsToFind))
                self.u.mSpeak("Other Robot found color")
                self.u.int2SpeakColor(self.receivedColor)
            if len(self.c.colorsToFind) == 0:
                self.u.mSpeak("Found all colors!")
                self.c.foundAllColors = True
            self.receivedMessage = False
            self.active = False
    
    def suppress(self):
        self.suppressed = True
        
    def __init__(self, u, c):
        self.receivedMessage = False
        self.receivedColor = -1
        
        self.u = u
        self.c = c
        
        self.user = "Null"
        
        self.suppressed = False
        self.active = False