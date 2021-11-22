from EmpireBuilder import Point, Benchmark, Simplex

b0 = Benchmark(Point(1,1),Point(10,10))
b1 = Benchmark(Point(2,5),Point(20,50))
b2 = Benchmark(Point(4,3),Point(40,30))
b3 = Benchmark(Point(1,5),Point(10,50))

test = Simplex(b0, b1, b2)

print Point.weightedAverage(
	(Point(2,4),3),
	(Point(4,6),2),
)

d = Point(2,4)

# print test.translate(d)