import mimetypes, time, sys
import unittest
import httplib
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth import *

if not (len(sys.argv) == 5 or len(sys.argv) == 7):
	print 'Usage: # python %s consumer_key consumer_secret oauth_token oauth_token_secret' % sys.argv[0]
	quit()

CONSUMER_KEY       = str(sys.argv[1])
CONSUMER_SECRET    = str(sys.argv[2])
OAUTH_TOKEN        = str(sys.argv[3])
OAUTH_TOKEN_SECRET = str(sys.argv[4])

SECOND_USER = False
if len(sys.argv) == 7:
    SECOND_OAUTH_TOKEN        = str(sys.argv[5]) ## for vote test
    SECOND_OAUTH_TOKEN_SECRET = str(sys.argv[6])
    SECOND_USER = True
	
class AuthTestCase(unittest.TestCase):
    def setUp(self):
        super(AuthTestCase, self).setUp()
        self.consumer_key       = CONSUMER_KEY
        self.consumer_secret    = CONSUMER_SECRET
        self.handler            = OAuthHandler(self.consumer_key,self.consumer_secret)

    def _testrequesttoken(self):
        headers = {}
        self.handler.apply_auth('https://api.500px.com/v1/oauth/request_token', 'POST', headers, { 'oauth_callback' : 'http://localhost' })
        conn = httplib.HTTPSConnection('api.500px.com')
        conn.request('POST', 'https://api.500px.com/v1/oauth/request_token', headers=headers)
        response = conn.getresponse()
        self.assert_( response.status == 200 )
        result = response.read()
        conn.close()
        print "this is your request token:\n%s" % result

    def _testauthurlwithverifier(self):
        redirect_uri = self.handler.get_authorization_url()
        print "Please visit and authorize at:\n%s" % redirect_uri

        verifier = raw_input("Paste received oauth_verifier (blank to exit): ").strip()
        if not verifier:
            return
        token = self.handler.get_access_token(verifier)

        print "this is your access token:\n%s" % token.key
        print "this is your access token secret:\n%s" % token.secret

    def _testxauth(self):
        username = raw_input("Input your username (blank to exit): ").strip()
        if not username:
            return
        password = raw_input("Input your password (blank to exit): ").strip()
        if not password:
            return
        token = self.handler.get_xauth_access_token(username,password)

        print "this is your access token:\n%s" % token.key
        print "this is your access token secret:\n%s" % token.secret
	
