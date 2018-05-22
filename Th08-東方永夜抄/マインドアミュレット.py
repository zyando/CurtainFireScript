# -*- coding: utf-8 -*-

WAY = 6
ANGLE_LIST = [RAD * 10, RAD * 20]

veclist = [Vector3(0, sin(a), cos(a)) * Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360.0 / WAY) * i) for a in ANGLE_LIST for i in range(WAY)]
veclist.append(Vector3.UnitZ)

def shot_red_amullet(mat = [Matrix3.Identity, Matrix3.RotationAxis(Vector3.UnitZ, RAD * 4)]):
    if REIMU_SHOT_FLAG.Pos.Length() < 0.01: return

    mat[0] = mat[0] * mat[1]

    for vec in veclist:
        vec = vec * mat[0]
        shot = EntityShot(WORLD, "AMULET", 0xA00000, 0.6)
        shot.Pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat
        shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * 12.0
        shot.Upward = (vec ^ (vec ^ Vector3.UnitZ)) * REIMU_HAND_BONE.WorldMat
        shot()
WORLD.AddTask(shot_red_amullet, 3, 0, 0)

homing_veclist = [Vector3(sin(a) * i, 0, -cos(a)) for a in [RAD * 30, RAD * 45] for i in -1, 1]

def shot_homing_amulet(speed = 12):
    if REIMU_SHOT_FLAG.Pos.Length() < 0.01: return

    for vec in homing_veclist:
        shot = EntityShot(WORLD, "AMULET", 0xA000A0, 0.6)
        shot.Pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat
        shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * speed
        shot.Upward = (vec ^ (vec ^ Vector3.UnitZ)) * REIMU_HAND_BONE.WorldMat

        def homing(shot = shot):
            vec = +shot.Velocity
            vec_to_target = +(CENTER_BONE.WorldPos - shot.Pos)
            alpha = (1 - vec * vec_to_target) * 0.4

            shot.Velocity = (vec + (vec_to_target - vec) * alpha) * speed
            shot.LivingLimit = shot.FrameCount + int((CENTER_BONE.WorldPos - shot.Pos).Length() / speed)
        shot.AddTask(homing, 0, 0, 0)
        shot()
WORLD.AddTask(shot_homing_amulet, 3, 0, 0)
