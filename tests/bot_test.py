import unittest
import praw
from NoVowelsBot import *

class BotTest(unittest.TestCase):

    @unittest.skip
    def test1_get_posts_from_test_subreddit(self):
        SCORE_THRESHOLD = 1
        DAYS = 14
        SINCE = (datetime.today() - timedelta(days=DAYS)).timestamp()
        NO_OF_POSTS = 2

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
    @unittest.skip
    def test3_create_post_add_comment(self):
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
    
    def test4_simulate_ordinary_work(self):
        # initialize bot
        SUBREDDITS = ['all']
        SCORE_THRESHOLD = 5000
        DAYS = 1
        SINCE = (datetime.today() - timedelta(days=DAYS)).timestamp()
        NO_OF_POSTS = 5

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
        # post   
        create_posts(reddit, clean_posts, 'NoVowelBotTest', 1)

if __name__ == '__main__':
    unittest.main()
