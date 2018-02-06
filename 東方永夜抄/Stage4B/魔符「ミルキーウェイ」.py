# -*- coding: utf-8 -*-
from random import random, randint, gauss

veclist = objvertices("ico.obj", 0)

def entity_to_shoot(vec, axis):
    axis = vec ^ (vec ^ axis)
    entity = Entity(WORLD)
    entity.Pos = vec
    entity.Rot = Quaternion.RotationAxis(axis, RAD * 12)

    def shot_star(task, entity = entity):
        shot = EntityShot(WORLD, "STAR_M", 0xA00000 if task.RunCount % 2 == 0 else 0x0000A0)
        shot.Pos = OWNER_BONE.WorldPos
        shot.Velocity = entity.Pos * 4
        shot.LivingLimit = 300
        shot()

        entity.Pos = entity.Pos * entity.Rot
    entity.AddTask(shot_star, 5, 50, 0, True)
    entity()
for vec in veclist:
    for axis in [Vector3.UnitX, Vector3.UnitZ]:
        entity_to_shoot(vec, axis)

colors = (0xA00000, 0xA0A000), (0x0000A0, 0x00A000)

def shot_small_star():
    for i in [-1, 1]:
        for j in range(8):
            color = colors[0] if i == 1 else colors[1]
            shot = EntityShot(WORLD, "STAR_S", color[randint(0, 2)])
            shot.Pos = OWNER_BONE.WorldPos + Vector3((gauss(0, 1) + 1) * i * 1000, gauss(0, 1) * 600, (gauss(0, 1) + 1) * -800)
            shot.Velocity = Vector3.UnitX * -i * 4 * Matrix3.RotationAxis(randomvec(), RAD * random() * 20)
            shot.LivingLimit = 300
            shot()
WORLD.AddTask(shot_small_star, 0, 300, 50)
