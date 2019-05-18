import unittest
from NoVowelsBot import *

class Init_test(unittest.TestCase):

    def valid_reddit_test(self):
        bot = NoVowelsBot('credentials.json')
        self.assertNotEqual(None, bot.botobject())

if __name__ == '__main__':
    unittest.main()