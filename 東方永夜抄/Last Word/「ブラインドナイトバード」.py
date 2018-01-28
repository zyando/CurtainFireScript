# -*- coding: utf-8 -*-
from random import random

axis1 = Vector3(1, 0, 0)
mat = Matrix3.RotationAxis(axis1, RAD * 12)

matlist1 = [~mat ^ 2, ~mat, Matrix3.Identity, mat, mat ^ 2]

axis2 = Vector3(-axis1.x, axis1.y, axis1.z)
mat = Matrix3.RotationAxis(axis2, RAD * 12)

matlist2 = [~mat ^ 2, ~mat, Matrix3.Identity, mat, mat ^ 2]

def world_task(color, angle, angle_offset, axis, matlist, way = 14):
	frame = Frame(Vector3.UnitZ * (~rot ^ (way / 2 + angle_offset / angle)), Quaternion.RotationAxis(axis, angle * 10))
	
	def shot_scale():
		for mat in matlist:
			for i in range(8):
				shot = EntityShot(WORLD, "SCALE", color)
				shot.Velocity = frame.vec * mat * (1 + i * 0.1) * 3.4
				shot.Pos = OWNER_BONE.WorldPos
				shot()
		frame.vec = frame.vec * frame.rot
	WORLD.AddTask(shot_scale, 2, way, 0)
WORLD.AddTask(lambda: world_task(0x0000A0, RAD, RAD * 50, axis1 ^ Vector3.UnitZ, matlist1), 64, 2, 0)
WORLD.AddTask(lambda: world_task(0x00A0A0, RAD, RAD * 50, axis2 ^ Vector3.UnitZ, matlist2), 64, 2, 16)