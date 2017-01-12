from base import *

if len(sys.argv) < 5:
	print 'Usage: # python %s consumer_key consumer_secret request_token request_token_secret' % sys.argv[0]
	quit()

CONSUMER_KEY       = str(sys.argv[1])
CONSUMER_SECRET    = str(sys.argv[2])
OAUTH_TOKEN        = str(sys.argv[3])
OAUTH_TOKEN_SECRET = str(sys.argv[4])

# https://github.com/500px/api-documentation/tree/master/endpoints/user
class UserTestCase(BaseTestCase):
	
    def setUp(self):
        self.consumer_key       = CONSUMER_KEY
        self.consumer_secret    = CONSUMER_SECRET
        self.oauth_token        = OAUTH_TOKEN
        self.oauth_token_secret = OAUTH_TOKEN_SECRET
        super(UserTestCase, self).setUp()

    def test_users(self):
        json = self.api.users()
        self.assertIsNotNone(json)

    def test_users_show(self):
        json = self.unauthorized_api.users_show(consumer_key=self.consumer_key, id='727199')
        self.assertIsNotNone(json)
        json = self.unauthorized_api.users_show(consumer_key=self.consumer_key, username='akirahrkw')
        self.assertIsNotNone(json)

        with self.assertRaises(FiveHundredClientError):
            self.unauthorized_api.users_show(consumer_key=self.consumer_key, id='0')

        json = self.api.users_show(require_auth=True,id='727199')
        self.assertIsNotNone(json)
        users = self.api.users_show(require_auth=True,username='akirahrkw')
        self.assertIsNotNone(json)

    def test_user_friends_a_get(self):
        json = self.unauthorized_api.users_friends(consumer_key=self.consumer_key, id=self.user_id, rpp=5, page=2)
        self.assertIsNotNone(json)
        self.assertEqual(json["friends"].__class__, dict)

        json = self.api.users_friends(require_auth=True, id=self.user_id, rpp=5, page=2)
        self.assertIsNotNone(json)
        self.assertEqual(json["friends"].__class__, dict)

    def test_user_friends_b_post(self):
        json = self.api.users_friends_post(require_auth=True,id=self.follower_id)
        self.assertIsNotNone(json)

    def test_user_friends_c_delete(self):
        json = self.api.users_friends_delete(require_auth=True,id=self.follower_id)
        self.assertIsNotNone(json)

    def test_user_followers(self):
        json = self.unauthorized_api.users_followers(consumer_key=self.consumer_key,id=self.user_id,rpp=5,page=2)
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['followers_count'])
        self.assertIsNotNone(json['followers'])

        json = self.api.users_followers(require_auth=True,id=self.user_id,rpp=5,page=2)
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['followers_count'])
        self.assertIsNotNone(json['followers'])

    def test_user_followers(self):
        json = self.unauthorized_api.users_search(consumer_key=self.consumer_key,term="akira")
        self.assertIsNotNone(json)
        self.assertIsNotNone(json['total_items'])
        self.assertIsNotNone(json['users'])
	
if __name__ == '__main__':
    del sys.argv[1:]
    unittest.main()