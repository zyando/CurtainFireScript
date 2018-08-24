# -*- coding: utf-8 -*-

shot_range = 800

WORLD.FrameCount = 480

def shot_randomvec(shottype, color, speed):
	shot = EntityShot(WORLD, shottype, color)
	shot.Velocity = randomvec() * speed * gauss(1, 0.3)
	shot.Upward = randomvec()
	shot.LifeSpan = shot_range / speed
	shot.Spawn()

WORLD.AddTask(lambda: [shot_randomvec("BUTTERFLY", 0xA000A0, uniform(3, 8)) for i in range(8)], 0, 300, 0)
WORLD.AddTask(lambda: [shot_randomvec("M", 0xA00000, uniform(3, 8)) for i in range(8)], 0, 300, 0)
WORLD.AddTask(lambda: [shot_randomvec("KNIFE", 0x0000A0, uniform(3, 8)) for i in range(8)], 0, 300, 0)
WORLD.AddTask(lambda: [shot_randomvec("STAR_S", 0x00A0A0, uniform(3, 8)) for i in range(8)], 0, 300, 0)
WORLD.AddTask(lambda: [shot_randomvec("RICE_M", 0x00A0A0, uniform(3, 8)) for i in range(8)], 0, 300, 0)
WORLD.AddTask(lambda: [shot_randomvec("AMULET", 0xA0A000, uniform(3, 8)) for i in range(8)], 0, 300, 0)
