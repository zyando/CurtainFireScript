# -*- coding: utf-8 -*-
from random import random, randint, gauss, uniform

veclist = objvertices("ico.obj", 2)

def shot_dia():
	for vec in veclist:
		if vec.z > -0.8:
			shot = EntityShot(WORLD, "DIA", 0xA00000)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * 4
			shot.LifeSpan = 200
			shot()
WORLD.AddTask(shot_dia, 30, 15, 90)

def shot_magic_circle(level, pos, vec, color, shot_vec, upward):
	parent = EntityShot(WORLD, "MAGIC_CIRCLE", color)
	parent.Pos = pos
	parent.Velocity = vec * 6
	parent.LifeSpan = 15 * (level + 1)
	parent.SetMotionInterpolationCurve(Vector2(0.4, 0.6), Vector2(0.4, 0.6), parent.LifeSpan)
	
	def shot_amulet():
		shot = EntityShot(WORLD, "AMULET", color)
		shot.Pos = parent.Pos
		shot.Upward = upward
		shot.LookAtVec = shot_vec
		
		def move(): shot.Velocity = shot_vec * 4
		shot.AddTask(move, 0, 1, 60)
		shot.LifeSpan = 60 + 90
		shot()
	parent.AddTask(shot_amulet, 1, 0, 0)
	
	if level < 3:
		def divide():
			for axis in [Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ]:
				if abs(vec * axis) < 0.9:
					mat = Matrix3.RotationAxis(axis, RAD * 90)
					shot_magic_circle(level + 1, parent.Pos, vec * mat, color, shot_vec, upward)
		parent.AddTask(divide, 0, 1, parent.LifeSpan - 1)
	parent()

for vec in [(Vector3.UnitX, Vector3.UnitY), (Vector3.UnitY, Vector3.UnitZ)]:
	for i in range(2):
		for color in [(0xA00000, Vector3.UnitZ, 50), (0x0000A0, -Vector3.UnitZ, 0)]:
			def task(vec = vec, i = i, color = color): shot_magic_circle(0, CENTER_BONE.WorldPos, vec[0] * (i * 2 - 1), color[0], color[1], vec[1])
			WORLD.AddTask(task, 100, 3, color[2])
