package com.example.generator

import com.example.sRDSL.ColorCondition
import com.example.sRDSL.ForwardForMove
import com.example.sRDSL.Missions
import com.example.sRDSL.RightForMove

class PythonGenerator {
	def static toPython(Missions root)'''
		#movementsList.py
		class missionsList:
		    def getMissionSet(self): 
		        return {
		        «listMissions(root)»
		        }
		    
		    def __init__(self, dslFunctions):
		        self.f = dslFunctions'''
       
      def static listMissions(Missions root)'''
      	«FOR mission: root.missions »
      	"«mission.name»": [
            «FOR movement : mission.movement_sequence»
                {
                    "moves":[[
                    	«FOR move : movement.movement»
							«move2Code(move.dir)»
                    	«ENDFOR» 
                    	]]
                    "conditions": [[
                    	«FOR condition : movement.conditions»
                    		«condition2Code(condition)»
                    	«ENDFOR»
                    self.f.colorCondition, {"shouldFind": [1]}
                    ]]
                },
                
            «ENDFOR»
            ]
      	«ENDFOR»'''
      	
	def static dispatch move2Code(ForwardForMove move)'''
 		self.f.forwardForMove, {"distance": "«move.distance»", "unit": "rotations"},'''
 		
 	def static dispatch move2Code(RightForMove move)'''
 		self.f.rightForMove, {"angle": "«move.degrees»", "unit": "«IF move.degrees != 0»degrees«ELSE»rotations«ENDIF»"},'''
 		
 	def static dispatch move2Code(RandomMove move)'''
 		self.f.randomWalk, {},'''
 		
 	def static dispatch condition2Code(ColorCondition colorCond)'''
 		self.f.colorCondition, {"shouldFind": [«IF colorCond.color == "BLACK"»1«ENDIF»]}'''
}