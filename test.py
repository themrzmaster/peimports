import pefile
import pydasm
import mysql.connector
import os

#mysql - localhost, root, 132331, pedata

cnx = mysql.connector.connect(user='root', password="132331", database='pedata')
cursor = cnx.cursor()




directory = os.getcwd()

def updateModules(directory):
	query_get_module = ("SELECT * FROM modules WHERE name LIKE %s", ("%" + name + "%",))
	for file in os.listdir(directory):
		if not file.endwith(".py"):
			pe = pefile.PE(file)
			for entry in pe.DIRECTORY_ENTRY_IMPORT:
				name = entry.dll
				cursor.execute(query_get_module)
				data = cursor.fetchall()
				print data






for file in os.listdir(directory):
	if not file.endwith(".py"):
		pe = pefile.PE(file)
		ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
		ep_ava = ep+pe.OPTIONAL_HEADER.ImageBase
		img_base = 401000
		data = pe.get_memory_mapped_image()
		offset = 0
		while offset < len(data):
			try:
				i = pydasm.get_instruction(data[offset:], pydasm.MODE_32)
				line = pydasm.get_instruction_string(i, pydasm.FORMAT_INTEL, ep_ava+offset)
				if '0x420468' in line:
					print line, offset
				offset += i.length
			except TypeError as et:
				#print 'erro ', offset
				offset += 12
