# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(5)]

WORLDS = [CreateWorld(PRESET_FILENAME + str(i)) for i in range(2)]

def get_idx(i, unit = (len(veclists[4]) / len(WORLDS)), min_idx = len(WORLDS)):
	return min(i / unit, min_idx - 1)

def get_acceleration(interval, length): return -(interval * interval) / (length * 2.0)

def phase5():
	interval = 100
	acceleration = get_acceleration(interval, 1100)

	print acceleration

	def shot_dia1():
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for idx, vec in enumerate(veclists[4]):
			shot = EntityShotStraight(WORLDS[get_idx(idx)], "DIA_BRIGHT", 0x000040)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * mat * 2
			shot.LifeSpan = 400
			shot.Spawn()
	WORLD.AddTask(shot_dia1, lambda i: max(5, interval + int(acceleration * i)), interval / -acceleration + 8, 0)

	def shot_dia2():
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for vec in veclists[2]:
			shot = EntityShotStraight(WORLD, "DIA_BRIGHT", 0x000040)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * mat * (2.0 if vec in veclists[1] else 4.0)
			shot.LifeSpan = 60 if vec in veclists[1] else 30

			def replace(orgn = shot):
				shot = EntityShotStraight(WORLD, "DIA", 0x0000A0)
				shot.Pos = orgn.Pos
				shot.Velocity = orgn.Velocity
				shot.LifeSpan = orgn.LifeSpan * 8
				shot.Spawn()
			WORLD.AddTask(replace, 0, 1, shot.LifeSpan)
			shot.Spawn()
	WORLD.AddTask(shot_dia2, 15, 120, 0)
WORLD.AddTask(phase5, 0, 1, 0)
