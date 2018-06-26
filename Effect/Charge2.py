# -*- coding: utf-8 -*-

def shot_laser1(task):
    shot = EntityShotStraight(WORLD, "DIA", 0x0000FF, Vector3(0.2, 0.2, 4))
    shot.Pos = randomvec() * 640 * uniform(0.5, 1)
    shot.LivingLimit = randint(35, 45) - task.ExecutedCount
    shot.Velocity = -shot.Pos * (1.0 / shot.LivingLimit)
    shot.Pos += HAND_BONE.WorldPos
    shot()

WORLD.AddTask(lambda t: [shot_laser1(t) for i in range(60)], 0, 25, 0, True)
