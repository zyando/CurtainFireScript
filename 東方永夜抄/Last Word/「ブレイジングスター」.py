# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
from vectorutil import *
from randomutil import *
import math

num_shot = 80
interval = 5

veclist = []
objvertices("ico_tru1.obj", lambda v: veclist.append(v))

#bone = EntityBone(WORLD, "Marisa", u"センター")

def WORLD_task(task):
	mat = Matrix3.RotationAxis(randomvec(), RAD * 180 * random())
	
	for vec in veclist:
		shot = EntityShot(WORLD, "STAR_M", 0xA00000 if task.RunCount % 2 == 0 else 0x0000A0)
		shot.Pos = bone.WorldPos
		shot.Velocity = vec * 1.2 * mat
		shot.SetMotionInterpolationCurve(Vector2(0.1, 0.9), Vector2(0.1, 0.9), 60)
		
		def bezier(shot = shot):
			shot.SetMotionInterpolationCurve(Vector2(0.8, 0.2), Vector2(0.8, 0.2), 60)
		shot.AddTask(bezier, 0, 1, 60)
		
		def move(shot = shot):
			shot.Velocity *= 3.4
		shot.AddTask(move, 0, 1, 120)
		shot()
WORLD.AddTask(WORLD_task, 3, 8, 325, True)
WORLD.AddTask(WORLD_task, 3, 10, 388, True)
WORLD.AddTask(WORLD_task, 1, 8, 447, True)
WORLD.AddTask(WORLD_task, 3, 10, 480, True)
WORLD.AddTask(WORLD_task, 3, 8, 510, True)
