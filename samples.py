
import mysql.connector



class Sample:
	#sample(0, 1823h24b3248, 9, '.root/samples')
	def __init__(self, fid, fhash, categ , path):
		self.id = fid
		self.f_hash = fhash
		self.cat = categ
		self.path = path


	#get sample by hash - return Sample obj
	@staticmethod
	def get_sample_hash(cnx, hash_s):
		query_get = "SELECT * FROM files WHERE hash = '" + hash_s + "'"
		cursor = cnx.cursor()
		cursor.execute(query_get)
		data = cursor.fetchall()
		if data:
			return True
		else:
			return False
