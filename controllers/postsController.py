from models import postsModel
from views import postsView
from models import authModel

class PostsController:
	def __init__(self):
		self.model = postsModel.PostsModel()
		self.view = postsView.PostsView()

	def run(self, uid, pid):
		"""
		Runs through the post action process
		"""

		userIsPrivileged = authModel.AuthModel().checkIfUserIsPrivileged(uid)
		postIsQuestion = self.model.checkIfPostIsQuestion(pid)

		postAction = ''
		while postAction is not 'Back':
			userHasVotedOnPost = self.model.checkIfUserHasVotedOnPost(pid, uid)
			postIsAcceptedAnswer = not postIsQuestion and self.model.checkIfAnswerIsAccepted(pid)

			# Prompts the user for the action they want to perform on the post
			postAction = self.view.getPostAction(
				postIsQuestion,
				userHasVotedOnPost,
				userIsPrivileged,postIsAcceptedAnswer
			)



			if postAction == 'Upvote Post':
				self.model.addVoteToPost(pid, uid)
				self.view.logMessage("Successfully upvoted post")

			elif postAction == 'Answer Question':
				postValues = self.view.getAnswerPostValues()
				title = postValues['title']
				body = postValues['body']
				postCreationIsSuccessful = self.model.createAnswer(title, body, pid, uid)

				if postCreationIsSuccessful:
					self.view.logMessage("Successfully added your answer")
				else:
					self.view.logMessage("Failed to add your answer")

			elif postAction == 'Give Badge to Poster':
				print("Archit")

			elif postAction == 'Add Tag to Post':
				print("Archit")

			elif postAction == 'Mark Answer As Accepted':
				qid = self.model.getQuestionAnsweredByPost(pid)

				questionHasAcceptedAnswer = self.model.checkIfQuestionHasAnAcceptedAnswer(qid)

				if questionHasAcceptedAnswer:
					overwriteAcceptedAnswer = self.view.promptToOverwriteAcceptedAnswer()

					if overwriteAcceptedAnswer:
						self.model.markAnswerAsAccepted(qid, pid, userIsPrivileged)
				else:
					self.model.markAnswerAsAccepted(qid, pid, userIsPrivileged)

			elif postAction == 'Edit Post':
				postValues = self.view.getPostValues()
				self.model.editPost(pid, postValues['title'], postValues['body'])
				self.view.logMessage("Post editted successfully")
