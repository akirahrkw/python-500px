from base import *

if len(sys.argv) < 5:
	print 'Usage: # python %s consumer_key consumer_secret request_token request_token_secret' % sys.argv[0]
	quit()

CONSUMER_KEY       = str(sys.argv[1])
CONSUMER_SECRET    = str(sys.argv[2])
OAUTH_TOKEN        = str(sys.argv[3])
OAUTH_TOKEN_SECRET = str(sys.argv[4])

# https://github.com/500px/api-documentation/tree/master/endpoints/blog
class BlogTestCase(BaseTestCase):

    def setUp(self):
        self.consumer_key       = CONSUMER_KEY
        self.consumer_secret    = CONSUMER_SECRET
        self.oauth_token        = OAUTH_TOKEN
        self.oauth_token_secret = OAUTH_TOKEN_SECRET
        super(BlogTestCase, self).setUp()

    def test_blogs(self):
        json = self.api.blogs(require_auth=True,rpp=1,page=1)
        self.assertIsNotNone(json)
        for blog in json['blog_posts']:
            json = self.api.blogs_id(require_auth=True, id=blog['id'])
            self.assertIsNotNone(json)
            json = self.api.blogs_comments(require_auth=True, id=blog['id'])
            self.assertIsNotNone(json)

    # def test_blog(self):
    #     json = self.api.blogs_post(title='title test', body='body test')
    #     self.assertIsNotNone(json)
	#
    #     json = self.api.blogs_update(id=json['id'], title='title test 2', body='body test 2')
    #     self.assertIsNotNone(json)
	#
    #     json_comment = self.api.blogs_comments_post(id=json['id'], body='test comment')
    #     self.assertIsNotNone(json_comment)
	#
    #     blogs = self.api.blogs_comments(id=json['id'])
    #     self.assertIsNotNone(blogs)
	#
    #     json_comment = self.api.comments_post(id=json_comment['comment']['id'], body='reply test comment')
    #     self.assertIsNotNone(json_comment)
	#
    #     json = self.api.blogs_delete(id=json['id'])
    #     self.assertIsNotNone(json)

if __name__ == '__main__':
    del sys.argv[1:]
    unittest.main()
