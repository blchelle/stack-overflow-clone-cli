from models import authModel
from views import authView
from controllers import MainController

class AuthController:
	def __init__(self, pathToDb):
		self.model = authModel.AuthModel(pathToDb)
		self.view = authView.AuthView()
		self.pathToDb = pathToDb

	def run(self):
		"""
		Runs through the authenticaiton process
		"""
		while (True):
			# Prompts and retrieves the users auth choice
			authAction = self.view.getAuthenticationAction()
			if(authAction == {} ):
				self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
				continue
			authAction = authAction['auth method']

			if authAction == 'Login':
				# Prompts and retrieves the users credentials
				credentials = self.view.getLoginCredentials()

				# Attempts to login the user with their credentials provided
				result = self.model.attemptLogin(credentials['uid'], credentials['password'])

				if result is not None:
					MainController.MainController(self.pathToDb).run(credentials['uid']) # move to main controller
				else:
					self.view.logMessage("#ERROR: Wrong uid or password, Try again")


			elif authAction == 'Create Account':
				# Prompts and retrieves the desired uid
				uid = self.view.getCreateAccountUid()

				# Continuously prompts the user for a uid until is is not taken
				uidIsUnique = self.model.getUserByUid(uid) == None
				if(len(uid)>4):
						self.view.logMessage('#ERROR: UID \'{}\' is longer than 4 characters.'.format(uid))
						self.view.logMessage("Please enter a valid uid")
						continue

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
				MainController.MainController(self.pathToDb).run(uid) # move to main controller
			else: # Exit
				break
		return
