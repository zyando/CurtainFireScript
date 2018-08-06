# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(3)]

def phase4():
	def shot_dia():
		mat = Matrix3.RotationAxis(randomvec(), RAD * 360 * random())
		
		for i in -1, 1:
			parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
			parent.Pos = CENTER_BONE.WorldPos
			parent.GetRecordedRot = lambda e: e.Rot

			def rotate(parent = parent, rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * 30 * i)): parent.Rot *= rot
			parent.AddTask(rotate, 0, 1, 120)
			parent.AddTask(lambda p = parent: p.AddRootBoneKeyFrame(), 0, 1, 60)

			parent()

			for vec in veclists[2]:
				shot = EntityShot(WORLD, "DIA_BRIGHT", 0x004000)
				shot.Pos = CENTER_BONE.WorldPos
				shot.Velocity = vec * mat * 2.0
				shot.LifeSpan = 60

				def replace(orgn = shot, parent = parent):
					shot = EntityShot(WORLD, "DIA", 0x00A000, parent)
					shot.Pos = orgn.Pos - CENTER_BONE.WorldPos
					shot.Velocity = orgn.Velocity
					shot.LifeSpan = 400

					def rotate(): shot.Velocity *= Matrix3(parent.Rot)
					shot.AddTask(rotate, 0, 1, 60)

					shot()
				shot.AddTask(replace, 0, 1, shot.LifeSpan)
				shot()
	WORLD.AddTask(shot_dia, 20, 13, 0)
WORLD.AddTask(phase4, 0, 1, 0)
