# -*- coding: utf-8 -*-

way = 5
angle = RAD * 50

matrices = Matrix3(1, 0, 0, 0, 1, 0, 0, 0, 1), Matrix3(0, 1, 0, 0, 0, 1, 1, 0, 0), Matrix3(0, 0, 1, 1, 0, 0, 0, 1, 0)

vec_axis_list = []
for i in range(way):
	vec = Vector3.UnitZ * Matrix3.RotationX(angle) * Matrix3.RotationY(RAD * (360.0 / way) * i)
	axis1 = cross(vec, Vector3.UnitY)
	axis2 = cross(vec, axis1)
	vec *= Matrix3.RotationAxis(axis2, RAD * (360.0 / way) * -i)
	axis1 = cross(vec, axis2)
	
	for mat in matrices[0:1]:
		vec_axis_list.append((vec * mat, axis1 * mat, axis2 * mat))

def task():
	for vec, axis1, axis2 in vec_axis_list:
		for i in -1, 1:
			spell(
			vec = vec * i, upward = axis2,
			prop = ("SCALE", 0xA000A0 if i > 0 else 0x0000A0),
			distance = 1024,
			wait_time = 60.0,

			get_speed1 = lambda t: 8.0,
			get_speed2 = lambda t: 16.0,

			get_vec_rot = lambda t, begin = 12, end = -24, a = axis2: Quaternion.RotationAxis(a, RAD * (begin + (end - begin) * t)),
			init_mgc_rotate = Quaternion.Identity,
			get_mgc_rotate = lambda t, a1 = axis1, a2 = axis2: Quaternion.RotationAxis(a2 * Matrix3.RotationAxis(a1, RAD * t), RAD * 3.2),

			num_shot = 16, interval_shot = 1,
			num_task = 9, interval_task = 24,

			#停止するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
			#実際の停止するフレームは、中心に到達するまでに経過するフレーム * pause_frame_func(t)で求められる
			get_pause_frame = lambda t: 0.1 + t * 1.1,
			#再発進するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
			get_restart_frame = lambda t: 320 * (1 - t * 0.42),
			)
WORLD.AddTask(task, 0, 1, 0)
