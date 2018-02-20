import os
import pefile
import pydasm

directory = os.path.dirname(os.path.abspath(__file__))
for file in os.listdir(directory):
	if not file.endswith(".py"):
		pe = pefile.PE(file)
		ep = pe.OPTIONAL_HEADER.AddressOfEntryPoint
		ep_ava = ep+pe.OPTIONAL_HEADER.ImageBase
		data = pe.get_memory_mapped_image()
		offset = 0
		while offset < len(data):
			try:
				i = pydasm.get_instruction(data[offset:], pydasm.MODE_32)
				line = pydasm.get_instruction_string(i, pydasm.FORMAT_INTEL, ep_ava+offset)
				if '0x420658' in line:
					print line, offset
				offset += i.length
			except TypeError as et:
				#print 'erro ', offset
				offset += 12
