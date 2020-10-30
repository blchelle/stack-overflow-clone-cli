import sqlite3
from models import authModel
from views import authView
from controllers import MainController

class AuthController:
	def __init__(self):
		self.model = authModel.AuthModel()
		self.view = authView.AuthView()

	def run(self):
		"""
		Runs through the authenticaiton process
		"""

		# Prompts and retrieves the users auth choice
		authAction = self.view.getAuthenticationAction()

		if authAction == 'Login':
			# Prompts and retrieves the users credentials
			credentials = self.view.getLoginCredentials()

			# Attempts to login the user with their credentials provided
			result = self.model.attemptLogin(credentials['uid'], credentials['password'])
			print(result)
			if result is not None:
				MainController.MainController().run(credentials['uid']) # move to main controller


		elif authAction == 'Create Account':
			# Prompts and retrieves the desired uid
			uid = self.view.getCreateAccountUid()

			# Continuously prompts the user for a uid until is is not taken
			uidIsUnique = self.model.getUserByUid(uid) == None
			while not uidIsUnique:
				# Outputs an error message if the uid is not unique
				self.view.logMessage('UID \'{}\' is taken :('.format(uid))

				# Prompts and retrieves the desired uid
				uid = self.view.getCreateAccountUid()

				# Validates that the requested uid is available
				uidIsUnique = self.model.getUserByUid(uid) == None


			# Prompts and retrieves the remainder of the users credentials
			credentials = self.view.getCreateAccountCredentials()

			name = credentials['name']
			city = credentials['city']
			password = credentials['password']

			# Creates an entry in the users table
			self.model.createAccount(name, city, uid, password)
			MainController.MainController().run(uid) # move to main controller
		else: # Exit
			return

		# TODO: Move into the main application
