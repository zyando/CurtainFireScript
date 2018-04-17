# -*- coding: utf-8 -*-

veclist0 = objvertices("ico_y.obj", 0)
veclist1 = objvertices("ico.obj", 1)

def shot_mgc(axis):
	mgc_list = []

	def shot_to_target():
		if len(mgc_list) == 0: return True

		mgc = mgc_list.pop()

		shot = EntityShot(WORLD, "S", 0xFFFFFF)
		shot.Pos = mgc.WorldPos
		shot.Velocity = +(TARGET_BONE.WorldPos - mgc.WorldPos) * 4
		shot.LivingLimit = 300
		shot()
	WORLD.AddTask(shot_to_target, 8, 0, 0)

	for pos in veclist1:
		if abs(pos * axis) > 0.95: continue

		parent = EntityShot(WORLD, "BONE", 0)
		parent.GetRecordedRot = lambda e: e.Rot
		parent.Pos = TARGET_BONE.WorldPos

		def rotate1(parent = parent, rot = Quaternion.RotationAxis(pos ^ (pos ^ axis), RAD * 0.25)): parent.Rot *= rot
		parent.AddTask(rotate1, 4, 75, 0)

		def rotate2(parent = parent, rot = Quaternion.RotationAxis(pos ^ (pos ^ axis), RAD * 1)): parent.Rot *= rot
		parent.AddTask(rotate2, 4, 75, 300)

		parent()

		mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0x0000A0, parent)
		mgc.Pos = pos * 100
		mgc.LookAtVec = pos
		mgc.Upward = axis

		def move(mgc = mgc):
			mgc.Velocity = mgc.LookAtVec * 2
		mgc.AddTask(move, 0, 1, 300)

		def shot_dia(mgc = mgc, parent = parent):
			for vec in veclist0:
				dot = vec * Vector3.UnitY

				if dot > 0: continue

				shot = EntityShot(WORLD, "DIA", 0xA000A0 if dot < -0.9 else 0x0000A0)

				shot.Pos = mgc.WorldPos
				shot.Velocity = vec * Matrix3(1, 0, 0, 0, 0, 1, 0, 1, 0) * Matrix3(mgc.GetRecordedRot(mgc)) * parent.Rot * 8
				shot.LivingLimit = 120
				shot()
		mgc.AddTask(shot_dia, 4, 100, 0)
		mgc()

		mgc_list.append(mgc)
WORLD.AddTask(lambda: [shot_mgc(a) for a in [Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ]], 0, 1, 0)
