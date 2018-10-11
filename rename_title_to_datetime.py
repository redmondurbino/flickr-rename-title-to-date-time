#!/usr/bin/env python

import argparse
import os
import flickrapi
import xml
import logging
import webbrowser
from datetime import datetime


logging.basicConfig()

default_api_key = unicode(os.environ.get('FLICKR_API_KEY',''))
print "default API_KEY=",default_api_key
default_api_secret = unicode(os.environ.get('FLICKR_API_SECRET',''))
print "default API_SECRET=",default_api_secret
default_flickr_user_id= os.environ.get('FLICKR_USER_ID','')
print "default FLICKR_USER_ID=",default_flickr_user_id
default_set_id = flickr_set_id= os.environ.get('FLICKR_SET_ID','')
print "default FLICKR_SET_ID=",default_set_id



#search = flickr.photos.search(user_id= flickr_user_id, per_page='100', text='-20')
#print "search=",xml.etree.ElementTree.tostring(search)

#sets = flickr.photosets.getList(user_id= flickr_user_id)

#print xml.etree.ElementTree.tostring(sets)


def find_date_taken(flickr, photo):
    photo_id = photo.get('id')
    #print photo_id
    info = flickr.photos.getInfo(photo_id=photo_id)
    date_taken = ""
    for elem in info.iter('dates'):
        if elem.attrib.has_key('taken'):
            date_taken = elem.attrib['taken']
            break  
    return date_taken

def calculate_new_title( date_taken):
    """Figure out what our new title should be"""
    # we get date taken me from flickr in the format "2018-08-05 17:30:06"
    # we want returned string to be "2018-07-22 at 22.08.58"
    datetime_object = datetime.strptime( date_taken, '%Y-%m-%d %H:%M:%S')
    new_title = datetime_object.strftime('%Y-%m-%d at %H.%M.%S')
    return new_title

    

def set_title(flickr, photo, title):
    photo_id = photo.get('id')
    response = flickr.photos.setMeta( photo_id=photo_id, title=title)
    if not ( response.attrib.has_key('stat') and response.attrib['stat'] == 'ok' ):
        print "Error changing title response = " + xml.etree.ElementTree.tostring(response)

def search_and_change(flickr, args):
	count =0
	changed=0
	output = ''
	dry_run = False

	if dry_run:
		print "dry run is true, not doing any actual changes"

	for photo in flickr.walk_set(args.flickr_set_id):
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
			date_taken = find_date_taken(flickr, photo)
			if date_taken:
				output +=  photo.get('title') + " " + date_taken + "\n"
				new_title = calculate_new_title(date_taken)
				print 'changing "%s" to "%s" id="%s"' % (title, new_title, photo_id)
				if not dry_run:
					set_title(flickr, photo, new_title)
					changed += 1
			else:
				print 'Warning could not find date taken for "%s" id="%s"' % (title,  photo_id)
		if count % 1000 == 0:
			print count

		#print "----- end -----"

	print "photos checked=",count
	print "photos renamed=", changed


def parse_args():
    """ Parse the arguments """
    parser = argparse.ArgumentParser(description = "Print the set ids and titles of a flickr user.")
    parser.add_argument("--api_key", default = default_api_key, help = "the flickr api key. https://www.flickr.com/services/api/misc.api_keys.html")
    parser.add_argument("--api_secret", default = default_api_secret, help = "the flickr api secret. https://www.flickr.com/services/api/misc.api_keys.html")
    parser.add_argument("--flickr_user_id", default = default_flickr_user_id, help = "your flickr user id. https://www.webpagefx.com/tools/idgettr/")
    parser.add_argument("--flickr_set_id", default = default_set_id, help = "the set (or album) you want to rename photos in. run print_set_ids.py to get a list")
    args = parser.parse_args()
    return args
    
    
def main(args):
	flickr = flickrapi.FlickrAPI(args.api_key, args.api_secret)
	flickr.authenticate_via_browser(perms='write')
	search_and_change(flickr, args)
	
if __name__ == '__main__':
	args = parse_args()
	main(args)