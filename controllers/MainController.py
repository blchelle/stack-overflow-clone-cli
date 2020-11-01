import sqlite3
from models import authModel
from views import view
from views import MainView
from models import MainModel

class MainController:
    def __init__(self):
        self.model = MainModel.MainModel()
        self.view = view.View()
        self.mainView = MainView.MainView()


    def run(self, user):
        """
        Runs through the main menu process
        """
        # Prompts and retrieves the users main action choice
        mainAction = self.mainView.getMainAction()

        if mainAction == 'Post a question':
            # Prompts and recieves question values
            postValues = self.mainView.getQuestionPostValues()

            # posts question to database
            self.model.postQuestion(postValues['title'], postValues['text'],user)
            self.view.logMessage("Question posted successfully")
            self.run(user)

        elif mainAction == 'Search for posts':
            # Prompts and recieves question valuesx
            postValues = self.mainView.getSearchValues()

            # posts question to database
            result,max_len = self.model.searchPost(postValues['keywords'])
            self.view.logMessage("Results displayed above")
            searchAction = self.mainView.getPostSearchAction(result[0:5],max_len,True)

            if(searchAction == "Show more results"):
                searchAction = self.mainView.getPostSearchAction(result,max_len,False)

            self.run(user)

        else: # Exit
            return