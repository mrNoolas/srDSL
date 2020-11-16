package com.example.generator

import com.example.sRDSL.Direction
import com.example.sRDSL.Missions
import com.example.sRDSL.Move
import com.example.sRDSL.Movement
import java.util.ArrayList
import java.util.List

class Auxiliary {
	def static List<Direction> getDirections(Movement root) {
	 	var List<Direction> directionlist = new ArrayList<Direction>()
	 	for (Move m : root){
	 		directionlist.add(m.dir)
	 	}
	 	return actionlist;
	 }
} 