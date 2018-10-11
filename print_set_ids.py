#!/usr/bin/env python

import os
import flickrapi
import xml
import logging
import webbrowser


logging.basicConfig()

api_key = unicode(os.environ.get('FLICKR_API_KEY',''))
print "API_KEY=",api_key
api_secret = unicode(os.environ.get('FLICKR_API_SECRET',''))
print "API_SECRET=",api_secret
flickr_user_id= os.environ.get('FLICKR_USER_ID','')
print "FLICKR_USER_ID=",flickr_user_id


flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read')

def print_set_ids(user_id=flickr_user_id):
	"""Prints out the set id and the set title for the given flickr user"""
	sets = flickr.photosets.getList(user_id= flickr_user_id)
	#print xml.etree.ElementTree.tostring(sets)
	print "SET_ID            SET_TITLE"
	for child in sets:
		for grandchild in child:
			set_id = grandchild.attrib['id']
			for greatgrandchild in grandchild.iter('title'):
				print set_id, greatgrandchild.text

		
def parse_args():
	return None
	
def main(args):
	print_set_ids()

if __name__ == '__main__':
	args = parse_args()
	main(args)


