# -*- coding: utf-8 -*-

veclist = []
objvertices("ico.obj", lambda v: veclist.append(v))

for vec in veclist:
	shot = EntityShot(WORLD, "S", 