class FivehundredPXTestCase(unittest.TestCase):
	
    def setUp(self):
        super(FivehundredPXTestCase, self).setUp()
        self.consumer_key       = CONSUMER_KEY
        self.consumer_secret    = CONSUMER_SECRET
        self.oauth_token        = OAUTH_TOKEN
        self.oauth_token_secret = OAUTH_TOKEN_SECRET
        self.handler            = OAuthHandler(self.consumer_key,self.consumer_secret)
        self.handler.set_access_token(self.oauth_token,self.oauth_token_secret)
        self.api		   	    = FiveHundredPXAPI(auth_handler=self.handler)
        self.unauthorized_api   = FiveHundredPXAPI()

        if SECOND_USER:
            self.second_handler            = OAuthHandler(self.consumer_key,self.consumer_secret)
            self.second_oauth_token        = SECOND_OAUTH_TOKEN
            self.second_oauth_token_secret = SECOND_OAUTH_TOKEN_SECRET
            self.second_handler.set_access_token(self.second_oauth_token, self.second_oauth_token_secret)
            self.second_api		           = FiveHundredPXAPI(auth_handler=self.second_handler)

        self.follower_id = '925306'
        self.user_id     = '642049'
        self.filepath    = 'images/africa.jpg'
		
    def tearDown(self):
        pass

    def testusers(self):
        self.api.users()
	
    def testusersshow(self):
        self.unauthorized_api.users_show(consumer_key=self.consumer_key, id='727199')
        self.unauthorized_api.users_show(consumer_key=self.consumer_key, username='akirahrkw')        
        self.unauthorized_api.users_show(consumer_key=self.consumer_key, email='akirahrkw@gmail.com')
        self.api.users_show(require_auth=True,id='727199')
        self.api.users_show(require_auth=True,username='akirahrkw')        
        self.api.users_show(require_auth=True,email='akirahrkw@gmail.com')

    def testuserfriends(self):
        self.unauthorized_api.users_friends(consumer_key=self.consumer_key,id=self.user_id,rpp=5,page=2)
        self.api.users_friends(require_auth=True,id=self.user_id,rpp=5,page=2)

        self.api.users_friends_post(require_auth=True,id=self.follower_id)
        self.api.users_friends_delete(require_auth=True,id=self.follower_id)

    def testuserfollowers(self):
        self.unauthorized_api.users_followers(consumer_key=self.consumer_key,id=self.user_id,rpp=5,page=2)
        self.api.users_followers(require_auth=True,id=self.user_id,rpp=5,page=2)

    def testblogs(self):
        self.unauthorized_api.blogs(consumer_key=self.consumer_key,rpp=2,page=1)
        blogs = self.api.blogs(require_auth=True,rpp=2,page=1)
        for blog in blogs['blog_posts']:
            blog     = self.api.blogs_id(require_auth=True,id=blog['id'])	
            comments = self.api.blogs_comments(require_auth=True,id=blog['id'])	

    def testblogspost(self):
        blog = self.api.blogs_post(title='title test', body='body test', tags='akira,hirakawa')
        time.sleep(2)
        uid = blog['id']
        self.api.blogs_update(id=uid, title='title test 2', body='body test 2', tags='akira,hirakawa')
        self.api.blogs_comments_post(id=uid, body='test blog comment')
        self.api.blogs_delete(id=uid)

    def testcollections(self):
        collection = self.api.collections_post(require_auth=True, title='collection title', path='test')
        self.api.collections_update(require_auth=True, id=collection['id'], title='collection title 2', path='test2')
        
        collections = self.api.collections(require_auth=True,rpp=2,page=1)
        for collection in collections['collections']:
            self.api.collections_id(require_auth=True, id=collection['id'])

        self.api.collections_delete(id=collection['id'])

    def testphotos(self):
        json = self.unauthorized_api.photos(feature='popular',consumer_key=self.consumer_key)
        json = self.api.photos(require_auth=True, feature='popular',rpp=3)
        self.assert_( len(json['photos']) == 3 )

        for photo in json['photos']:
            photo_id = photo['id']
            self.unauthorized_api.photos_id(id=photo_id,consumer_key=self.consumer_key)
            self.api.photos_id(require_auth=True,id=photo_id)
            self.unauthorized_api.photos_comments(id=photo_id,consumer_key=self.consumer_key)

    def testphotosgenerator(self):
        gen = self.api.photos(require_auth=True, feature='popular',rpp=1, as_generator=True)
        for g in gen: g

    def testphotossearch(self):
        json = self.unauthorized_api.photos_search(consumer_key=self.consumer_key,term='test',rpp=1,page=1)
        json = self.api.photos_search(require_auth=True, term='test',rpp=1,page=1)
        self.assert_( len(json['photos']) == 1 )

    def _update_photo(self,photo_id):
        self.api.photos_comments_post(id=photo_id,body='test comment')

        self.api.photos_favorite_post(id=photo_id)
        self.api.photos_favorite_delete(id=photo_id)
	
        self.api.photos_tags_post(id=photo_id,tags='test,test2')
        self.api.photos_tags_delete(id=photo_id,tags='test,test2')

        if SECOND_USER:
            self.api.photos_vote_post(id=photo_id,vote='1')

        self.api.photos_update(id=photo_id,name='akira test',description='akira description')

    def testphotospost(self):

        api =  self.api if not SECOND_USER else self.second_api
        access_key =  self.oauth_token if not SECOND_USER else self.second_oauth_token
        json = api.photos_post()
        photo_id   = json['photo']['id']
        upload_key = str(json['upload_key'])

        api.upload_photo(
            photo_id=photo_id,
            filename=self.filepath,
            consumer_key=self.consumer_key,
            upload_key=upload_key,
            access_key=access_key
        )
        time.sleep(3)
        self._update_photo(photo_id)
        time.sleep(1)
        api.photos_delete(id=photo_id)

        json = api.photos_post()
        photo_id   = json['photo']['id']
        upload_key = str(json['upload_key'])
        file_type = mimetypes.guess_type(self.filepath)
        
        fp = open(self.filepath,'rb')

        api.upload_photo(
            photo_id=photo_id,
            fp=fp,
            file_type=file_type[0],
            consumer_key=self.consumer_key,
            upload_key=upload_key,
            access_key=access_key
        )

        fp.close()
        time.sleep(3)
        api.photos_delete(id=photo_id)


if __name__ == '__main__':
    del sys.argv[1:]
    unittest.main()
