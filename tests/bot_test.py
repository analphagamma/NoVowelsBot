import unittest
from NoVowelsBot import *

class BotTest(unittest.TestCase):
    
    def test1_file_not_found(self):
        '''
        Test whether the right exception is thrown if the
        login file is not present.
        '''
        bot = NoVowelsBot('notexisting.json')
        self.assertRaises(LoginFileNotFound, lambda: bot.login_details())

    def test2_invalid_json(self):
        bot = NoVowelsBot('bad_file.json')
        self.assertRaises(NotJSONFileError, lambda: bot.login_details())

    def test3_incomplete_login_empty(self):
        bot = NoVowelsBot('bad_credentials_empty.json')
        self.assertRaises(IncompleteLoginDetailsError, lambda: bot.login_details())

    def test4_incomplete_login_missing(self):
        bot = NoVowelsBot('bad_credentials_missing.json')
        self.assertRaises(IncompleteLoginDetailsError, lambda: bot.login_details())
                          
if __name__ == '__main__':
    unittest.main()