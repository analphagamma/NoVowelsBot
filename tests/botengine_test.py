import unittest
from modules.BotEngine import BotEngine
from NoVowelsBot import NoVowelsBot

class BotEngineTest(unittest.TestCase):
    
    def test_remove_vowels(self):
        posts = [{'title': 'Title with a vowel for you',
                  'text': 'Does it have all the vowels? Only you know.',
                  'id': 0}]
        engine = BotEngine(None, posts)
        self.assertEqual(engine.remove_vowels(),
                        [{'title': 'Ttl wth vwl fr y',
                         'text': 'Ds t hv ll th vwls? nly y knw.',
                         'id': 0}])

    def test_add_comment(self):
        nvbot = NoVowelsBot('credentials.json')
        reddit = nvbot.init_bot()
        engine = BotEngine(reddit, [])
        engine.add_comment(reddit.subreddit('NoVowelBotTest'),
                           'bq4v8d')


    @unittest.skip
    def test_create_post(self):
        pass

if __name__ == '__main__':
    unittest.main()