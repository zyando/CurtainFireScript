# -*- coding: utf-8 -*-
from random import random

veclist0 = []
objvertices("ico.obj", lambda v: veclist0.append(+v), 0)

veclist2 = []
objvertices("ico.obj", lambda v: veclist2.append(+v), 2)

def task_to_shoot_mgc_crcl(task, axis):
	mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 90)
	
	def get_parent(vec, parent_dict = {}):
		if not parent_dict.has_key(vec):
			parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
			parent.GetRecordedRot = lambda e: e.Rot
			parent.LivingLimit = 120
			
			def rotate(rot = Quaternion.RotationAxis(vec ^ (vec ^ axis), RAD * (1.5 if task.RunCount % 2 == 0 else -1.5))): parent.Rot *= rot
			parent.AddTask(rotate, 0, 120, 0)
			parent()
			
			parent_dict[vec] = parent
		
		return parent_dict[vec]
	
	move_func_list = []
	WORLD.AddTask(lambda: [f() for f in move_func_list], 0, 1, 100)
	
	for vec in veclist0:
		parent = get_parent(vec)
		
		mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0xA0A0A0, parent)
		mgc.Velocity = vec * 5.0
		mgc.LivingLimit = 120
		
		def shot_l(mgc = mgc, parent = parent, vec = vec):
			shot = EntityShot(WORLD, "L", 0xA00000 if task.RunCount % 2 == 0 else 0x0000A0)
			shot.Pos = mgc.WorldPos + randomvec() * random() * 200
			shot()
			
			def move(velocity = vec * parent.Rot):
				shot.Velocity = velocity * 2
				shot.LivingLimit = shot.FrameCount + 320
			return move
		
		mgc.AddTask(lambda shot_l = shot_l: move_func_list.extend([shot_l() for i in range(3)]), 0, 60, 30)
		mgc()
WORLD.AddTask(lambda t: [task_to_shoot_mgc_crcl(t, a) for a in Vector3.UnitX, Vector3.UnitZ], 90, 10, 0, True)

def shot_dia(speed, livinglimit):
	for vec in veclist2:
		shot = EntityShot(WORLD, "DIA", 0x000040)
		shot.Velocity = vec * speed
		shot.LivingLimit = livinglimit
		shot()
WORLD.AddTask(lambda: [shot_dia(s, l) for s, l in (4.0, 240), (3.0, 250)], 30, 30, 0)