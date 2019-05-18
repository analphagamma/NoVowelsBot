import praw
import json
from datetime import datetime, timedelta
import sys
from pprint import pprint

from modules.BotEngine import BotEngine

# constants
SUBREDDITS = ['all']
SCORE_THRESHOLD = 1000
YDAY = (datetime.today() - timedelta(days=1)).timestamp() # yesterday 00:00 in UNIX timestamp
NO_OF_POSTS = 5

# getting login information
class NoVowelsBot():

    def __init__(self, login_info):
        self.login_info = login_info

    def login_details(self):
        '''
        Return the login info as a dictionary.
        It contains the following keys:
        client_id
        client_secret
        user_agent
        user_name
        password
        '''

        # test if file is present
        try:
            f = open('./resources/'+self.login_info, 'r')
        except FileNotFoundError:
            raise LoginFileNotFound
        
        # test if JSON file is valid
        try:
            login = json.load(f)
        except json.decoder.JSONDecodeError:
            f.close() # close the file before panicking
            raise NotJSONFileError
        f.close() # we don't need the file open anymore

        # test for empty values or missing keys
        if '' in login.values() or \
            None in [login.get('client_id'),
                     login.get('client_secret'),
                     login.get('user_agent'),
                     login.get('username'),
                     login.get('password')]:
            raise IncompleteLoginDetailsError

        return login
    
    def init_bot(self):
        login = self.login_details()
        # initialize Reddit object
        return praw.Reddit(client_id     = login.get('client_id'),
                           client_secret = login.get('client_secret'),
                           user_agent    = login.get('user_agent'),
                           user_name     = login.get('username'),
                           password      = login.get('password')
                           )

class LoginFileNotFound(Exception):
    '''
    Custom exception to be raised when the json file with the
    login info is not found.
    '''
    pass

class NotJSONFileError(Exception):
    '''
    Custom exception to be raised when the credentials file
    isn't a valid json
    '''
    pass

class IncompleteLoginDetailsError(Exception):
    '''
    Custom exception for incorrect credentials file structure
    '''
    pass

if __name__ == '__main__':
    # initialize bot
    nvbot = NoVowelsBot('credentials.json')
    # get reddit instance
    reddit = nvbot.init_bot()
    # define which subreddit(s) we're looking at
    subreddits = reddit.subreddit('+'.join(SUBREDDITS))

    # main loop for bot
    # collect todays top posts
    no_posts = 0
    posts = []
    for submission in subreddits.top(time_filter='day'):
        if submission.score >= SCORE_THRESHOLD and \
           submission.created_utc > YDAY and \
           submission.is_self:
            posts.append({'title': submission.title,
                          'text' : submission.selftext,
                          'id'  : submission.id})
            no_posts += 1
            if no_posts > NO_OF_POSTS:
                break
    
    # if no new top posts - quit
    if posts == []:
        sys.exit(0)

    # "clean" posts
    engine = BotEngine(reddit, posts)

    clean_posts = engine.remove_vowels()
    pprint(clean_posts)
    # post on /r/fckvwls
    fckvwls = reddit.subreddit('fckvwls')
    engine.create_posts(fckvwls)