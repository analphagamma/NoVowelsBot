import re

class Reader:
    '''
    This class crawls a list of subreddits,
    finds the top n text posts and returns
    a list of objects that contain post data.

    reddit_instance -> a praw.Reddit object with valid login information
    subreddit      -> a string - a valid subreddit
    '''
    
    def __init__(self, reddit_instance, subreddit):
        self.reddit_instance = reddit_instance
        self.subreddit       = subreddit
    
    def get_top_posts(self, n):
        post_list = []
        for post in self.reddit_instance.subreddit(self.subreddit).top():
            if post.is_self:
                post_list.append({'title': post.title,
                                  'text' : post.selftext})
                if len(post_list) == n:
                    return post_list 
        return post_list


class PostTransformer:
    '''
    This class removes the vowels from the post title and text.
    
    posts -> a list of dictionaries - {'title': str, 'text': str}
    '''
    def __init__(self, posts):
        self.posts = posts

    def remove_vowels(self):
        # compile 1 or more of the vowels ignoring the case
        vowels  = re.compile('[aeiou]', re.I)
        clean_posts = []
        for post in self.posts:
            title = re.sub(vowels, '', post['title'])
            text  = re.sub(vowels, '', post['text'])
            clean_posts.append({'title': ' '.join(title.split()),
                                'text' : ' '.join(text.split())
                                })
        return clean_posts

class Poster:
    '''
    So that I don't have to search the documentation again:
    submit(title, selftext=None, url=None, flair_id=None, flair_text=None, resubmit=True, send_replies=True, nsfw=False, spoiler=False, collection_id=None)
Add a submission to the subreddit.

Parameters:	
title – The title of the submission.
selftext – The markdown formatted content for a text submission. Use an empty string, '', to make a title-only submission.
url – The URL for a link submission.
collection_id – The UUID of a Collection to add the newly-submitted post to.
flair_id – The flair template to select (default: None).
flair_text – If the template’s flair_text_editable value is True, this value will set a custom text (default: None).
resubmit – When False, an error will occur if the URL has already been submitted (default: True).
send_replies – When True, messages will be sent to the submission author when comments are made to the submission (default: True).
nsfw – Whether or not the submission should be marked NSFW (default: False).
spoiler – Whether or not the submission should be marked as a spoiler (default: False).
Returns:	
A Submission object for the newly created submission.

Either selftext or url can be provided, but not both.

For example to submit a URL to /r/reddit_api_test do:

title = 'PRAW documentation'
url = 'https://praw.readthedocs.io'
reddit.subreddit('reddit_api_test').submit(title, url=url)
'''
    pass