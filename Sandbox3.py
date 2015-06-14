# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 20:47:53 2015

@author: Michele
"""
#from urllib2 import urlopen #API library?
import json #json parsing library  simplejson simplejson.load(json string holding variable)
import requests
#import pprint
import urllib2

userID = '2338633'
collectionID = 'FH7WPHPV'
apiKey = ''

#function to send a get request
def api_get(userID, collectionID):
    api_url = 'https://api.zotero.org/users/%s/collections/%s/items?v=3' % (userID, collectionID)
    zotero_response = requests.get(api_url)
    print zotero_response.status_code
    return zotero_response

#parse the json into a python object
def parse_zotero(zotero_response):
    encoded_data = json.dumps(data.content)
    parsed_data = json.loads(encoded_data)
    return parsed_data

def data_get(userID, collectionID):
    api_url = 'https://api.zotero.org/users/%s/collections/%s/items?v=3' % (userID, collectionID)
    data_json = json.load(urllib2.urlopen(api_url))
    return data_json


data = api_get(userID, collectionID)
print("Status code: ", data.status_code)
#print(data.content)
data_parsed = parse_zotero(data)

"""def print_zotero(data):
    for i in data:
        print data['data']['key']
        """

testtwo = data_get(userID, collectionID)

print("length: ", len(data_parsed))

for count, element in enumerate(testtwo):
    print count, element['key'], element['data']['date'], element['data']['creators']
    
print(testtwo)

author_list = ""
for i, record in enumerate(testtwo):
    for j, author in enumerate(record['data']['creators']):
        new_author = author['lastName']
        author_list = author_list + ', ' + new_author
        print i, j, record['data']['date'], author['lastName']
