# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
import math
way = 3
num_divide = 5

shotDict = {}
for i in range(num_divide):
	shotDict[i] = []
	
def shot_func(pos, vec, level):
	shot = EntityShot(WORLD, "M", 0x0000A0)
	shot.Pos = pos
	shot.Velocity = vec * 8
	shot()
	
	laser = EntityShot(WORLD, "LASER_LINE", 0x0000A0)
	if laser.ModelData.OwnerEntities.Count == 1:
		for vert in laser.ModelData.Vertices:
			vert.Pos = Vector3(vert.Pos.x * 2, vert.Pos.y * 2, vert.Pos.z * 4000) 
	
	laser.Pos = pos
	laser.Recording = Recording.LocalMat
	laser.Rot = Matrix3.LookAt(vec, Vector3.UnitY)
	
	morph = laser.CreateVertexMorph("V_" + laser.MaterialMorph.MorphName, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
	laser.AddMorphKeyFrame(morph, 0, 1)
	laser.AddMorphKeyFrame(morph, 29, 1)
	laser.AddMorphKeyFrame(morph, 30, 0)
	laser.AddMorphKeyFrame(morph, 80, 0)
	
	laser.LivingLimit = 80
	laser()
	
	if level < num_divide:
		def shot_task_func():
			mat1 = Matrix3.RotationAxis(+(vec ^ Vector3.UnitY), RAD * 60)
			mat2 = Matrix3.RotationAxis(vec, RAD * (360 / way))
			shotVec = vec * mat1
			
			for i in range(way):
				shot_func(shot.Pos, +shotVec, level + 1)
				shotVec = shotVec * mat2
		shot.AddTask(shot_task_func, 0, 1, 6)
		shot.LivingLimit = 7
shot_func(Vector3.Zero, -Vector3.UnitZ, 0)
