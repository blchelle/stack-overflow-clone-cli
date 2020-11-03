import sqlite3
from models import authModel
from views import view
from views import MainView
from models import MainModel
from controllers import postsController

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

        # Continuously prompt the user for the user until they specify "Log Out"
        while True:

            mainAction = self.mainView.getMainAction()

            if mainAction == 'Post a question':
                # Prompts and recieves question values
                postValues = self.mainView.getQuestionPostValues()

                # posts question to database
                self.model.postQuestion(postValues['title'], postValues['text'],user)
                self.view.logMessage("Question posted successfully")
                continue

            elif mainAction == 'Search for posts':
                # Prompts and recieves question valuesx
                postValues = self.mainView.getSearchValues()
                if(postValues['keywords']==""):
                    print("Please enter one or more keywords to search for")
                    continue

                # posts question to database
                result,max_len = self.model.searchPost(postValues['keywords'])
                self.view.logMessage("Results displayed below")
                show=5
                more=True
                searchAction = self.mainView.getPostSearchAction(result[0:show],max_len,more)
                self.view.logMessage(" "+searchAction)
                show+=5
                if(show>len(result)):
                    show=len(result)

                while(searchAction == "Show more results"):
                    if(show>len(result)):
                        show=len(result)
                        more=False
                        searchAction = self.mainView.getPostSearchAction(result[show-5:show],max_len,more)
                        self.view.logMessage(" "+searchAction)
                        break
                
                    searchAction = self.mainView.getPostSearchAction(result[show-5:show],max_len,more)
                    self.view.logMessage(" "+searchAction)
                    show+=5
                    if(show>len(result)):
                        show=len(result)
                        more=False

                if(searchAction == "Back"):
                    continue
                selectedPost = searchAction.split()[0]
                postsController.PostsController().run(user, selectedPost)
            else:
                break
        return
