#movementsList.py

class missionsList:
    def getMissionSet(self): 
        return {
            "missionName": {
                { # movement, consists of multiple moves with stop-conditions
                    # moves calls [multiple [movement function, {with arguments}]]
                    "moves": [[self.f.forwardMove, {"distance": 2, "unit": "rotations"}]], 
                    "conditions": {self.f.colorCondition, {"shouldFind": [1]}}
                },
                {
                    "moves": [
                        [self.f.rightForMove, {"angle": 0.5, "unit": "rotations"}], 
                        [self.f.randomWalk, {}]
                    ]
                }
            }
        }
    
    def __init__(self, dslFunctions):
        self.f = dslFunctions
        