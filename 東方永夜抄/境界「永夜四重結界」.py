# -*- coding: utf-8 -*-

cube_edges = []

for vtx in [Vector3(xz * y, y, xz) for xz in [1, -1] for y in [1, -1]]:
    for mat in Matrix3(-1, 1, 1), Matrix3(1, -1, 1), Matrix3(1, 1, -1):
        cube_edges.append((vtx, vtx * mat))

def task(color, scale):
    parent = EntityShot(WORLD, "BONE", 0)
    parent.GetRecordedRot = lambda e: e.Rot
    parent.LivingLimit = 240

    def rotate(rot = Quaternion.RotationAxis(randomvec(), RAD * 90)): parent.Rot *= rot
    parent.AddTask(rotate, 30, 0, 0)

    def effect():
        for i in range(16):
            shot = EntityShot(WORLD, "DIA", color, Vector3(1, 1, 10))
            shot.Velocity = randomvec() * 80
            shot.Pos = +shot.Velocity * scale * (1 + random()) * 0.5
            shot.LivingLimit = 50
            shot()
    parent.AddTask(effect, 0, 0 ,0)

    parent()

    for edge in cube_edges:
        shot = EntityShot(WORLD, "LASER_LINE", color, Vector3(8, 8, scale * 2), parent)
        shot.LivingLimit = 240
        shot.Pos = edge[0] * scale
        shot.LookAtVec = edge[1] - edge[0]

        morph = shot.CreateVertexMorph(lambda v: Vector3(-v.x, -v.y, 0))
        shot.AddMorphKeyFrame(morph, 1, 0)
        shot.AddMorphKeyFrame(morph, 0, 30)
        shot.AddMorphKeyFrame(morph, 0, 210)
        shot.AddMorphKeyFrame(morph, 1, 240)
        shot()

def quadruple_barrier():
    task(0xFF00FF, 480)
    task(0xFF0000, 440)
    task(0x0000FF, 400)
    task(0xA000A0, 360)
WORLD.AddTask(quadruple_barrier, 0, 1, 0)
