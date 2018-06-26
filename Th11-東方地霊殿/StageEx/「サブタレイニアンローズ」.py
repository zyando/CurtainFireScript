# -*- coding: utf-8 -*-

rose_poslist, linelist = objlines("rose_lowpolygon2.obj")

def shot_rose(shot_factory, rose_rot, scale, blooming_frame, livinglimit):
	for pos in rose_poslist:
		shot = shot_factory()
		shot.Velocity = pos * rose_rot * scale * (1.0 / blooming_frame)
		shot.LivingLimit = livinglimit
		shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), blooming_frame)
		
		def stop(shot = shot): shot.Velocity *= 0
		shot.AddTask(stop, 0, 1, blooming_frame)
		
		shot()

way = 32

def shot_s(world, color, rotangle, way = 32):
	shotlist = []
	
	mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 180)
	
	for vec in [Vector3.UnitZ * Matrix3.RotationY(RAD * 360.0 / way * i * rotangle) for i in range(way)]:
		shot = EntityShot(world, "S", color)
		shot.Velocity = vec * mat * 1.6
		shot.LivingLimit = 330
		shot()
		shotlist.append(shot)
	
	def shot_rose_task(task):
		parent = shotlist[task.ExecutedCount % way]
		shot_rose(lambda: EntityShot(world, "S", color, 0.6, parent), Matrix3.LookAt(+parent.Velocity, randomvec()), 0.6, 8, 12)
	WORLD.AddTask(shot_rose_task, 3, 100, 20, True)
	
WORLD.AddTask(lambda w = CreateWorld("「サブタレニアンローズ」 BlueRose"): shot_s(w, 0x0000A0, 1), 180, 2, 0)
WORLD.AddTask(lambda w = CreateWorld("「サブタレニアンローズ」 RedRose"): shot_s(w, 0xA00000, -1), 180, 2, 90)
