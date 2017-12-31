# -*- coding: utf-8 -*-
from random import random, randint

vecList = []
objvertices("ico.obj", lambda v: vecList.append(+v), 1)

def shot_M():
	for v in vecList:
		shot = EntityShot(WORLD, M, 0xFFFFFF)
		shot.Pos = OWNER_BONE.WorldPos + v * 12.0
		shot.Velocity = v * 2.0
		shot()
WORLD.AddTask(shot_M, 30, 10, 10)

def world_task1(task):
	entity = Entity(WORLD)
	entity.Pos = randomvec()
	
	upward = entity.Pos ^ (entity.Pos ^ randomvec())
	mat = Matrix3.RotationAxis(upward, RAD * (20.0 + random() * 20.0))
	
	def world_task2(upward = upward, mat = mat):
		shot_amulet(entity.Pos, upward)
		entity.Pos = entity.Pos * mat
	WORLD.AddTask(world_task2, randint(1, 5), 8, 0)
	
	task.Interval -= randint(4, 8)
WORLD.AddTask(world_task1, 90, 5, 10, True)

def shot_amulet(vec, upward):
	mat = Matrix3.RotationAxis(vec ^ (vec ^ Vector3.UnitY), RAD * (4.0 + random() * 6.0))
	vecList = [vec * mat, vec, vec * ~mat]
	upwardList = [upward * mat, upward, upward * mat]
	
	def shot_func1(original):
		shot = EntityShot(WORLD, AMULET, 0xFF00FF)
		shot.Pos = original.Pos
		shot.Velocity = +(TARGET_BONE.WorldPos - shot.Pos) * 2.0
		shot.Upward = original.Upward
		shot()
	
	def shot_func2(original):
		shot = EntityShot(WORLD, S, 0xFF00FF)
		shot.Pos = original.Pos
		shot.Upward = original.Upward
		shot.AddTask(lambda s = shot :shot_func1(s) , 0, 1, 19)
		shot.LivingLimit = 20
		shot()
	
	def shot_func3(original):
		shot = EntityShot(WORLD, AMULET, 0xFF0000)
		shot.Pos = original.Pos
		shot.Velocity = (TARGET_BONE.WorldPos - shot.Pos) * 0.02
		shot.Upward = original.Upward
		shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 40)
		shot.AddTask(lambda s = shot :shot_func2(s) , 0, 1, 39)
		shot.LivingLimit = 40
		shot()
	
	def shot_func4(original):
		shot = EntityShot(WORLD, S, 0xFF0000)
		shot.Pos = original.Pos
		shot.Upward = original.Upward
		shot.AddTask(lambda s = shot :shot_func3(s) , 0, 1, 19)
		shot.LivingLimit = 20
		shot()
	
	for i in range(len(vecList)):
		for j in range(16):
			shot = EntityShot(WORLD, AMULET, 0xFFFFFF)
			shot.Pos = OWNER_BONE.WorldPos
			shot.Velocity = vecList[i] * (0.25 * j + 1) * 2
			shot.Upward = upwardList[i]
			shot.AddTask(lambda s = shot :shot_func4(s) , 0, 1, 39)
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 40)
			shot.LivingLimit = 40
			shot()
