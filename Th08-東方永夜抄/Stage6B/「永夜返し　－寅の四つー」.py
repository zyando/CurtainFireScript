# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 3)

def phase0():
	def shot_dia():
		for vec in veclist:
			shot = EntityShot(WORLD, "DIA", 0x4040A0)
			shot.Velocity = vec * 10
			shot.LifeSpan = 150

			def pause(shot = shot): shot.Velocity *= 0
			shot.AddTask(pause, 0, 1, 15)

			def move(shot = shot, vec = vec): shot.Velocity = vec * -10
			shot.AddTask(move, 0, 1, 30)
			shot.Spawn()
	WORLD.AddTask(shot_dia, 2, 9, 0)
WORLD.AddTask(phase0, 80, 8, 0)

def phase1(task):
	shot = EntityShot(WORLD, "L", 0xA00000)
	shot.Velocity = Vector3.UnitX * (task.ExecutedCount % 2 * 2 - 1) * 3
	shot.LifeSpan = 300
	shot.Spawn()

	def turn():
		shot.Velocity = normalize(TARGET_BONE.WorldPos - shot.Pos) * 3
	shot.AddTask(turn, 0, 1, 60)
WORLD.AddTask(phase1, 8, 75, 90, True)
