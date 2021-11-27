def sanitize(string):
	string = string.replace('\xc3\xa9','e')
	string = string.replace('\xef\xbb\xbf','')
	string = string.replace('\n','')
	string = string.replace('\r','')
	return string

def uniquify(arr,startnum=1):
	if len(set(arr)) == len(arr):
		return arr
	duplicates = arr[:]
	for x in set(arr):
		duplicates.remove(x)
	duplicates = set(duplicates)
	for x in duplicates:
		n = startnum
		for y in xrange(len(arr)):
			if arr[y] == x:
				arr[y] = arr[y] + str(n)
				n += 1
	return arr

def csv(filepath,delimeter=','):
	row = 1
	headers = []
	data = []
	with open(filepath) as file:
		for line in file.readlines():
			if row == 1:
				headers = line.split(delimeter)
				headers = [ sanitize(h) for h in headers ]
				headers = uniquify(headers)
			else:
				datum = line.split(delimeter)
				datum = datum = [ sanitize(h) for h in datum ]
				datum = dict([ (headers[c],datum[c]) for c in xrange(len(headers)) ])
				data.append(datum)
			row += 1
	return data