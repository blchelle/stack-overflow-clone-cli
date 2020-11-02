from views import view
from PyInquirer import style_from_dict, Token, prompt, Separator

class MainView(view.View):
    """
    A base class for views which is not intended to be instantiated
    """

    def getMainAction(self):
        """
        Asks the user what course of action they want to take

        Returns
        -------
        'Post a question' or 'Search for posts' or 'Exit'
        """

        options = [
            {
                'type': 'list',
                'message': 'Select an action',
                'name': 'action method',
                'choices': [
                    "Post a question",
                    "Search for posts",
                    "Log Out"
                ]
            }
        ]

        return prompt(options, style=self.style)['action method']

    def getQuestionPostValues(self):
        """
        Prompts the user to enter title and body for question

        Returns
        -------
        The title and body of question
        """

        postQuestionPrompts = [
            {
                'type': 'input',
                'message': 'Enter question title:',
                'name': 'title'
            },
            {
                'type': 'input',
                'message': 'Enter question body: ',
                'name': 'text'
            }
        ]

        return prompt(postQuestionPrompts, style=self.style)

    def getSearchValues(self):
        """
        Prompts the user to enter keyword to search for posts

        Returns
        -------
        keywords for searching
        """

        SearchPrompts = [
            {
                'type': 'input',
                'message': 'Enter one or more keyword to Search: ',
                'name': 'keywords'
            }
        ]

        return prompt(SearchPrompts, style=self.style)

    def getPostSearchAction(self,result,max_len,showprompt):
        """
        Prompts the user to choose post from Search result

        Returns
        -------
        selected post
        """
        listy=[]

        for post in result:
            string=""
            i=0
            for column in post:
                if(i <4):
                    string+=str(column).ljust(max_len[i], ' ')
                else:
                    string+=str(column)
                string+="   "
                i+=1

            listy.append(string)
        if(showprompt):
            listy.append("Show more results")


        postSearchPrompts = [
            {
                'type': 'list',
                'message': 'Select a Post',
                'name': 'action method',
                'choices': listy
            }
        ]

        return prompt(postSearchPrompts, style=self.style)['action method']
