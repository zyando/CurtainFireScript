# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *

from VecMath import *
from vectorutil import *
from randomutil import uniform, random
import math

world.ModelName = u"神技「八方鬼縛陣」"

RAD = math.pi / 180.0

def create_veclist(path):
	veclist = []
	openobj(path, lambda v: veclist.append(+v))
	return veclist
vectors_dict = {path[0:-4] : create_veclist(path) for path in ["ico.obj", "ico_y.obj", "ico_tru1.obj", "ico_tru2.obj", "dod.obj", "ico_dod.obj", "snub_cube.obj"]}

def shot_omnidirectinal():
	for vec in vectors_dict["ico"]:
		shot = EntityShot(world, "AMULET", 0xA00000)
		shot.Velocity = vec * 4
		shot.LivingLimit = 150
		
		mat = Matrix3(1, 0, 0, 0, 0, 1, 0, 1, 0) * Matrix3.LookAt(+vec, Vector3.UnitY)
		
		def divide(src = shot, src_vec = vec, mat = mat):
			for vec in vectors_dict["ico_y"]:
				vec = vec * mat
				dot = vec * src_vec
				
				if -0.99 < dot and dot < 0.99:
					shot = EntityShot(world, "AMULET", 0xA00000 if 0 < dot else 0xFFD700)
					shot.Pos = src.Pos
					shot.Velocity = vec * 4
					shot.Upward = src_vec
					shot.LivingLimit = 150
					shot()
		shot.AddTask(divide, 0, 1, 30)
		shot()
world.AddTask(shot_omnidirectinal, 5, 60, 0)

def shot_every_directinal():
	def shot_s(task):
		mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 20)
		
		for vec in vectors_dict["ico_tru2"]:
			vec  = vec * mat
			shot = EntityShot(world, "S", 0xFFFFFF)
			shot.Velocity = vec * (3 - task.RunCount * 0.15) 
			shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 30)
			shot.LivingLimit = 40
			
			def stop(shot = shot, vec = vec): shot.Velocity *= 0
			shot.AddTask(stop, 0, 1, 30)
			
			def shot_red_scale(src = shot, vec = vec):
				shot = EntityShot(world, "SCALE", 0xA00000)
				shot.Pos = src.Pos
				shot.LookAtVec = vec
				shot.LivingLimit = 200
				
				def move(shot = shot): shot.Velocity = vec * 2
				shot.AddTask(move, 0, 1, 20)
				
				shot()
			shot.AddTask(shot_red_scale, 0, 1, 40)
			shot()
	world.AddTask(shot_s, 3, 5, 0, True)
world.AddTask(shot_every_directinal, 60, 3, 60)