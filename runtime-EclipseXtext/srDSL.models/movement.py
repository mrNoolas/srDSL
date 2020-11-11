from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_D, SpeedRPS, SpeedPercent, LargeMotor
from time import sleep


class movement:
    def canMoveForward(self, useUltrasonic = True):
        if useUltrasonic:
            return not (self.v.onBorder() or self.v.isColliding() or self.v.isCloseToColliding())
        else:
            return not (self.v.onBorder() or self.v.isColliding())
    
    
    """
    tries to rotate to the nearest border (which it is not currently on) in the given direction
    """
    def __findBorder(self, direction, rotations = 0):
        if rotations == 0 :
            rotations = 2 * self.one80Rotations
    
        colCheckFunc = self.u.checkTouchR
        if direction < 0:               
            self.u.mSpeak('left')       
            a = self.negSpeedPerc
            b = self.speedPerc                    
        elif direction > 0:
            self.u.mSpeak('right')
            a = self.speedPerc
            b = self.negSpeedPerc
            colCheckFunc = self.u.checkTouchL
            
        onBorder = True
        self.engine.on_for_rotations(a, b, rotations, block=False)        
        while not colCheckFunc() and self.engine.is_running and (not self.v.onBorder() or onBorder):
            if not self.v.onBorder():
                onBorder = False
            sleep(self.sensorInterval)
                
        self.engine.off(brake=True)
        
        if self.u.checkTouchR() or self.u.checkTouchL():
            self.u.mSpeak('Border not found!')
            return -1
        elif not self.v.onBorder() or onBorder: # if onBorder is True, the rotator never left the border it was already on...
            return 0
        return 1
        
        
    '''
    Tries to do a safe rotation, but assumes to be currently on a border
    
    Returns 1 if it succeeded, color sensor is guaranteed to be inside or on the border (there is one exception, see below)
    Returns 0  rotation failed: color sensor is guaranteed to be inside or on the border
    Returns -1 rotation failed: color sensor must be outside of border
    Returns -2 rotation failed: color sensor location status is unknown
    
    If the robot is situated in the corner, looking at the border the following will result in failure:
    the robot starts turning, looks inside the corner, looks at the border at the other side of the corner, and then rotates the sensor outside of the border.
    This is very difficult to detect compared to the case of moving past a straight edge, unless timing is used. 
    '''
    def __onBorderSafeRotate(self, direction, rotations):
        """
        Rotate to find a second border crossing within 180 degrees.
        If it is not found, the rotation is safe, return to desired rotation (The robot may be looking at the border after rotation)
        Else, rotation is unsafe if the desired amount of rotations is smaller than the rotations required to find the second border.
        """
        onBorder = True 
        sawTwoBorders = False
        colCheckFunc = self.u.checkTouchR
        a = 0
        b = 0
        
        if direction < 0:               
            self.u.mSpeak('left')       
            a = self.negSpeedPerc
            b = self.speedPerc                    
        elif direction > 0:
            self.u.mSpeak('right')
            a = self.speedPerc
            b = self.negSpeedPerc
            colCheckFunc = self.u.checkTouchL
            
        self.engine.on_for_rotations(a, b, rotations, block=False)        
        while (not colCheckFunc()) and self.engine.is_running:
                if not self.v.onBorder() :
                    onBorder = False
                elif not onBorder :
                    # Currently on border and onBorder has been False, so this is second border occurence
                    sawTwoBorders = True  
                    onBorder = True
                    
                sleep(self.sensorInterval)
                
        self.engine.off(brake=True)
        
        if self.u.checkTouchR() or self.u.checkTouchL():
            self.u.mSpeak('Could not rotate, collision!')
            if onBorder or sawTwoBorders:
                return 0
            else:
                if self.__findBorder(-direction):
                    return 0
                return -2 # rotating back into the direction we came from should work. If not, the environment has changed and we cannot react to that :(
            
        # Rotations was successful so far. If two borders were seen, then whole turn is successful. (If the robot never left the border, this is also fine)
        if sawTwoBorders or onBorder:
            return 1
        else:
            secondBorder = self.__findBorder(direction, self.one80Rotations - rotations)
                    
            if (self.u.checkTouchR() or self.u.checkTouchL()) or secondBorder == 1:
                # collission or second border was found, so we don't know our current rotation or whether the sensor is outside of the border or not...                
                # return to initial state
                if self.__findBorder(-direction) == 1:
                    return 0
                return -2 # This is only reached if an edge case occured or if the environment has changed during the rotations.
            elif secondBorder == -1:
                # error :(, bumped into something while looking for second border
                if self.__findBorder(-direction) == 1:
                    return 0
                return -2
            else :
                # initial turn was successful and no second border found, so the turn is valid
                return 1
        return -2 # should be unreachable
    
    
    """
    Returns 1 if it succeeded, color sensor is guaranteed to be inside or on the border
    Returns 0  rotation failed: color sensor is guaranteed to be inside or on the border
    Returns -1 rotation failed: color sensor must be outside of border
    Returns -2 rotation failed: color sensor location status is unknown
    """
    def __blindSafeRotate(self, direction, rotations):
        """
        Rotate to find either 0 or 2 crossings within the turning rotations.
        If 0 or 2 borders are found, the rotation is safe, return to desired rotation (The robot may be looking at the border after rotation)
        Else, rotation is unsafe.
        """
        onBorder = False 
        sawOneBorder = False
        sawTwoBorders = False
        colCheckFunc = self.u.checkTouchR
        a = 0
        b = 0
        
        if direction < 0:               
            self.u.mSpeak('left')       
            a = self.negSpeedPerc
            b = self.speedPerc                    
        elif direction > 0:
            self.u.mSpeak('right')
            a = self.speedPerc
            b = self.negSpeedPerc
            colCheckFunc = self.u.checkTouchL
            
        self.engine.on_for_rotations(a, b, rotations, block=False)        
        while (not colCheckFunc()) and self.engine.is_running:
                if not self.v.onBorder() :
                    onBorder = False
                else :
                    if not sawOneBorder:
                        sawOneBorder = True
                    elif not onBorder:
                        # Currently on border and onBorder has been False, so this is second border occurence
                        sawTwoBorders = True  
                        
                    onBorder = True
                    
                sleep(self.sensorInterval)
                
        self.engine.off(brake=True)
        
        if self.u.checkTouchR() or self.u.checkTouchL():
            self.u.mSpeak('Could not rotate, collision!')
            if onBorder or sawTwoBorders:
                return 0
            elif sawOneBorder:
                # Try to turn back to the previous border
                if self.__findBorder(-direction) == 1:
                    return 0
                return -2 # should be unreachable if the environment is static; moving back the way we came should succeed
            else:
                # Try to turn back to the previous border
                if self.__findBorder(-direction) == 1:
                    return 0
                return -1
            
        # Rotations was successful so far. If two borders were seen, then whole turn is successful. (If the robot never left the border, this is also fine)
        if sawTwoBorders or not sawOneBorder or onBorder:
            return 1
        elif sawOneBorder:
            #print("hello hello")
            secondBorder = self.__findBorder(direction, self.one80Rotations)
                        
            if secondBorder == -1:
                return -2 # error while looking for second border
            elif secondBorder == 1:
                # There is a second border further along, and the angle is less than 180 degrees, so the desired position is outside of the board
                # stay here on the border, but return failure
                return 0
            
            # No other borders found, so rotation was valid. Return to desired position and report success:
            if self.rotate(-direction, self.one80Rotations) and not self.v.onBorder(): # extra onBorder check to take care of rotation imperfections 
                return 1
            return 0               
        elif self.__findBorder(-direction) == 1: # crossed one border so turn is invalid. Return to previous border
            return 0 
        return -2
    
    """
    Tries to execute the rotation in a safe way. 
    rotations must be greater than 0. Assumes that the robot is currently in a valid position.
    The final rotation is at most 180 degrees
    
    @param rotations: if this is greater than half a turn, it may lead to the robot turning the other way.
    
    Returns 1 if it succeeded, color sensor is guaranteed to be inside or on the border (there is one exception, see below)
    Returns 0  rotation failed: color sensor is guaranteed to be inside or on the border
    Returns -1 rotation failed: color sensor must be outside of border
    Returns -2 rotation failed: color sensor location status is unknown
    
    If the robot is situated in the corner, looking at the border the following will result in failure:
    the robot starts turning, looks inside the corner, looks at the border at the other side of the corner, and then rotates the sensor outside of the border.
    This is very difficult to detect compared to the case of moving past a straight edge, unless timing is used. 
    """
    def safeRotate(self, direction, rotations):
        if rotations <= 0:
            return 0
        
        # First check if the rotations are expected to make the robot turn more than 180 degrees:
        rotations = rotations % (2 * self.one80Rotations) # strip full turns
        if rotations > self.one80Rotations:
            direction *= -1
            rotations %= self.one80Rotations
        
        if self.v.onBorder() :
            return self.__onBorderSafeRotate(direction, rotations)
        else :
            return self.__blindSafeRotate(direction, rotations)
    
    def forward(self, rotations):    
        if self.canMoveForward():
            self.engine.on_for_rotations(self.speedPerc, self.speedPerc, rotations, brake=True, block=False)    
             
        # counter to reduce the queries to the ultrasonic sensor 
        USCtr = 0
        while self.canMoveForward(USCtr == self.USInterval - 1) and self.engine.is_running :
            USCtr += 1
            USCtr %= self.USInterval
            sleep(self.sensorInterval)
            
        self.engine.off(brake=True)
        if not self.canMoveForward():
            self.u.mSpeak('Blocked!')
                        
    '''
    Tries to move backward, but does not guarantee that the robot stays within operational parameters.
    '''
    def backward(self, rotations):
        self.engine.on_for_rotations(self.negSpeedPerc, self.negSpeedPerc, rotations, block=True)
            
    '''
    use direction = 0 to do nothing, direction = -1 for left (counterclockwise) and direction = 1 for right (clockwise)
    '''
    def rotate(self, direction, rotations):
        colCheckFunc = self.u.checkTouchR       
        if direction < 0: 
            self.u.mSpeak('left')
            self.engine.on_for_rotations(self.negSpeedPerc, self.speedPerc, rotations, block=False)  
        elif direction > 0:
            self.u.mSpeak('right')
            self.engine.on_for_rotations(self.speedPerc, self.negSpeedPerc, rotations, block=False)
            colCheckFunc = self.u.checkTouchL
                
        while (not colCheckFunc()) and self.engine.is_running :
                sleep(self.sensorInterval)
        self.engine.off(brake=True)
                
        if self.u.checkTouchR() or self.u.checkTouchL():
            self.u.mSpeak('Could not rotate, collision!')
            return False
        
        return True
    
    
    def __init__(self, vitals, utils):
        self.v = vitals
        self.u = utils
        
        speed = 80
        self.speedPerc = SpeedPercent(speed) 
        self.negSpeedPerc = SpeedPercent(-speed) 
        self.sensorInterval = 0#0.001
        self.USInterval = 100
        
        # 1.125 is about the amount of wheel rotations to make a 180 degree turn
        self.one80Rotations = 1.125
        
        self.engine = MoveTank(OUTPUT_A, OUTPUT_D)
        self.left_motor = LargeMotor(OUTPUT_A)
        