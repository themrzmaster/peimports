import pefile
import pydasm
import mysql.connector
import os

#mysql - localhost, root, 132331, pedata

cnx = mysql.connector.connect(user='root', password="132331", database='pedata')
cursor = cnx.cursor()



directory = os.getcwd() + "/files"
#print directory

def updateFiles(file):
	#print file
	query_get = "SELECT * FROM files WHERE hash = '" + file + "'"
	#print query_get
	cursor.execute(query_get)
	data = cursor.fetchall()
	if not data:
		query_add = "INSERT INTO files (hash) VALUES ('" + file + "')"
		#rint query_add
		cursor.execute(query_add)
		cnx.commit()

def updateModules(file):
	print file
	pe = pefile.PE(file)
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
	pe = pefile.PE(file)
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
				cursor.execute(query_set)
				cnx.commit()

def extract(file):
	lista = {}
	soma = {}
	lista_count = {}
	x = 0
	count = 0
	pe = pefile.PE(file)
	ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
	ep_ava = ep+pe.OPTIONAL_HEADER.ImageBase
	data = pe.get_memory_mapped_image()
	for entry in pe.DIRECTORY_ENTRY_IMPORT:
		module_name = entry.dll
		for imp in entry.imports: #for each function imported calculate how many times it was called, jumped
			lista[str(hex(imp.address))] = imp.name
	lista_offset = list(lista.keys())
	offset = 0
	count = 0
	for item in lista_offset:
		lista_count[item] = 0

	#print lista_count	
	while offset < len(data):
		try:
			i = pydasm.get_instruction(data[offset:], pydasm.MODE_32)
			line = pydasm.get_instruction_string(i, pydasm.FORMAT_INTEL, ep_ava+offset)
			if line:
				#if any(item in line for item in lista_offset):
				for w in lista_offset:
					if w in line:
						lista_count[w] += 1
					#count += 1
				offset += i.length
			else:
				offset += 12
		except TypeError as et:
			#print 'erro ', offset
			offset += 12
		#lista_count[value] = count
	#print lista_count
	for keys, value in lista_count.iteritems():
		name = lista[keys]
		#print name
		query_get_api = "SELECT idapis FROM apis WHERE name = '" + name + "'"
		cursor.execute(query_get_api)
		row = cursor.fetchall()
		api_id = row[0][0]

		query_get_hash = "SELECT idfile FROM files WHERE hash = '" + str(file) + "'"
		cursor.execute(query_get_hash)
		row = cursor.fetchall()
		hash_id = row[0][0]
		#check if already added
		query_check = "SELECT * FROM extract WHERE hash = '" + str(hash_id) + "' AND api = '" + str(api_id) + "'"
		cursor.execute(query_check)
		data = cursor.fetchall()
		if not data:
			query_add = "INSERT INTO extract (hash, api, call_number) VALUES ('" + str(hash_id) + "', "  + str(api_id) + ", "  + str(value) + " )"
			cursor.execute(query_add)
		#print query_check
	cnx.commit()	
	#print lista

for file in os.listdir(directory):
		if not file.endswith(".py") or not file.endswith(".git") :
			updateFiles(file)
			updateModules(file)
			updateAPI(file)
			extract(file)


cnx.close()

