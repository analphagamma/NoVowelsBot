import praw
import re
import json
from datetime import datetime, timedelta
from time import sleep
import sys, os.path
from pprint import pprint

# getting login information
class NoVowelsBot():

    def __init__(self, login_info):
        self.login_info = login_info

    def get_login_details(self):
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
        if os.path.isfile('./resources/'+self.login_info):
            # if the bot is run locally we get the login details from the JSON file
            f = open('./resources/'+self.login_info, 'r')
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
        else:
            # if run on Heroku we need to use the config vars
            login = {
                'username'      : os.environ.get('username'),
                'password'      : os.environ.get('password'),
                'client_id'     : os.environ.get('client_id'),
                'client_secret' : os.environ.get('client_secret'),
                'user_agent'    : os.environ.get('user_agent')
            }
            # test for empty values or missing keys
            if '' in login.values() or \
                None in [login.get('client_id'),
                        login.get('client_secret'),
                        login.get('user_agent'),
                        login.get('username'),
                        login.get('password')]:
                raise IncompleteLoginDetailsError
            else:
                return login
    
    def init_bot(self):
        login = self.get_login_details()
        # initialize Reddit object
        return praw.Reddit(client_id     = login.get('client_id'),
                           client_secret = login.get('client_secret'),
                           user_agent    = login.get('user_agent'),
                           username     = login.get('username'),
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

def remove_vowels(post):
    '''
    Removes vowels from a post's title and selftext
    '''
    # compile 1 or more of the vowels ignoring the case
    vowels  = re.compile('[aeiou]', re.I)
    title = re.sub(vowels, '', post['title'])
    text  = re.sub(vowels, '', post['text'])
    return {'title': ' '.join(title.split()),
            'text' : ' '.join(text.split()),
            'id'   : post['id']}

def get_posts(sub, score, since_day, no_posts):
    # collect todays top posts
    posts_collected = 0
    posts = []
    for submission in sub.top(time_filter='day'):
        if submission.score >= score and \
        submission.created_utc > since_day and \
        submission.is_self:
            posts.append({'title': submission.title,
                        'text' : submission.selftext,
                        'id'  : submission.id})
            posts_collected += 1
            if posts_collected > no_posts:
                break
    # if no new top posts - quit
    if posts == []:
        return None
    else:
        return posts

def create_posts(reddit, posts, sub='fckvwls'):
    '''
    Creates a post on the subreddit specified.
    
    posts   -> list of dicts - a list of posts with keys 'title', 'text', 'id'
    sub     -> str - a subreddit name. defaults to 'fckvlws'. only change it for tests
    '''

    def add_comment(submission_id):
        '''
        Adds a comment to the subreddit where the post was read from

        submission_id -> str - used to create a Submission object
        '''

        submission = reddit.submission(id=submission_id)
        text = '''This post was featured in /r/fckvwls.   
    We removed the unnecessary 👎 vowels 🤮 because to be honest they're disgusting.💩   
    ---   
    *(See my source code [here](https://github.com/analphagamma/NoVowelsBot))*'''

        submission.reply(text)

    target_sub = reddit.subreddit(sub)
    for post in posts:
        clean_post = remove_vowels(post)
        try:
            target_sub.submit(title    = clean_post['title'],
                              selftext = clean_post['text'])
            add_comment(post['id'])
        except praw.exception.APIException:
            print('We\'re still doing it too much... :(')
        # to avoid "you're doing that too much."
        sleep(600)

if __name__ == '__main__':
    # constants
    SUBREDDITS = ['all']
    SCORE_THRESHOLD = 5000
    DAYS = 1
    SINCE = (datetime.today() - timedelta(days=DAYS)).timestamp() # yesterday 00:00 in UNIX timestamp
    NO_OF_POSTS = 5

    # initialize bot
    nvbot = NoVowelsBot('credentials.json')
    # get reddit instance
    reddit = nvbot.init_bot()
    # define which subreddit(s) we're looking at
    subreddits = reddit.subreddit('+'.join(SUBREDDITS))
    posts = get_posts(subreddits, SCORE_THRESHOLD, SINCE, NO_OF_POSTS)
    # exit if no posts meet the requirements
    if not posts:
        sys.exit(0)
    clean_posts = list(map(remove_vowels, posts))
    # post on /r/fckvwls    
    create_posts(reddit, clean_posts)