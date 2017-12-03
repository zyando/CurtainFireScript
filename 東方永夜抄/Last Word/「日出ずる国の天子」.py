# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
import math

target = Vector3(0, 0, 80)

wayVerti = 10
wayHoriz = 20

matVerti = Matrix3.RotationAxis(Vector3.UnitX, RAD * (180 / (wayVerti + 2)))
matHoriz = Matrix3.RotationAxis(Vector3.UnitY, RAD * (360 / wayHoriz))

vecList1 = []
vecList2 = []
vec1 = Vector3(0, -1, 0)

for i in range(wayVerti):
	vec1 = vec1 * matVerti
	vecList2.append(vec1)

for i in range(wayHoriz):
	vecList2 = map(lambda v: v * matHoriz, vecList2)
	vecList1.append(vecList2)

def WORLD_task_func1():
	vecStack = vecList1[:]
	
	def WORLD_task_func2():
		vecList2 = vecStack.pop()
		
		for vec in vecList2:
			shot = EntityShot(WORLD, LASER_LINE, 0x0000A0)
			
			if shot.ModelData.OwnerEntities.Count == 1:
				for vert in shot.ModelData.Vertices:
					vert.Pos = Vector3(vert.Pos.x * 1, vert.Pos.y * 1, vert.Pos.z * 4000)
			
			morph = shot.CreateVertexMorph("V_" + shot.MaterialMorph.MorphName, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
			shot.AddMorphKeyFrame(morph, 0, 1)
			shot.AddMorphKeyFrame(morph, 59, 1)
			shot.AddMorphKeyFrame(morph, 60, 0)
			shot.AddMorphKeyFrame(morph, 120, 0)
			
			shot.Recording = Recording.LocalMat
			shot.Rot = Matrix3.LookAt(vec, Vector3.UnitY)
			
			shot.LivingLimit = 120
			shot()
	WORLD.AddTask(WORLD_task_func2, 2, wayHoriz, 0)
WORLD.AddTask(WORLD_task_func1, 200, 2, 0)

def WORLD_task_func3():
	mat = Matrix3.RotationAxis(Vector3.UnitY, RAD * 180 / wayHoriz)
	vecStack = vecList1[:]
	vecStack.reverse()
	
	def WORLD_task_func4():
		vecList2 = vecStack.pop()
		
		for vec in vecList2:
			vec = vec * mat
			
			shot = EntityShot(WORLD, "LASER_LINE", 0xA00000)
			
			if shot.ModelData.OwnerEntities.Count == 1:
				for vert in shot.ModelData.Vertices:
					vert.Pos = Vector3(vert.Pos.x * 1, vert.Pos.y * 1, vert.Pos.z * 4000)
			
			morph = shot.CreateVertexMorph("V_" + shot.MaterialMorph.MorphName, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
			shot.AddMorphKeyFrame(morph, 0, 1)
			shot.AddMorphKeyFrame(morph, 59, 1)
			shot.AddMorphKeyFrame(morph, 60, 0)
			shot.AddMorphKeyFrame(morph, 120, 0)
			
			shot.Recording = Recording.LocalMat
			shot.Rot = Matrix3.LookAt(vec, Vector3.UnitY)
			
			shot.LivingLimit = 120
			shot()
	WORLD.AddTask(WORLD_task_func4, 2, wayHoriz, 0)
WORLD.AddTask(WORLD_task_func3, 200, 2, 40)

vecList3 = [+Vector3(-1, 1, 1), +Vector3(1, 1, -1), +Vector3(1, -1, 1), +Vector3(-1, -1, -1)]

for vec in vecList3:
	posList = [Vector3(40, 20, 0), Vector3(-40, 20, 0)]
	rot = Quaternion.RotationAxis(vec ^ (vec ^ Vector3.UnitY), RAD * 30)
	rotList = [rot, ~rot]
	
	for i in range(len(posList)):
		pos = posList[i]
		quat = rotList[i]
		
		parentShot1 = EntityShot(WORLD, BONE, 0xFFFFFF)
		parentShot1.Pos = pos
		parentShot1.Recording = Recording.LocalMat
		parentShot1()
		
		parentShot2 = EntityShot(WORLD, MAGIC_CIRCLE, 0xFFFFFF, parentShot1)
		parentShot2.Recording = Recording.LocalMat
		parentShot2.Pos = vec * 12
		parentShot2.Rot = Quaternion.RotationAxis(Vector3.UnitZ ^ vec, math.acos(vec.z))
		parentShot2()
		
		def shot_task_func1(parentShot1 = parentShot1, parentShot2 = parentShot2, quat = quat):
			parentShot1.Rot *= quat
			
			shot = EntityShot(WORLD, S, 0x0000A0)
			shot.Velocity = +(parentShot2.WorldPos - parentShot1.WorldPos) * -1.0
			shot.Pos = parentShot2.WorldPos
			shot()
			
			shot = EntityShot(WORLD, S, 0xA00000)
			shot.Velocity = +(target - parentShot2.WorldPos) * 1.0
			shot.Pos = parentShot2.WorldPos
			shot()
		parentShot1.AddTask(shot_task_func1, 20, 12, 0)

