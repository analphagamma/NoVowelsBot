import praw
import json

# getting login information
class NoVowelsBot():

    def __init__(self, login_info):
        self.login_info = login_info

        # open and loaf login info
        with open('./resources/'+self.login_info, 'r') as f:
            self.LOGIN = json.load(f)
        # initialize Reddit object
        self.reddit = praw.Reddit(client_id     = self.LOGIN.get('client_id'),
                                  client_secret = self.LOGIN.get('client_secret'),
                                  user_agent    = self.LOGIN.get('user_agent'),
                                  user_name     = self.LOGIN.get('user_name'),
                                  password      = self.LOGIN.get('password')
                                  )
    def botobject(self):
        return self.reddit
