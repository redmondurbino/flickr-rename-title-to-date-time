import os
import flickrapi
import xml
import logging
import webbrowser


logging.basicConfig()

api_key = unicode(os.environ.get('FLICKR_API_KEY',''))
print api_key
api_secret = unicode(os.environ.get('FLICKR_API_SECRET',''))
print api_secret
flickr_user_id= os.environ.get('FLICKR_USER_ID','')

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read')


print('Step 1: authenticate')
# Only do this if we don't have a valid token already
#if not flickr.token_valid(perms='read'):
if False:

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms='read')
    print authorize_url
    webbrowser.open_new(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = str(input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)


photos = flickr.photos.search(user_id= flickr_user_id, per_page='10')
sets = flickr.photosets.getList(user_id= flickr_user_id)

print xml.etree.ElementTree.tostring(sets)