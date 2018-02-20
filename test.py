import pefile
import pydasm
import mysql.connector
import os

#mysql - localhost, root, 132331, pedata

cnx = mysql.connector.connect(user='root', password="132331", database='pedata')
cursor = cnx.cursor()



directory = os.getcwd() + "/files"
print directory

def updateFiles(file):
	query_get = "SELECT * FROM files WHERE hash = '" + file + "'"
	print query_get
	cursor.execute(query_get)
	data = cursor.fetchall()
	if not data:
		query_add = "INSERT INTO files (hash) VALUES ('" + file + "')"
		print query_add
		cursor.execute(query_add)
		cnx.commit()

def updateModules(file):
	pe = pefile.PE(directory+"/"+file)
	for entry in pe.DIRECTORY_ENTRY_IMPORT:
		name = entry.dll
		query_get_module = "SELECT * FROM modules WHERE name = "
		query_get = query_get_module + "'"+name+"'"
		#print query_get
		cursor.execute(query_get)
		data = cursor.fetchall()
		if not data:
			#not added yet
			query_add_module = "INSERT INTO modules (name) VALUES ('" + name + "')"
			#print query_add_module
			cursor.execute(query_add_module)
			emp_no = cursor.lastrowid
			#print emp_no
			cnx.commit()

def updateAPI(file):
	pe = pefile.PE(directory+"/"+file)
	for entry in pe.DIRECTORY_ENTRY_IMPORT:
		name = entry.dll
		query_get_id = "SELECT idmodules FROM modules WHERE name = '" + name + "'"
		cursor.execute(query_get_id)
		row = cursor.fetchall()
		mod_id = row[0][0]
		for imp in entry.imports:
			query_get = "SELECT * FROM apis WHERE name = '" + imp.name + "'"
			cursor.execute(query_get)
			data = cursor.fetchall()
			if not data:
				m_id = str(mod_id)
				query_set = "INSERT INTO apis (module, name) VALUES (" + m_id + ",'" + imp.name + "')" 
				print query_set

for file in os.listdir(directory):
		if not file.endswith(".py") or not file.endswith(".git") :
			updateFiles(file)
			updateModules(file)
			updateAPI(file)


cnx.close()

#for file in os.listdir(directory):
#	if not file.endswith(".py"):
#		pe = pefile.PE(file)
#		ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
#		ep_ava = ep+pe.OPTIONAL_HEADER.ImageBase
##		data = pe.get_memory_mapped_image()
#		offset = 0
#		while offset < len(data):
#			try:
#				i = pydasm.get_instruction(data[offset:], pydasm.MODE_32)
#				line = pydasm.get_instruction_string(i, pydasm.FORMAT_INTEL, ep_ava+offset)
#				if '0x420468' in line:
#					print line, offset
#				offset += i.length
#			except TypeError as et:
#				#print 'erro ', offset
#				offset += 12
