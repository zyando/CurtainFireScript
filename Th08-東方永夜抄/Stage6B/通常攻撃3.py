# -*- coding: utf-8 -*-
from random import choice

veclist0 = objvertices("ico.obj", 0)
veclist2 = objvertices("ico.obj", 2)

def task_to_shoot_mgc_crcl(axis):
	move_func_list = []
	WORLD.AddTask(lambda: [f() for f in move_func_list], 0, 1, 100)

	for vec in veclist0:
		axis = vec ^ (vec ^ axis)
		
		for i in 1, -1:
			mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0xA0A0A0, 2)
			mgc.Velocity = vec * 8.0
			mgc.LifeSpan = 120
			
			def rotate(mgc = mgc, rot = Matrix3.RotationAxis(axis * i, RAD * 2)):
				mgc.Velocity *= rot
			mgc.AddTask(rotate, 0, 120, 0)
			
			def shot_task(mgc = mgc, vec = vec, i = i, types = ("L", "M", "S", "M", "S")):
				shot = EntityShot(WORLD, choice(types), 0xA000A0 if i > 0 else 0x00A0A0)
				shot.Pos = mgc.WorldPos + randomvec() * gauss(0, 300)
				shot.LifeSpan = 600
				shot()

				def move(velocity = -vec * Quaternion.RotationAxis(axis * i, RAD * uniform(30, 60))):
					shot.Velocity = velocity * 2
					shot.SetMotionInterpolationCurve(Vector2(0.7, 0.3), Vector2(0.7, 0.3), 90)
				return move
			mgc.AddTask(lambda shot_task = shot_task: move_func_list.extend([shot_task() for i in range(2)]), 5, 12, 30 + randint(0, 5))
			mgc()
WORLD.AddTask(lambda: task_to_shoot_mgc_crcl(Vector3.UnitY), 90, 7, 0)

def shot_dia():
	mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

	for vec in veclist2:
		shot = EntityShot(WORLD, "DIA_BRIGHT", 0x000040)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = vec * mat * 4
		shot.LifeSpan = 240
		shot()
WORLD.AddTask(shot_dia, 30, 23, 0)
