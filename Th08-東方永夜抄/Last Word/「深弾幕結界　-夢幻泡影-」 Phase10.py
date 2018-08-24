# -*- coding: utf-8 -*-

def shot_amulet():
	for i in range(64):
		shot = EntityShot(WORLD, "AMULET", 0xA00000)
		shot.Pos = randomvec() * random() * 1024
		shot.LookAtVec = -+shot.Pos
		shot.Upward = randomvec()
		
		def move(s = shot): s.Velocity = +s.Pos * -1
		shot.AddTask(move, 0, 1, 210 - WORLD.FrameCount)
		
		shot.Spawn()
WORLD.AddTask(shot_amulet, 0, 150, 0)
