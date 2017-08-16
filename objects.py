#!/usr/bin/env python3
import math
class Vertex:
	def __init__(self,x,y,z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)
	def rotate_x(self, angle):
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		ny = self.y * cosa - self.z * sina
		nz = self.y * sina + self.z * cosa
		self.y = ny
		self.z = nz
	def rotate_y(self, angle):
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		nz = self.z * cosa - self.x * sina
		nx = self.z * sina + self.x * cosa
		self.x = nx
		self.z = nz
	def rotate_z(self, angle):
		rad = angle * math.pi / 180
		cosa = math.cos(rad)
		sina = math.sin(rad)
		nx = self.x * cosa - self.y * sina
		ny = self.x * sina + self.y * cosa
		self.x = nx
		self.y = ny
	def project(self, vp_width, vp_height, fov=256, vp_distance=4):
		factor = fov / (vp_distance + self.z)
		x = self.x * factor + vp_width / 2
		y = -self.y * factor + vp_height / 2
		return (x,y)
class Face:
	def __init__(self,vertices,color=(255,255,255),no_rotate=False):
		self.vertices = vertices
		self.dont_rotate = no_rotate
		self.color = [color[0],color[1],color[2]]
		self.shading = 1.0
	def shade(self,shading):
		self.shading *= shading
		for i in range(0,3):
			self.color[i] *= shading
			if self.color[i] > 255:
				self.color[i] = 255
			elif self.color[i] < 0:
				self.color[i] = 0
			self.color[i] = int(self.color[i])
	def unshade(self):
		shading = 1/self.shading
		self.shade(shading)
def do_depth_cull(face):
	avg_z = 0
	for v in face.vertices:
		avg_z += v.z
	avg_z /= len(face.vertices)
	return 0-avg_z
class FaceGroup:
	def __init__(self,faces,x,y,z):
		self.faces = faces
		self.xoff = x
		self.yoff = y
		self.zoff = z
	def shade(self,shading):
		for face in self.faces:
			face.shade(shading)
	def faces_prioritized(self): # depth culling
		return sorted(self.faces,key=do_depth_cull)
	def unshade(self):
		for face in self.faces:
			face.unshade()
	def offset(self):
		for face in self.faces:
			for vertex in face.vertices:
				vertex.x += self.xoff
				vertex.y += self.yoff
				vertex.z += self.zoff
	def unoffset(self):
		for face in self.faces:
			for vertex in face.vertices:
				vertex.x -= self.xoff
				vertex.y -= self.yoff
				vertex.z -= self.zoff
	def rotate(self,x,y,z):
		for face in self.faces:
			if face.dont_rotate:
				continue
			for vertex in face.vertices:
				vertex.rotate_x(x)
				vertex.rotate_y(y)
				vertex.rotate_z(z)
