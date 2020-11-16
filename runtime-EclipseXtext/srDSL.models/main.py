from utils import utils
from vitals import vitals
from movementController import movementController
from threading import Thread
from missionsList import missionsList
from execMovements import execMovements
from checkConditions import checkConditions
from DSLFunctions import DSLFunctions
from time import sleep

def main():
    u = utils()
    v = vitals(u)
    m = movementController(u, v)
    f = DSLFunctions(m, u)

    missions = missionsList(f).getMissionSet()
    for mission in missions:
        for movement in missions[mission]:
            behaviors = [execMovements(movement["moves"]), checkConditions(movement["conditions"])]
            Thread(target=scheduler, args=(behaviors)).start()
            Thread(target=runner, args=(behaviors)).start()
    print("Shutting down...")
    return 0
        
def scheduler(behaviors):
    activeBehavior = 0 #Standard = movementController
    highest = 0 #Standard = movementController
    behaviors[highest].active = True
    while not behaviors[1].isDone: 
        #print("MASTER: Current running behavior " + str(activeBehavior))
        #print("Colors to be checked:")
        #print(behaviors[1].colorsToFind)
        for i in range(len(behaviors)-1, -1, -1):
            if i > activeBehavior:
                if behaviors[i].takeControl() and behaviors[activeBehavior].active:
                    print("MASTER: Behavior " + str(i) + " wants to take control!")
                    print("MASTER: Suppressing behavior " + str(activeBehavior))
                    behaviors[activeBehavior].suppress()
                    print("MASTER: Starting behavior " + str(i))
                    behaviors[i].suppressed = False
                    behaviors[i].active = True
                    activeBehavior = i
            elif not behaviors[activeBehavior].active:
                #No behavior is running, thus the highest can be started. 
                if behaviors[i].takeControl():
                    print("MASTER: Starting behavior " + str(i))
                    behaviors[i].suppressed = False
                    behaviors[i].active = True
                    activeBehavior = i
        sleep(0.1)
                    
def runner(behaviors):
    while not behaviors[1].isDone:
        for i in range(len(behaviors)-1, -1, -1): 
            if behaviors[i].active:
                #print("MASTER: Thread runs behavior " + str(i))
                behaviors[i].action();
    
main()
