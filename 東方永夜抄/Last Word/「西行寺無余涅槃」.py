# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
import math

def create_veclist(path):
	veclist = []
	objvertices(path, lambda v: veclist.append(+v))
vectors_list = [create_veclist(path) for path in ["ico.obj", "ico_tru1.obj", "dod.obj", "ico_dod.obj", "snub_cube.obj"]]

def WORLD_task():
	def shot_laser():
		for vec in vectors_list[1]:
			flag = vec in vectors_list[0]
			shot = EntityShot(WORLD, LASER, 0xA000A0 if flag else 0x0000A0)
			
			if shot.ModelData.OwnerEntities.Count == 1:
				for vert in shot.ModelData.Vertices:
					vert.Pos = Vector3(vert.Pos.x * 80, vert.Pos.y * 80, -vert.Pos.z * 800 - 24)
			
			morph = shot.CreateVertexMorph("V_" + shot.MaterialMorph.MorphName, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
			shot.AddMorphKeyFrame(morph, 0, 1)
			shot.AddMorphKeyFrame(morph, 69, 1)
			shot.AddMorphKeyFrame(morph, 70, 0)
			shot.AddMorphKeyFrame(morph, 180, 0)
			shot.AddMorphKeyFrame(morph, 200, 1)
			shot.LivingLimit = 200
			
			shot.Recording = Recording.LocalMat
			
			rot = Matrix3.LookAt(vec, Vector3.UnitY)
			shot.Rot = rot * Matrix3.RotationAxis(vec ^ (vec ^ Vector3.UnitY), RAD * (170 if flag else -170))
			def set_rotation(shot = shot, rot = rot):
				shot.Rot = rot
			shot.AddTask(set_rotation, 0, 1, 50)
			shot()
	#WORLD.AddTask(shot_laser, 200, 2, 0)
	
	def shot_l():
		for vec in vectors_list[0]:
			shot = EntityShot(WORLD, L, 0xFF4040)
			shot.Velocity = vec * 0.8
			shot.Pos = +shot.Velocity * 20
			shot.LivingLimit = 400
			
			def divide_shot(shot = shot):
				for i in range(3):
					newShot = EntityShot(WORLD, shot.Property)
					newShot.Velocity = shot.Velocity * (1 + i) * 1.5
					newShot.Pos = shot.Pos
					newShot.LivingLimit = 200
					newShot()
			shot.AddTask(divide_shot, 0, 1, 40)
			shot()
	#WORLD.AddTask(shot_l, 0, 1, 200)
	
	def shot_butterfly_gb():
		for vec in vectors_list[2] + vectors_list[3] + vectors_list[4]:
			flag = vec in vectors_list[3]
			
			for i in range(3 if flag else 2):
				shot = EntityShot(WORLD, BUTTERFLY, 0x0000A0 if flag else 0xA000A0)
				shot.Velocity = vec * (0.4 + i * 0.2)
				shot.Pos = +shot.Velocity * 20
				shot.LivingLimit = 400 - i * 50
				
				def divide_shot(shot = shot):
					for i in range(3):
						newShot = EntityShot(WORLD, shot.Property)
						newShot.Velocity = shot.Velocity * -(1 + i * 0.2)
						newShot.Pos = shot.WorldPos
						newShot.SetMotionInterpolationCurve(Vector2(0.6, 0.0), Vector2(0.0, 0.45), 300)
						newShot.LivingLimit = 300
						newShot()
					
					for i in range(3):
						newShot = EntityShot(WORLD, shot.Property)
						newShot.Velocity = shot.Velocity * (1 + i) * 1.4
						newShot.Pos = shot.WorldPos
						newShot.LivingLimit = 300
						newShot()
				shot.AddTask(divide_shot, 0, 1, 60 - i * 5)
				shot()
	#WORLD.AddTask(shot_butterfly_gb, 0, 1, 0)
	
	def shot_butterfly_r(task):
		parentShot = EntityShot(WORLD, BONE, 0xFFFFFF)
		parentShot.Recording = Recording.LocalMat
		quat = Quaternion.RotationAxis(Vector3.UnitY, RAD * 48  * (1 if task.RunCount % 2 == 0 else -1))
		
		def rotate():
			parentShot.Rot *= quat
		parentShot.AddTask(rotate, 0, 1, 120)
		parentShot()
		
		for vec in vectors_list[2] + vectors_list[4]:
			for i in range(2):
				shot = EntityShot(WORLD, BUTTERFLY, 0xA00000, parentShot)
				shot.Velocity = vec * (0.4 + i * 0.2)
				shot.Pos = +shot.Velocity * 20
				
				def divide_shot(shot = shot):
					shotVec = shot.Velocity *  shot.ParentEntity.Rot
					
					for i in range(3):
						newShot = EntityShot(WORLD, shot.Property)
						newShot.Velocity = shotVec * -(1 + i * 0.2)
						newShot.Pos = shot.WorldPos
						newShot.SetMotionInterpolationCurve(Vector2(0.6, 0.0), Vector2(0.0, 0.45), 300)
						newShot.LivingLimit = 200
						newShot()
					
					for i in range(3):
						newShot = EntityShot(WORLD, shot.Property)
						newShot.Velocity = shotVec * (1 + i) * 1.2
						newShot.Pos = shot.WorldPos
						newShot.LivingLimit = 200
						newShot()
				shot.AddTask(divide_shot, 0, 1, 120 - i * 5)
				shot.LivingLimit = 400
				shot()
	WORLD.AddTask(shot_butterfly_r, 15, 4, 60, True)
WORLD.AddTask(WORLD_task, 0, 1, 0)
