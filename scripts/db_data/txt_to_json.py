# return number of tabs before each word
def countTabs(line):
	for i, c in enumerate(line):
		if c != '\t':
			return i

def insertTabs(tabs):
	s = ""
	for i in range(tabs):
		s += '\t'
	return s

def standard(line, tabs):
	s =  "{ \n" + insertTabs(tabs) + "\"name\":\"" + line.strip() + "\",\n"
	# skipping tooltip for now
	s += insertTabs(tabs) + "\"weight\": 1,\n"
	s += insertTabs(tabs) + "\"children\":["
	return s

# add data as a sibling
def makeSib(line, tabs):
	return "]}," + standard(line, tabs)

def makeAbove(line, tabs):
	return "]} ]}," + standard(line, tabs)

f = open('interests.txt', 'r')

json = "["

prev = 0
first = True
for line in f:
	tabs = countTabs(line)

	if first:
		json += standard(line, tabs)
		first = False
		continue

	if tabs == prev:
		json += makeSib(line, tabs)
	elif tabs > prev:
		json += standard(line, tabs) # makeChild essentially
	else:
		json += makeAbove(line, tabs)

	prev = tabs

while tabs > 0:
	json += "]}"
	tabs -= 1

json += "]"
f.close()
#print json

f = open('interests2.json', 'w')
f.write(json)
f.close()

'''
I didn't know you could do this		https://docs.python.org/2/tutorial/inputoutput.html

serializing the object to a file: So if f is a file object opened for writing
json.dump(x, f)
To decode the object again, if f is a file object which has been opened for reading:
x = json.load(f)
'''

