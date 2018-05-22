# -*- coding: utf-8 -*-

parent1 = EntityShot(WORLD, "BONE", 0)
parent1.Pos = HAND_BONE.WorldPos
parent1()

parent2 = EntityShot(WORLD, "BONE", 0)
def record2(): parent2.Pos = CENTER_BONE.WorldPos
parent2.AddTask(record2, 0, 90, 0)
parent2()

def shot_laser1(task):
	shot = EntityShotStraight(WORLD, "DIA", 0x0000FF, Vector3(0.05, 0.05, 1), parent1)
	shot.Pos = randomvec() * 640 * random()
	shot.LivingLimit = randint(55, 65) - task.ExecutedCount
	shot.Velocity = -shot.Pos * (1.0 / shot.LivingLimit)
	shot()
WORLD.AddTask(lambda t: [shot_laser1(t) for i in range(256)], 0, 50, 0, True)

def shot_laser2(task):
	shot = EntityShotStraight(WORLD, "DIA", 0xFF0000, Vector3(0.4, 0.4, 8), parent1)
	shot.Velocity = randomvec() * 1280 * (1.0 / (randint(15, 20) - task.ExecutedCount))
	shot.Pos = Vector3.Zero + shot.Velocity * random()
	shot.LivingLimit = 60
	shot()
WORLD.AddTask(lambda t: [shot_laser2(t) for i in range(256)], 0, 10, 60, True)

def shot_effect(task):
	shot = EntityShotStraight(WORLD, "S", 0xFF0090, 0.5, parent2)
	shot.Pos = randomvec() * 640 * (random() * 0.5 + 0.5)
	shot.LivingLimit = randint(55, 60) - task.ExecutedCount
	shot.Velocity = -shot.Pos * (1.0 / shot.LivingLimit)
	shot()
WORLD.AddTask(lambda t: [shot_effect(t) for i in range(128)], 0, 50, 90, True)
