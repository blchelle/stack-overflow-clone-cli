from models import model
import uuid
import pandas as pd

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

        """

        searchPostsQuery_1 = \
        '''
            SELECT p.pid AS pID, p.pdate AS pDate , p.title AS Title , p.body AS Body , p.poster AS Poster,
            IFNULL((SELECT MAX(v.vno) FROM votes v WHERE p.pid=v.pid),0) AS no_of_votes,
            (SELECT COUNT(DISTINCT a.pid) FROM questions q ,answers a WHERE q.pid=p.pid AND a.qid=q.pid) AS no_of_answers,
        '''
        keywords = keywordString.split()
        s=""
        tag_count=""
        s+=searchPostsQuery_1
        for keyword in keywords:
            s+="    (p.title like \'%"
            s+=keyword
            s+="%\')+"

            s+="(p.body like \'%"
            s+=keyword
            s+="%\')+"

            if(keyword!=keywords[0]):
                tag_count+="or "
            tag_count+="t.tag=\'"
            tag_count+=keyword
            tag_count+="\' "
            
        s+='''
            (SELECT COUNT(DISTINCT t.tag) FROM tags t WHERE ('''
        s+=tag_count
        s+=") AND t.pid=p.pid) AS Matches "
        s+='''FROM posts p
            ORDER BY Matches DESC
            LIMIT 5;'''


        # print(s)
        # print("")

        #   Executes and commits the query with the passed in parameters
        self.cursor.execute(s)
        # row	=self.cursor.fetchone()	
        # print(row.keys())
        result=self.cursor.fetchall()
        print(pd.read_sql_query(s,self.connection))
	

        self.connection.commit()
        return result
