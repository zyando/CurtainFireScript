# -*- coding: utf-8 -*-

way = 3
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
			vec_axis_list.append((vec * mat, axis1 * mat * j, axis2 * mat))

def task():
	for vec, axis1, axis2 in vec_axis_list:
		for i in [1, 1.1]:
			spell(
			vec = vec, upward = axis2,
			prop = ("AMULET", 0xA000A0 if vec.z > 0 else 0xA00000),
			distance = 1024,
			wait_time = 60.0,
			
			get_speed1 = lambda t, i = i: 8.0 + t * i * 1,
			get_speed2 = lambda t: 16.0,
			
			get_vec_rot = lambda t, axis = axis1, begin = 0, end = 16: Matrix3.RotationAxis(axis, RAD * (begin + (end - begin) * t)),

			init_mgc_rotate = Quaternion.Identity,
			get_mgc_rotate = lambda r, i, a1 = axis1, a2 = axis2, a3 = vec: 
			Quaternion.RotationAxis(a1, math.pi * 2 * cos(i * RAD * 0.2) * sin(i * RAD * 1)) * 
			Quaternion.RotationAxis(a2, math.pi * 2 * sin(i * RAD * 0.2) * sin(i * RAD * 1)),

			num_shot = 220, interval_shot = 1,
			num_task = 1, interval_task = 220,
			
			get_pause_frame = lambda t: 0.1 + t * 2,
			get_restart_frame = lambda t: 320 * (1 - t * 0.4),
			)
	
	for vec, axis1, axis2 in vec_axis_list:
		spell(
		vec = vec, upward = axis2,
		prop = ("AMULET", 0x0000A0),
		distance = 900,
		wait_time = 60.0,
		
		get_speed1 = lambda t: 8.0,
		get_speed2 = lambda t: 16.0,
		
		get_vec_rot = lambda t, axis = axis1, begin = 0, end = -10: Quaternion.RotationAxis(axis, RAD * (begin + (end - begin) * t)),

		init_mgc_rotate = Quaternion.Identity,
		get_mgc_rotate = lambda r, i, a1 = -axis1: Quaternion.RotationAxis(a1, RAD * 3 * i),
		
		num_shot = 3, interval_shot = 1,
		num_task = 21, interval_task = 10,
		
		get_pause_frame = lambda t: 0.1 + t * 1.0,
		get_restart_frame = lambda t: 350 * (1 - t * 0.5),
		)
WORLD.AddTask(task, 0, 1, 0)
