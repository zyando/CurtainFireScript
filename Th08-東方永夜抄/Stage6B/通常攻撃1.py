# -*- coding: utf-8 -*-
from random import choice

veclist = [Vector3(x * (r + 1) * 0.02, 0, 1) for x in [1, -1] for r in range(2)] + [Vector3.UnitZ]

def shot_dia(vec, axis, color1, color2):
	mat1 = Matrix3.LookAt(vec, randomvec())
	mat2 = Matrix3.RotationAxis(vec ^ (vec ^ axis), RAD * 150)
	
	for vec in veclist:
		vec *= mat1
		
		shot = EntityShot(WORLD, "DIA_BRIGHT", color1)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = vec * 4
		shot.LifeSpan = 45
		shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), shot.LifeSpan)
		
		def replace_shot(org = shot):
			shot = EntityShot(WORLD, "DIA", color2)
			shot.Pos = org.Pos
			shot.Velocity = +org.Velocity * mat2 * 4
			shot.LifeSpan = 400
			shot()
		shot.AddTask(replace_shot, 0, 1, shot.LifeSpan)
		shot()
WORLD.AddTask(lambda: [shot_dia(randomvec(), choice(Vector3.Units), 0x000040, 0x0000A0) for i in range(3)], 0, 600, 0)
WORLD.AddTask(lambda: [shot_dia(randomvec(), -choice(Vector3.Units), 0x400000, 0xA00000) for i in range(3)], 0, 600, 0)

def shot_rice():
	vec_to_target = +(TARGET_BONE.WorldPos - CENTER_BONE.WorldPos + randomvec() * gauss(0, 100))
	
	for i in range(10):
		shot = EntityShot(WORLD, "RICE_M", 0xA00000)
		shot.Velocity = vec_to_target * (4 + i * 1)
		shot.LifeSpan = 200
		shot()
WORLD.AddTask(shot_rice, 60, 20, 0)
