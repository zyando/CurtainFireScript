# -*- coding: utf-8 -*-

def shot_dia():
	if YUKARI_SHOT_FLAG.Pos.y <= 1: return
	
	shot = EntityShotStraight(WORLD, "DIA", 0x800050, Vector3(0.5, 0.5, 12))
	shot.Pos = Vector4(0, 0, -20, 1) * YUKARI_HAND_BONE.WorldMat + vec4(randomvec() * random() * random() * 60)
	shot.Velocity = +(CENTER_BONE.WorldPos - YUKARI_HAND_BONE.WorldPos) * 30
	shot.LifeSpan = 100
	shot.Spawn()
WORLD.AddTask(lambda: [shot_dia() for i in range(4)], 0, 0, 0)
