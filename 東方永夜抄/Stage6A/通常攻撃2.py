# -*- coding: utf-8 -*-
from random import random

veclist0 = []
objvertices("ico.obj", lambda v: veclist0.append(+v), 0)

veclist1 = []
objvertices("ico.obj", lambda v: veclist1.append(+v), 1)

def task_to_shoot_while_rotating(vec, axis, shottype, color, init_angle, angle_interval, speed, livinglimit):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0
	
	axis = vec ^ (vec ^ axis)
	rot = Matrix3.RotationAxis(axis, angle_interval)
	
	frame = Frame(vec * Matrix3.RotationAxis(axis, init_angle), rot)
	
	def shot_dia():
		shot = EntityShot(WORLD, shottype, color)
		shot.Velocity = frame.vec * speed
		shot.LivingLimit = livinglimit
		shot()
		
		frame.vec *= frame.rot
	return shot_dia

for vec in veclist0:
	for axis in Vector3.UnitX, Vector3.UnitZ:
		for i in range(4):
			WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "DIA", 0xA00000, RAD * i * 20, RAD * 4, 1 + i * 0.5, (4 - i) * 100), 2, 420, 60)

def task_to_shoot_mgc_crcl():
	mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 90)
	
	for vec in veclist1:
		mgc_crcl = EntityShot(WORLD, "MAGIC_CIRCLE", 0xFFFFFF)
		mgc_crcl.Velocity = vec * 4 * mat
		mgc_crcl.LivingLimit = 150
		
		def shot_s(mgc_crcl = mgc_crcl):
			shot = EntityShot(WORLD, "S", 0x0000A0)
			shot.Pos = mgc_crcl.Pos + randomvec() * (random() * 50)
			shot.LivingLimit = 120
			shot()
		mgc_crcl.AddTask(shot_s, 0, 120, 0)
		mgc_crcl()
WORLD.AddTask(task_to_shoot_mgc_crcl, 180, 5, 0)