# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(5)]

def shot_dia():
	mat = Matrix3.RotationAxis(randomvec(), RAD * 30)
	
	for vec in veclists[4]:
		shot = EntityShotStraight(WORLD, "DIA_BRIGHT", 0x400000)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = vec * mat * 6
		shot.LifeSpan = 60
		
		def replace(flag = (vec in veclists[3]), orgn = shot):
			shot = EntityShotStraight(WORLD, "DIA", 0xA00000)
			shot.Pos = orgn.Pos
			shot.Velocity = orgn.Velocity * (2.0 if flag else -1.0)
			shot.LifeSpan = (200 if flag else 460) - (1 - (normalize(shot.Velocity)).z) * 80
			shot.Spawn()
		WORLD.AddTask(replace, 0, 1, shot.LifeSpan)
		shot.Spawn()
WORLD.AddTask(shot_dia, 20, 13, 0)
