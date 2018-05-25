# -*- coding: utf-8 -*-

def diffence_effect():
	vec = Vector3.UnitZ * HAND_BONE.WorldMat
	
	for i in range(128):
		particle = EntityShotStraight(WORLD, "DIA", 0x900070, Matrix4(Matrix3(0.1, 0.1, 2), Vector3(0, 0, -5)))
		particle.Pos = vec4(Vector3.UnitZ * -4) * HAND_BONE.WorldMat
		particle.Velocity = +Vector3(0, 1, uniform(0, 0.8)) * 12 * Matrix3.RotationZ(RAD * random() * 360) * HAND_BONE.WorldMat
		particle.LivingLimit = 20
		particle()
WORLD.AddTask(diffence_effect, 0, 45, 0)
