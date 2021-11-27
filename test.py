from datetime import datetime
START = datetime.now()
from csv import csv
from transform import Point, PointMap, SimplexMap
from translator import Translator

pointmaps = []
for bm in csv('benchmarks.csv'):
	game = Point(bm['Column'],bm['Row'])
	real = Point(bm['Lon'],bm['Lat'])
	pm = PointMap(game,real)
	pointmaps.append(pm)
	# print "{Place},{Lon},{Lat},{Kind}".format(**bm)

# for pm in pointmaps:
# 	print list(pm.a(0))

EmpireBuilder = Translator(*pointmaps)
# print [ SimplexMap(*[ pointmaps[i] for i in s ]) for s in EmpireBuilder.delaunay.simplices ]
	# print SimplexMap(*[ pointmaps[i] for i in s ])

# print EmpireBuilder.piecewise(Point(1,1))

# print EmpireBuilder.broadcast(Point(50,50)).google()

# exit()

version = 10
count = 0
template = "R{row}C{col},{lon},{lat},{kind}"

# template = "({col},-{row})"
# for col in xrange(17*(version-1),17*version):
# for col in xrange(1,68):
for country in ["CAN","USA","MEX"]:
	filepath = 'exports/v{}{}.csv'.format(version,country.lower())
	print '>>', filepath
	with open(filepath,'w') as file:

		def p(s):
			file.write(s)
			file.write('\n')
			print s

		p("Title,Lon,Lat,Kind")
		for city in csv('cities.csv'):
			if city['Country'] == country.upper():
				# print city
				loc = EmpireBuilder.broadcast(Point(int(city['Col']),int(city['Row'])))  
				if loc:
					count += 1

					p(template.format(
						row=city['Row'],
						col=city['Col'],
						lon=loc.x,
						lat=loc.y,
						kind=city['Terrain'] if city['CitySize'] == 'None' else city['CitySize']
					))
					# print EmpireBuilder.piecewise(Point(col,row)).google()
					# exit()

			# print count

print datetime.now() - START