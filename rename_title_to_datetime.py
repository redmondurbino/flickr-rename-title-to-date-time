import os
import flickrapi
import xml
import logging
import webbrowser
from datetime import datetime


logging.basicConfig()

api_key = unicode(os.environ.get('FLICKR_API_KEY',''))
print api_key
api_secret = unicode(os.environ.get('FLICKR_API_SECRET',''))
print api_secret
flickr_user_id= os.environ.get('FLICKR_USER_ID','')
flickr_set_to_rename= os.environ.get('FLICKR_SET_TO_RENAME','')

#flickr_set_to_rename ='72157659400135206'

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='write')


#search = flickr.photos.search(user_id= flickr_user_id, per_page='100', text='-20')
#print "search=",xml.etree.ElementTree.tostring(search)

#sets = flickr.photosets.getList(user_id= flickr_user_id)

#print xml.etree.ElementTree.tostring(sets)


def find_date_taken(photo):
    photo_id = photo.get('id')
    #print photo_id
    info = flickr.photos.getInfo(photo_id=photo_id)
    date_taken = ""
    for elem in info.iter('dates'):
        if elem.attrib.has_key('taken'):
            date_taken = elem.attrib['taken']
            break  
    return date_taken

def calculate_new_title(date_taken):
    """Figure out what our new title should be"""
    # we get date taken me from flickr in the format "2018-08-05 17:30:06"
    # we want returned string to be "2018-07-22 at 22.08.58"
    datetime_object = datetime.strptime( date_taken, '%Y-%m-%d %H:%M:%S')
    new_title = datetime_object.strftime('%Y-%m-%d at %H.%M.%S')
    return new_title

    

def set_title(photo, title):
    photo_id = photo.get('id')
    response = flickr.photos.setMeta( photo_id=photo_id, title=title)
    if not ( response.attrib.has_key('stat') and response.attrib['stat'] == 'ok' ):
        print "Error changing title response = " + xml.etree.ElementTree.tostring(response)

count =0
output = ''
dry_run = False
for photo in flickr.walk_set(flickr_set_to_rename):
    count += 1
    #print count, photo.get('title'), photo.get('id')
    #print "----- photo -----"
    #print xml.etree.ElementTree.tostring(photo)
    photo_id = photo.get('id')
    #print photo_id
    #info = flickr.photos.getInfo(photo_id=photo_id)
    #print "----- info -----"
    #print xml.etree.ElementTree.tostring(info)
    #print "---- date taken --- "

    title = photo.get('title')
    
    # find photos that don't start with the year 20xx,
    if title and not title.startswith('20'):
        date_taken = find_date_taken( photo)
        if date_taken:
            output +=  photo.get('title') + " " + date_taken + "\n"
            new_title = calculate_new_title(date_taken)
            print 'changing "%s" to "%s" id="%s"' % (title, new_title, photo_id)
            if not dry_run:
                set_title(photo, new_title)
        else:
            print 'Warning could not find date taken for "%s" id="%s"' % (title,  photo_id)
    if count % 1000 == 0:
        print count

    #print "----- end -----"



