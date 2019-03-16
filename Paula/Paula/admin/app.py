from flask import Flask
from flask import render_template, request
import mysql.connector
app = Flask(__name__)
cnx = mysql.connector.connect(user='root', host='172.17.0.1', database='app', password = 'password', port='10000')

@app.route('/',  methods = ['GET', 'POST'])
def hello_world():
	mycursor = cnx.cursor()
	sql = "SELECT * FROM fly"
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	return render_template('base.html', list=myresult)

@app.route('/removehtml',  methods = ['GET', 'POST'])
def SHOWremoveHtml():
	return render_template('remove.html')

@app.route('/addhtml',  methods = ['GET', 'POST'])
def ShowaddHtml():
	return render_template('add.html')

@app.route('/remove', methods = ['GET', 'POST'])
def removePlane():
	mycursor = cnx.cursor()
	sql = "DELETE FROM fly WHERE id = '"+request.form['RID']+"'"
	mycursor.execute(sql)
	cnx.commit()
	return "Succes to remove fly"

@app.route('/add', methods = ['GET', 'POST'])
def addPlane():
	mycursor = cnx.cursor()# id sursa dest
	sql = "insert into fly values ('"+request.form['ID'] + "', '" + request.form['START'] + "', '" + request.form['FINISH'] + "', " + request.form['HOUR'] + ", " + request.form['DAY'] + ", " + request.form['TIME'] + ", "+ request.form['SEATS'] +")"
	mycursor.execute(sql)
	cnx.commit()
	return "Succes to add a fly "+request.form['START']+" ===>>>> "+request.form['FINISH']

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
