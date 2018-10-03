# -*- coding: utf-8 -*-
from random import choice

veclist = [Vector3(x * (r + 1) * 0.015, 0, 1) for x in [1, -1] for r in range(2)] + [Vector3.UnitZ]

def shot_dia(vec, axis, color1, color2):
	mat1 = Matrix3.LookAt(vec, randomvec())
	mat2 = Matrix3.RotationAxis(cross3(vec, vec, axis), RAD * 150)
	
	for vec in veclist:
		vec *= mat1
		
		shot = EntityShot(WORLD, "DIA_BRIGHT", color1)
		shot.Velocity = vec * 16
		shot.Pos = CENTER_BONE.WorldPos + normalize(shot.Velocity) * 20
		shot.LifeSpan = 45
		shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), shot.LifeSpan)
		
		def replace_shot(org = shot):
			shot = EntityShot(WORLD, "DIA", color2)
			shot.Pos = org.Pos
			shot.Velocity = normalize(org.Velocity) * mat2 * 8
			shot.LifeSpan = 400
			shot.Spawn()
		shot.AddTask(replace_shot, 0, 1, shot.LifeSpan)
		shot.Spawn()
WORLD.AddTask(lambda: [shot_dia(randomvec(), choice(Vector3.Units), 0x000040, 0x0000A0) for i in range(4)], 0, 600, 0)
WORLD.AddTask(lambda: [shot_dia(randomvec(), -choice(Vector3.Units), 0x400000, 0xA00000) for i in range(4)], 0, 600, 0)

def shot_rice():
	vec_to_target = normalize(REIMU_CNETR_BONE.WorldPos - CENTER_BONE.WorldPos)
	
	for i in range(10):
		shot = EntityShot(WORLD, "RICE_M", 0xA00000)
		shot.Velocity = vec_to_target * (16 + i * 1)
		shot.Pos = CENTER_BONE.WorldPos + normalize(shot.Velocity) * 20
		shot.LifeSpan = 200
		shot.Spawn()
WORLD.AddTask(shot_rice, 45, 20, 240)
