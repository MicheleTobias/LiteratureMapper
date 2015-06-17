# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LiteratureMapper
                                 A QGIS plugin
 Add spatial locations to the citations in your Zotero database.
                              -------------------
        begin                : 2015-06-06
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Michele Tobias & Alex Mandel
        email                : mmtobias@ucdavis.edu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QObject, SIGNAL
from PyQt4.QtGui import QAction, QIcon, QTableWidget, QTableWidgetItem, QMessageBox
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from literature_mapper_dialog import LiteratureMapperDialog, TableInterface
import os.path
import json #json parsing library  simplejson simplejson.load(json string holding variable)
import requests
from qgis.core import QgsMessageLog
import urllib2
from qgis.gui import *


class LiteratureMapper:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # a reference to our map canvas
        self.canvas = self.iface.mapCanvas()  #CHANGE
        # this QGIS tool emits as QgsPoint after each click on the map canvas
        self.clickTool = QgsMapToolEmitPoint(self.canvas)
        
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'LiteratureMapper_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = LiteratureMapperDialog()
        self.dlgTable = TableInterface()
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Literature Mapper')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'LiteratureMapper')
        self.toolbar.setObjectName(u'LiteratureMapper')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('LiteratureMapper', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/LiteratureMapper/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Store locations in your Zotero database.'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        # For clicking on the canvas - checks to see if a click happened
        result = QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.handleMouseDown)
        #QMessageBox.information( self.iface.mainWindow(),"Info", "connect = %s"%str(result) )
        QObject.connect(self.dlgTable.pushButton_Save, SIGNAL("clicked()"), self.saveZotero)
    
    # Function to record a mouse click - works with the above code
    # change this so it puts the point in the table
    def handleMouseDown(self, point, button):
        #QMessageBox.information( self.iface.mainWindow(),"Info", "X,Y = %s,%s" % (str(point.x()),str(point.y())) )
        # get active table cell
        # get mouse click X & Y
        # put X & Y in the cell - 
        self.dlgTable.tableWidget_Zotero.setItem(self.dlgTable.tableWidget_Zotero.currentRow(),4,QTableWidgetItem('{"type": "Point", "coordinates": [%s, %s]}' % (str(point.x()),str(point.y()))))
        # --TODO: finess the geometry string into a geoJSON geometry string
        # TODO: accept other geometry types besides points

    def saveZotero(self):
        #Write what happens to save to zotero here
        pass

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Literature Mapper'),
                action)
            self.iface.removeToolBarIcon(action)
    
    def store(self):
        s = QSettings()
        s.setValue("literaturemapper/myapikey", self.dlg.lineEdit_APIKey.text())
        s.setValue("literaturemapper/myuserid",  self.dlg.lineEdit_UserID.text())
        s.setValue("literaturemapper/mycollectionkey", self.dlg.lineEdit_CollectionKey.text())

    def read(self):
        s = QSettings()
        self.dlg.lineEdit_APIKey.setText(s.value("literaturemapper/myapikey", ""))
        self.dlg.lineEdit_UserID.setText(s.value("literaturemapper/myuserid", ""))
        self.dlg.lineEdit_CollectionKey.setText(s.value("literaturemapper/mycollectionkey", ""))



    def run(self):
        """Run method that performs all the real work"""
        # make our clickTool the tool that we'll use for now
        self.canvas.setMapTool(self.clickTool)
        
        # show the dialog
        self.dlg.show()
        self.read()
        # Run the dialog event loop
        result = self.dlg.exec_()
        self.store()
        # See if OK was pressed
        
        if result == 1:
            # send the API request
            #function to send a get request  # arrange the input into an API call that checks with Zotero 
            def api_get(userID, collectionID):
                api_url = 'https://api.zotero.org/users/%s/collections/%s/items?v=3' % (userID, collectionID)
                zotero_response = requests.get(api_url)
                #print zotero_response.status_code
                return zotero_response
            
            #function to parse the Zotero API data
            def parse_zotero(zotero_response):
                encoded_data = json.dumps(data.content)
                parsed_data = json.loads(encoded_data)
                return parsed_data
            
            
            def data_get(userID, collectionID):
                api_url = 'https://api.zotero.org/users/%s/collections/%s/items?v=3' % (userID, collectionID)
                data_json = json.load(urllib2.urlopen(api_url))
                return data_json
            
            #hardcoded variables ---- change to get them from the interface
            #userID = '2338633'
            #collectionID = '7VGCKIXX'
            #apiKey = ''
            
            #Getting the variables the user entered
            userID = self.dlg.lineEdit_UserID.text()
            collectionID = self.dlg.lineEdit_CollectionKey.text()
            apiKey = self.dlg.lineEdit_APIKey.text()
            
            #Log the numbers the user entered
            QgsMessageLog.logMessage("User ID: %s" % userID, 'LiteratureMapper', QgsMessageLog.INFO)
            QgsMessageLog.logMessage("Collection ID: %s" % collectionID, 'LiteratureMapper', QgsMessageLog.INFO)
            QgsMessageLog.logMessage("API Key: %s" % apiKey, 'LiteratureMapper', QgsMessageLog.INFO)
            
            #Send a Get Request to test the connection and get the collection data
            data = api_get(userID, collectionID)
            data_parsed = parse_zotero(data)
            data_json = data_get(userID, collectionID)
                        
            #if the server response = 200, start the window that records geometry from map canvas clicks.
            if data.status_code == 200:
                self.iface.messageBar().pushMessage("Zotero is ready!", level=1)
                #open a new interface
                self.dlgTable.show()
                
                #put the data into a table in the interface
                self.dlgTable.tableWidget_Zotero.setRowCount(len(data_json))
                self.dlgTable.tableWidget_Zotero.verticalHeader().setVisible(False)
                
                for i, record in enumerate(data_json):
                    key = QTableWidgetItem(record['data']['key'])
                    self.dlgTable.tableWidget_Zotero.setItem(i, 0, key)
                    year = QTableWidgetItem(record['data']['date'])
                    self.dlgTable.tableWidget_Zotero.setItem(i, 1, year)
                    author_list = ""
                    # TODO: implement a check to see if 'lastName' exists
                    for j, author in enumerate(record['data']['creators']):
                        new_author = author['lastName']
                        author_list = author_list + ', ' + new_author
                    self.dlgTable.tableWidget_Zotero.setItem(i, 2, QTableWidgetItem(author_list[2 : len(author_list)]))
                    title = QTableWidgetItem(record['data']['title'])
                    self.dlgTable.tableWidget_Zotero.setItem(i, 3, title)
                #for i, record in enumerate(data_json):
                 #   for j, element in enumerate(record):
                  #      item = QTableWidgetItem(record['data'][element])
                   #     self.dlgTable.tableWidget_Zotero.setItem(i, j, item)              
                
                #get location from mouse click --> happens in another part of the code above
                
                # TODO: Put Request to Zotero: put the location in the Extra field
                # TODO: Put points on the map canvas
                # TODO: Save Shapefile option
                # TODO: Docable or auto switch back to the table after canvas click
                # TODO: Transform coordinates if not in WGS84
                # TODO: Hand-entering the X & Y
                
            else:
                self.iface.messageBar().pushMessage("Zotero cannot connect. Check the IDs you entered and try again.", level=1)


               
            # Pull in a list of citations from the collection specified
            # Put the citations into a table
            # Select a citation in the table, then let the user click to add the geometry to the appropriate column.
            
            
            #from urllib2 import urlopen #API library?
            #import json #json parsing library
            #pass
