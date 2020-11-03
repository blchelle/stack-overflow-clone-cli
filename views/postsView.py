from views import view
from PyInquirer import prompt

class PostsView(view.View):

	def getPostAction(self, postIsQuestion, userHasVoted, userIsPrivileged, answerIsAccepted):
		"""
		Asks the user how they'd like to authenticate and returns the result

		Returns
		-------
		'Login' or 'Create Account' or 'Exit'
		"""

		choices = []
		if not userHasVoted:
			choices.append('Upvote Post')
		if postIsQuestion:
			choices.append('Answer Question')
		if userIsPrivileged:
			choices.append('Give Badge to Poster')
			choices.append('Add Tag to Post')
			choices.append('Edit Post')

			if not postIsQuestion and not answerIsAccepted:
				choices.append('Mark Answer As Accepted')

		choices.append('Back')


		options = [
			{
				'type': 'list',
				'message': 'Select an action',
				'name': 'post action',
				'choices': choices
			}
		]

		return prompt(options, style=self.style)['post action']

	def getAnswerPostValues(self):
		"""
		Prompts the user to enter title and body for an answer

		Returns
		-------
		The title and body of an answer
		"""

		postAnswerPrompts = [
			{
				'type': 'input',
				'message': 'Enter answer title:',
				'name': 'title'
			},
			{
				'type': 'input',
				'message': 'Enter answer body: ',
				'name': 'body'
			}
		]

		return prompt(postAnswerPrompts, style=self.style)
	def getPostValues(self):
		"""
		Prompts the user to enter title and body for a post

		Returns
		-------
		The title and body of an answer
		"""

		postAnswerPrompts = [
			{
				'type': 'input',
				'message': 'Enter post title:',
				'name': 'title'
			},
			{
				'type': 'input',
				'message': 'Enter post body: ',
				'name': 'body'
			}
		]

		return prompt(postAnswerPrompts, style=self.style)


	def promptToOverwriteAcceptedAnswer(self):
		"""
		Prompts the user if they would like to overwrite the accepted answer for a question

		Returns
		-------
		bool
			True if the user selects yes,
			False otherwise
		"""

		overwritePrompt = {
			"type": "confirm",
			"name": "confirm",
			"message": "There is already an accepted answer, would you like to overwrite it?"
		}

		# Prompts the user if they want to overwrite the existing accepted anwser
		return prompt(overwritePrompt, style=self.style)['confirm']
	
	def getBadgeValues(self):
		"""
		Asks the user which badge type and name to give poster 

		Returns
		-------
		Badge Type and Name
		"""

		badges = []
		badges.append('Gold')
		badges.append('Silver')
		badges.append('Bronze')


		options = [
			{
				'type': 'list',
				'message': 'Select the Type of Badge to give',
				'name': 'bType',
				'choices': badges
			},

			{
				'type': 'input',
				'message': 'Enter the Badge name:',
				'name': 'bName'
			}
		]

		return prompt(options, style=self.style)

	def getTagValue(self):
		"""
		Asks the value of the tag to be placed on the post

		Returns
		-------
		Tag Name
		"""


		options = [

			{
				'type': 'input',
				'message': 'Enter the Tag:',
				'name': 'tag'
			}
		]

		return prompt(options, style=self.style)['tag']

	def getEditPostValues(self):
		"""
		Prompts the user to enter title and body for editing a post

		Returns
		-------
		title and body string list
		"""

		editPostAnswerPrompts = [
			{
				'type': 'input',
				'message': 'Enter new title:',
				'name': 'title'
			},
			{
				'type': 'input',
				'message': 'Enter new body: ',
				'name': 'body'
			}
		]

		return prompt(editPostAnswerPrompts, style=self.style)

