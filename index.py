from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

def getAuthenticationAction():
	options = [
		{
			'type': 'list',
			'message': 'Select an action',
			'name': 'authentication method',
			'choices': [
				"Login",
				"Create Account",
				"Exit"
			]
		}
	]

	return prompt(options, style=style)['authentication method']

def getLoginCredentials():
	questions = [
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

	return prompt(questions, style=style)

def getCreateAccountCredentials():
	questions = [
		{
			'type': 'input',
			'message': 'Enter your desired uid:',
			'name': 'uid'
		},
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

	return prompt(questions, style=style)

authenticationMethod = getAuthenticationAction()

if authenticationMethod == 'Login':
	credentials = getLoginCredentials()
	print(credentials)
elif authenticationMethod == 'Create Account':
	credentials = getCreateAccountCredentials()
	print(credentials)