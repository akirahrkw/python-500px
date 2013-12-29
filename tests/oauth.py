import mimetypes, httplib, time, sys, os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth import *

if len(sys.argv) < 3:
	print 'Usage: # python %s consumer_key consumer_secret' % sys.argv[0]
	quit()

CONSUMER_KEY    = str(sys.argv[1])
CONSUMER_SECRET = str(sys.argv[2])

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        super(AuthTestCase, self).setUp()
        self.handler = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)

    def test_auth_request_token(self):
        print 'test_auth_request_token...\n'
        headers = {}
        self.handler.apply_auth('https://api.500px.com/v1/oauth/request_token', 'POST', headers, { 'oauth_callback' : 'http://localhost' })
        conn = httplib.HTTPSConnection('api.500px.com')
        conn.request('POST', 'https://api.500px.com/v1/oauth/request_token', headers=headers)
        response = conn.getresponse()
        self.assert_( response.status == 200 )
        result = response.read()
        conn.close()
        print "request token: %s\n" % result

    def test_authorization_url_with_verifier(self):
        print 'test_authorization_url_with_verifier...\n'
        print "Please visit this endpoint and authorize at:\n%s\n" % self.handler.get_authorization_url()
        verifier = raw_input("Paste received oauth_verifier (blank to exit): ").strip()
        if not verifier:
            return

        token = self.handler.get_access_token(verifier)
        print "access token: %s\n" % token.key
        print "access token secret: %s\n" % token.secret

    def test_xauth(self):
        print 'test_xauth...\n'
        token = self.handler.get_request_token()
        print "request token: %s\n" % token.key
        print "request token secret: %s\n" % token.secret

        request_token = raw_input("Input request token (blank to exit): ").strip()
        if not request_token:
            return

        request_token_secret = raw_input("Input request token secret (blank to exit): ").strip()
        if not request_token_secret:
            return

        self.handler.set_request_token(request_token,request_token_secret)

        username = raw_input("Input your username (blank to exit): ").strip()
        if not username:
            return

        password = raw_input("Input your password (blank to exit): ").strip()
        if not password:
            return

        token = self.handler.get_xauth_access_token(username,password)
        print "access token: %s\n" % token.key
        print "access token secret: %s\n" % token.secret

if __name__ == '__main__':
    del sys.argv[1:]
    unittest.main()