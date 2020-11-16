#movementsList.py

class missionsList:
    def getMissionSet(self): 
        return {
            "missionName": [
                { # movement, consists of multiple moves with stop-conditions
                    # moves calls [multiple [movementController function, {with arguments}, loops]]
                    "moves": [[self.f.forwardForMove, {"distance": 1, "unit": "rotations"}, False]], 
                    "conditions": [[self.f.colorCondition, {"shouldFind": [4]}]]
                },
                {
                    "moves": [
                        [self.f.rightForMove, {"angle": 0.5, "unit": "rotations"}, False], 
                        [self.f.randomStep, {}, True]
                    ],
                    "conditions": [[self.f.colorCondition, {"shouldFind": [4]}]]
                }
            ]
        }
    
    def __init__(self, dslFunctions):
        self.f = dslFunctions
        