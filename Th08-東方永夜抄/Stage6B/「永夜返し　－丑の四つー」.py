# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 2)

parent_list = []
for i in -1, 1:
    parent = EntityShot(WORLD, "BONE", 0)
    parent.GetRecordedRot = lambda e: e.Rot

    def rotate(p = parent, rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * i * 170)): p.Rot *= rot
    parent.AddTask(rotate, 160, 4, 160)
    parent()
    parent_list.append(parent)

def shot_dia(task):
    for vec in veclist:
        for i in range(2):
            shot = EntityShot(WORLD, "DIA", 0xA00000 if i == 0 else 0x0000A0, parent_list[i])
            shot.Velocity = vec * Quaternion(Vector3.UnitY, RAD * (i * 2 - 1) * task.ExecutedCount * 16) * 8
            shot.LifeSpan = 160
            shot.Spawn()
WORLD.AddTask(shot_dia, 10, 60, 0, True)
