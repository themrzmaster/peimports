import pefile
import pydasm
import mysql.connector
import os

#mysql - localhost, root, 132331, pedata

cnx = mysql.connector.connect(user='root', password="132331", database='pedata')
cursor = cnx.cursor()




directory = os.getcwd() + "/files"
print directory
def updateModules(file):
	pe = pefile.PE(directory+"/"+file)
	for entry in pe.DIRECTORY_ENTRY_IMPORT:
		name = entry.dll
		query_get_module = ("SELECT * FROM modules "
							"WHERE name LIKE")
		print query_get_module, ("'"+name+"'")
		cursor.execute(query_get_module, ("'"+name+"'"))
		#data = cursor.fetchall()
		data = 0
		if not data:
			#not added yet
			query_add_module = ("INSERT INTO modules "
								"(name) " 
								"VALUES (")
			print query_add_module, name, ")"
			#cursor.execute(query_add_module, name)
			emp_no = cursor.lastrowid
			print emp_no


for file in os.listdir(directory):
		if not file.endswith(".py") or not file.endswith(".git") :
			updateModules(file)



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
