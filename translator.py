from numpy import array
from scipy.spatial import Delaunay
from transform import Point, PointMap, SimplexMap, WASM
from csv import csv
from datetime import datetime

class Translator(object):
	"""docstring for Translator"""
	def __init__(self, *pointmaps):
		super(Translator, self).__init__()
		self.pointmaps = pointmaps
		self.delaunay = Delaunay(array([ pm.a(0) for pm in pointmaps ]))
		self.simplexmaps = [ SimplexMap(*[ pointmaps[i] for i in s ]) for s in self.delaunay.simplices ]
	def piecewise(self, point):
		for pm in self.pointmaps:
			if point == pm.point0:
				return pm.point1
		index = self.delaunay.find_simplex(point.a())
		if index >= 0:
			return self.simplexmaps[index].translate(point)
	def broadcast(self, point):
		for pm in self.pointmaps:
			if point == pm.point0:
				return pm.point1
		vertices = []
		for s in xrange(len(self.simplexmaps)):
			sm = self.simplexmaps[s]
			for p in xrange(len(sm.simplex0)):
				spoint = sm.simplex0[p]
				pindex = self.delaunay.simplices[s][p]
				weight = self.pointmaps[pindex].weight
				weight *= abs(point - spoint) ** -2
				vertices.append((sm,weight))
		# hybrid = SimplexMap.weightedAverage(vertices)
		hybrid = WASM(*vertices)
		# print hybrid
		return hybrid.translate(point)