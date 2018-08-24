# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(5)]

waiting = 225
phase_length = 1020 - waiting

binder = [Quaternion.RotationAxis(Vector3.UnitY, RAD * -10)]
def rotate(rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * (270.0 / phase_length))): binder[0] *= rot
WORLD.AddTask(rotate, 0, 0, waiting)

def shot_rice():
	for vec in veclists[2]:
		shot = EntityShot(WORLD, "RICE_M", 0xA00000)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = vec * binder[0] * 12
		shot.LifeSpan = 120
		shot.Spawn()
WORLD.AddTask(shot_rice, 5, 0, 0)

def shot_dia():
	for vec in veclists[4]:
		if vec.z > 0.9: continue
		
		shot = EntityShot(WORLD, "DIA_BRIGHT", 0x400000)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = vec * binder[0] * 12
		shot.LifeSpan = 120
		shot.Spawn()
WORLD.AddTask(shot_dia, 40, 0, 40)

veclist = [Vector3(sin(RAD * 50), 0, -cos(RAD * 50)) * Matrix3.RotationZ(RAD * 60 * i) for i in range(6)] + [-Vector3.UnitZ]
matlist = [Matrix3.LookAt(v, Vector3.UnitY) for v in veclist]

def shot_dia_to_target():
	vec = noramlize(REIMU_CENTER_BONE.WorldPos - CENTER_BONE.WorldPos)

	for mat in matlist:
		for i in range(3):
			shot = EntityShot(WORLD, "SCALE", 0x0000A0)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * mat * (1 + i * 0.5) * 6
			shot.LifeSpan = 400
			shot.Spawn()
WORLD.AddTask(shot_dia_to_target, 5, 0, 622)
