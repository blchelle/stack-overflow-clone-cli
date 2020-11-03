from models import model
import sqlite3
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

		try:
			self.cursor.execute(loginQuery, (uid, password,))
			return self.cursor.fetchone()
		except sqlite3.Error as e:
			print(e)

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


		try:
			# Executes and commits the query with the passed in parameters
			self.cursor.execute(insertUserQuery, (uid, name, password, city,))
			self.connection.commit()
		except sqlite3.Error as e:
			print(e)




	def getUserByUid(self, uid):
		"""
		Inserts the new user into the users table

		Parameters
		----------
		uid : str
			The uid given at the command-line

		Returns
		-------
		None or {}
			None if no user has the uid specified
			Otherwise, returns the user with the uid
		"""

		# Query template for getting a user by uid
		getUserQuery = \
		'''
			SELECT uid
			FROM users
			WHERE uid = ?;
		'''

		try:
			# Executes and returns the result of the query
			self.cursor.execute(getUserQuery, (uid,))
			return self.cursor.fetchone()
		except sqlite3.Error as e:
			print(e)



	def checkIfUserIsPrivileged(self, uid):
		"""
		Determines if the user with the passed in uid is privileged or not

		Parameters
		----------
		uid : str
			The uid to check for

		Returns
		-------
		bool
			True if the user hasan entry in the privileged table, false otherwise
		"""

		# Query for finding a user in the privileged table
		getUserPrivilegeQuery = \
		'''
			SELECT uid
			FROM privileged
			WHERE uid = ?;
		'''


		try:
			# Executes the query to determine if the user is privileged
			self.cursor.execute(getUserPrivilegeQuery, (uid,))
			return self.cursor.fetchone() is not None
		except sqlite3.Error as e:
			print(e)
