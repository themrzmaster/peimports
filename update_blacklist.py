import xml.etree.ElementTree as ET
import mysql.connector

<<<<<<< HEAD
cnx = mysql.connector.connect(user='root', password="", database='pedata')
=======
cnx = mysql.connector.connect(user='root', password="132331", database='pedata')
>>>>>>> d059ac2b7a0bf65bbe0747c138f7d307aec0868c
cursor = cnx.cursor()


def update_ref(file):
	tree = ET.parse(file)
	root = tree.getroot()
	libs_tree = root[0]
	for ch in libs_tree:
		try:
			module = str(ch.attrib['name']).lower()
			bl = ch.attrib['bl']
			query_get = "SELECT idmodules, blacklist FROM modules WHERE lower(name) = '" + module + "'"
			cursor.execute(query_get)
			data = cursor.fetchall()
			print "checking " + module
			if data:
				q_id = data[0][0]
				print "updating.."
				query_update = "UPDATE modules SET blacklist = " + bl + " WHERE idmodules = "  + str(q_id)
				cursor.execute(query_update)
			for fcts in ch: #for each lib(module)
				for fct in fcts:
					api = str(fct.text).lower()
					bl = fct.attrib['bl']
					query_get = "SELECT idapis, name FROM apis WHERE lower(name) = '" + api + "'"
					cursor.execute(query_get)
					data = cursor.fetchall()
					print "checking api" + api
					if data:
						q_id = data[0][0]
						print "updating..."
						query_update = "UPDATE apis SET blacklist = " + bl + " WHERE idapis = "  + str(q_id)
						cursor.execute(query_update)
				#print lib[0]
				#print fcts
		except KeyError as e:
			print e
				

update_ref('functions.xml')
cnx.commit()