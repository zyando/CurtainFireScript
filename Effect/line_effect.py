# -*- coding: utf-8 -*-

WORLD.FrameOffset = -1

pos_binder = {}

def spawn_particle(bone, interval = 0.5):
	pos = bone.WorldMat.Translation

	if bone.EntityId not in pos_binder or PARTICLE_CONTROLLER.Pos.x == 0:
		pos_binder[bone.EntityId] = pos
		return 
	
	prevpos = pos_binder[bone.EntityId]

	dis = (prevpos - pos).Length()
	num = max(1, int(dis / interval))

	for i in range(num):
		t = (1.0 / num) * i
		particle = EntityShot(WORLD, "PARTICLE", 0x404040, 0.5)
		particle.Pos = pos + (prevpos - pos) * t
		particle.LifeSpan = 30
		particle.Spawn()

		morph = particle.CreateVertexMorph(1, lambda v: -v)
		particle.AddMorphKeyFrame(morph, t / particle.LifeSpan, 0)
		particle.AddMorphKeyFrame(morph, 1, particle.LifeSpan)
	pos_binder[bone.EntityId] = pos
WORLD.AddTask(lambda: [spawn_particle(bone) for bone in OPTION_BALL_BONES], 0, 0, 0)