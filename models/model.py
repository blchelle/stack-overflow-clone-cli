import sqlite3
import os

class Model:
	def __init__(self, pathToDb):
		"""
		Sets up the connection and cursor for any of the children models to use
		"""

		# Validates that the path given is a valid, existing db
		pathToDbFromModel = __file__.rpartition('/')[0] +'/../' + pathToDb
		if not os.path.exists(pathToDbFromModel) or pathToDb.split('.')[-1] != 'db':
			print("No database exists at the path specified")
			exit(-1)

		self.connection = sqlite3.connect(__file__.rpartition('/')[0] +'/../' + pathToDb)
		self.cursor = self.connection.cursor()