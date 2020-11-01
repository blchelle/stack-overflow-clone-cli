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
		userHasVotedOnPost = self.model.checkIfUserHasVotedOnPost(pid, uid)
		postIsQuestion = self.model.checkIfPostIsQuestion(pid)

		postAction = self.view.getPostAction(postIsQuestion, userHasVotedOnPost, userIsPrivileged)

		if postAction == 'Upvote Post':
			print("Brocks")
		elif postAction == 'Answer Question':
			print("Archit")
		elif postAction == 'Give Badge to Poster':
			print("Archit")
		elif postAction == 'Add Tag to Post':
			print("Archit")
		elif postAction == 'Mark Answer As Accepted':
			print("Brocks")
		elif postAction == 'Edit Post':
			print("Archit")