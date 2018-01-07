# -*- coding: utf-8 -*-
from random import uniform, random

def create_veclist(path):
	veclist = []
	objvertices(path[0] + ".obj", lambda v: veclist.append(+v), path[1])
	return veclist
pathlist =  [("ico", 0), ("ico", 2), ("ico_y", 0)]
vectors_dict = {path[0] + str(path[1]) : create_veclist(path) for path in pathlist}

def shot_omnidirectinal():
	for vec in vectors_dict["ico0"]:
		shot = EntityShot(WORLD, "AMULET", 0xA00000)
		shot.Pos = OWNER_BONE.WorldPos
		shot.Velocity = vec * 6
		shot.Pos = +shot.Velocity * 20
		shot.LivingLimit = 130
		
		mat = Matrix3(1, 0, 0, 0, 0, 1, 0, 1, 0) * Matrix3.LookAt(+vec, Vector3.UnitY)
		
		def divide(src = shot, src_vec = vec, mat = mat):
			for vec in vectors_dict["ico_y0"]:
				vec = vec * mat
				dot = vec * src_vec
				
				if -0.99 < dot and dot < 0.99:
					shot = EntityShot(WORLD, "AMULET", 0xA00000 if 0 < dot else 0xFFD700)
					shot.Pos = src.Pos
					shot.Velocity = vec * 6
					shot.Upward = src_vec
					shot.LivingLimit = 80
					shot()
		shot.AddTask(divide, 0, 1, 50)
		shot()
WORLD.AddTask(shot_omnidirectinal, 2, 100, 0)

def shot_every_directinal():
	def shot_s(task):
		mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 20)
		
		for vec in vectors_dict["ico2"]:
			vec  = vec * mat
			shot = EntityShot(WORLD, "S", 0xFFFFFF)
			shot.Velocity = vec * (12 - task.RunCount * 0.6) 
			shot.Pos = OWNER_BONE.WorldPos + +shot.Velocity * 10
			shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 30)
			shot.LivingLimit = 40
			
			def stop(shot = shot, vec = vec): shot.Velocity *= 0
			shot.AddTask(stop, 0, 1, 30)
			
			def shot_red_scale(src = shot, vec = vec):
				shot = EntityShot(WORLD, "SCALE", 0xA00000)
				shot.Pos = src.Pos
				shot.LookAtVec = vec
				shot.LivingLimit = 100
				
				def move(shot = shot): shot.Velocity = vec * 6
				shot.AddTask(move, 0, 1, 20)
				
				shot()
			shot.AddTask(shot_red_scale, 0, 1, 40)
			shot()
	WORLD.AddTask(shot_s, 3, 5, 0, True)
WORLD.AddTask(shot_every_directinal, 60, 4, 60)