# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 10:39:08 2018

@author: mmtobias
"""

import json
import requests
import urllib.request
from math import ceil

userID = ''
collectionID = ''
apiKey = ''

def api_get(userID, collectionID, apiKey, limit=100, start=0):
    api_url = 'https://api.zotero.org/users/%s/collections/%s/items?key=%s&limit=%s&start=%s&itemType=-attachment || note' % (userID, collectionID, apiKey, limit, start)
    #QgsMessageLog.logMessage(api_url, 'LiteratureMapper', Qgis.Info)
    zotero_response = requests.get(api_url)
    return zotero_response

def parse_zotero(zotero_response):
    #encoded_data = json.dumps(zotero_response.content)
	  #encoded_data = json.dumps(data.content)
    #parsed_data = json.loads(encoded_data)
    parsed_data = json.loads(zotero_response.content.decode('utf-8'))
    return parsed_data


data = api_get(userID, collectionID, apiKey)
data_json = parse_zotero(data)



# accessing the Extra field:
# data_json[2]['data']['extra']


# Text to work with as an example of what this should look like.
text_extra = 'Notes about a citation. Some other stuff that is too important to erase. <geojson>{"type": "Point", "coordinates": [-121.943352010208, 36.5996662302192]}</geojson> Plus someone put something after this because they could.'

# STUFF THAT DIDN'T WORK BUT MIGHT HELP LATER:
# split the extra string 
#text_extra_parts = text_extra.split("<geojson>")
#remove the end tag
#test_extra_parts = text_extra[1].replace("/geojson>", "")
#test_extra_parts = text_extra[1].strip("/geojson>")
#json_string = text_extra_parts[1]

# Get the geojson string from the extra field
geojson_str = text_extra[text_extra.find("<geojson>")+9:text_extra.find("</geojson>")]


# How do we update the string and then insert it into the extra string?

#get the stuff in front of the <geojson> and after </geojson>, then concatenate them with the new spatial string?
before_geojson = text_extra[0 : text_extra.find("<geojson>")]
after_geojson = text_extra[text_extra.find("</geojson>")+10:]

# Put it back together
# -----> saveZotero() function's extraString gets what we have here in geojson_str

new_extra = before_geojson + "<geojson>" + geojson_str + "</geojson>" + after_geojson








