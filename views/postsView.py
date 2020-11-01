from views import view
from PyInquirer import prompt

class PostsView(view.View):

	def getPostAction(self, postIsQuestion, userHasVoted, userIsPrivileged):
		"""
		Asks the user how they'd like to authenticate and returns the result

		Returns
		-------
		'Login' or 'Create Account' or 'Exit'
		"""

		choices = []
		if not userHasVoted:
			choices.append("Upvote Post")
		if postIsQuestion:
			choices.append("Answer Question")
		if userIsPrivileged:
			choices.append("Give Badge to Poster")
			choices.append("Add Tag to Post")
			choices.append("Edit Post")

			if not postIsQuestion:
				choices.append("Mark Answer As Accepted")


		options = [
			{
				'type': 'list',
				'message': 'Select an action',
				'name': 'post action',
				'choices': choices
			}
		]

		return prompt(options, style=self.style)['post action']
