# -*- coding: utf-8 -*-
from MMDataIO.Pmx import BoneFlags

shot_range = 800

def shot_randomvec(shottype, color, parent, link_parent, speed):
    shot = EntityShot(WORLD, shottype, color, parent)
    shot.Velocity = randomvec() * speed
    shot.Upward = randomvec()
    shot.LivingLimit = shot_range / speed

    if link_parent != None:
        shot.RootBone.LinkParentId = link_parent.RootBone.BoneId
        shot.RootBone.LinkWeight = 1.0
        shot.RootBone.Flag |= BoneFlags.LOCAL_LINK
    shot()

parentlist = [EntityShot(WORLD, "BONE", 0) for i in range(2)]

for idx, parent in enumerate(parentlist):
    parent.GetRecordedRot = lambda e: e.Rot

    def rotate(p = parent, rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * (idx * 2 - 1) * 90)): p.Rot *= rot
    parent.AddTask(rotate, 180, 0, 0)
    parent()

WORLD.AddTask(lambda: [shot_randomvec("BUTTERFLY", 0x0000A0, None, None, uniform(3, 8)) for i in range(8)], 0, 80, 0)
WORLD.AddTask(lambda: [shot_randomvec("M", 0x00A0A0, None, parentlist[0], uniform(3, 8)) for i in range(9)], 0, 80, 95)
WORLD.AddTask(lambda: [shot_randomvec("KNIFE", 0x00A000, parentlist[1], None, uniform(3, 8)) for i in range(10)], 0, 80, 180)
WORLD.AddTask(lambda: [shot_randomvec("STAR_S", 0xA0A000, parentlist[0], None, uniform(3, 8)) for i in range(11)], 0, 80, 250)
WORLD.AddTask(lambda: [shot_randomvec("RICE_M", 0xA00000, parentlist[1], None, uniform(3, 8)) for i in range(12)], 0, 80, 320)
WORLD.AddTask(lambda: [shot_randomvec("AMULET", 0xA000A0, parentlist[0], None, uniform(3, 8)) for i in range(13)], 0, 80, 390)
