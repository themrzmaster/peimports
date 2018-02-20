import pefile
import pydasm
import mysql.connector

#mysql - localhost, root, 132331, pedata

cnx = mysql.connector.connect(user='root', password="132331", database='pedata')
cursor = cnx.cursor()

pe = pefile.PE('21e2bfb55a7d692f5bbde6cc53914b84')
ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
ep_ava = ep+pe.OPTIONAL_HEADER.ImageBase
img_base = 401000
data = pe.get_memory_mapped_image()
offset = 0
print img_base
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
