# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
from vectorutil import randomvec
from randomutil import random
import math

vecList = []
objvertices("ico_tru1.obj", lambda v: vecList.append(v))

num_clone = 25
pause_frame = 56
move_frame = 110
"""
owner_centerbone = EntityBone(WORLD, "Sakuya", u"センター")
owner_r_handbone = EntityBone(WORLD, "Sakuya", u"右手首")
owner_l_handbone = EntityBone(WORLD, "Sakuya", u"左手首")

targetbone = EntityBone(WORLD, "Reimu", u"センター")
"""

pauseList = []

def WORLD_task_func():
	target = Entity(WORLD)
	target.Pos = Vector3(100, 0, 50)
	target.Velocity = Vector3(-1, 1, 0)
	target.LivingLimit = 120
	target()
	
	cloneList = []
	
	def shot_knife1(way = 5):
		vec = randomvec()
		mat = Matrix3.RotationAxis(vec ^ (vec ^ randomvec()), RAD * 20)
		vec = vec * (mat ^ 2)
		mat = ~mat
		
		for i in range(way):
			for j in range(2):
				shot = EntityShot(WORLD, KNIFE, 0xFFD700)
				shot.Velocity = vec * (1 + j * 0.5)
				shot.Pos = shot.Velocity
				shot.LivingLimit = 600
				shot()
				
				pauseList.append(shot)
			vec = vec * mat
	WORLD.AddTask(shot_knife1, 0, 1, 10)
	
	def shot_knife2(angle, axis):
		for vec in vecList:
			vec = vec
			mat = Matrix3.RotationAxis(vec ^ (vec ^ axis), angle)
			
			shot = EntityShot(WORLD, KNIFE, 0x0000A0)
			shot.Velocity = vec * 4.0
			shot.Pos = shot.Velocity
			shot.LivingLimit = 200
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 30)
			
			def shot_task_func(shot = shot, mat = mat):
				shot.Velocity = shot.Velocity * mat * 0.5
			shot.AddTask(shot_task_func, 0, 1, 30)
			shot()
			
			cloneList.append(shot)
			pauseList.append(shot)
	WORLD.AddTask(lambda: shot_knife2(RAD * 60, Vector3.UnitZ), 0, 1, 0)
	WORLD.AddTask(lambda: shot_knife2(-RAD * 60, Vector3.UnitZ), 0, 1, 5)
	
	def shot_knife3():
		shot = EntityShot(WORLD, KNIFE, 0x0000A0)
		shot.Velocity = +target.WorldPos * 2.0
		shot.Pos = shot.Velocity * 4
		shot.LivingLimit = 200
		shot()
		
		cloneList.append(shot)
		pauseList.append(shot)
	WORLD.AddTask(shot_knife3, 3, 12, 10)

	get_waiting_frame = lambda frame = WORLD.FrameCount + move_frame: frame - WORLD.FrameCount
	
	def pause():
		for shot in pauseList:
			shot.Velocity = Vector3.Zero

			def move(shot = shot):
				shot.Velocity = shot.LookAtVec
			shot.AddTask(move, 0, 1, get_waiting_frame())
	WORLD.AddTask(pause, 0, 1, pause_frame)
	
	def clone(task):
		for src in cloneList:
			interval = +src.LookAtVec * 16

			shot = EntityShot(WORLD, KNIFE, 0xA0A0A0)
			shot.LookAtVec = src.LookAtVec
			shot.Pos = src.Pos + interval * (-num_clone / 3 + task.RunCount)
			shot.LivingLimit = 120

			def move(shot = shot):
				shot.Velocity = +shot.LookAtVec * 8.0
			shot.AddTask(move, 0, 1, get_waiting_frame())
			shot()
	WORLD.AddTask(clone, 0, num_clone, 60, True)
WORLD.AddTask(WORLD_task_func, 120, 2, 0)
