# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 1)

def f(x): return x ** 3 / 3.0 - x ** 2 -24 * x

def pow_(x, p): return abs(x) ** p * (1 if x > 0 else -1)

cos_binder = [Vector3.UnitZ, Matrix3.RotationY(RAD * 0.25)]
vec_binder = [Vector3.UnitY, Matrix3.RotationAxis(randomvec() ^ Vector3.UnitY, RAD * 1)]
rot_binder = [Matrix3.Identity]

def shot_dia():
	for vec in veclist:
		shot = EntityShotStraight(WORLD, "DIA", 0xFF40FF)
		shot.Velocity = vec * rot_binder[0] * 8
		shot.LifeSpan = 80
		shot.Spawn()
	cos_binder[0] = +(cos_binder[0] * cos_binder[1])
	vec_binder[0] = +(vec_binder[0] * vec_binder[1])
	
	rot_binder[0] *= Matrix3.RotationAxis(vec_binder[0], pow_(RAD * f(cos_binder[0].z * 10) * 0.25, 1.5))
WORLD.AddTask(shot_dia, 0, 900, 0)
