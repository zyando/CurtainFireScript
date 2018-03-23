# -*- coding: utf-8 -*-

shot_list = []

MAX_DISTANCE = 320
POINT_LIST = [v * i * MAX_DISTANCE for i in [-1, 1] for v in [Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ]]

COLORS = [0xFF0000, 0xA00040, 0xFF00FF, 0x4000A0, 0x0000FF, 0x0040A0, 0x00FFFF, 0x00A040, 0x00FF00]
COLORS.reverse()

veclist = objvertices("ico.obj", 3)

def is_collide(shot):
    return any([abs(shot.Pos[i]) > MAX_DISTANCE for i in range(3)]) or any([(s.Pos - shot.Pos).Length() < 30 for s in shot_list])

def shot_amulet(color):
    pos = randomvec() * 40
    mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

    for vec in veclist:
        shot = EntityShot(WORLD, "AMULET", color)
        shot.Pos = pos
        shot.Velocity = vec * mat * 5

        def check_collision(shot = shot, is_needed = [True]):
            if is_needed[0] and is_collide(shot):
                shot.Velocity *= 0

                def set_lookat(vec = +(POINT_LIST[POINT_LIST.index(min(POINT_LIST, key = lambda p: (shot.Pos - p).Length()))] - shot.Pos)):
                    shot.AddRootBoneKeyFrame()
                    shot.LookAtVec = vec
                shot.AddTask(set_lookat, 0, 1, 5)

                def add_list(): shot_list.append(shot)
                shot.AddTask(add_list, 0, 1, 30)

                is_needed[0] = False
        shot.AddTask(check_collision, 0, 0, 0)

        shot()
WORLD.AddTask(lambda: shot_amulet(COLORS.pop()), 30, len(COLORS), 0)

def shot_amulet_and_sphere(vec = [Vector3.UnitZ], mat = Matrix3.RotationAxis(randomvec() ^ Vector3.UnitZ, RAD * 15)):
    for i in range(24):
        shot = EntityShot(WORLD, "M", 0xFF0000)
        shot.Velocity = vec[0] * Matrix3.RotationAxis(randomvec(), RAD * 20) * 12
        shot.LivingLimit = 400
        shot()

    for i in range(40):
        shot = EntityShot(WORLD, "S", 0xFF0000)
        shot.Velocity = vec[0] * Matrix3.RotationAxis(randomvec(), RAD * 20) * 12
        shot.LivingLimit = 400
        shot()

    for i in range(40):
        shot = EntityShot(WORLD, "XS", 0xFFFFFF)
        shot.Velocity = vec[0] * Matrix3.RotationAxis(randomvec(), RAD * 20) * 12
        shot.LivingLimit = 400
        shot()

    vec[0] = vec[0] * mat
WORLD.AddTask(shot_amulet_and_sphere, 5, 24, 330)

def move(move_num = 5):
    for i in range(len(veclist)):
        if len(shot_list) == 0: return True

        shot = shot_list.pop()
        shot.AddRootBoneKeyFrame()
        shot.Velocity = shot.LookAtVec * 6
WORLD.AddTask(move, 0, 0, 390)
