# -*- coding: utf-8 -*-

way = 4
angle = RAD * 30

matrices = Matrix3(1, 0, 0, 0, 1, 0, 0, 0, 1), Matrix3(0, 1, 0, 0, 0, 1, 1, 0, 0), Matrix3(0, 0, 1, 1, 0, 0, 0, 1, 0)

vec_axis_list = []
for i in range(way):
	for j in 1, -1:
		vec = Vector3.UnitZ * j * Matrix3.RotationX(angle) * Matrix3.RotationY(RAD * (360.0 / way) * i)
		axis1 = cross(vec, Vector3.UnitY)
		axis2 = cross(vec, axis1)
		vec *= Matrix3.RotationAxis(axis2, RAD * (360.0 / way) * -i)
		axis1 = cross(vec, axis2)
		
		for mat in matrices[0:3]:
			vec_axis_list.append((vec * mat, axis1 * mat, axis2 * mat))

curve = CubicBezierCurve(Vector2(0, 0), Vector2(0.9, 0.1), Vector2(0.1, 0.5), Vector2(1, 1))

def task():
	for vec, axis1, axis2 in vec_axis_list:
		spell(
		vec = vec, upward = axis2,
		prop = ("SCALE", 0xA000A0 if vec.z > 0 else 0x0000A0, 1),
		distance = 1024,
		wait_time = 60.0,
		
		get_speed1 = lambda t: 8.0,
		get_speed2 = lambda t: 12.0,
		
		get_vec_rot = lambda t, axis2 = axis2, begin = 0.0, end = 18: Quaternion.RotationAxis(axis2, RAD * (begin + (end - begin) * curve.SolveYFromX(t))),

		init_mgc_rotate = Quaternion.Identity,
		get_mgc_rotate = lambda i, a1 = axis1, a2 = axis2: Quaternion.RotationAxis(a1 * Matrix3.RotationAxis(a2, RAD * 1.3 * i), RAD * 2.65),
		
		num_shot = 6, interval_shot = 2,
		num_task = 16, interval_task = 16,
		
		get_pause_frame = lambda t: 0.1 + t * 1.3,
		get_restart_frame = lambda t: 320 * (1 - t * 0.52),
		)
WORLD.AddTask(task, 0, 1, 0)
