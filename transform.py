from numpy import linalg
from numpy.matrixlib.defmatrix import matrix

class Matrix(matrix):
	def __init__(self, *args, **kwargs):
		super(Matrix, self).__init__(*args, **kwargs)
	def __invert__(self):
		return linalg.inv(self)
	def inv(self):
		return self.__invert__()
	@staticmethod
	def weightedAverage(*tuples):
		total_weight = sum([ weight for matrix, weight in tuples ])
		total_matrix = sum(
			[ matrix*weight for matrix, weight in tuples[1:] ],
			tuples[0][0] * tuples[0][1]
		)
		return total_matrix / total_weight


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
		return "@({})".format(','.join(
			[ str(c) if c % 1 else str(int(c)) for c in self.coords ]
		))
	def __repr__(self):
		return self.__str__()
	def google(self):
		return "{}, {}".format(self.y, self.x)
	def svgp(self):
		return "{},{}".format(self.x, self.y)
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
	def __abs__(self):
		return sum([ c**2 for c in self.coords ])**0.5
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
		self.weight = 1
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
	@staticmethod
	def weightedAverage(*tuples):
		return PointMap(
			Point.weightedAverage(*[ (pointmap.point0, weight) for pointmap, weight in tuples ]),
			Point.weightedAverage(*[ (pointmap.point1, weight) for pointmap, weight in tuples ]),
		)

class SimplexMap(object):
	"""docstring for SimplexMap"""
	def __init__(self, *pointmaps):
		super(SimplexMap, self).__init__()
		if pointmaps:
			self.simplex0 = Simplex(*[ pm.point0 for pm in pointmaps ])
			self.simplex1 = Simplex(*[ pm.point1 for pm in pointmaps ])
		else:
			self.simplex0 = None
			self.simplex1 = None
	def translate(self, point):
		point -= self.simplex0.origin
		generic = point / self.simplex0
		result = self.simplex1.matrix * generic
		return self.simplex1.origin + result
	def __str__(self):
		return "{} -> {}".format(self.simplex0, self.simplex1)
	def __repr__(self):
		return self.__str__()
	@staticmethod
	def weightedAverage(*tuples):
		# return 0
		# for sm, weight in tuples:
		# 	print sm.simplex0, weight
		result = SimplexMap()
		result.simplex0 = Simplex.weightedAverage(*[ (sm.simplex0, weight) for sm, weight in tuples ])
		result.simplex1 = Simplex.weightedAverage(*[ (sm.simplex1, weight) for sm, weight in tuples ])
		return result

	# def weightedAverage(*tuples):
	# 	dims = len(tuples[0][0].simplex0.origin)
	# 	print dims
	# 	simplex0s = []
	# 	simplex1s = []
	# 	for sm, weight in tuples:
	# 		simplex0s.append((sm.simplex0,weight))
	# 		simplex1s.append((sm.simplex1,weight))
	# 	print simplex0s
	# 	for s, w in simplex0s:
	# 		print s
	# 		for p in s:
	# 			print p
	# 	print simplex1s
	# 	pass
	# 	# return SimplexMap(*[ PointMap.weightedAverage([  ]) for simplexmap, weight in tuples ])

class Simplex(object):
	"""docstring for Simplex"""
	def __init__(self, *points):
		super(Simplex, self).__init__()
		if points:
			self.points = points
			self.origin = points[0]
			basis = [ p - points[0] for p in points[1:] ]
			self.matrix = Matrix([ b.a() for b in basis ]).transpose()
		else:
			self.points = "Abstract"
			self.origin = None
			self.matrix = None
	def __add__(self, other):
		if type(other) is Simplex:
			result = Simplex()
			result.origin = self.origin + other.origin
			result.matrix = self.matrix + other.matrix
			return result
	def __sub__(self, other):
		if type(other) is Simplex:
			result = Simplex()
			result.origin = self.origin - other.origin
			result.matrix = self.matrix - other.matrix
			return result
	def __mul__(self, other):
		if type(other) in [int, long, float]:
			result = Simplex()
			result.origin = self.origin * other
			result.matrix = self.matrix * other
			return result
	def __div__(self, other):
		if type(other) in [int, long, float]:
			result = Simplex()
			result.origin = self.origin / other
			result.matrix = self.matrix / other
			return result
	def __iter__(self):
		for point in self.points:
			yield point
	def __getitem__(self, index):
		return self.points[index]
	def __len__(self):
		return len(self.points)
	def __str__(self):
		return "<{}>".format(''.join([ str(p) for p in self.points ]))
	def __repr__(self):
		return self.__str__()
	@staticmethod
	def weightedAverage(*tuples):
		total_weight = sum([ weight for simplex, weight in tuples ])
		total_simplex = sum(
			[ simplex*weight for simplex, weight in tuples[1:] ],
			tuples[0][0] * tuples[0][1]
		)
		return total_simplex / total_weight


class WeightedAggregateSimplexMap(object):
	"""docstring for WeightedAggregateSimplexMap"""
	def __init__(self, *tuples):
		super(WeightedAggregateSimplexMap, self).__init__()
		self.tuples = tuples
	def translate(self, point):
		# for sm in self.tuples[0]:
		# 	for k in sm:
		# 		print k
		# 	print '*'*204
				# exit()
		return Point.weightedAverage(*[ (sm.translate(point), weight) for sm, weight in self.tuples ])
		
WASM = WeightedAggregateSimplexMap