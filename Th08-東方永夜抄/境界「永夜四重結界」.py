# -*- coding: utf-8 -*-

cube_edges = []

for vtx in [Vector3(xz * y, y, xz) for xz in [1, -1] for y in [1, -1]]:
    for mat in Matrix3(-1, 1, 1), Matrix3(1, -1, 1), Matrix3(1, 1, -1):
        cube_edges.append((vtx, vtx * mat))

def task(color, scale):
    border = EntityShot(WORLD, "CUBE_BORDER", color, scale)
    border.Pos = CENTER_BONE.WorldPos
    border.GetRecordedRot = lambda e: e.Rot
    border.LivingLimit = 240

    morph = border.CreateVertexMorph(lambda v: -v * 0.9)
    border.AddMorphKeyFrame(morph, 1, 0)
    border.AddMorphKeyFrame(morph, 0, 15)

    def rotate(rot = Quaternion.RotationAxis(randomvec(), RAD * 90)): border.Rot *= rot
    border.AddTask(rotate, 30, 0, 0)

    def effect():
        for i in range(16):
            shot = EntityShot(WORLD, "DIA", color, Vector3(1, 1, 10))
            shot.Velocity = randomvec() * 80
            shot.Pos = CENTER_BONE.WorldPos + +shot.Velocity * scale * (1 + random()) * 0.5
            shot.LivingLimit = 50
            shot()
    border.AddTask(effect, 0, 0 ,0)

    border()

def quadruple_barrier():
    task(0xFF00FF, 480)
    task(0xFF0000, 440)
    task(0x0000FF, 400)
    task(0xA000A0, 360)
WORLD.AddTask(quadruple_barrier, 0, 1, 0)
