from models import model
import uuid
import sqlite3

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


        insertPostQuery = \
        '''
            INSERT INTO posts
            VALUES (?,DATE('now', 'localtime'),?,?,?);
        '''
        insertQuestionQuery = \
        '''
            INSERT INTO questions
            VALUES (?,?);
        '''
        try:
            # Executes and commits the query with the passed in parameters
            self.cursor.execute(insertPostQuery,(pid ,title, body, poster))
            self.cursor.execute(insertQuestionQuery, (pid, ""))
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(e)



    def searchPost(self,keywordString):
        """
       search posts from the database


        Parameters
        ----------
        keywordString: str
            search keywords

        Return
        ----------
        result: list of lists
        max_len: list of formatting numbers

        """
        #Get the list of keywords to search for
        keywords = keywordString.split()

        #Create a String to include all keywords to search for in all needed tables
        s = \
        '''
            SELECT p.pid AS pID, p.pdate AS pDate , p.title AS Title , p.body AS Body , p.poster AS Poster,
            IFNULL((SELECT MAX(v.vno) FROM votes v WHERE p.pid=v.pid),0) AS no_of_votes,
            (SELECT COUNT(DISTINCT a.pid) FROM questions q ,answers a WHERE q.pid=p.pid AND a.qid=q.pid) AS no_of_answers,
            (SELECT "N/A" FROM answers a WHERE p.pid = a.pid),
        '''

        #For every  keyword, add the checks required and count matches and order them
        for keyword in keywords:

            if(keyword!=keywords[0]):
                s+=" + "

            s+='''
            ((p.title like \'%'''
            s+=keyword
            s+="%\') OR "

            s+="(p.body like \'%"
            s+=keyword
            s+="%\') OR "

            s+="(SELECT COUNT(DISTINCT t.tag) FROM tags t WHERE t.tag like \'%"
            s+=keyword
            s+="%\'AND t.pid=p.pid))"

        s+='''
            AS Matches '''
        s+='''FROM posts p
            WHERE Matches > 0
            ORDER BY Matches DESC
            ;'''

        #   Executes and commits the query with the passed in parameters
        try:
            self.cursor.execute(s)
            result=self.cursor.fetchall()

            self.cursor.execute("SELECT MAX(LENGTH(pid)) FROM posts;")
            pid_len = self.cursor.fetchone()
            self.cursor.execute("SELECT MAX(LENGTH(title)) FROM posts;")
            title_len = self.cursor.fetchone()
            self.cursor.execute("SELECT MAX(LENGTH(body)) FROM posts;")
            body_len = self.cursor.fetchone()
            #formatting lengths are retrived from max
            max_len=[pid_len[0],10,title_len[0],body_len[0],4,4,4,4]
            if(None in max_len):
                max_len=[10,10,10,10,10,10,10,10]

            self.connection.commit()
            return result, max_len
        except sqlite3.Error as e:
            self.connection.rollback()
            print(e)
