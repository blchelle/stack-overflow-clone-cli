from views import view
from PyInquirer import style_from_dict, Token, prompt, Separator

class AuthView(view.View):

	def getAuthenticationAction(self):
		"""
		Asks the user how they'd like to authenticate and returns the result

		Returns
		-------
		'Login' or 'Create Account' or 'Exit'
		"""

		options = [
			{
				'type': 'list',
				'message': 'Select an action',
				'name': 'auth method',
				'choices': [
					"Login",
					"Create Account",
					"Exit"
				]
			}
		]

		return prompt(options, style=self.style)['auth method']

	def getLoginCredentials(self):
		"""
		Prompts the user to enter their credentials and returns the result

		Returns
		-------
		{}
			The users entered login credentials
		"""

		loginPrompts = [
			{
				'type': 'input',
				'message': 'Enter your uid:',
				'name': 'uid'
			},
			{
				'type': 'password',
				'message': 'Enter your password:',
				'name': 'password'
			}
		]

		return prompt(loginPrompts, style=self.style)

	def getCreateAccountCredentials(self):
		"""
		Prompts the user to enter their account information
		and returns the result

		Returns
		-------
		{}
			The users entered information
		"""

		createAccountPrompts = [
			{
				'type': 'input',
				'message': 'Enter your name:',
				'name': 'name'
			},
			{
				'type': 'input',
				'message': 'Enter your city:',
				'name': 'city'
			},
			{
				'type': 'password',
				'message': 'Enter your desired password:',
				'name': 'password'
			}
		]

		return prompt(createAccountPrompts, style=self.style)

	def getCreateAccountUid(self):
		"""
		Prompts and retrieves the users desired uid

		This is separate from getCreateAccountCredentials because we
		want to be able to tell the user if their uid is not unique
		before making them input the rest of their information

		Returns
		-------
		str
			The uid entered by the user
		"""

		uidPrompt = [
			{
				'type': 'input',
				'message': 'Enter your desired uid:',
				'name': 'uid'
			}
		]

		return prompt(uidPrompt, style=self.style)['uid']
