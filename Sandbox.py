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

# arrange the input into an API call that checks with Zotero 
#query_params = { 'key': '',
                #'userID': '2338633',
                #'collectionID': 'NR8XU5N6'
		 		#}

endpoint = 'https://api.zotero.org'
response = requests.get('https://api.zotero.org/users/2338633/collections/7VGCKIXX/items?v=3')
#response = requests.get(endpoint, params = query_params)


print(response.status_code)

print(response.content)
 
test = 'https://api.zotero.org/users/%s/collections/%s/items?v=3' % (userID, collectionID)
print(userID)
print(test)


#if response.status_code = 200:
    #print 'Go ahead!'

userID = '2338633'
collectionID = '7VGCKIXX'
apiKey = 'RBdQF6QREuQGvjXezOgqHiQO'

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
        



