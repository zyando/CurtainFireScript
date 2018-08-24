# -*- coding: utf-8 -*-

COLORS = 0xE60012, 0xF39800, 0xFFF100, 0x009944, 0x0068B7, 0x1D2088, 0x920783 

way = 16
angle = RAD * 30

matrices = Matrix3(1, 0, 0, 0, 1, 0, 0, 0, 1), Matrix3(0, 1, 0, 0, 0, 1, 1, 0, 0), Matrix3(0, 0, 1, 1, 0, 0, 0, 1, 0)

vec_axis_list = []
for i in range(way):
	vec = Vector3.UnitZ * Matrix3.RotationX(angle) * Matrix3.RotationY(RAD * (360.0 / way) * i)
	axis = cross2(vec, Vector3.UnitY)
	vec *= Matrix3.RotationAxis(axis, RAD * (360.0 / way) * -i)
	
	for mat in matrices[0:1]:
		vec_axis_list.append((vec * mat, axis * mat))

def laser_task(vec, axis):
	def shot_laser(binder = [vec], rot = Quaternion.RotationAxis(axis, RAD * 8)):
		shot = EntityShot(WORLD, "SCALE", COLORS[randint(0, len(COLORS) - 1)], Vector3(1, 1, 20))
		shot.Pos = binder[0] * 80 * gauss(1, 0.2)
		shot.Velocity = binder[0] * Matrix3.RotationAxis(randomvec(), RAD * 20 * gauss()) * 16
		shot.Upward = randomvec()
		shot.LifeSpan = 120
		shot.Spawn()
		
		binder[0] *= rot
	WORLD.AddTask(shot_laser, 3, 26, 0)

def s_task():
	def shot_s():
		shot = EntityShot(WORLD, "S", COLORS[randint(0, len(COLORS))])
		shot.Pos = randomvec() * 200 * gauss()
		shot.Velocity = Vector3.UnitZ * Quaternion.RotationAxis(randomvec(), RAD * gauss(20)) * 5
		shot.LifeSpan = 300
		
		def acc(a = Vector3(0, 0, -shot.Velocity.Length() / 30 * 2)): shot.Velocity += a
		shot.AddTask(acc, 0, 30, 0)
		shot.Spawn()
	WORLD.AddTask(lambda: [shot_s() for i in range(16)], 0, 60, 0)

for vec, axis in vec_axis_list:
	for i in 1, -1:
		WORLD.AddTask(lambda v = vec, a = axis * i: laser_task(v, a), 100, 3, 0)
WORLD.AddTask(s_task, 100, 3, 0)
