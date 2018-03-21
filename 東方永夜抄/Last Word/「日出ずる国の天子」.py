# -*- coding: utf-8 -*-

target = Vector3(0, 0, 80)

wayVerti = 10
wayHoriz = 20

matVerti = Matrix3.RotationAxis(Vector3.UnitX, RAD * (180 / (wayVerti + 2)))
matHoriz = Matrix3.RotationAxis(Vector3.UnitY, RAD * (360 / wayHoriz))

veclist1 = []
veclist2 = []
vec1 = Vector3(0, -1, 0)

for i in range(wayVerti):
	vec1 = vec1 * matVerti
	veclist2.append(vec1)

for i in range(wayHoriz):
	veclist2 = map(lambda v: v * matHoriz, veclist2)
	veclist1.append(veclist2)

def world_task_func1():
	vecStack = veclist1[:]

	def shot_laser():
		veclist2 = vecStack.pop()

		for vec in veclist2:
			shot = EntityShot(WORLD, "LASER_LINE", 0x0000A0, Vector3(1, 1, 4000))

			morph = shot.CreateVertexMorph(lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
			shot.AddMorphKeyFrame(morph, 1, 0)
			shot.AddMorphKeyFrame(morph, 1, 59)
			shot.AddMorphKeyFrame(morph, 0, 60)
			shot.AddMorphKeyFrame(morph, 0, 120)

			shot.GetRecordedRot = lambda e: e.Rot
			shot.Pos = CENTER_BONE.WorldPos
			shot.Rot = Matrix3.LookAt(vec, Vector3.UnitY)

			shot.LivingLimit = 120
			shot()
	WORLD.AddTask(shot_laser, 2, wayHoriz, 0)
WORLD.AddTask(world_task_func1, 200, 2, 0)

def world_task_func3():
	mat = Matrix3.RotationAxis(Vector3.UnitY, RAD * 180 / wayHoriz)
	vecStack = veclist1[:]
	vecStack.reverse()

	def shot_laser():
		veclist2 = vecStack.pop()

		for vec in veclist2:
			vec = vec * mat

			shot = EntityShot(WORLD, "LASER_LINE", 0xA00000, Vector3(1, 1, 4000))

			morph = shot.CreateVertexMorph(lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
			shot.AddMorphKeyFrame(morph, 1, 0)
			shot.AddMorphKeyFrame(morph, 1, 59)
			shot.AddMorphKeyFrame(morph, 0, 60)
			shot.AddMorphKeyFrame(morph, 0, 120)

			shot.GetRecordedRot = lambda e: e.Rot
			shot.Pos = CENTER_BONE.WorldPos
			shot.Rot = Matrix3.LookAt(vec, Vector3.UnitY)

			shot.LivingLimit = 120
			shot()
	WORLD.AddTask(shot_laser, 2, wayHoriz, 0)
WORLD.AddTask(world_task_func3, 200, 2, 40)

veclist3 = [+Vector3(-1, 1, 1), +Vector3(1, 1, -1), +Vector3(1, -1, 1), +Vector3(-1, -1, -1)]

for vec in veclist3:
	poslist = [Vector3(40, 40, 0), Vector3(-40, 40, 0), Vector3(40, -40, 0), Vector3(-40, -40, 0)]
	rot = Quaternion.RotationAxis(vec ^ (vec ^ Vector3.UnitY), RAD * 30)
	rotlist = [rot, ~rot] * 2

	for pos, rot in zip(poslist, rotlist):
		parentShot1 = EntityShot(WORLD, "BONE", 0xFFFFFF)
		parentShot1.Pos = CENTER_BONE.WorldPos + pos
		parentShot1.GetRecordedRot = lambda e: e.Rot
		parentShot1()

		parentShot2 = EntityShot(WORLD, "MAGIC_CIRCLE", 0xFFFFFF, parentShot1)
		parentShot2.GetRecordedRot = lambda e: e.Rot
		parentShot2.Pos = vec * 12
		parentShot2.Rot = Matrix3.LookAt(vec, Vector3.UnitY)
		parentShot2()

		def shot_butterfly(parentShot1 = parentShot1, parentShot2 = parentShot2, rot = rot):
			parentShot1.Rot *= rot

			shot = EntityShot(WORLD, "BUTTERFLY", 0x0000A0)
			shot.Pos = parentShot2.WorldPos
			shot.Velocity = +(parentShot2.WorldPos - parentShot1.WorldPos) * -1.0
			shot()

			shot = EntityShot(WORLD, "BUTTERFLY", 0xA00000)
			shot.Pos = parentShot2.WorldPos
			shot.Velocity = +(TARGET_BONE.WorldPos - shot.Pos) * 1.0
			shot()
		parentShot1.AddTask(shot_butterfly, 10, 30, 0)
