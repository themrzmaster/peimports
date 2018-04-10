import mysql.connector

<<<<<<< HEAD
cnx = mysql.connector.connect(user='root', password="", database='pedata')
=======
cnx = mysql.connector.connect(user='root', password="132331", database='pedata')
>>>>>>> d059ac2b7a0bf65bbe0747c138f7d307aec0868c
cursor = cnx.cursor()

q1 = "select hash from extract where api = 6;"
cursor.execute(q1)
data = cursor.fetchall()

for item in data:
	h_id = item[0]
	q1 = "select hash from extract where api = 4979 and hash = " +h_id+ ";"
	cursor.execute(q1)
	data = cursor.fetchall()
	print data