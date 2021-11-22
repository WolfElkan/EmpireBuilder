from numpy import mat, linalg
from numpy.matrixlib.defmatrix import matrix

class Point(object):
	"""docstring for Point"""
	def __init__(self, x, y):
		super(Point, self).__init__()
		self.x = x
		self.y = y
	def a(self):
		return [self.x,self.y]
	def m(self):
		return mat([[self.x],[self.y]])
	def floatify(self):
		return Point(float(self.x),float(self.y))
	def __str__(self):
		return "({},{})".format(self.x,self.y)
	def __repr__(self):
		return self.__str__()
	def __add__(self, other):
		if type(other) is Point:
			return Point(self.x + other.x, self.y + other.y)
		elif type(other) is matrix:
			return Point(
				self.x + other.tolist()[0][0], 
				self.y + other.tolist()[1][0]  
			)
	def __sub__(self, other):
		if type(other) is Point:
			return Point(self.x - other.x, self.y - other.y)
		elif type(other) is matrix:
			return Point(
				self.x - other.tolist()[0][0], 
				self.y - other.tolist()[1][0]  
			)
	def __mul__(self, other):
		if type(other) in [int, long, float]:
			return Point(self.x * other, self.y * other)

class Benchmark(object):
	"""An object containing two points.  xy0 should map to xy1"""
	def __init__(self, *args):
		if len(args) == 2:
			point0, point1 = args
			x0 = point0.x
			y0 = point0.y
			x1 = point1.x
			y1 = point1.y
			weight = 1
		elif len(args) == 4:
			x0, y0, x1, y1 = args
			weight = 1
		self.x0 = float(x0)
		self.y0 = float(y0)
		self.x1 = float(x1)
		self.y1 = float(y1)
		self.weight = weight
	def __str__(self):
		return "({},{}) -> ({},{})".format(self.x0, self.y0, self.x1, self.y1)
	def __repr__(self):
		return self.__str__()
	def a(self, num):
		if num == 0:
			return [self.x0, self.y0]
		elif num == 1:
			return [self.x1, self.y1]
	def m(self, num):
		return mat([self.a(num)])
	def p(self, num):
		return Point(*self.a(num))

print Benchmark(1,1,10,10)


class Benchmark(object):
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
			return [self.x0, self.y0]
		elif num == 1:
			return [self.x1, self.y1]
	def m(self, num):
		return mat([self.a(num)])
	def p(self, num):
		return Point(*self.a(num))
		

print Benchmark(Point(1,1),Point(10,10))

exit()

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

# print Point(2,4).m()

b0 = Benchmark(Point(1,1),Point(10,10))
b1 = Benchmark(Point(2,5),Point(20,50))
b2 = Benchmark(Point(4,3),Point(40,30))

test = Simplex(b0, b1, b2)

d = Point(2,4)

print test.translate(d)