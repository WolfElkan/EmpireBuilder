from transform import Point, PointMap, SimplexMap

b0 = PointMap(Point(1,1),Point(10,10))
b1 = PointMap(Point(2,5),Point(20,50))
b2 = PointMap(Point(4,3),Point(40,30))
# b3 = PointMap(Point(1,5),Point(10,50))

test = SimplexMap(b0, b1, b2)

# print test.mat0inv
# print test.simplex0.matrix.inv()
# print test.matrix1
# print test.simplex1.matrix

assert Point.weightedAverage(
	(Point(2,4),3),
	(Point(4,6),2),
) == Point(2.8,4.8)

d = Point(2,4)

# print test.translate(d)
print test.translate(d)



		