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
        s+=searchPostsQuery_1
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
            ORDER BY Matches DESC
            ;'''


        # print(s)
        # print("")

        #   Executes and commits the query with the passed in parameters
        self.cursor.execute(s)
        # row	=self.cursor.fetchone()	
        # print(row.keys())
        result=self.cursor.fetchall()
        #print(pd.read_sql_query(s,self.connection))
        
        self.cursor.execute("SELECT MAX(LENGTH(pid)) FROM posts;")
        pid_len = self.cursor.fetchone()
        self.cursor.execute("SELECT MAX(LENGTH(title)) FROM posts;")
        title_len = self.cursor.fetchone()
        self.cursor.execute("SELECT MAX(LENGTH(body)) FROM posts;")
        body_len = self.cursor.fetchone()
        max_len=[pid_len[0],10,title_len[0],body_len[0]]
	

        self.connection.commit()
        return result,max_len
