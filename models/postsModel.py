from models import model

class PostsModel(model.Model):
	def checkIfPostIsQuestion(self, pid):
		"""
		Determines if the post is a question

		Parameters
		----------
		pid : str
			The pid of the post

		Returns
		-------
		bool
			True if the post is a question
			False otherwise
		"""

		postIsQuestionQuery = \
		'''
			SELECT pid
			FROM questions
			WHERE pid = ?
		'''

		self.cursor.execute(postIsQuestionQuery, (pid,))
		return self.cursor.fetchone() is not None

	def checkIfUserHasVotedOnPost(self, pid, uid):
		"""
		Determines if the user has voted on the post

		Parameters
		----------
		pid : str
			The pid of the post
		uid : str
			The uid of the user

		Returns
		-------
		bool
			True if the user has voted on the post
			False otherwise
		"""

		userHasVotedQuery = \
		'''
			SELECT uid, pid
			FROM votes
			WHERE
				pid = ?
				AND uid = ?
		'''

		self.cursor.execute(userHasVotedQuery, (pid, uid,))
		return self.cursor.fetchone() is not None


	def addVoteToPost(self, pid, uid):
		"""
		Adds a row to the votes table for the post and user specified

		Parameters
		----------
		pid : str
			The pid of the post being voted on
		uid : str
			The uid of the user giving the vote
		"""

		# Query for getting the number of votes on a post
		numVotesForPostQuery = \
		'''
			SELECT MAX(vno)
			FROM votes
			WHERE pid = ?;
		'''

		# Executes the query and adds 1 to the result for vno
		self.cursor.execute(numVotesForPostQuery, (pid,))
		vno = self.cursor.fetchone() + 1

		# Query to inserts a new element into the votes table
		insertVoteQuery = \
		'''
			INSERT INTO votes
			VALUES (?,?,DATE('now'),?);
		'''

		# Executes the query to insert a row in to the votes table
		self.cursor.execute(insertVoteQuery, (pid, vno, uid,))
		self.connection.commit()

	def getAcceptedAnswer(self, qid):
		"""
		Determines if a question already has an accepted answer

		Parameters
		----------
		qid : str
			The id of the question to update

		Returns
		-------
		None or str
			None if there is no accepted answere
			Otherwise, returrn the pid of the accepted answer
		"""

		# Query to find the accepted answer for a question
		acceptedAnswerQuery = \
		'''
			SELECT theaid
			FROM questions
			WHERE qid = ?
		'''

		# Executes the query to find the accepted answer
		self.cursor.execute(acceptedAnswerQuery, (qid,))


	def markAnswerAsAccepted(self, qid, theaid, userIsPriviliged):
		"""
		Updates a row in the questions table to change the accepted answer

		Parameters
		----------
		qid : str
			The id of the question to update
		theaid : str
			The id of the new accepted answer for the question
		userIsPrivileged : boolean
			Whether or not the user has permission to perform this action
		"""

		# Ensures that the user is privileged
		# This option should be disabled from the view anyways,
		# but its better to be defensive about it
		if not userIsPriviliged:
			return

		# Query to update the accepted answer for a question
		updateAcceptedAnswerQuery = \
		'''
			UPDATE questions
			SET theaid = ?
			WHERE qid = ?
		'''

		# Executes the query to update the accepted answer for a question
		self.cursor.execute(updateAcceptedAnswerQuery, (theaid, qid))
		self.cursor.commit()

	def createAnswer(self, title, body, qid):
		"""
		Inserts a post into the posts table and the answers table

		This implemented as a transaction since we don't want one insert to succeed
		while the other insert fails

		Parameters
		----------
		title : str
			The title of the answer post
		body : str
			The body of the answer post
		qid : str
			The pid of the question which the post is answering
		"""
