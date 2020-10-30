from models import model

class AuthModel(model.Model):

	def attemptLogin(self, uid, password):
		"""
		Checks the users table to find a match of the username
		and password

		Parameters
		----------
		uid : str
			The uid given at the command-line
		password : str
			The password given at the command-line

		Return
		----------
		None or {}
			The result of the login query
			Return will be none if no such user is found
			Otherwise, the return will be the users information
		"""

		# Template query for checking if the user is logged in
		loginQuery = \
		'''
			SELECT *
			FROM users
			WHERE
				uid = ?
				AND pwd = ?;
		'''

		# Executes the query with the passed in parameters
		self.cursor.execute(loginQuery, (uid, password,))
		return self.cursor.fetchone()

	def createAccount(self, name, city, uid, password):
		"""
		Inserts the new user into the users table

		Parameters
		----------
		name : str
			The name given at the command-line
		city : str
			The city given at the command-line
		uid : str
			The uid given at the command-line
		password : str
			The password given at the command-line
		"""

		# Query template to insert a user into the database
		insertUserQuery = \
		'''
			INSERT INTO users
			VALUES (?,?,?,?,DATE('now'));
		'''

		# Executes and commits the query with the passed in parameters
		self.cursor.execute(insertUserQuery, (uid, name, password, city,))
		self.connection.commit()

	def getUserByUid(self, uid):
		"""
		Inserts the new user into the users table

		Parameters
		----------
		uid : str
			The uid given at the command-line

		Return
		None or {}
			None if no user has the uid specified
			Otherwise, returns the user with the uid
		"""

		# Query template for getting a user by uid
		getUserQuery = \
		'''
			SELECT uid
			FROM users
			WHERE uid = ?
		'''

		# Executes and returns the result of the query
		self.cursor.execute(getUserQuery, (uid,))
		return self.cursor.fetchone()