# -*- coding: utf-8 -*-
from System.Collections.Generic import List
from MikuMikuPlugin import *

STEP = 2

if SCENE.ActiveModel == None: exit()

model = SCENE.ActiveModel

for bone in model.Bones:
	for layer in bone.SelectedLayers:
		if len([f for f in layer.Frames if f.Selected]) < 2: continue
		
		startframe = layer.SelectedFrames.GetEnumerator().Current
		endframe = None
		
		for frame in reversed(layer.Frames):
			if frame.Selected:
				endframe = frame
		
		frames = [layer.GetFrame(i) for i in range(startframe.FrameNumber, endframe.FrameNumber + 1, STEP)]
		
		for frame_num in range(startframe.FrameNumber, endframe.FrameNumber + 1):
			layer.RemoveKeyFrame(frame_num)
		
		layer.AddKeyFrame(List[MotionFrameData](frames))
