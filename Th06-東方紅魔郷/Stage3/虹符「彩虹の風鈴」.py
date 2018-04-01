# -*- coding: utf-8 -*-

COLORS = [0x00A0A0, 0xA0A000, 0x00A0A0, 0xA000A0, 0xA00000]

def task_to_shoot_while_rotating(vec, axis, num_pitch, num_yaw, angle_pitchyaw, shottype, angle_interval, speed, livinglimit):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0

	veclist = []

	rot_pitch = Matrix3.RotationAxis(vec ^ axis, angle_pitchyaw)
	rot_yaw = Matrix3.RotationAxis(axis ^ (vec ^ axis), angle_pitchyaw)

	for pitch in range(num_pitch):
		vec *= rot_pitch
		added_vec = vec * (rot_yaw ^ pitch)
		for yaw in range(num_yaw):
			added_vec *= rot_yaw
			veclist.append((added_vec, COLORS[(pitch + yaw) % len(COLORS)]))

	shot_dia_list = []

	for vec, color in veclist:
		binder = Entity(WORLD)
		binder.vec = vec

		def shot_dia(color = color, binder = binder, rot = Matrix3.RotationAxis(vec ^ (vec ^ axis), angle_interval)):
			shot = EntityShot(WORLD, shottype, color)
			shot.Velocity = binder.vec * speed
			shot.LivingLimit = livinglimit

			shot()

			binder.vec *= rot
		shot_dia_list.append(shot_dia)
	return lambda: [func() for func in shot_dia_list]

def get_color(vec):
	color = int(abs(vec.x) * 0xFF), int(abs(vec.y) * 0xFF), int(abs(vec.z) * 0xFF)
	return min(COLORS, key = lambda c: sum([pow(color[i] - (c >> i * 8 & 0xFF), 2) for i in range(3)]))

axislist = [Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ]

tasks = []

tasks.extend([task_to_shoot_while_rotating(v * i, a, 5, 8, RAD * 12 * i, "DIA", RAD * 8, 6, 160) for i in [1, -1] for v in [Vector3.UnitZ] for a in axislist])
tasks.extend([task_to_shoot_while_rotating(v, a, 2, 2, RAD * 8, "DIA", RAD * 14, 8, 120) for v in objvertices("ico.obj", 0) for a in [Vector3.UnitY]])
tasks.extend([task_to_shoot_while_rotating(v, a, 1, 1, 0, "DIA", RAD * 10, 4, 240) for v in objvertices("ico.obj", 0) for a in [Vector3.UnitX]])

def task_list():
	for task in tasks:
		task()
WORLD.AddTask(task_list, 4, 100, 0)
