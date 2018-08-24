# -*- coding: utf-8 -*-

veclist_list = [objvertices("ico.obj", i) for i in [1, 2]]

def task():
    def shot_laser(binder = [Vector3.UnitZ * Matrix3.RotationX(RAD * 45), Matrix3.Identity, Matrix3.RotationZ(RAD * 5)], way = 18, rot_x = Matrix3.RotationX(RAD * -3)):
        vec = binder[0] * binder[1]

        rot_z = Matrix3.RotationZ(RAD * 360 / way)

        for i in range(way):
            shot = EntityShot(WORLD, "LASER", 0x000A0, Vector3(8, 8, 1000))
            shot.LookAtVec = vec
            shot.LifeSpan = 45

            morph = shot.CreateVertexMorph(lambda v: Vector3(-v.x, -v.y, 0))
            shot.AddMorphKeyFrame(morph, 1, 0)
            shot.AddMorphKeyFrame(morph, 0, 15)
            shot.AddMorphKeyFrame(morph, 0, 30)
            shot.AddMorphKeyFrame(morph, 1, 45)

            shot.Spawn()

            vec *= rot_z
        binder[0] *= rot_x
        binder[1] *= binder[2]
    WORLD.AddTask(shot_laser, 5, 10, 0)

    def shot_s():
        mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

        for vec in veclist_list[1]:
            i = 1 if (vec in veclist_list[0]) else 2

            shot = EntityShot(WORLD, "S", 0x0000A0)
            shot.Velocity = vec * mat * 3
            shot.LifeSpan = 300 / i
            shot.Spawn()
    WORLD.AddTask(shot_s, 15, 6, 5)

    def shot_l():
        mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

        for vec in veclist_list[1]:
            vec *= mat

            if vec * Vector3.UnitZ > -0.75: continue

            shot = EntityShot(WORLD, "L", 0xA000A0)
            shot.Velocity = vec * 10
            shot.LifeSpan = 100
            shot.Spawn()
    WORLD.AddTask(shot_l, 5, 10, 30)
WORLD.AddTask(task, 120, 5, 0)
