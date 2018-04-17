# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(3)]

#phase_start_frame = 3428 + WORLD.FrameCount
#phase_finish_frame = 4366 - 120
phase_start_frame = 1860
phase_finish_frame = 2220
phase_length = phase_finish_frame - phase_start_frame

WORLD.FrameCount = phase_start_frame #- 322
WORLD.MaxFrame = phase_length + 400

def phase4():
	parent_list = []

	for i in -1, 1:
		parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
		parent.GetRecordedRot = lambda e: e.Rot
		def rotate(parent = parent, rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * 179.5 * i)):
			parent.Rot *= rot
		parent.AddTask(rotate, 360, 3, 0)
		parent()

		parent_list.append(parent)

	def shot_dia():
		for i in -1, 1:
			parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
			parent.GetRecordedRot = lambda e: e.Rot

			def rotate(parent = parent, rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * 30 * i)): parent.Rot *= rot
			parent.AddTask(rotate, 0, 1, 120)
			parent.AddTask(lambda p = parent: p.AddRootBoneKeyFrame(), 0, 1, 60)

			parent()

			mat = Matrix3.RotationAxis(randomvec(), RAD * 360 * random())

			for vec in veclists[2]:
				shot = EntityShot(WORLD, "DIA_BRIGHT", 0x004000)
				shot.Velocity = vec * mat * 2.0
				shot.LivingLimit = 60

				def replace(orgn = shot, parent = parent):
					shot = EntityShot(WORLD, "DIA", 0x00A000, parent)
					shot.Pos = orgn.Pos
					shot.Velocity = orgn.Velocity
					shot.LivingLimit = 400

					def rotate(): shot.Velocity *= Matrix3(parent.Rot)
					shot.AddTask(rotate, 0, 1, 60)

					shot()
				shot.AddTask(replace, 0, 1, shot.LivingLimit)
				shot()
	WORLD.AddTask(shot_dia, 15, phase_length / 15, 0)
WORLD.AddTask(phase4, 0, 1, 0)
