# -*- coding: utf-8 -*-

def create_veclist(num_way):
    vec = Vector3.UnitY

    num_pitch = num_way / 2 + 1
    mat_pitch = Matrix3.RotationAxis(Vector3.UnitX, RAD * 180.0 / num_pitch)

    mat_yaw = Matrix3.RotationAxis(Vector3.UnitY, RAD * 360.0 / num_way)

    for pitch in range(num_way / 2):
        vec = vec * mat_pitch

        for yaw in range(num_way):
            vec = vec * mat_yaw
            yield vec

mat = [Matrix3.Identity, Matrix3.RotationAxis(Vector3.UnitY, RAD * 6)]

def shot_knife1(task, veclist_list = [list(create_veclist(i)) for i in range(2, 13)]):
    for vec in veclist_list[min(len(veclist_list) - 1, task.ExecutedCount / 6)]:
        shot = EntityShot(WORLD, "KNIFE", 0xA00000)
        shot.Velocity = vec * mat[0] * 8
        shot.LifeSpan = 100
        shot.Spawn()

    mat[0] *= mat[1]
WORLD.AddTask(shot_knife1, 5, 80, 0, True)

def shot_knife2(veclist = list(create_veclist(30))):
    for vec in veclist:
        shot = EntityShot(WORLD, "KNIFE", 0xA00000)
        shot.Velocity = vec * mat[0] * 12
        shot.LifeSpan = 50
        shot.Spawn()

    mat[0] *= mat[1]
WORLD.AddTask(shot_knife2, 2, 100, 400)
