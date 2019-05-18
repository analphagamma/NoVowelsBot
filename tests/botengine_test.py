import unittest
from modules.BotEngine import Reader, PostTransformer
from NoVowelsBot import NoVowelsBot

class BotEngineTest(unittest.TestCase):
    
    @unittest.skip('skipping this now')
    def testReader_get_top_test(self):
        bot = NoVowelsBot('credentials.json')
        reddit = bot.botobject()
        reader = Reader(reddit, 'NoVowelBotTest')
        top_results = reader.get_top_posts(1)[0]

        self.assertEqual(top_results['title'], 'NoVowelBotTest has been created')
        self.assertEqual(top_results['text'] , 'This is a test environment for the NoVowelBot')

    def testTransform_1_remove_vowel_test(self):
        posts = [{'title': 'Title with a vowel for you',
                  'text': 'Does it have all the vowels? Only you know.'}]
        transform_obj = PostTransformer(posts)
        print(transform_obj.remove_vowels())


    def testPoster_1_test(self):
        pass

if __name__ == '__main__':
    unittest.main()