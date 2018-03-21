# -*- coding: utf-8 -*-

target = EntityShot(WORLD, "S", 0xA00000, 2)

def turn():
    target.Velocity = +(randomvec() * uniform(-0.2, 0.2) - +target.Pos) * uniform(-5, 5)
WORLD.AddTask(turn, 60, 0, 0)
target()

parent = EntityShot(WORLD, "BONE", 0)
parent.GetRecordedRot = lambda e: e.Rot

binder = Entity(WORLD)

def rotate(rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * 30)):
    binder.Rot *= rot * Quaternion.RotationAxis(randomvec(), RAD * 5 * uniform(-1, 1))
binder.AddTask(rotate, 5, 0, 0)
binder()

def update(t_pos, t_rot):
    parent.Pos += (target.WorldPos - parent.Pos) * t_pos
    parent.Rot = Quaternion.Interpolate(parent.Rot, binder.Rot, t_rot)
parent.AddTask(lambda: update(0.16, 0.08), 0, 0, 0)
parent()

ghost = EntityShot(WORLD, "S", 0xFFFFFF, 2, parent)
ghost.Pos = Vector3.UnitZ * 40
ghost()
