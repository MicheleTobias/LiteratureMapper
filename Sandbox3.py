# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 20:47:53 2015

@author: Michele
"""
#from urllib2 import urlopen #API library?
import json #json parsing library  simplejson simplejson.load(json string holding variable)
import requests
#import pprint


userID = '2338633'
collectionID = '7VGCKIXX'
apiKey = ''

#function to send a get request
def api_get(userID, collectionID):
    api_url = 'https://api.zotero.org/users/%s/collections/%s/items?v=3' % (userID, collectionID)
    zotero_response = requests.get(api_url)
    print zotero_response.status_code
    return zotero_response

api_get('2338633', '7VGCKIXX')

data = api_get(userID, collectionID)
print(data.status_code)
print(data.content)

def print_zotero(data):
    for i in data:
        print data['data']['key']
        

#make this into a function
encoded_data = json.dumps(data.content)
parsed_data = json.loads(encoded_data)
print(parsed_data)