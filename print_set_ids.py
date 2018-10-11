#!/usr/bin/env python

import argparse
import os
import flickrapi
import xml
import logging
import webbrowser


logging.basicConfig()

default_api_key = unicode(os.environ.get('FLICKR_API_KEY',''))
print "default API_KEY=",default_api_key
default_api_secret = unicode(os.environ.get('FLICKR_API_SECRET',''))
print "default API_SECRET=",default_api_secret
default_flickr_user_id= os.environ.get('FLICKR_USER_ID','')
print "default FLICKR_USER_ID=",default_flickr_user_id


def print_set_ids(flickr,args):
	"""Prints out the set id and the set title for the given flickr user"""
	sets = flickr.photosets.getList(user_id= args.flickr_user_id)
	#print xml.etree.ElementTree.tostring(sets)
	print "SET_ID            SET_TITLE"
	for child in sets:
		for grandchild in child:
			set_id = grandchild.attrib['id']
			for greatgrandchild in grandchild.iter('title'):
				print set_id, greatgrandchild.text

		
def parse_args():
    """ Parse the arguments """
    parser = argparse.ArgumentParser(description = "Print the set ids and titles of a flickr user.")
    parser.add_argument("--api_key", default = default_api_key, help = "the flickr api key. https://www.flickr.com/services/api/misc.api_keys.html")
    parser.add_argument("--api_secret", default = default_api_secret, help = "the flickr api secret. https://www.flickr.com/services/api/misc.api_keys.html")
    parser.add_argument("--flickr_user_id", default = default_flickr_user_id, help = "your flickr user id. https://www.webpagefx.com/tools/idgettr/")
    args = parser.parse_args()
    return args
	
def main(args):
	flickr = flickrapi.FlickrAPI(args.api_key, args.api_secret)
	flickr.authenticate_via_browser(perms='read')
	print_set_ids(flickr, args)

if __name__ == '__main__':
	args = parse_args()
	main(args)


