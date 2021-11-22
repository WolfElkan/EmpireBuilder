from numpy import mat, linalg
from numpy.matrixlib.defmatrix import matrix

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
		return mat([ [c] for c in self.coords ])
	def floatify(self):
		return Point(*[ float(c) for c in self.coords ])
	def __str__(self):
		return "({})".format(','.join([ str(c) for c in self.coords ]))
	def __repr__(self):
		return self.__str__()
	def __add__(self, other):
		if type(other) is Point:
			return Point(*[ self[k] + other[k] for k in xrange(len(self)) ])
		elif type(other) is matrix:
			other = other.tolist()
			return Point(*[ self[k] + other[k][0] for k in xrange(len(self)) ])
	def __sub__(self, other):
		if type(other) is Point:
			return Point(*[ self[k] - other[k] for k in xrange(len(self)) ])
		elif type(other) is matrix:
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
	@staticmethod
	def weightedAverage(*tuples):
		total_weight = sum([ weight for point, weight in tuples ])
		total_point = sum(
			[ point*weight for point, weight in tuples[1:] ],
			tuples[0][0] * tuples[0][1]
		)
		return total_point / total_weight


class Benchmark(object):
	"""An object containing two points.  point0 should map to point1"""
	def __init__(self, point0, point1):
		super(Benchmark, self).__init__()
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

class Simplex(object):
	"""docstring for Simplex"""
	def __init__(self, *benchmarks):
		super(Simplex, self).__init__()
		self.benchmarks = benchmarks
		self.origin0 = benchmarks[0].p(0)
		self.origin1 = benchmarks[0].p(1)
		basis0 = [ b.p(0) - benchmarks[0].p(0) for b in benchmarks ]
		basis1 = [ b.p(1) - benchmarks[0].p(1) for b in benchmarks ]
		matrix0 = mat([ b.a() for b in basis0[1:] ]).transpose()
		self.mat0inv = linalg.inv(matrix0)
		self.matrix1 = mat([ b.a() for b in basis1[1:] ]).transpose()
	def translate(self, point):
		point -= self.origin0
		generic = self.mat0inv * point.m()
		result = self.matrix1 * generic
		return self.origin1 + result