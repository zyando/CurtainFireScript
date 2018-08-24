# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 3)

parent_list = []
for i in -1, 1:
	parent = EntityShot(WORLD, "BONE", 0)
	parent.Pos = CENTER_BONE.WorldPos
	parent.GetRecordedRot = lambda e: e.Rot

	def rotate(parent = parent, rot = Quaternion.RotationAxis(Vector3.UnitY * i, RAD * 90)): parent.Rot *= rot
	parent.AddTask(rotate, 180, 4, 180)
	parent.Spawn()
	parent_list.append(parent)

def phase0():
	shot = EntityShot(WORLD, "L", 0xFF0000)
	shot.Pos = CENTER_BONE.WorldPos
	shot.Velocity = normalize(TARGET_BONE.WorldPos - shot.Pos) * 3
	shot.LifeSpan = 240
	shot.Spawn()

	def shot_dia(task):
		for vec in veclist:
			shot = EntityShot(WORLD, "DIA", 0x404080, parent_list[task.ExecutedCount % 2])
			shot.Velocity = vec * ~shot.ParentEntity.Rot * 3
			shot.LifeSpan = 320
			shot.Spawn()
	WORLD.AddTask(shot_dia, 8, 20, 0, True)
WORLD.AddTask(phase0, 220, 3, 0)
