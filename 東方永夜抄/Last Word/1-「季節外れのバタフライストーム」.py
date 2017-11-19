# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
import math

RAD = math.pi / 180.0

vecList = []
objvertices("ico_tru1.obj", lambda v: vecList.append(v))

for vec in vecList:
	for axis in [Vector3.UnitX, Vector3.UnitZ]:
		axis = vec ^ (vec ^ axis)
		
		parent1 = Entity(world)
		parent1.Pos = vec * 20.0
		parent1()
		
		mat0 = Matrix3.RotationAxis(axis, RAD * 16)
		mat1 = Matrix3.RotationAxis(axis, RAD * 80)
		mat2 = Matrix3.RotationAxis(axis, RAD * -6)
		matList = [mat0, mat1, mat2, mat2]
		
		def shot_task_func0(task, parent1 = parent1, matList = matList):
			def shot_task_func1(task = task, parent1 = parent1, matList = matList):
				parent1.Pos = parent1.Pos * matList[0]
				matList[2] = matList[3] *  matList[2]
				
				shot = EntityShot(world, "S", 0xFFFFFF)
				shot.Pos = parent1.Pos
				shot.Velocity = +shot.Pos * 0.4
				shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 60)
				shot.LivingLimit = 60
				shot()
				
				def shot_task_func2(shot = shot, matList = matList):
					shot1 = EntityShot(world, "BUTTERFLY", 0xA0A000)
					shot1.Pos = shot.Pos
					shot1.Velocity = +shot.Pos * 1.6
					shot1.LivingLimit = 200
					shot1()
					
					shot1 = EntityShot(world, "BUTTERFLY", 0x00A000)
					shot1.Pos = shot.Pos
					shot1.Velocity = (+shot.Pos * 1.6) *matList[1]
					shot1.LivingLimit = 200
					shot1()
					
					if task.RunCount == 1:
						shot1 = EntityShot(world, "BUTTERFLY", 0x0000A0)
						shot1.Pos = shot.Pos
						shot1.Velocity = (+shot.Pos * 1.6) * (matList[1] ^ 2) * matList[2]
						shot1.LivingLimit = 200
						shot1()
			parent1.AddTask(shot_task_func1, 5, 12, 0)
		parent1.AddTask(shot_task_func0, 130, 2, 0, True)
		
		parent2 = Entity(world)
		parent2.Pos = vec * 20.0
		parent2()
		
		mat0 = Matrix3.RotationAxis(axis, RAD * 16)
		
		def shot_task_func3(task, parent2 = parent2, mat0 = mat0):
			def shot_task_func4(task = task, parent2 = parent2, mat0 = mat0):
				parent2.Pos = parent2.Pos * (mat0 if task.RunCount % 2 == 0 else ~mat0)
				
				shot = EntityShot(world, "BUTTERFLY", 0x0000A0 if task.RunCount % 2 == 0 else 0xA00000)
				shot.Pos = parent2.Pos
				shot.Velocity = +parent2.Pos * 4.5
				shot.LivingLimit = 100
				shot()
			parent2.AddTask(shot_task_func4, 2, 20, 0)
		parent2.AddTask(shot_task_func3, 40, 4, 90, True)
		