import mysql.connector

cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='app', password = 'password', port='10000')
mycursor = cnx.cursor()
sql = "create table fly (id varchar(255), s varchar(255), d varchar(255), h int, day int, time int, seats int )"
mycursor.execute(sql)
sql = "create table ticket (id int, route varchar(255))"
mycursor.execute(sql)
cnx.commit()