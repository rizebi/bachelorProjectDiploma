import mysql.connector

cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='app', password = 'password', port='10000')
mycursor = cnx.cursor()
		
sql = "insert into fly values ('a', 'BUCURESTI', 'PLOIESTI', 13, 200, 1, 5)"
mycursor.execute(sql)

sql = "insert into fly values ('b', 'BUCURESTI', 'CONSTANTA', 13, 200, 2, 3)"
mycursor.execute(sql)

sql = "insert into fly values ('c', 'PLOIESTI', 'SIBIU', 8, 201, 1, 5)"
mycursor.execute(sql)

sql = "insert into fly values ('d', 'CONSTANTA', 'TULCEA', 8, 201, 1, 5)"
mycursor.execute(sql)

sql = "insert into fly values ('e', 'SIBIU', 'FOCSANI', 13, 201, 1, 5)"
mycursor.execute(sql)

sql = "insert into fly values ('f', 'TULCEA', 'FOCSANI', 15, 201, 2, 5)"
mycursor.execute(sql)

sql = "insert into fly values ('g', 'BRASOV', 'ORADEA', 15, 201, 2, 5)"
mycursor.execute(sql)

sql = "insert into fly values ('h', 'ORADEA', 'TIMISOARA', 18, 202, 2, 5)"
mycursor.execute(sql)

sql = "insert into fly values ('i', 'BRASOV', 'TIMISOARA', 15, 201, 1, 5)"
mycursor.execute(sql)
cnx.commit()

