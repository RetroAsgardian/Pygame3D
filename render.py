#!/usr/bin/env python
import pygame, objects
class PerspectiveWindow:
	def __init__(self,loop_cb,width=800,height=600):
		pygame.init()
		self.surf = pygame.display.set_mode((width,height))
		pygame.display.set_caption("PerspectiveWindow")
		self.facegroups = {}
		self.cb = loop_cb
	def add_fg(self,fgname,fg):
		self.facegroups[fgname] = fg
	def run(self):
		running = True
		while running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
			self.cb()
			pygame.time.Clock().tick(50)
			self.surf.fill((0,0,0))
			for fg in self.facegroups.values():
				for face in fg.faces_prioritized():
					vxy = []
					for v in face.vertices:
						p = v.project(self.surf.get_width(),self.surf.get_height())
						x = int(p[0])
						y = int(p[1])
						vxy.append((x,y))
						#self.surf.fill((255,255,255),(x,y,2,2))
					vxy.append(vxy[0])
					pygame.draw.polygon(self.surf,face.color,vxy,0)
			pygame.display.flip()
if __name__ == "__main__":
	vertices = [
		objects.Vertex(-1, 1,-1), # front left  top    0
		objects.Vertex( 1, 1,-1), # front right top    1
		objects.Vertex( 1,-1,-1), # front right bottom 2
		objects.Vertex(-1,-1,-1), # front left  bottom 3
		objects.Vertex(-1, 1, 1), # back  left  top    4
		objects.Vertex( 1, 1, 1), # back  right top    5
		objects.Vertex( 1,-1, 1), # back  right bottom 6
		objects.Vertex(-1,-1, 1), # back  left  bottom 7
	]
	faces = [
		objects.Face([vertices[0],vertices[1],vertices[5],vertices[4]],(1,255,255)), # top
		objects.Face([vertices[2],vertices[3],vertices[7],vertices[6]]), # bottom
		objects.Face([vertices[1],vertices[2],vertices[6],vertices[5]],(255,255,1),True), # right
		objects.Face([vertices[0],vertices[3],vertices[7],vertices[4]],(255,1,255),True), # left
		objects.Face([vertices[0],vertices[1],vertices[2],vertices[3]],(1,255,1),True), # front
		objects.Face([vertices[4],vertices[5],vertices[6],vertices[7]],(255,127,1),True) # back
	]
	face_group = objects.FaceGroup(faces,0,0,0)
	face_group.offset()
	flipflop = 0
	counter = 0
	def _main_loop_cb():
		global shade_val, flipflop, counter
		face_group.unoffset()
		if flipflop == 0:
			face_group.rotate(1,0,0)
			counter += 1
		elif flipflop == 1:
			face_group.rotate(0,1,0)
			counter += 1
		elif flipflop == 2:
			face_group.rotate(0,0,1)
			counter += 1
		if counter >= 360:
			counter = 0
			flipflop += 1
		if flipflop > 2:	
			flipflop = 0
	face_group.offset()
	pw = PerspectiveWindow(_main_loop_cb)
	pw.add_fg("fg",face_group)
	pw.run()
