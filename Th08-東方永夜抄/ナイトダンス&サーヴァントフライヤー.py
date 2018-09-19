# -*- coding: utf-8 -*-

parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
parent.GetRecordedRot = lambda e: e.Rot

def update(t):
    parent.Pos += (CENTER_BONE.WorldPos - parent.Pos) * t
    parent.Rot *= (Quaternion(HAND_BONE.WorldRot) * ~parent.Rot) ^ t
parent.AddTask(lambda: update(0.05), 0, 0, 0)

update(1)

parent.Spawn()

def night_dacce():
    for i in 1, -1:
        shot = EntityShot(WORLD, "DIA", 0xFFFFFF, Vector3(0.5, 0.5, 2.5))
        shot.Pos = Vector4(2 * i, 0, 2, 1) * HAND_BONE.WorldMat
        shot.Velocity = Vector3.UnitZ * HAND_BONE.WorldMat * 16.0
        shot.LifeSpan = 100
        shot.Spawn()
WORLD.AddTask(night_dacce, 2, 100, 25)

def servant_flyer(pos, lookat):
    mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0x800000, 1.4)
    mgc.Parent = parent
    mgc.Pos = pos
    mgc.LookAtVec = lookat

    def shot_scale():
        shot = EntityShot(WORLD, "SCALE", 0xA0A0A0)
        shot.Pos = mgc.WorldPos
        shot.Velocity = Vector3.UnitZ * HAND_BONE.WorldMat * 16.0
        shot.LifeSpan = 100
        shot.Spawn()
    mgc.AddTask(shot_scale, 2, 100, 25)
    mgc()
WORLD.AddTask(lambda: [servant_flyer(p * Matrix3(i, 1, 1), Vector3.UnitZ * i) for p in Vector3(20, 2, -4), Vector3(40, 6, -1) for i in 1, -1], 0, 1, 0)
