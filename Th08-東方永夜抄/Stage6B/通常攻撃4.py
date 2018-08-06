# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 0)

def task(vec, axis):
	def shot_task(binder = [vec], rot = Matrix3.RotationAxis(vec ^ (vec ^ axis), RAD * 16)):
		shot = EntityShot(WORLD, "RICE_M", 0x0000A0)
		shot.Velocity = binder[0] * 6
		shot.LifeSpan = 100
		shot.SetMotionInterpolationCurve(Vector2(0.3, 0.9), Vector2(0.5, 0.95), shot.LifeSpan)
		
		def replace(org = shot):
			shot = EntityShotStraight(WORLD, "RICE_M", 0xA00000)
			shot.Pos = org.Pos
			shot.Velocity = +org.Velocity * Matrix3.RotationAxis(randomvec() ^ org.Velocity, math.pi * gauss(0, 0.5)) * -2
			shot.LifeSpan = 300
			shot()
		shot.AddTask(replace, 0, 1, shot.LifeSpan)
		shot()
		
		binder[0] *= rot
	WORLD.AddTask(shot_task, 4, 100, 1)

for vec in veclist:
	for axis in Vector3.Units:
		task(vec, axis)
