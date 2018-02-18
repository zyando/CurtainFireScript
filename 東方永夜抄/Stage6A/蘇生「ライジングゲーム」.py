# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(4)]

def phase0():
	root = EntityShot(WORLD, "BONE", 0xA0A0A0)
	root.LivingLimit = 180

	root.Velocity = (TARGET_BONE.WorldPos + randomvec() * 80 - root.Pos) * (1.0 / 60)
	root()

	def shot_around_target(task):
		root.Velocity = (TARGET_BONE.WorldPos + randomvec() * 80 - root.Pos) * (1.0 / 60)
		root.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 60)

		for idx, veclist in enumerate(veclists):
			for vec in veclist:
				pos = root.Pos + vec * (1 + idx) * 30

				if (pos - TARGET_BONE.WorldPos).Length() < 90: continue

				shot = EntityShot(WORLD, "S", 0x0000A0)
				shot.Pos = pos
				shot.LivingLimit = 150
				shot()
	WORLD.AddTask(shot_around_target, 60, 2, 60, True)

	for vec in Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ:
		mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0x808080, root)
		mgc.LivingLimit = 180
		mgc.LookAtVec = vec
		mgc()
#WORLD.AddTask(phase0, 180, 8, 0)



def task_to_shoot_while_rotating(vec, axis, shottype, color, specular, angle_interval, speed, livinglimit):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0

	axis = vec ^ (vec ^ axis)

	binder = Entity(WORLD)
	binder.vec = vec

	def shot_dia(rot = Matrix3.RotationAxis(axis, angle_interval)):
		shot = EntityShot(WORLD, shottype, color)
		shot.Velocity = binder.vec * speed
		shot.LivingLimit = livinglimit
		shot.ModelData.Materials[0].Shininess = specular
		shot()

		binder.vec *= rot
	return shot_dia

for vec in veclists[1]:
	for axis in Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ:
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "DIA", 0x400000, 130, RAD * 3, 4.0, 240), 2, 480, 90)
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "M", 0xA00000, 108, RAD * -4, 4.0, 240), 6, 160, 90)
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "L", 0xA00000, 0, RAD * 4, 6.0, 180), 10, 96, 90)
