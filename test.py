import pefile
import pydasm
import mysql.connector
import os

<<<<<<< HEAD
=======


>>>>>>> d059ac2b7a0bf65bbe0747c138f7d307aec0868c


directory = os.getcwd()
n_files = len(os.walk(directory).next()[2])
n_processed = 0
#print directory

#mysql - localhost, root, 132331, pedata
def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b] 


def checkProcessed(file):
	global n_processed
	hash_file = between(file, "_", ".vir")
	query_get = "SELECT * FROM files WHERE hash = '" + hash_file + "'"
	cursor.execute(query_get)
	data = cursor.fetchall()
	n_processed += 1
	if data:
		return True
	else:
		return False


cnx = mysql.connector.connect(user='root', password="", database='pedata')
cursor = cnx.cursor()

<<<<<<< HEAD
directory = os.getcwd()
n_files = len(os.walk(directory).next()[2])
n_processed = 0
#print directory
=======
>>>>>>> d059ac2b7a0bf65bbe0747c138f7d307aec0868c

#mysql - localhost, root, 132331, pedata
def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b] 


def checkProcessed(file):
	global n_processed
	hash_file = between(file, "_", ".vir")
	query_get = "SELECT * FROM files WHERE hash = '" + hash_file + "'"
	cursor.execute(query_get)
	data = cursor.fetchall()
	n_processed += 1
	if data:
		return True
	else:
		return False




def updateFiles(file):
	#print file
	hash_file = between(file, "_", ".vir")
	query_get = "SELECT * FROM files WHERE hash = '" + hash_file + "'"
	#print query_get
	cursor.execute(query_get)
	data = cursor.fetchall()
	if not data:
		query_add = "INSERT INTO files (hash) VALUES ('" + hash_file + "')"
		#rint query_add
		cursor.execute(query_add)
		cnx.commit()

def updateModules(file, pe):
	hash_file = between(file, "_", ".vir")
	try:
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
	except AttributeError as e:
		#skip
		print e		

def updateAPI(file, pe):
	try:
		for entry in pe.DIRECTORY_ENTRY_IMPORT:
			name = entry.dll
			query_get_id = "SELECT idmodules FROM modules WHERE name = '" + name + "'"
			cursor.execute(query_get_id)
			row = cursor.fetchall()
			mod_id = row[0][0]
			for imp in entry.imports:
				if imp.name:
					query_get = "SELECT * FROM apis WHERE name = '" + imp.name[0:45] + "'"
					cursor.execute(query_get)
					data = cursor.fetchall()
					if not data:
						m_id = str(mod_id)
						query_set = "INSERT INTO apis (module, name) VALUES (" + m_id + ",'" + imp.name[0:45] + "')" 
						cursor.execute(query_set)

			cnx.commit()			
	except AttributeError as e:
		print e	

def extract(file, pe):
	lista = {}
	soma = {}
	lista_count = {}
	x = 0
	count = 0
	hash_file = between(file, "_", ".vir")
	ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
	ep_ava = ep+pe.OPTIONAL_HEADER.ImageBase
	data = pe.get_memory_mapped_image()
	try:
		for entry in pe.DIRECTORY_ENTRY_IMPORT:
			module_name = entry.dll
			for imp in entry.imports: #for each function imported calculate how many times it was called, jumped
				if imp.name:
					lista[str(hex(imp.address))] = imp.name[0:45]
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
			query_get_api = "SELECT idapis FROM apis WHERE name = '" + name[0:45] + "'"
			cursor.execute(query_get_api)
			row = cursor.fetchall()
			api_id = row[0][0]

			query_get_hash = "SELECT idfile FROM files WHERE hash = '" + str(hash_file) + "'"
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
	except AttributeError as e:
		print e		
	cnx.commit()	
	#print lista

for file in os.listdir(directory):
		if not file.endswith(".py") or not file.endswith(".git") :
			if not checkProcessed(file):
				print "processing " + str(n_processed) + " of " + str(n_files) + " ..."
				try:
					print file
					pe = pefile.PE(file)
					updateFiles(file)
					updateModules(file, pe)
					updateAPI(file, pe)
					extract(file, pe)
				except PEFormatError as e:
					print "no PE.. skipping..."



cnx.close()

