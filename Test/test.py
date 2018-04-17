# -*- coding: utf-8 -*-

def shot_random():
    for i in range(16):
        shot = EntityShot(WORLD, "DIA", 0x0000A0)
        shot.Velocity = randomvec() * 10
        shot.LivingLimit = 120
        shot()
WORLD.AddTask(shot_random, 0, 100, 0)
