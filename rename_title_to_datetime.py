import os
import flickrapi
import xml

api_key = unicode(os.environ.get('FLICKR_API_KEY',''))
api_secret = unicode(os.environ.get('FLICKR_API_KEY',''))
flickr_user_id= os.environ.get('FLICKR_USER_ID','')

flickr = flickrapi.FlickrAPI(api_key, api_secret)


photos = flickr.photos.search(user_id= flickr_user_id, per_page='10')
sets = flickr.photosets.getList(user_id= flickr_user_id)

print xml.etree.ElementTree.tostring(sets)