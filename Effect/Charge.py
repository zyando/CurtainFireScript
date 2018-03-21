# -*- coding: utf-8 -*-

from random import random, randint

parent = EntityShot(WORLD, "BONE", 0)
def record(): parent.Pos = CENTER_BONE.WorldPos + -Vector3.UnitY * CENTER_BONE.WorldMat
parent.AddTask(record, 0, 90, 0)
parent()

def shot_laser1(task):
    shot = EntityShot(WORLD, "DIA", 0x0000FF, Vector3(0.4, 0.4, 4))
    shot.Pos = randomvec() * 640 * random()
    shot.LivingLimit = randint(35, 45) - task.ExecutedCount
    shot.Velocity = -shot.Pos * (1.0 / shot.LivingLimit)
    shot()
WORLD.AddTask(lambda t: [shot_laser1(t) for i in range(60)], 0, 30, 0, True)

def shot_laser2(task):
    shot = EntityShot(WORLD, "DIA", 0xFF0000, Vector3(0.4, 0.4, 8))
    shot.Pos = Vector3.Zero
    shot.LivingLimit = 60
    shot.Velocity = randomvec() * 640 * (1.0 / (randint(15, 20) - task.ExecutedCount))
    shot()
WORLD.AddTask(lambda t: [shot_laser2(t) for i in range(60)], 0, 10, 40, True)

def shot_effect(task):
    shot = EntityShot(WORLD, "S", 0xFF0090, 4)
    shot.Pos = randomvec() * 640 * (random() * 0.5 + 0.5)
    shot.LivingLimit = randint(60, 70) - task.ExecutedCount
    shot.Velocity = -shot.Pos * (1.0 / shot.LivingLimit)
    shot()
WORLD.AddTask(lambda t: [shot_effect(t) for i in range(40)], 0, 50, 90, True)
