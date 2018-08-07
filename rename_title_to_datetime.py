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
flickr_set_to_rename= os.environ.get('FLICKR_SET_TO_RENAME','')

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='write')


photos = flickr.photos.search(user_id= flickr_user_id, per_page='10')
sets = flickr.photosets.getList(user_id= flickr_user_id)

#print xml.etree.ElementTree.tostring(sets)

for photo in flickr.walk_set(flickr_set_to_rename):
    print photo.get('title'), photo.get('id')
    print xml.etree.ElementTree.tostring(photo)
    photo_id = photo.get('id')
    print photo_id
    info = flickr.photos.getInfo(photo_id=photo_id)
    print "----- info -----"
    print xml.etree.ElementTree.tostring(info)
    print "---- date taken --- "
    print photo.tag
    print photo.attrib
    for child in photo.getchildren():
        print child.tag, child.attrib
    #print "----- info -----"
    #exif = flickr.photos.getExif(photo_id=photo_id)
    #print xml.etree.ElementTree.tostring(exif)
    print "----- end -----"

