# -*- coding: utf-8 -*-

def diffence_effect(task):
	for i in range(128):
		particle = EntityShot(WORLD, "DIA", 0xFFFFFF, Matrix4(Matrix3(0.1, 0.1, 2), Vector3(0, 0, -4)))
		particle.Pos = randomvec() * uniform(60, 80)
		particle.LivingLimit = randint(36, 38) - task.ExecutedCount
		particle.Velocity = -particle.Pos * (1.0 / particle.LivingLimit)
		particle.SetMotionInterpolationCurve(Vector2(0.7, 0.4), Vector2(0.9, 0.3), particle.LivingLimit + 1)
		particle()
WORLD.AddTask(diffence_effect, 0, 35, 0, True)
