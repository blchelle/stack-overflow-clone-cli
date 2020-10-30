from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token

class View:
	"""
	A base class for views which is not intended to be instantiated
	"""

	def __init__(self):
		self.style = style_from_dict({
			Token.Separator: '#cc5454',
			Token.QuestionMark: '#673ab7 bold',
			Token.Selected: '#cc5454',  # default
			Token.Pointer: '#673ab7 bold',
			Token.Instruction: '',  # default
			Token.Answer: '#f44336 bold',
			Token.Question: '',
		})

	def logMessage(self, message):
		"""
		Logs a message to the console

		Parameters
		----------
		message : str
			The message to log
		"""

		print("  " + message)
