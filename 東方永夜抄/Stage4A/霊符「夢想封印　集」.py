# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
from vectorutil import *
from randomutil import random, randint
import math

TARGET = Vector3(0, 0, 100)

vecList = []
objvertices("ico.obj", lambda v: vecList.append(v))

def shot_M():
	for v in vecList:
		shot = EntityShot(WORLD, M, 0xFFFFFF)
		shot.Pos = v * 12.0
		shot.Velocity = v * 2.0
		shot()
WORLD.AddTask(shot_M, 30, 10, 10)

def WORLD_task_func2():
	entity = Entity(WORLD)
	entity.Pos = randomvec()
	entity.Upward = entity.Pos ^ (entity.Pos ^ randomvec())
	
	mat = Matrix3.RotationAxis(entity.Upward, RAD * (20.0 + random() * 20.0))
	
	def WORLD_task_func3(mat = mat):
		shot_amulet(entity.Pos, entity.Upward)
		entity.Pos = entity.Pos * mat
	WORLD.AddTask(WORLD_task_func3, randint(2, 8), 8, 0)
WORLD.AddTask(WORLD_task_func2, 90, 5, 10)

def shot_amulet(vec, upward):
	mat = Matrix3.RotationAxis(vec ^ (vec ^ Vector3.UnitY), RAD * (4.0 + random() * 6.0))
	vecList = [vec * mat, vec, vec * ~mat]
	upwardList = [upward * mat, upward, upward * mat]
	
	def shot_func1(original):
		shot = EntityShot(WORLD, AMULET, 0xFF00FF)
		shot.Pos = original.Pos
		shot.Velocity = +(TARGET - shot.Pos) * 2.0
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
		shot.Velocity = (TARGET - shot.Pos) * 0.02
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
		for j in range(12):
			shot = EntityShot(WORLD, AMULET, 0xFFFFFF)
			shot.Velocity = vecList[i] * (0.25 * j + 1)
			shot.Upward = upwardList[i]
			shot.AddTask(lambda s = shot :shot_func4(s) , 0, 1, 39)
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 40)
			shot.LivingLimit = 40
			shot()
