# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 20:47:53 2015

@author: Michele
"""
#from urllib2 import urlopen #API library?
#import json #json parsing library
import requests
#import pprint
import pyzotero

userID = '2338633'
collectionID = '7VGCKIXX'
apiKey = 'RBdQF6QREuQGvjXezOgqHiQO'

# arrange the input into an API call that checks with Zotero 
#query_params = { 'key': 'RBdQF6QREuQGvjXezOgqHiQO',
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

#################
zot = zotero.Zotero(collectionID, 'user', apiKey)



#if response.status_code = 200:
    #print 'Go ahead!'
