# -*- coding: utf-8 -*-
from random import random

veclist = []

way = 15
mat = Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360.0 / way))
vec = Vector3.UnitY

for i in range(way):
	veclist.append(vec)
	vec = vec * mat

task_interval = 90
num_shot_in_line = 20
num_line = 10
interval = 2

def shot_task1():
	axis = -Vector3.UnitZ * owner_centerbone.WorldMat
	
	root = Entity(WORLD)
	root.Rot = Quaternion.RotationAxis(Vector3.UnitZ, RAD * random() * 180)
	
	def rotate(root = root, rotate_quat = Quaternion.RotationAxis(Vector3.UnitZ, RAD * 6)):
		root.Rot *= rotate_quat 
	root.AddTask(rotate, interval, num_line, 0)
	root()
	
	for vec in veclist:
		parent1 = Entity(WORLD, root)
		parent1.Velocity = vec * 10
		parent1()
		
		def shot_task2(parent1 = parent1, bonemat = CENTER_BONE.WorldMat):
			parent2 = Entity(WORLD)
			parent2.Pos = vec4(parent1.WorldPos) * bonemat
			parent2.Velocity = axis * 20
			parent2()
			
			def shot_scale(parent2 = parent2, upward = +Vector3(parent1.WorldPos.x, parent1.WorldPos.y, 0) * bonemat):
				mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 6)
				vec = axis * mat * 0.1
				
				for i in range(2):
					shot = EntityShot(WORLD, "SCALE", 0xA000A0)
					shot.Pos = parent2.Pos
					shot.Upward = upward
					shot.Velocity = vec * (i * 2 - 1)
					
					def move(shot = shot, v = +shot.Velocity):
						shot.Velocity = v * 4
					shot.AddTask(move, 0, 1, task_interval)
					shot()
			parent2.AddTask(shot_scale, 1, num_shot_in_line, 0)
		parent1.AddTask(shot_task2, interval, num_line, 1)
WORLD.AddTask(shot_task1, task_interval, 2, 0)
