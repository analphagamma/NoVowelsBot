import re

class BotEngine:
    '''
    This class removes the vowels from the post title and text.
    
    posts -> a list of dictionaries - {'title': str, 'text': str}
    '''
    def __init__(self, reddit_instance, posts):
        self.reddit_instance = reddit_instance
        self.posts = posts

    def remove_vowels(self):
        '''
        Removes vowels from all posts' title and selftext
        '''
        # compile 1 or more of the vowels ignoring the case
        vowels  = re.compile('[aeiou]', re.I)
        clean_posts = []
        for post in self.posts:
            title = re.sub(vowels, '', post['title'])
            text  = re.sub(vowels, '', post['text'])
            clean_posts.append({'title': ' '.join(title.split()),
                                'text' : ' '.join(text.split()),
                                'id'   : post['id']
                                })
        return clean_posts

    def create_posts(self, subreddit):
        '''
        Creates a post on the subreddit specified.
        
        subreddit -> a Subreddit object
        '''
        posts = self.remove_vowels()
        for post in posts:
            subreddit.submit(title=post['title'],
                             selftext=post['text'])
            self.add_comment(subreddit, post['id'])

    def add_comment(self, sub, submission_id):
        '''
        Adds a comment to the subreddit where the post was read from

        submission_id -> str - used to create a Submission object
        '''

        submission = self.reddit_instance.submission(id=submission_id)
        text = '''This post was featured in /r/fckvwls.   
We removed the unnecessary vowels because to be honest they're disgusting.   
   
^(See my source code at https://github.com/analphagamma/NoVowelsBot)'''

        submission.reply(text)