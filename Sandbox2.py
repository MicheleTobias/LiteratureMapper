from pyzotero import zotero

userID = '2338633'
collectionID = '7VGCKIXX'
apiKey = 'RBdQF6QREuQGvjXezOgqHiQO'

#################
#zot = zotero.Zotero(collectionID, 'user', apiKey)
zot = zotero.Zotero(userID, 'user', apiKey)

items = zot.items()

for item in items:
    print('Item Type: %s | Key: %s') % (item['data']['itemType'], item['data']['key'])



