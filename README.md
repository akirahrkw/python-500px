python-500px
======
A Python client for 500px API, inspired by tweepy(https://github.com/tweepy/tweepy), python-instagram(https://github.com/Instagram/python-instagram)

Installation
----
pip install python-500px

Requires
----
  * httplib2
  * simplejson

Usage
----
	from fivehundredpx.client import FiveHundredPXAPI
	from fivehundredpx.auth   import *
	
	unauthorized_api = FiveHundredPXAPI(handler)
	
	handler = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
	handler.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
	api = FiveHundredPXAPI(handler)
	api.users()
	
Methods
----
  * api.photos()
  * api.photos_search()
  * api.photos_id()
  * api.photos_post()
  * api.photos_delete()
  * api.photos_comments()
  * api.photos_comments_post()
  * api.photos_favorite_post()
  * api.photos_favorite_delete()
  * api.photos_tags_post()
  * api.photos_tags_delete()
  * api.photos_vote_post()
  * api.upload_photo()
  * api.photos_update()
  * api.users()
  * api.users_show()
  * api.users_friends()
  * api.users_followers()
  * api.users_friends_post()
  * api.users_friends_delete()
  * api.blogs()
  * api.blogs_id()
  * api.blogs_comments()
  * api.blogs_comments_post()
  * api.blogs_post()
  * api.blogs_delete()
  * api.blogs_update()
  * api.collections()
  * api.collections_id()
  * api.collections_post()
  * api.collections_update()
  * api.collections_delete()

please check test.py

