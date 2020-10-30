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
            self.model.postQuestion(user, postValues['title'], postValues['text'])
            self.view.logMessage("Question posted successfully")
            self.run(user)

        else: # Exit
            return
