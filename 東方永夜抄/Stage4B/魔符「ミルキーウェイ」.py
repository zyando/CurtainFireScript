# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
from entities import EntityShotWithParticle
from vectorutil import *
from randomutil import random, randint, gaussian
import math

veclist = []
objvertices("ico.obj", lambda v: veclist.append(v))

def entity_to_shoot(vec, axis):
    axis = vec ^ (vec ^ axis)
    entity = Entity(WORLD)
    entity.Pos = vec
    entity.Rot = Quaternion.RotationAxis(axis, RAD * 12)

    def shot_star(task, entity = entity):
        shot = EntityShotWithParticle(WORLD, STAR_M, 0xA00000 if task.RunCount % 2 == 0 else 0x0000A0)
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
        for j in range(2):
            color = colors[0] if i == 1 else colors[1]
            shot = EntityShotWithParticle(WORLD, STAR_S, color[randint(0, 2)])
            shot.Pos = Vector3(gaussian(0.5, 0.5) * i * 500, gaussian() * 300, gaussian(0.5, 0.5) * -800)
            shot.Velocity = Vector3.UnitX * -i * 2 * Matrix3.RotationAxis(randomvec(), RAD * random() * 20)
            shot.LivingLimit = 300
            shot()
WORLD.AddTask(shot_small_star, 0, 300, 50)
