# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(3)]

def shot_dia():
	mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

	for vec in veclists[2]:
		shot = EntityShot(WORLD, "DIA_BRIGHT", 0x000040)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = vec * mat * (2.0 if vec in veclists[1] else 4.0)
		shot.LifeSpan = 90 if vec in veclists[1] else 45

		def replace(orgn = shot):
			shot = EntityShot(WORLD, "DIA", 0x0000A0)
			shot.Pos = orgn.Pos
			shot.Velocity = orgn.Velocity
			shot.LifeSpan = orgn.LifeSpan * 8
			shot()
		shot.AddTask(replace, 0, 1, shot.LifeSpan)
		shot()
WORLD.AddTask(shot_dia, lambda i: int(max(20 - i * 0.5, 5)), 0, 0)
