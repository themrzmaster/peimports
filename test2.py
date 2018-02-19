import pefile

pe = pefile.PE('21e2bfb55a7d692f5bbde6cc53914b84')

for entry in pe.DIRECTORY_ENTRY_IMPORT:
  print entry.dll
  for imp in entry.imports:
    print '\t', hex(imp.address), imp.name
