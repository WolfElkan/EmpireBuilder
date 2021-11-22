from numpy import linalg
from numpy.matrixlib.defmatrix import matrix

class Matrix(matrix):
	def __init__(self, *args, **kwargs):
		super(Matrix, self).__init__(*args, **kwargs)
	def __invert__(self):
		return linalg.inv(self)
	def inv(self):
		return self.__invert__()

class Point(object):
	"""docstring for Point"""
	def __init__(self, *coords):
		super(Point, self).__init__()
		self.coords = coords
	def __getattribute__(self, attr):
		if attr == 'x':
			return self.coords[0]
		elif attr == 'y':
			return self.coords[1]
		else:
			return super(Point, self).__getattribute__(attr)
	def __getitem__(self, index):
		return self.coords[index]
	def __iter__(self):
		for c in self.coords:
			yield c
	def __len__(self):
		return len(self.coords)
	def a(self):
		return self.coords
	def m(self):
		return Matrix([ [c] for c in self.coords ])
	def floatify(self):
		return Point(*[ float(c) for c in self.coords ])
	def __str__(self):
		return "({})".format(','.join(
			[ str(c) if c % 1 else str(int(c)) for c in self.coords ]
		))
	def __repr__(self):
		return self.__str__()
	def __add__(self, other):
		if type(other) is Point:
			return Point(*[ self[k] + other[k] for k in xrange(len(self)) ])
		elif type(other) in [Matrix, matrix]:
			other = other.tolist()
			return Point(*[ self[k] + other[k][0] for k in xrange(len(self)) ])
	def __sub__(self, other):
		if type(other) is Point:
			return Point(*[ self[k] - other[k] for k in xrange(len(self)) ])
		elif type(other) in [Matrix, matrix]:
			other = other.tolist()
			return Point(*[ self[k] - other[k][0] for k in xrange(len(self)) ])
	def __mul__(self, other):
		if type(other) in [int, long, float]:
			return Point(*[ c * other for c in self ])
	def __div__(self, other):
		if type(other) in [int, long]:
			other = float(other)
		if type(other) in [float]:
			return Point(*[ c / other for c in self ])	
		if type(other) is Simplex:
			other = other.matrix
		if type(other) is Matrix:
			return other.__invert__() * self.m()
	def __eq__(self, other):
		if type(other) is not Point:
			return False
		if len(other) != len(self):
			return False
		for k in range(len(self)):
			if self[k] != other[k]:
				return False
		return True
	@staticmethod
	def weightedAverage(*tuples):
		total_weight = sum([ weight for point, weight in tuples ])
		total_point = sum(
			[ point*weight for point, weight in tuples[1:] ],
			tuples[0][0] * tuples[0][1]
		)
		return total_point / total_weight


class PointMap(object):
	"""An object containing two points.  point0 should map to point1"""
	def __init__(self, point0, point1):
		super(PointMap, self).__init__()
		self.point0 = point0.floatify()
		self.point1 = point1.floatify()
	def __str__(self):
		return "{} -> {}".format(self.point0, self.point1)
	def __repr__(self):
		return self.__str__()
	def a(self, num):
		if num == 0:
			return self.point0.coords
		elif num == 1:
			return self.point1.coords
	def m(self, num):
		return mat([self.a(num)])
	def p(self, num):
		return Point(*self.a(num))

class SimplexMap(object):
	"""docstring for SimplexMap"""
	def __init__(self, *pointmaps):
		super(SimplexMap, self).__init__()
		self.simplex0 = Simplex(*[ pm.point0 for pm in pointmaps ])
		self.simplex1 = Simplex(*[ pm.point1 for pm in pointmaps ])
	def translate(self, point):
		point -= self.simplex0.origin
		generic = point / self.simplex0
		result = self.simplex1.matrix * generic
		return self.simplex1.origin + result
		print result
	def __str__(self):
		return "{} -> {}".format(self.simplex0, self.simplex1)

class Simplex(object):
	"""docstring for Simplex"""
	def __init__(self, *points):
		super(Simplex, self).__init__()
		self.points = points
		self.origin = points[0]
		self.basis = [ p - points[0] for p in points[1:] ]
		self.matrix = Matrix([ b.a() for b in self.basis ]).transpose()
	def contains(self, guest):
		if type(guest) is Point:
			pass
	def encircles(self, point):
		pass
	def __str__(self):
		return "<{}>".format(''.join([ str(p) for p in self.points ]))