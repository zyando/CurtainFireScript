# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
from vectorutil import *
from random import random, randint, gaussian
import math

veclist = []
objvertices("ico.obj", lambda v: veclist.append(v))

colors = 0xA00000, 0x00A000, 0x0000A0, 0xA0A000, 0xA000A0, 0x00A0A0

def shoot_laser_every_direction(color, vec, axis, is_begining_with_vanish):
    shot = EntityShot(WORLD, LASER, color)
    shot.Recording = Recording.LocalMat
    shot.Rot = Matrix3.LookAt(vec, Vector3.UnitY)

    def rotate(rot = Quaternion.RotationAxis(vec ^ (vec ^ axis), RAD * 120)):
        shot.Rot *= rot
    shot.AddTask(rotate, 120, 4, 120)

    scale = Matrix3(80, 0, 0, 0, 80, 0, 0, 0, 800)
    if shot.ModelData.OwnerEntities.Count == 1:
        for vert in shot.ModelData.Vertices: vert.Pos = vert.Pos * scale

    scale = Matrix3(-0.9, 0, 0, 0, -0.9, 0, 0, 0, 0)
    morph = shot.CreateVertexMorph("V_" + shot.MaterialMorph.MorphName, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))

    def vanish():
        shot.AddMorphKeyFrame(morph, 0, 0.0)
        shot.AddMorphKeyFrame(morph, 10, 1.0)
        shot.AddMorphKeyFrame(morph, 70, 1.0)
        shot.AddMorphKeyFrame(morph, 80, 0.0)
    shot.AddTask(vanish, 140, 4, 70 if is_begining_with_vanish else 0)
    shot()
count = 0
for vec in veclist:
    for axis in [Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ]:
        shoot_laser_every_direction(colors[count % len(colors)], vec, axis, True)
        shoot_laser_every_direction(colors[count % len(colors)], vec, -axis, False)
        count += 1
