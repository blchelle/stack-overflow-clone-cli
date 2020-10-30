from models import model
import uuid

class MainModel(model.Model):

    def postQuestion(self, title, body, poster):
        """
        inserts question posts into the database


        Parameters
        ----------
        title : str
            title of question
        body : str
            body of question
        poster: str
            username of poster

        Return
        ----------
        None or {}

        """
        pid = str(uuid.uuid4()).replace('-','')
        insertPostQuery = \
        '''
            INSERT INTO posts
            VALUES (?,DATE('now'),?,?,?);
        '''
        insertQuestionQuery = \
        '''
            INSERT INTO questions
            VALUES (?,?);
        '''

        # Executes and commits the query with the passed in parameters
        self.cursor.execute(insertPostQuery,(pid ,title, body, poster))
        self.cursor.execute(insertQuestionQuery, (pid, ""))
        self.connection.commit()
