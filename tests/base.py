import mimetypes, httplib, time, sys, os
import unittest

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
sys.path.append(path)

from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth   import *
from fivehundredpx.errors import FiveHundredClientError

class BaseTestCase(unittest.TestCase):
	
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.handler            = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.handler.set_access_token(self.oauth_token, self.oauth_token_secret)
        self.api		   	    = FiveHundredPXAPI(auth_handler=self.handler)
        self.unauthorized_api   = FiveHundredPXAPI()
        self.follower_id = '925306' # test user id
        self.user_id     = '727199' # this is akirahrkw's id
        self.photo = None # sample photo for test

    def tearDown(self):
        pass

    def _get_sample_photo(self):
        if not self.photo:
            json = self.api.photos(require_auth=True, feature='user', user_id=self.follower_id, rpp=1)
            self.assertIsNotNone(json)
            self.photo = json['photos'][0]
        return self.photo	