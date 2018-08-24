# -*- coding: utf-8 -*-

def phase0(vertices = WavefrontObject("rising_game.obj", lambda v: v * 40)):
	def shot_s():
		pos = randomvec() * 40
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for vtx in [v * mat + pos for v in vertices.veclist]:
			if vtx.Length() < 80: continue

			shot = EntityShot(WORLD, "S", 0x0000A0)
			shot.Pos = TARGET_BONE.WorldPos + vtx
			shot.LifeSpan = randint(120, 135)
			shot.Spawn()
	WORLD.AddTask(shot_s, 30, 3, 0)
WORLD.AddTask(phase0, 240, 8, 0)
