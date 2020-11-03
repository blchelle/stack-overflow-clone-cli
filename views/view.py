from __future__ import print_function, unicode_literals

from PyInquirer import style_from_dict, Token

class View:
	"""
	A base class for views which is not intended to be instantiated
	"""

	def __init__(self):
		self.style = style_from_dict({
			Token.Separator: '#CC5454',
			Token.QuestionMark: '#BCBBBB bold',
			Token.Selected: '#F48024',  # default
			Token.Pointer: '#F48024 bold',
			Token.Instruction: '',  # default
			Token.Answer: '#F48024 bold',
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
