from base import *
import datetime

if len(sys.argv) < 5:
	print 'Usage: # python %s consumer_key consumer_secret request_token request_token_secret' % sys.argv[0]
	quit()

CONSUMER_KEY       = str(sys.argv[1])
CONSUMER_SECRET    = str(sys.argv[2])
OAUTH_TOKEN        = str(sys.argv[3])
OAUTH_TOKEN_SECRET = str(sys.argv[4])

# https://github.com/500px/api-documentation/tree/master/endpoints/photo
class PhotoTestCase(BaseTestCase):

    def setUp(self):
        self.consumer_key       = CONSUMER_KEY
        self.consumer_secret    = CONSUMER_SECRET
        self.oauth_token        = OAUTH_TOKEN
        self.oauth_token_secret = OAUTH_TOKEN_SECRET
        super(PhotoTestCase, self).setUp()

    def test_photos(self):
        json = self.unauthorized_api.photos(feature='popular',consumer_key=self.consumer_key)
        self.assertIsNotNone(json)

        json = self.api.photos(require_auth=True, feature='popular',rpp=1, image_size=[2,3])
        self.assertIsNotNone(json)
        self.assertTrue(len(json['photos']) != 0)

        for photo in json['photos']:
            photo_id = photo['id']
            json = self.api.photos_id(require_auth=True, id=photo_id)
            self.assertIsNotNone(json)
            json = self.api.photos_comments(require_auth=True, id=photo_id)
            self.assertIsNotNone(json)
            json = self.api.photos_favorites(require_auth=True, id=photo_id)
            self.assertIsNotNone(json)
            json = self.api.photos_votes(require_auth=True, id=photo_id)
            self.assertIsNotNone(json)

    def test_photos_search(self):
        json = self.api.photos_search(term='test',consumer_key=self.consumer_key)
        self.assertIsNotNone(json)

    def test_photos_comments_post(self):
        photo = self._get_sample_photo()
		# to prevent 403 error
        i = datetime.datetime.now()
        json = self.api.photos_comments_post(id=photo['id'], body='this is akira' + str(i))
        self.assertIsNotNone(json)

    def test_photo_vote(self):
        photo = self._get_sample_photo()
        try:
            self.api.photos_vote_post(id=photo['id'], vote="1")
        except FiveHundredClientError as e:
            if not e.status == 403:
                raise e

    def test_photo_favirite(self):
        photo = self._get_sample_photo()
        json = self.api.photos_favorite_post(id=photo['id'])
        self.assertIsNotNone(json)
        json = self.api.photos_favorite_delete(id=photo['id'])
        self.assertIsNotNone(json)

    def test_photos_tags_post(self):
        photo = self._get_sample_photo()
        json = self.api.photos_tags_post(id=photo['id'], tags="test,test2")
        self.assertIsNotNone(json)

    def test_photos_tags_delete(self):
        photo = self._get_sample_photo()
        json = self.api.photos_tags_delete(id=photo['id'], tags="test,test2")
        self.assertIsNotNone(json)

    def test_photos_report(self):
        photo = self._get_sample_photo()
        json = self.api.photos_report(id=photo['id'], reason="1")
        self.assertIsNotNone(json)

    def test_photos_generator(self):
        gen = self.api.photos(require_auth=True, feature='popular',rpp=1, as_generator=True)
        for json in gen: self.assertIsNotNone(json)

if __name__ == '__main__':
    del sys.argv[1:]
    unittest.main()		