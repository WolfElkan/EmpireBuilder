from csv import csv

countries = {
	'c':'CAN',
	'u':'USA',
	'm':'MEX',
}
count = 0
cities = csv('citymap3.csv')
points = []

print "Name,Row,Col,Country,Terrain,CitySize,mark"

for r in range(1,len(cities)+1):
	row = cities[r-1]
	for col in row:
		mark = row[col]
		if mark:
			# print mark,
			city = {
				'R':r,
				'C':col,
				# 'Country':countries[mark[-1]],
				'mark':mark,
				'terrain': 'Mountain' if len(mark) == 2 else 'Flat',
				'CitySize':'None',
				'Name':"R{}C{}".format(r,col),
			}
			if '_' in mark:
				if mark[0] == '1':
					city['CitySize'] = 'Small'
				elif mark[0] == '2':
					city['CitySize'] = 'Medium'
				elif mark[0] == '3':
					city['CitySize'] = 'Major'
				city['Name'] = mark[3:]
				city['Country'] = countries[mark[1]]
			else:
				city['Country'] = countries[mark[-1]]


			count += 1
			# print city
			print "{Name},{R},{C},{Country},{terrain},{CitySize},{mark}".format(**city)
			# points.append(city)
# print count


# for p in points:
