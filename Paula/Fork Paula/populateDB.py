#!/usr/bin/python


import mysql.connector

db = mysql.connector.connect(user='root', host='127.0.0.1', database='app', password = 'password', port='7000')
cursor = db.cursor()

sql = "CREATE TABLE zbor (ID varchar(255), plecare varchar(255), sosire varchar(255), ora int, zi int, durata int, locuri int )"
cursor.execute(sql)
sql = "CREATE TABLE bilet (ID int, IDZbor varchar(255))"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('a', 'CONSTANTA', 'PLOIESTI', 1, 140, 1, 3)"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('b', 'FOCSANI', 'CONSTANTA', 14, 140, 2, 9)"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('c', 'PLOIESTI', 'SIBIU', 8, 139, 1, 5)"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('d', 'CONSTANTA', 'TULCEA', 8, 139, 1, 5)"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('e', 'PLOIESTI', 'FOCSANI', 15, 201, 1, 5)"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('f', 'TULCEA', 'FOCSANI', 15, 201, 2, 5)"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('g', 'TIMISOARA', 'ORADEA', 16, 201, 2, 5)"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('h', 'ORADEA', 'TIMISOARA', 10, 202, 2, 5)"
cursor.execute(sql)

sql = "INSERT INTO zbor VALUES ('i', 'BRASOV', 'TIMISOARA', 15, 201, 1, 5)"
cursor.execute(sql)


db.commit()