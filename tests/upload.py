from base import *

if len(sys.argv) < 5:
	print 'Usage: # python %s consumer_key consumer_secret request_token request_token_secret' % sys.argv[0]
	quit()

CONSUMER_KEY       = str(sys.argv[1])
CONSUMER_SECRET    = str(sys.argv[2])
OAUTH_TOKEN        = str(sys.argv[3])
OAUTH_TOKEN_SECRET = str(sys.argv[4])

# https://github.com/500px/api-documentation/blob/master/endpoints/photo/POST_photos.md
# https://github.com/500px/api-documentation/blob/master/endpoints/upload/POST_upload.md
class UploadTestCase(BaseTestCase):
	
    def setUp(self):
        self.consumer_key       = CONSUMER_KEY
        self.consumer_secret    = CONSUMER_SECRET
        self.oauth_token        = OAUTH_TOKEN
        self.oauth_token_secret = OAUTH_TOKEN_SECRET
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),"."))
        self.filepath    = path + '/images/africa.jpg'
        super(UploadTestCase, self).setUp()

    def test_photo_upload_path(self):

        json = self.api.photos_post(name='test photo',description='test description')
        self.assertIsNotNone(json)

        photo_id   = json['photo']['id']
        upload_key = str(json['upload_key'])

        json = self.api.upload_photo(
            photo_id=photo_id,
            filename=self.filepath,
            consumer_key=self.consumer_key,
            upload_key=upload_key,
            access_key=self.oauth_token
        )
        self.assertIsNotNone(json)
        time.sleep(2)

        json = self.api.photos_update(id=photo_id,name='test photo 2',description='test description 2', privacy="0")
        self.assertIsNotNone(json)

        time.sleep(10)
        json = self.api.photos_delete(id=photo_id)
        self.assertIsNotNone(json)

    def test_photo_upload_binary(self):
        json = self.api.photos_post()
        self.assertIsNotNone(json)
        
        photo_id   = json['photo']['id']
        upload_key = str(json['upload_key'])
        file_type = mimetypes.guess_type(self.filepath)
        
        fp = open(self.filepath,'rb')

        json = self.api.upload_photo(
            photo_id=photo_id,
            fp=fp,
            file_type=file_type[0],
            consumer_key=self.consumer_key,
            upload_key=upload_key,
            access_key=self.oauth_token
        )
        fp.close()
        self.assertIsNotNone(json)
        time.sleep(10)
        self.api.photos_delete(id=photo_id)

if __name__ == '__main__':
    del sys.argv[1:]
    unittest.main()