from flask import Flask
from flask import render_template, request
import mysql.connector
app = Flask(__name__)
cnx = mysql.connector.connect(user='root', host='172.17.0.1', database='app', password = 'password', port='10000')

class Nod:
	def __init__(self):
		self.time = 100000
		self.ids = []
		self.day = 0
		self.hour = 0
		self.during = 0

	def __repr__(self):
		return " (time: %s, ids: %s, day:%s, hour:%s, during:%s)\n\n" % (self.time, self.ids, self.day, self.hour,self.during)

def test_time(day ,hour, during, obj):
	day = day+ (hour + during)/24
	hour = (hour + during)%24

	if obj[4] > day:
		return 1
	if obj[4] == day:
		if obj[3] >hour:
			return 1
	return 0

def getRoutes(routes, start, array):
	l=[]
	day = array[start].day
	hour = array[start].hour
	during = array[start].during


	for a in routes:
		if a[1]== start:
			if test_time(day, hour, during, a)==1:
				l.append(a)
	return l


def calculate(dayS, hourS, dayF, hourF, t):
	#calculez cand ajunge trenu apoi
	dayS = dayS + (hourS + t)/24
	hourS = (hourS + t) % 24

	#caulculez diferenta de timp
	if dayS == dayF:
		return hourF-hourS
	else:
		#diferenta de ora pana a doua zi
		h1 = 24-hourS
		#diferenta de zile
		day1 = dayF - dayS
		#h total este egala cu diferenta de ore pana a doua zi + diferenta de zile*24 +
		# orele de la 00:00 pana plecare
		h = h1 + (day1-1)*24 + hourF
		return h

def getoptimal(source, FINAL, day):

	mycursor = cnx.cursor()
	sql = "SELECT * FROM fly"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	routes= myresult

	array = []

	for route in routes:
		array.append(route[1])
		array.append(route[2])

	arrayStations = list(set(array))
	if source in arrayStations:
		print 'ok'
	else:
		return []

	if FINAL in arrayStations:
		print 'ok'
	else:
		return []

	array={}


	for elem in arrayStations:
		array[elem] = Nod()

	array[source].time = 0
	array[source].day = day
	L = []
	l = getRoutes(routes,source,array)

	for rout in l:
		dest = rout[2]
		time = array[source].time + rout[5]
		if array[dest].time > time:
			array[dest].time = time
			array[dest].day = rout[4]
			array[dest].hour = rout[3]
			array[dest].during = rout[5]
			array[dest].ids.append(rout[0])

		L.append(dest)

	while(L!=[]):
		newL=[]
		for obj in L:
			source = obj
			l = getRoutes(routes, source, array)
			for rout in l:
				dest = rout[2]
				newL.append(dest)
				time = array[source].time + rout[5] + calculate(array[source].day, array[source].hour, rout[4], rout[3], rout[5])
				if array[dest].time > time:
					array[dest].time = time
					array[dest].day = rout[4]
					array[dest].hour = rout[3]
					array[dest].during = rout[5]
					array[dest].ids = array[source].ids
					array[dest].ids.append(rout[0])

		L=newL

	response = []
	vector=[]
	if array[FINAL].time!=100000:
		response.append(array[FINAL].ids)
		for fly in myresult:
			for id in array[FINAL].ids:
				if fly[0]==id:
					vector.append(fly)
	response.append(vector)
	return response




@app.route('/', methods=['GET'])
def hello_world():
	return "work"

@app.route('/getOptimalRoute', methods=['GET','POST'])
def getOptiomalRoute():
	rez = getoptimal(request.form['SOURCE'], request.form['DEST'], int(request.form['DAY']))
	if rez ==[]:
		return "NU s-a gasit drum"
	return render_template("rezerv.html", source = request.form['SOURCE'], dest = request.form['DEST'], rez = rez)


@app.route('/rezerv', methods=['GET','POST'])
def bookTicket():
	return "Rezerved Succesfully "

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
