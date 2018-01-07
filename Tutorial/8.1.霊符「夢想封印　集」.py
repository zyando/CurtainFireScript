# -*- coding: utf-8 -*-

veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 1)

#白の中弾を発射する関数
def shot_m():
	for vec in veclist:
		shot = EntityShot(WORLD, "M", 0xFFFFFF)
		shot.Velocity = vec * 2
		shot.LivingLimit = 200
		shot()
WORLD.AddTask(shot_m, 30, 10, 10)
