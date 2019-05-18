import praw
import json

# getting login information
class NoVowelsBot():

    def __init__(self, login_info):
        self.login_info = login_info

    def login_details(self):
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
        try:
            f = open('./resources/'+self.login_info, 'r')
        except FileNotFoundError:
            raise LoginFileNotFound
        
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
                     login.get('user_name'),
                     login.get('password')]:
            raise IncompleteLoginDetailsError
            
        return login
    
    def reddit_instance(self):
        login = self.login_details()
        # initialize Reddit object
        return praw.Reddit(client_id     = login.get('client_id'),
                           client_secret = login.get('client_secret'),
                           user_agent    = login.get('user_agent'),
                           user_name     = login.get('user_name'),
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