import unittest
from NoVowelsBot import *

class BotTest(unittest.TestCase):
    
    def test_init_1_file_not_found(self):
        '''
        Test whether the right exception is thrown if the
        login file is not present.
        '''
        bot = NoVowelsBot('notexisting.json')
        self.assertRaises(LoginFileNotFound, lambda: bot.get_login_details())

    def test_init_2_invalid_json(self):
        bot = NoVowelsBot('bad_file.json')
        self.assertRaises(NotJSONFileError, lambda: bot.get_login_details())

    def test_init_3_incomplete_login_empty(self):
        bot = NoVowelsBot('bad_credentials_empty.json')
        self.assertRaises(IncompleteLoginDetailsError, lambda: bot.get_login_details())

    def test_init_4_incomplete_login_missing(self):
        bot = NoVowelsBot('bad_credentials_missing.json')
        self.assertRaises(IncompleteLoginDetailsError, lambda: bot.get_login_details())
    
    def test_init_5_successful_login(self):
        bot = NoVowelsBot('credentials.json')
        reddit = bot.init_bot()
        self.assertNotEqual(reddit.user.me(), None)
    
    def test_remove_vowels(self):
        post = {'title': 'Title with a vowel for you',
                  'text': 'Does it have all the vowels? Only you know.',
                  'id': 0}
        self.assertEqual(remove_vowels(post),
                        {'title': 'Ttl wth vwl fr y',
                         'text': 'Ds t hv ll th vwls? nly y knw.',
                         'id': 0})

    def test_get_posts_from_test_subreddit(self):
        SCORE_THRESHOLD = 1
        DAYS = 14
        SINCE = (datetime.today() - timedelta(days=DAYS)).timestamp()
        NO_OF_POSTS = 5
        nvbot = NoVowelsBot('credentials.json')
        reddit = nvbot.init_bot()
        test_sub = reddit.subreddit('NoVowelBotTest')
        posts = get_posts(test_sub, SCORE_THRESHOLD, SINCE, NO_OF_POSTS)
        self.assertEqual(posts[0],
                        {'title': 'NoVowelBotTest has been created',
                          'text' : 'This is a test environment for the NoVowelBot',
                          'id'   : 'bq4v8d'})
                          
if __name__ == '__main__':
    unittest.main()