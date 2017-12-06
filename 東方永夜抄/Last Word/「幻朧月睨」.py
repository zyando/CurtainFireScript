# -*- coding: utf-8 -*-
from random import random

vecList = []
objvertices("ico.obj", lambda v: vecList.append(v), 1)

posList = [Vector3(40, 0, 0), Vector3(0, 40, 20)]

def world_task():
	posStack = posList[:]
	
	def shot_m_task():
		pos = posStack.pop()
		mat = Matrix3.RotationAxis(randomvec(), RAD * 180 * random())
		
		def shot_m(task):
			for vec in vecList:
				vec = vec * mat
				
				shot = EntityShot(WORLD, M, 0x0000A0)
				shot.Pos = vec * task.RunCount * 20 + pos
				shot.LivingLimit = 90
				shot()
				
				def move(shot = shot, vec = vec):
					newShot = EntityShot(WORLD, M, 0xA00000)
					newShot.Pos = shot.Pos
					newShot.Velocity = vec * 2.4
					newShot()
				shot.AddTask(move, 0, 1, shot.LivingLimit)
		WORLD.AddTask(shot_m, 2, 12, 30, True)
		
		def shot_bullet(prop, speed, limit):
			mat = Matrix3.RotationAxis(randomvec(), RAD * 180 * random())
			
			for vec in vecList:
				vec = vec * mat
				
				shot = EntityShot(WORLD, prop)
				shot.Velocity = vec * speed
				shot.LivingLimit = limit
				shot()
		WORLD.AddTask(lambda: shot_bullet(ShotProperty(BULLET, 0xA00000), 4.8, 30), 0, 1, 30)
		WORLD.AddTask(lambda: shot_bullet(ShotProperty(BULLET, 0x0000A0), 4.5, 30), 0, 1, 30)
		WORLD.AddTask(lambda: shot_bullet(ShotProperty(BULLET, 0xA00000), 4.5, 28), 0, 1, 32)
		WORLD.AddTask(lambda: shot_bullet(ShotProperty(BULLET, 0x0000A0), 4.2, 28), 0, 1, 32)
		WORLD.AddTask(lambda: shot_bullet(ShotProperty(BULLET, 0xA00000), 4.2, 24), 0, 1, 36)
	WORLD.AddTask(shot_m_task, 90, 2, 0)
WORLD.AddTask(world_task, 0, 1, 0)