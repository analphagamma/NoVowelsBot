import unittest
import praw
from NoVowelsBot import *

class BotTest(unittest.TestCase):

    def test1_get_posts_from_test_subreddit(self):
        SCORE_THRESHOLD = 1
        DAYS = 14
        SINCE = (datetime.today() - timedelta(days=DAYS)).timestamp()
        NO_OF_POSTS = 2

        #reddit = praw.Reddit('NoVowelsBot', user_agent='NoVowelBot - Finds top self posts, removes the vowels from the text and reposts them in /r/fckvwls')
        # initialize bot
        nvbot = NoVowelsBot('credentials.json')
        # get reddit instance
        reddit = nvbot.init_bot()
        test_sub = reddit.subreddit('NoVowelBotTest')
        posts = get_posts(test_sub, SCORE_THRESHOLD, SINCE, NO_OF_POSTS)
        self.assertEqual(posts[0],
                        {'title' : 'Second Test',
                          'text' : 'Second test text.',
                          'id'   : 'brgext'})

    def test2_remove_vowels(self):
        post = {'title': 'Title with a vowel for you',
                  'text': 'Does it have all the vowels? Only you know.',
                  'id': 0}
        self.assertEqual(remove_vowels(post),
                        {'title': 'Ttl wth vwl fr y',
                         'text': 'Ds t hv ll th vwls? nly y knw.',
                         'id': 0})
    
    def test3_create_post_add_comment(self):
        #reddit = praw.Reddit('NoVowelsBot', user_agent='NoVowelBot - Finds top self posts, removes the vowels from the text and reposts them in /r/fckvwls')
        # initialize bot
        nvbot = NoVowelsBot('credentials.json')
        # get reddit instance
        reddit = nvbot.init_bot()
        posts = [
            {'title': 'NoVowelBotTest has been created',
             'text' : 'This is a test environment for the NoVowelBot',
             'id'   : 'bq4v8d'}
             ]
        create_posts(reddit, posts, 'NoVowelBotTest')
    

if __name__ == '__main__':
    unittest.main()