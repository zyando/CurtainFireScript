# -*- coding: utf-8 -*-
from random import random

SCALE = 4

obj = WavefrontObject("space_filling.obj", lambda v: v * 25 * SCALE)
connected_vtx_dict = {v : obj.create_list_connected_vertex(v) for v in obj.veclist}

group_each_length_of_laser = [(0, 0b001)]

def task():
	pos_and_target_list = []
	mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 20)
	
	def shot_laser(vtx, level):
		for connected_vtx in connected_vtx_dict[vtx]:
			if (vtx, connected_vtx) in pos_and_target_list: continue
			
			pos_and_target_list.append((vtx, connected_vtx))
			
			vec = connected_vtx - vtx
			length = vec.Length()
			
			shot = EntityShot(WORLD, "M", 0xA00000)
			shot.Pos = vtx * mat
			shot.Velocity = vec * mat * (1.0 / 5)
			shot.LivingLimit = 5
			
			if shot.ModelData.OwnerEntities.Count == 1:
				for vertex in shot.ModelData.Vertices: vertex.Pos *= 0.3 * SCALE
			shot()
			
			length_min, group = min(group_each_length_of_laser, key = lambda t: abs(length - t[0]))
			if abs(length_min - length) > 0.1:
				group = 0b001 << len(group_each_length_of_laser)
				group_each_length_of_laser.append((length, group))
			
			laser = EntityShot(WORLD, "LASER_LINE", 0xA00000)
			laser.Recording = Recording.LocalMat
			laser.Pos = vtx * mat
			laser.Rot = Matrix3.LookAt(+(vec * mat), Vector3.UnitY)
			laser.LivingLimit = 100
			
			if laser.ModelData.OwnerEntities.Count == 1:
				scale = Matrix3(2 * SCALE, 0, 0, 0, 2 * SCALE, 0, 0, 0, length)
				for vertex in laser.ModelData.Vertices: vertex.Pos *= scale
				
			morph = laser.CreateVertexMorph(lambda v: Vector3(v.x * -0.95, v.y * -0.95, 0))
			laser.AddMorphKeyFrame(morph, 1, 0)
			laser.AddMorphKeyFrame(morph, 0, 5)
			laser.AddMorphKeyFrame(morph, 0, 95)
			laser.AddMorphKeyFrame(morph, 1, 100)
			
			laser.AddTask(lambda v = connected_vtx: shot_laser(v, level + 1), 0, 1, 5)
			laser()
	shot_laser(Vector3.Zero, 0)
WORLD.AddTask(task, 200, 2, 10)

veclist2 = []
objvertices("ico.obj", lambda v: veclist2.append(+v), 2)

def shot_l():
	for vec in veclist2:
		if vec * Vector3.UnitZ < -0.3: continue
		
		shot = EntityShot(WORLD, "L", 0xFF0000)
		shot.Velocity = vec * 1.2 * SCALE
		shot.LivingLimit = 200
		
		if shot.ModelData.OwnerEntities.Count == 1:
			for vertex in shot.ModelData.Vertices: vertex.Pos *= 1 * SCALE
		
		shot()
#WORLD.AddTask(shot_l, 30, 16, 0)

veclist3 = []
objvertices("ico.obj", lambda v: veclist3.append(+v), 3)

def shot_dia():
	mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 10)
	
	for vec in veclist3:
		if +(TARGET_BONE.WorldPos - OWNER_BONE.WorldPos) * vec < 0.7: continue
		
		shot = EntityShot(WORLD, "DIA", 0x0000A0)
		shot.Pos = OWNER_BONE.WorldPos
		shot.Velocity = vec * mat * 4 * SCALE
		shot.LivingLimit = 200
		
		if shot.ModelData.OwnerEntities.Count == 1:
			for vertex in shot.ModelData.Vertices: vertex.Pos *= 0.8 * SCALE
			
		shot()
#WORLD.AddTask(shot_dia, 10, 40, 0)