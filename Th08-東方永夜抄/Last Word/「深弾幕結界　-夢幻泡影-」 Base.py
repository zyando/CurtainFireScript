# -*- coding: utf-8 -*-
import MMDataIO.Pmx

def spell(
	vec, upward, prop,
	distance,
	wait_time,
	get_speed1, get_speed2,
	get_vec_rot,
	init_mgc_rotate, get_mgc_rotate,
	num_shot, interval_shot,
	num_task, interval_task,
	get_pause_frame,
	get_restart_frame
	):
	
	start_frame = WORLD.FrameCount + wait_time
	
	total_num = interval_task * num_task
	total_num_inv = 1.0 / total_num
	
	distance_inv = 1.0 / distance
	
	parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
	parent.GetRecordedRot = lambda e: e.Rot
	parent.Rot = init_mgc_rotate
	parent.Spawn()
	
	circle = EntityShot(WORLD, "MAGIC_CIRCLE", 0xFFFFFF, 6)
	circle.Parent = parent
	circle.GetRecordedRot = lambda e: e.Rot
	circle.Velocity = vec * (distance / wait_time)
	circle.Rot = Matrix3.LookAt(vec, Vector3.UnitY)
	
	def stop(): circle.Velocity *= 0
	circle.AddTask(stop, 0, 1, wait_time)
	
	def go_out(): circle.Velocity = normalize(circle.Pos) * 12
	circle.AddTask(go_out, 0, 1, wait_time + interval_task * num_task)
	circle.Spawn()
	
	def add_shot_task():
		def shot_amulet():
			count = (WORLD.FrameCount - start_frame) * total_num_inv
			speed = get_speed1(count)
			
			shot = EntityShot(WORLD, *prop)
			shot.Pos = circle.WorldPos
			shot.Velocity = shot.Pos * distance_inv * get_vec_rot(count) * -speed
			shot.Upward = upward
			shot.LifeSpan = 1000
			
			def pause(velocity = shot.Velocity):
				if shot.Velocity == velocity: shot.Velocity *= 0
			shot.AddTask(pause, 0, 1, int(distance / speed * get_pause_frame(count)))
			
			def restart(vec = normalize(shot.Velocity)):
				shot.Velocity = vec * get_speed2(count)
			shot.AddTask(restart, 0, 1, int(get_restart_frame(count)))
			shot.Spawn()
		WORLD.AddTask(shot_amulet, interval_shot, num_shot, 0)
	WORLD.AddTask(add_shot_task, interval_task, num_task, wait_time)
	
	def rotate(task):
		parent.Rot = parent.Rot * get_mgc_rotate(task.ExecutedCount)
	WORLD.AddTask(rotate, 0, 1200, 1, True)
	
	def shot_amulet_outside():
		shot = EntityShot(WORLD, *prop)
		shot.Pos = circle.WorldPos
		shot.Velocity = normalize(circle.WorldPos) * 2.0
		shot.Upward = upward
		shot.LifeSpan = 1000
		shot.Spawn()
	circle.AddTask(shot_amulet_outside, 0, int(num_task * interval_task * 0.8), wait_time)
