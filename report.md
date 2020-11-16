# DSL assignment 1
Gerhard van der Knijff s1006946, David Vonk s4681533

## Code overview
In the runtime models we made as much code as possible handled by static files. This means that the DSL essentially generates a configuration file, which is then used by the code to perform the necessary actions.

The DSL generates missionList.py which contains the missions to be performed. 
The missionlist contains one or more missions. Each mission consists of one or more movements.
Each movement is a combination of some moves and a set of conditions. 

During execution a move is done; as soon as the move is finished, the conditions are checked. If they are not met, the next move of the movement is done, until either all moves were performed, or the condition was met.

All the movements and missions are carried out in order.


### Other code files
The movementController has all the higher-level code for physical movements of the rover. It constantly verifies whether the rover is in a valid position, and whether the rover is looking at a border or not.

The utils and vitals files handle some basic functionality that is used by other files. For example sounds and sensor readings are handled here.

execMovements and checkConditions are iterated based on the current movement and its condition. They execute the function calls as specified in the missionList. 


## DSL overview
The DSL is specified in such a way that it adheres closely to natural language. We chose to keep the current possibilities for the rover limited, as this allows for easier implementation. THe current languege nonetheless gives quite some expressiveness for the rover.

### Unfinished
We had some trouble with defining commands that do not have parameters. We have a move forward option that should run infinitely (until the condition is met) and a move forward for a set distance. We could not get the infinite version to work properly with our current code. 

We do have some ideas on what we could try, but after spending many hours our time has unfortunately run out.
