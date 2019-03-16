#!/usr/bin/python

import mysql.connector

db = mysql.connector.connect(user='root', host='172.17.0.1', database='app', password = 'password', port='7000')
cursor = db.cursor()

if __name__ == '__main__':
	print 'Hello from admin (aici se adauga si se sterg zboruri)'
	while 1:
		pass