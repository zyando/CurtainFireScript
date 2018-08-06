# -*- coding: utf-8 -*-
from random import random, randint, gauss, uniform

num_wave = 6

veclists = []
for i in range(num_wave): veclists.append([])

def bevel_vert(vert, connected, mult = 0.5 / (num_wave - 1)):
	sub = connected - vert
	for i in range(num_wave):
		veclists[i].append(+(vert + sub * (mult * i)))
ObjFile("ico.obj").divide(2).bevel(bevel_vert)

for i in range(num_wave):
	veclists[i] = set(veclists[i])

def shot_dia(pos, color, init_speed, spread_time, divergence_time):
	for i in range(len(veclists)):
		veclist = veclists[i]
		
		for vec in veclist:
			shot = EntityShot(WORLD, "DIA", color)
			shot.Pos = CENTER_BONE.WorldPos + pos
			shot.LifeSpan = divergence_time - WORLD.FrameCount + 55
			
			shot.Velocity = vec * init_speed
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 60)
			def pause(shot = shot, vec = vec, i = i): shot.Velocity *= 0
			shot.AddTask(pause, 0, 1, 40)
			
			def spread(shot = shot, vec = vec, i = i): 
				shot.Velocity = vec * i * 0.8
				shot.SetMotionInterpolationCurve(Vector2(0.6, 0.4), Vector2(0.4, 0.6), 30)
			shot.AddTask(spread, 0, 1, spread_time - WORLD.FrameCount)
			
			def convergence(shot = shot, vec = vec, i = i): 
				shot.Velocity = -vec * i * 0.8
				shot.SetMotionInterpolationCurve(Vector2(0.7, 0.3), Vector2(0.7, 0.3), 30)
			shot.AddTask(convergence, 0, 1, spread_time - WORLD.FrameCount + 30)
			
			shot.AddTask(pause, 0, 1, spread_time - WORLD.FrameCount + 60)
			
			def divergence(shot = shot, vec = vec, i = i): shot.Velocity = vec * 20
			shot.AddTask(divergence, 0, 1, divergence_time - WORLD.FrameCount)
			shot()
WORLD.AddTask(lambda: shot_dia(Vector3(0, 0, 0), 0x0000A0, 3.0, 70, 140), 0, 1, 0)

WORLD.AddTask(lambda: shot_dia(Vector3(0, 0, 0), 0x0000A0, 3.0, 240, 320), 0, 1, 170)
WORLD.AddTask(lambda: shot_dia(Vector3(20, 20, -20), 0xA00000, 3.0, 250, 320), 0, 1, 180)

WORLD.AddTask(lambda: shot_dia(Vector3(0, 40, 60), 0x0000A0, 3.0, 430, 520), 0, 1, 350)
WORLD.AddTask(lambda: shot_dia(Vector3(-60, -30, -20), 0xA00000, 3.0, 440, 520), 0, 1, 360)
WORLD.AddTask(lambda: shot_dia(Vector3(60, -30, -20), 0xA00000, 3.0, 450, 520), 0, 1, 370)

WORLD.AddTask(lambda: shot_dia(Vector3(100, 0, -200), 0xA00000, 3.0, 640, 710), 0, 1, 560)
WORLD.AddTask(lambda: shot_dia(Vector3(-100, 0, -140), 0x0000A0, 3.0, 680, 750), 0, 1, 600)
WORLD.AddTask(lambda: shot_dia(Vector3(100, 0, -80), 0xA00000, 3.0, 720, 790), 0, 1, 640)
WORLD.AddTask(lambda: shot_dia(Vector3(-100, 0, -20), 0x0000A0, 3.0, 760, 830), 0, 1, 680)
WORLD.AddTask(lambda: shot_dia(Vector3(100, 0, 40), 0xA00000, 3.0, 800, 870), 0, 1, 720)

WORLD.AddTask(lambda: shot_dia(Vector3(0, 0, 0), 0x0000A0, 3.0, 980, 1090), 0, 1, 900)
WORLD.AddTask(lambda: shot_dia(Vector3(0, 0, 0), 0xA00000, 3.5, 990, 1090), 0, 1, 910)
WORLD.AddTask(lambda: shot_dia(Vector3(0, 0, 0), 0xA000A0, 4.0, 1000, 1090), 0, 1, 920)
WORLD.AddTask(lambda: shot_dia(Vector3(0, 0, 0), 0xA00000, 4.5, 1010, 1090), 0, 1, 930)
WORLD.AddTask(lambda: shot_dia(Vector3(0, 0, 0), 0xA000A0, 5.0, 1020, 1090), 0, 1, 940)

WORLD.MaxFrame = 1200
