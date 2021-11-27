from datetime import datetime
START = datetime.now()
from csv import csv
from transform import Point, PointMap, SimplexMap
from translator import Translator
import os

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

version = 1
count = 0
template = '\t<circle cx="{lon}" cy="{lat}" r="1" class="{Country} {kind}"/>'

filepath = 'exports/test.html'
os.remove(filepath)
print '>>', filepath
with open(filepath,'w') as file:

	def p(s):
		file.write(s)
		file.write('\n')
		print s

	p('<link rel="stylesheet" type="text/css" href="style.css">')
	p('<svg width="700" height="500">')
	for city in csv('cities.csv'):
		# if city['Country'] == country.upper():
			# print city
			loc = EmpireBuilder.broadcast(Point(int(city['Col']),int(city['Row'])))  
			if loc:
				count += 1
				city.update({
					'lon':(loc.x+130)*10,
					'lat':(60-loc.y)*10,
					'kind':city['Terrain'] if city['CitySize'] == 'None' else city['CitySize'],
				})
				p(template.format(**city))

				# exit()
	p('</svg>')
				# print EmpireBuilder.piecewise(Point(col,row)).google()
		# print count

print datetime.now() - START