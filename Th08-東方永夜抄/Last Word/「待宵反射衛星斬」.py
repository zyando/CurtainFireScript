# -*- coding: utf-8 -*-

veclist = []

way = 15
mat = Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360.0 / way))
vec = Vector3.UnitY

for i in range(way):
	veclist.append(vec)
	vec = vec * mat

task_interval = 120
num_shot_in_line = 24
num_line = 12
interval = 2

def shot_task1():
	axis = -Vector3.UnitZ * CENTER_BONE.WorldMat
	
	root = Entity(WORLD)
	root.Rot = Quaternion.RotationAxis(Vector3.UnitZ, RAD * random() * 180)
	root()
	
	def rotate(root = root, rotate_quat = Quaternion.RotationAxis(Vector3.UnitZ, RAD * 6)):
		root.Rot *= rotate_quat 
	WORLD.AddTask(rotate, interval, num_line, 0)
	
	for vec in veclist:
		parent1 = EntityMoving(WORLD, root)
		parent1.Velocity = vec * 16
		parent1()
		
		def shot_task2(parent1 = parent1, bonemat = CENTER_BONE.WorldMat):
			parent2 = EntityMoving(WORLD)
			parent2.Pos = vec4(parent1.WorldPos) * bonemat
			parent2.Velocity = axis * 26
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
						shot.Velocity = v * 8
					shot.AddTask(move, 0, 1, task_interval)
					shot()
			WORLD.AddTask(shot_scale, 1, num_shot_in_line, 0)
		WORLD.AddTask(shot_task2, interval, num_line, 1)
WORLD.AddTask(shot_task1, task_interval, 2, 0)
