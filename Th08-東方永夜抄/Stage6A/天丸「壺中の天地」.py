# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 1)

anglelist = [(RAD * a, color) for a, color in [(80, 0x0000A0), (70, 0x0000A0), (10, 0xA000A0), (-10, 0xA000A0), (-70, 0xA00000), (-80, 0xA00000)]]

def shot_mgc(axis):
	mgc_list = []

	def shot_to_target():
		if len(mgc_list) == 0: return True

		mgc = mgc_list.pop()

		shot = EntityShot(WORLD, "S", 0xFFFFFF)
		shot.Pos = mgc.WorldPos
		shot.Velocity = +(TARGET_BONE.WorldPos - mgc.WorldPos) * 4
		shot.LifeSpan = 300
		shot.Spawn()
	WORLD.AddTask(shot_to_target, 8, 0, 0)

	for pos in veclist:
		if abs(pos * axis) > 0.95: continue

		parent = EntityShot(WORLD, "BONE", 0)
		parent.GetRecordedRot = lambda e: e.Rot
		parent.Pos = TARGET_BONE.WorldPos

		def rotate(parent = parent, rot = Quaternion.RotationAxis(pos ^ (pos ^ axis), RAD * 0.5)): parent.Rot *= rot
		parent.AddTask(rotate, 4, 75, 300)

		parent()

		mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0x000080, parent)
		mgc.Pos = pos * 100
		mgc.LookAtVec = pos
		mgc.Upward = axis

		def move(mgc = mgc):
			mgc.Velocity = mgc.LookAtVec * 2
		mgc.AddTask(move, 0, 1, 300)

		def shot_dia(mgc = mgc, parent = parent, axis = pos ^ (pos ^ axis)):
			for angle, color in anglelist:
				shot = EntityShot(WORLD, "DIA", color)

				shot.Pos = mgc.WorldPos
				shot.Velocity = +mgc.Pos * parent.LocalMat * Matrix3.RotationAxis(axis, angle) * 8
				shot.LifeSpan = 120
				shot.Spawn()
		mgc.AddTask(shot_dia, 4, 100, 0)
		mgc()

		mgc_list.append(mgc)
WORLD.AddTask(lambda: [shot_mgc(a) for a in [Vector3.UnitX, Vector3.UnitZ]], 0, 1, 0)
