import sqlite3

class Model:
	def __init__(self):
		"""
		Sets up the connection and cursor for any of the children models to use
		"""
		self.connection = sqlite3.connect(__file__.rpartition('/')[0] +'/../sql/mp1.db')
		self.cursor = self.connection.cursor()