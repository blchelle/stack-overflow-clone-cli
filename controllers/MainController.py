from views import view
from views import MainView
from models import MainModel
from controllers import postsController

class MainController:
    def __init__(self, pathToDb):
        self.model = MainModel.MainModel(pathToDb)
        self.view = view.View()
        self.mainView = MainView.MainView()
        self.pathToDb = pathToDb


    def run(self, user):
        """
        Runs through the main menu process
        """
        # Prompts and retrieves the users main action choice

        # Continuously prompt the user for the user until they specify "Log Out"
        while True:

            mainAction = self.mainView.getMainAction()
            if(mainAction == {}):
                self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
                continue
            mainAction = mainAction['action method']

            if mainAction == 'Post a question':
                # Prompts and recieves question values
                postValues = self.mainView.getQuestionPostValues()

                # posts question to database
                self.model.postQuestion(postValues['title'], postValues['text'],user)
                self.view.logMessage("Question posted successfully")
                continue

            elif mainAction == 'Search for posts':
                # Prompts and recieves search values
                postValues = self.mainView.getSearchValues()
                if(postValues['keywords'].strip()==""):
                    self.view.logMessage("#ERROR: Please enter one or more keywords to search for")
                    continue

                # finds all search results from the database
                result,max_len = self.model.searchPost(postValues['keywords'])
                if(result == []):
                    self.view.logMessage("# NO MATCHING RESULTS, try a different keyword")
                    continue
                self.view.logMessage("Results displayed below")
                #counters for showing 5 results at a time

                numPostsRemaining = len(result) - 5
                if (numPostsRemaining > 0):
                    more = True
                else:
                    more = False

                searchAction = self.mainView.getPostSearchAction(result[0:5], max_len, more)
                if(searchAction == {} ):
                    self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
                    continue
                searchAction = searchAction['action method']

                # Posting selected post to screen
                self.view.logMessage(" "+searchAction)

                #show 5 more as asked more
                pageNumber = 0
                while(searchAction == "Show more results"):
                    #show the max results possible here and break
                    pageNumber += 1

                    if (numPostsRemaining - 5 > 0):
                        more = True
                    else:
                        more = False

                    searchAction = self.mainView.getPostSearchAction(
                        result[pageNumber * 5 : pageNumber * 5 + min(numPostsRemaining, 5)],
                        max_len,
                        more
                    )

                    if(searchAction == {} ):
                        self.view.logMessage("#ERROR: Don't Click on the Options, Try again with keystrokes")
                        continue
                    searchAction = searchAction['action method']

                    numPostsRemaining -= 5

                if(searchAction == "Back"):
                    continue

                #retrieve the post id and go to post action menu
                selectedPost = searchAction.split()[0]
                postsController.PostsController(self.pathToDb).run(user, selectedPost)

            else: # Log out
                return
