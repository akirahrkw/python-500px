# python-500px

A Python client for the [500px API](https://github.com/500px/api-documentation).

this library was inspired by [tweepy](https://github.com/tweepy/tweepy) and [python-instagram](https://github.com/Instagram/python-instagram)

***

## Installation
    pip install python-500px

## Requires
  * simplejson

## Usage

```python
from fivehundredpx.client import FiveHundredPXAPI
from fivehundredpx.auth   import *

unauthorized_api = FiveHundredPXAPI(handler)
unauthorized_api.users_show(consumer_key=CONSUMER_KEY, id='727199')

handler = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
handler.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = FiveHundredPXAPI(handler)
api.users()
```

## Authentication

Please check 500px's [authentication document](https://github.com/500px/api-documentation/tree/master/authentication). `tests/oauth.py` shows how to get request/access token.

```python
# verifier:
self.handler.get_authorization_url() # go to this url and get verifier
token = self.handler.get_access_token(verifier)
token.key, token.secret

# xauth:
token = self.handler.get_request_token()
self.handler.set_request_token(token.key, token.secret)
token = self.handler.get_xauth_access_token(username, password)
token.key, token.secret
```

## Methods

  * api.photos()
  * api.photos_search()
  * api.photos_id()
  * api.photos_post()
  * api.photos_update()
  * api.photos_delete()
  * api.photos_comments()
  * api.photos_comments_post()
  * api.photos_favorites()
  * api.photos_favorite_post()
  * api.photos_favorite_delete()
  * api.photos_tags_post()
  * api.photos_tags_delete()
  * api.photos_votes()
  * api.photos_vote_post()
  * api.upload_photo()
  * api.users()
  * api.users_show()
  * api.users_search()
  * api.users_friends()
  * api.users_followers()
  * api.users_friends_post()
  * api.users_friends_delete()
  * api.blogs()
  * api.blogs_id()
  * api.blogs_comments()
  * api.comments_post()
  * api.collections()
  * api.collections_id()
  * api.collections_post()
  * api.collections_update()
  * api.collections_delete()

## Test
    python tests/oauth.py      [cunsumer_key] [consumer_secret]
    python tests/blog.py       [cunsumer_key] [consumer_secret] [oauth_token] [oauth_token_secret]
    python tests/collection.py [cunsumer_key] [consumer_secret] [oauth_token] [oauth_token_secret]
    python tests/user.py       [cunsumer_key] [consumer_secret] [oauth_token] [oauth_token_secret]
    python tests/photo.py      [cunsumer_key] [consumer_secret] [oauth_token] [oauth_token_secret]
    python tests/upload.py     [cunsumer_key] [consumer_secret] [oauth_token] [oauth_token_secret]

[authentication]: https://github.com/500px/api-documentation/tree/master/authentication
[authorize]: https://github.com/500px/api-documentation/blob/master/authentication/POST_oauth_authorize.md
[request_token]: https://github.com/500px/api-documentation/blob/master/authentication/POST_oauth_requesttoken.md
[access_token]: https://github.com/500px/api-documentation/blob/master/authentication/POST_oauth_accesstoken.md
