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


photos = flickr.photos.search(user_id= flickr_user_id, per_page='10')
sets = flickr.photosets.getList(user_id= flickr_user_id)

print xml.etree.ElementTree.tostring(sets)