from models import model
import uuid
import sqlite3

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
			WHERE pid = ?;
		'''

		try:

			self.cursor.execute(postIsQuestionQuery, (pid,))
			return self.cursor.fetchone() is not None
		except sqlite3.Error as e:
			print(e)



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
				AND uid = ?;
		'''

		try:
			self.cursor.execute(userHasVotedQuery, (pid, uid,))
			return self.cursor.fetchone() is not None
		except sqlite3.Error as e:
			print(e)




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
			SELECT COUNT(*)
			FROM votes
			WHERE pid = ?;
		'''

		try:
			# Executes the query and adds 1 to the result for vno
			self.cursor.execute(numVotesForPostQuery, (pid,))
		except sqlite3.Error as e:
			self.connection.rollback()
			print(e)




		numberOfVotes = int(self.cursor.fetchone()[0])
		vno = numberOfVotes + 1

		# Query to inserts a new element into the votes table
		insertVoteQuery = \
		'''
			INSERT INTO votes
			VALUES (?,?,DATE('now'),?);
		'''

		try:
			# Executes the query to insert a row in to the votes table
			self.cursor.execute(insertVoteQuery, (pid, vno, uid,))
			self.connection.commit()
		except sqlite3.Error as e:
			self.connection.rollback()
			print(e)





	def checkIfAnswerIsAccepted(self, aid):
		"""
		Determines if the answer to a question is already the accepted answer

		Parameters
		----------
		aid : str
			The pid of the answer
		"""

		answerIsAcceptedQuery = \
		'''
			SELECT *
			FROM questions
			WHERE theaid = ?;
		'''

		try:
			self.cursor.execute(answerIsAcceptedQuery, (aid,))
			return self.cursor.fetchone() is not None
		except sqlite3.Error as e:
			print(e)



	def checkIfQuestionHasAnAcceptedAnswer(self, qid):
		"""
		Determines if a question already has an accepted answer

		Parameters
		----------
		qid : str
			The id of the question to update

		Returns
		-------
		str or None
			False if there is no accepted answer
			True otherwise
		"""

		# Query to find the accepted answer for a question
		acceptedAnswerQuery = \
		'''
			SELECT theaid
			FROM questions
			WHERE pid = ?;
		'''

		try:
			# Executes the query to find the accepted answer
			self.cursor.execute(acceptedAnswerQuery, (qid,))
			result = self.cursor.fetchone()
			return result[0] != ''
		except sqlite3.Error as e:
			print(e)





	def markAnswerAsAccepted(self, qid, theaid, userIsPrivileged):
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
		if not userIsPrivileged:
			return

		# Query to update the accepted answer for a question
		updateAcceptedAnswerQuery = \
		'''
			UPDATE questions
			SET theaid = ?
			WHERE pid = ?;
		'''

		try:
			# Executes the query to update the accepted answer for a question
			self.cursor.execute(updateAcceptedAnswerQuery, (theaid, qid,))
			self.connection.commit()
		except sqlite3.Error as e:
			self.connection.rollback()
			print(e)




	def createAnswer(self, title, body, qid, uid):
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
		uid : str
			The uid of the user creating the answer

		Returns
		-------
		bool
			True if the answer was successfully inserted into both tables
			False if there was an error at either step
		"""

		checkPIDExistsQuery = \
        '''
            SELECT pid
            FROM posts
            WHERE pid = ?;
        '''
		
		pidExists = True
		while(pidExists):
			pid = str(uuid.uuid4()).replace('-','')[:4]
			self.cursor.execute(checkPIDExistsQuery,(pid,))
			if(self.cursor.fetchone() is None):
					pidExists = False

		createAnswerQuery = \
		'''
			INSERT INTO answers
			VALUES (?,?);
		'''

		createPostQuery = \
		'''
			INSERT INTO posts
			VALUES (?,DATE('now'),?,?,?);
		'''

		try:
			self.cursor.execute(createAnswerQuery, (pid, qid))
			self.cursor.execute(createPostQuery, (pid, title, body, uid,))
			self.connection.commit()
			return True
		except:
			self.connection.rollback()
			return False

	def getQuestionAnsweredByPost(self, pid):
		"""
		Gets the qid of the question which the answer post is answering

		Parameters
		----------
		pid : str
			The pid of the answer

		Returns
		-------
		str
			The qid of the question answered by the answer
		"""

		getQuestionQuery = \
		'''
			SELECT qid
			FROM answers
			WHERE pid = ?;
		'''


		try:
			self.cursor.execute(getQuestionQuery, (pid,))
			return self.cursor.fetchone()[0]
		except sqlite3.Error as e:
			print(e)



	def addBadgeToPoster(self,bType,bName,pid,userIsPrivileged):
		"""
		Add to the badges table and ubadges table

		Parameters
		----------
		bType : str
			Badge Type
		bName : str
			Name given to the badge by user for poster
		pid : str
			post id
		userIsPrivileged : boolean
			Whether or not the user has permission to perform this action
		"""

		# Ensures that the user is privileged
		# This option should be disabled from the view anyways,
		# but its better to be defensive about it
		if not userIsPrivileged:
			return

		# Query to add the badge to poster

		badgeExistsQuery = \
		'''
			SELECT bname
			FROM badges
			WHERE bname like ?;
		'''

		try:
			self.cursor.execute(badgeExistsQuery, (bName,))
			if(self.cursor.fetchone() is not None):
				return -1
		except sqlite3.Error as e:
			print(e)




		posterQuery = \
		'''
			SELECT poster
			FROM posts
			WHERE pid=?;
		'''

		try:

			self.cursor.execute(posterQuery, (pid,))
			uid = self.cursor.fetchone()[0]
		except sqlite3.Error as e:
			print(e)



		ubadgeExistsQuery = \
		'''
			SELECT bname
			FROM ubadges
			WHERE bdate = DATE('now') and uid = ?;
		'''


		try:
			self.cursor.execute(ubadgeExistsQuery, (uid,))
			if(self.cursor.fetchone() is not None):
				return -2
		except sqlite3.Error as e:
			print(e)




		addBadge = \
		'''
			INSERT INTO badges
			VALUES (?,?);
		'''

		adduBadge = \
		'''
			INSERT INTO ubadges
			VALUES (?,DATE('now'),?);
		'''


		try:
			# Executes the query to update the accepted answer for a question
			self.cursor.execute(addBadge, (bName, bType,))
			self.cursor.execute(adduBadge, (uid,bName,))
			self.connection.commit()
			return False
		except sqlite3.Error as e:
			self.connection.rollback()
			print(e)



	def addTagToPost(self,tag,pid,userIsPrivileged):
		"""
		Add to the tags table

		Parameters
		----------
		tag : str
			tag name
		pid : str
			post id
		userIsPrivileged : boolean
			Whether or not the user has permission to perform this action
		"""

		# Ensures that the user is privileged
		# This option should be disabled from the view anyways,
		# but its better to be defensive about it
		if not userIsPrivileged:
			return

		# Query to add the badge to poster

		tagExistsQuery = \
		'''
			SELECT tag
			FROM tags
			WHERE tag like ?;
		'''

		try:
			self.cursor.execute(tagExistsQuery, (tag,))
			if(self.cursor.fetchone() is not None):
				return True
		except sqlite3.Error as e:
			print(e)



		addTag = \
		'''
			INSERT INTO tags
			VALUES (?,?);
		'''

		try:
			# Executes the query to update the accepted answer for a question
			self.cursor.execute(addTag, (pid,tag,))
			self.connection.commit()
			return False
		except sqlite3.Error as e:
			self.connection.rollback()
			print(e)





	def editPost(self, pid, title, body):
		"""
		edit posts with the specified pid

		Parameters
		----------
		pid : str
			The pid of the answer
		title: str
			The title of the post
		body: str
			The body of the posts

		Returns
		-------
		"""

		editPostQuery = \
		'''
			UPDATE posts
			set title = ?, body = ? where pid = ?;
		'''

		try:
			self.cursor.execute(editPostQuery, (title, body, pid))
			self.connection.commit()
		except sqlite3.Error as e:
			self.connection.rollback()
			print(e)
