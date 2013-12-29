from base import *

if len(sys.argv) < 5:
	print 'Usage: # python %s consumer_key consumer_secret request_token request_token_secret' % sys.argv[0]
	quit()

CONSUMER_KEY       = str(sys.argv[1])
CONSUMER_SECRET    = str(sys.argv[2])
OAUTH_TOKEN        = str(sys.argv[3])
OAUTH_TOKEN_SECRET = str(sys.argv[4])

# https://github.com/500px/api-documentation/tree/master/endpoints/collections
class CollectionTestCase(BaseTestCase):

    def setUp(self):
        self.consumer_key       = CONSUMER_KEY
        self.consumer_secret    = CONSUMER_SECRET
        self.oauth_token        = OAUTH_TOKEN
        self.oauth_token_secret = OAUTH_TOKEN_SECRET
        super(CollectionTestCase, self).setUp()

    def test_collections(self):
        json = self.api.collections()
        self.assertIsNotNone(json)

    def test_collection(self):
        try:
            json = self.api.collections_post(title="Test Title", path='test')
            self.assertIsNotNone(json)
            json = self.api.collections_id(id=json['id'])
            self.assertIsNotNone(json)
            json = self.api.collections_update(id=json['id'], title="Test Title2", path='test2')
            self.assertIsNotNone(json)
            json = self.api.collections_delete(id=json['id'])
            self.assertIsNotNone(json)
        except FiveHundredClientError as e:
            if not e.status == 403:
                raise e

if __name__ == '__main__':
    del sys.argv[1:]
    unittest.main()