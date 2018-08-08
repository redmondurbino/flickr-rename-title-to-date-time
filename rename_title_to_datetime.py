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

flickr_set_to_rename ='72157659400135206'

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='write')


#search = flickr.photos.search(user_id= flickr_user_id, per_page='100', text='-20')
#print "search=",xml.etree.ElementTree.tostring(search)

#sets = flickr.photosets.getList(user_id= flickr_user_id)

#print xml.etree.ElementTree.tostring(sets)

count =0
for photo in flickr.walk_set(flickr_set_to_rename):
    count += 1
    print count, photo.get('title'), photo.get('id')
    print "----- photo -----"
    print xml.etree.ElementTree.tostring(photo)
    photo_id = photo.get('id')
    print photo_id
    info = flickr.photos.getInfo(photo_id=photo_id)
    print "----- info -----"
    print xml.etree.ElementTree.tostring(info)
    print "---- date taken --- "

    
    date_taken = ""
    for elem in info.iter('dates'):
        if elem.attrib.has_key('taken'):
            date_taken = elem.attrib['taken']
            break
        else:
            print "Warning no date taken info for ",  xml.etree.ElementTree.tostring(elem)
    print photo.get('title'), "date_taken= ",date_taken

    print "----- end -----"

