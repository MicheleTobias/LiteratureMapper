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
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QObject, QVariant, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QTableWidget, QTableWidgetItem, QMessageBox
# Initialize Qt resources from file resources.py
#from . import resources_rc
# Import the code for the dialog
from .literature_mapper_dialog import LiteratureMapperDialog, TableInterface
import os.path
import json #json parsing library  simplejson simplejson.load(json string holding variable)
import requests
import urllib.request, urllib.error, urllib.parse
import re
from qgis.core import QgsGeometry, QgsFeature, QgsMessageLog, QgsPoint, QgsVectorLayer, QgsField, QgsProject
from qgis.gui import QgsMapToolEmitPoint

class MapToolEmitPoint(QgsMapToolEmitPoint):
    canvasDoubleClicked = pyqtSignal()
    
    #def canvasDoubleClickedEvent():
     #   self.canvasDoubleClicked.emit()

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
        self.menu = self.tr('&Literature Mapper')

        self.toolbar = self.iface.addToolBar('LiteratureMapper')
        self.toolbar.setObjectName('LiteratureMapper')

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
            text=self.tr('Store locations in your Zotero database.'),
            callback=self.run,
            parent=self.iface.mainWindow())
        
        # Signal for clicking on the canvas
        #result = QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.handleMouseDown)
            
        # Signal for Saving data to Zotero
        #QObject.connect(self.dlgTable.pushButton_Save, SIGNAL("clicked()"), self.saveZotero)
        self.dlgTable.pushButton_Save.clicked.connect(self.saveZotero)

        # Signal for Point digitizing button
        #QObject.connect(self.dlgTable.pushButton_Point, SIGNAL("clicked()"), self.digitizePoint)
        self.dlgTable.pushButton_Point.clicked.connect(self.digitizePoint)
        
        # Signal for Multipoint digitizing button
        #QObject.connect(self.dlgTable.pushButton_Multipoint, SIGNAL("clicked()"), self.digitizeMultipoint)
        self.dlgTable.pushButton_Multipoint.clicked.connect(self.digitizeMultipoint)
        # Signal for Finish Multipoint digitizing button
        #QObject.connect(self.dlgTable.pushButton_FinishMultipoint, SIGNAL("clicked()"), self.handleFinishMultipoint)

    def handleMouseDown(self, point, button):
        # Function to record a mouse click - works with the above code
        self.dlgTable.tableWidget_Zotero.setItem(self.dlgTable.tableWidget_Zotero.currentRow(),4,QTableWidgetItem('{"type": "Point", "coordinates": [%s, %s]}' % (str(point.x()),str(point.y()))))
        
        #put point in the memory shp
        self.fet = QgsFeature()
        self.fet.setGeometry(QgsGeometry.fromPoint(point))
        #self.fet.setAttributes([key_str, year_str, author_list, title_str, extra_str])
        self.fet.setAttributes(
        [self.dlgTable.tableWidget_Zotero.item(self.dlgTable.tableWidget_Zotero.currentRow(),0).text(),
        self.dlgTable.tableWidget_Zotero.item(self.dlgTable.tableWidget_Zotero.currentRow(),1).text(),
        self.dlgTable.tableWidget_Zotero.item(self.dlgTable.tableWidget_Zotero.currentRow(),2).text(),
        self.dlgTable.tableWidget_Zotero.item(self.dlgTable.tableWidget_Zotero.currentRow(),3).text(),
        self.dlgTable.tableWidget_Zotero.item(self.dlgTable.tableWidget_Zotero.currentRow(),4).text()])
        self.pointProvider.addFeatures([self.fet])
        self.pointLayer.updateExtents()
        self.iface.mapCanvas().refresh()

        # Make the plugin come back to the top
        self.dlgTable.activateWindow()

        # TODO: accept other geometry types besides points

    def saveZotero(self):
        #Write what happens to save to zotero here
        rows = list(range(0, QTableWidget.rowCount(self.dlgTable.tableWidget_Zotero)))
        for row in rows:
            #get the itemID(zotero key) and geometry cells from the table - itemAt(x,y)
            itemKey = self.dlgTable.tableWidget_Zotero.item(row, 0).text()
            extraString = self.dlgTable.tableWidget_Zotero.item(row, 4).text()
            QgsMessageLog.logMessage("row: %s  itemKey: %s  extraString: %s" % (row, itemKey, extraString), 'LiteratureMapper', QgsMessageLog.INFO)
            
            request_url = 'https://api.zotero.org/users/%s/items/%s' % (self.userID, itemKey)
            item_request = requests.get(request_url)
            QgsMessageLog.logMessage("Item Request Response: %s" % item_request.status_code, 'LiteratureMapper', QgsMessageLog.INFO)
            item_json = json.load(urllib.request.urlopen(request_url))
            item_json['data']['extra'] = extraString
            item_json=json.dumps(item_json)
            put_request = requests.put(request_url, data=item_json, headers={'Authorization': 'Bearer %s' % (self.apiKey), 'Content-Type': 'application/json'})
            QgsMessageLog.logMessage("Put Response: %s" % put_request.status_code, 'LiteratureMapper', QgsMessageLog.INFO)
            statuscode = put_request.status_code
        # Message bar for result
        # TODO: make it check all the results, not just the last one
        if statuscode == 204:
            self.iface.messageBar().pushMessage("Locations saved to Zotero.", level=4)
            #QMessageBox.information(self.dlgTable(),"Info", "Locations Saved")
        else:
            self.iface.messageBar().pushMessage("Failed to save locations to Zotero", level=3)

    def digitizePoint(self):
        QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.handleMouseDown)
        
    def handleMouseDownMultipoint(self, point):
        x = point.x()
        y = point.y()
        newPoint = [x, y]
        self.pointList.append(newPoint)
        
        QgsMessageLog.logMessage("x: %s ... y: %s" % (x, y), 'LiteratureMapper', QgsMessageLog.INFO)
        QgsMessageLog.logMessage("x: %s ... y: %s" % (type(x), type(y)), 'LiteratureMapper', QgsMessageLog.INFO)
        QgsMessageLog.logMessage("newPoint: %s" % newPoint, 'LiteratureMapper', QgsMessageLog.INFO)
        QgsMessageLog.logMessage("newPoint: %s" % type(newPoint), 'LiteratureMapper', QgsMessageLog.INFO)
        QgsMessageLog.logMessage("self.pointList: %s" % self.pointList, 'LiteratureMapper', QgsMessageLog.INFO)
        
        self.dlgTable.tableWidget_Zotero.setItem(self.dlgTable.tableWidget_Zotero.currentRow(),4,QTableWidgetItem('{"type": "Multipoint", "coordinates": %s}' % self.pointList))
        
        #QObject.connect(self.clickTool, SIGNAL("canvasDoubleClicked(const QgsPoint &, Qt::MouseButton)"), self.handleMouseDownMultipointFinish)
        #Needs a special implementation of canvasDoubleClicked because it is a virtual method and needs to be told what to do.  
        #http://stackoverflow.com/questions/19973188/emit-and-catch-double-click-signals-from-qgsmapcanvas
        
    # def handleFinishMultipoint(self):
    #     try:
    #         self.pointList
    #     except:
    #         pass
    #     else:
    #         self.dlgTable.tableWidget_Zotero.setItem(self.dlgTable.tableWidget_Zotero.currentRow(),4,QTableWidgetItem('{"type": "Multipoint", "coordinates": %s}' % self.pointList))
        
    def handleMouseDownMultipointFinish(self):
        self.dlgTable.tableWidget_Zotero.setItem(self.dlgTable.tableWidget_Zotero.currentRow(),4,QTableWidgetItem('{"type": "Multipoint", "coordinates": %s}' % self.pointList))
        # TODO: Fix double click signal
        # TODO: put the multipoints into a memory shp
        # TODO: populate the multipoint memory shp with existing multipoints
    
    def digitizeMultipoint(self):
        #Empty list for storing points for digitizing
        self.pointList = []
        QgsMessageLog.logMessage("self.pointList: %s" % self.pointList, 'LiteratureMapper', QgsMessageLog.INFO)
        QgsMessageLog.logMessage("self.pointList: %s" % type(self.pointList), 'LiteratureMapper', QgsMessageLog.INFO)
        #resultMultipoint = QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint)"), self.handleMouseDownTwo)
        QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.handleMouseDownMultipoint)
        #QObject.connect(self.clickTool, SIGNAL("canvasDoubleClicked()"), self.handleMouseDownTwoFinish)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr('&Literature Mapper'),
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
            def api_get(userID, collectionID, apiKey):
                api_url = 'https://api.zotero.org/users/%s/collections/%s/items?key=%s' % (userID, collectionID, apiKey)
                zotero_response = requests.get(api_url)
                #print zotero_response.status_code
                return zotero_response
            
            #function to parse the Zotero API data
            def parse_zotero(zotero_response):
                encoded_data = json.dumps(data.content)
                parsed_data = json.loads(encoded_data)
                return parsed_data
            
            
            def data_get(userID, collectionID, apiKey):
                api_url = 'https://api.zotero.org/users/%s/collections/%s/items?v=3&key=%s' % (userID, collectionID, apiKey)
                data_json = json.load(urllib.request.urlopen(api_url))
                return data_json
                        
            #Getting the variables the user entered
            self.userID = self.dlg.lineEdit_UserID.text()
            self.collectionID = self.dlg.lineEdit_CollectionKey.text()
            self.apiKey = self.dlg.lineEdit_APIKey.text()
            
            #Log the numbers the user entered
            QgsMessageLog.logMessage("User ID: %s" % self.userID, 'LiteratureMapper', QgsMessageLog.INFO)
            QgsMessageLog.logMessage("Collection ID: %s" % self.collectionID, 'LiteratureMapper', QgsMessageLog.INFO)
            QgsMessageLog.logMessage("API Key: %s" % self.apiKey, 'LiteratureMapper', QgsMessageLog.INFO)
            
            #Send a Get Request to test the connection and get the collection data
            data = api_get(self.userID, self.collectionID, self.apiKey)
            data_parsed = parse_zotero(data)
            data_json = data_get(self.userID, self.collectionID, self.apiKey)
                        
            #if the server response = 200, start the window that records geometry from map canvas clicks.
            if data.status_code == 200:
                #self.iface.messageBar().pushMessage("Zotero is ready!", level=1)
                #open a new interface
                self.dlgTable.show()
                
                #put the data into a table in the interface
                self.dlgTable.tableWidget_Zotero.setRowCount(len(data_json))
                self.dlgTable.tableWidget_Zotero.verticalHeader().setVisible(False)
                
                #Create the empty Point shapefile memory layer
                self.pointLayer = QgsVectorLayer("Point", "Literature_Points", "memory")
                self.pointProvider = self.pointLayer.dataProvider()
                QgsMapLayer.instance().addMapLayer(self.pointLayer)
                # add fields
                self.pointProvider.addAttributes([QgsField("Key", QVariant.String),
                    QgsField("Year",  QVariant.Int),
                    QgsField("Author", QVariant.String),
                    QgsField("Title", QVariant.String),
                    QgsField("Geometry", QVariant.String)
                    ])
                self.pointLayer.updateFields() # tell the vector layer to fetch changes from the provider
                
                #Create the empty shapefile memory layer
                self.multipointLayer = QgsVectorLayer("Multipoint", "Literature_Multipoints", "memory")
                self.multipointProvider = self.multipointLayer.dataProvider()
                QgsMapLayer.instance().addMapLayer(self.multipointLayer)
                # add fields
                self.multipointProvider.addAttributes([QgsField("Key", QVariant.String),
                    QgsField("Year",  QVariant.Int),
                    QgsField("Author", QVariant.String),
                    QgsField("Title", QVariant.String),
                    QgsField("Geometry", QVariant.String)
                    ])
                self.multipointLayer.updateFields() # tell the vector layer to fetch changes from the provider
                
                for i, record in enumerate(data_json):
                    key = QTableWidgetItem(record['data']['key'])
                    self.dlgTable.tableWidget_Zotero.setItem(i, 0, key)
                    key_str = record['data']['key']

                    year = QTableWidgetItem(record['data']['date'])
                    self.dlgTable.tableWidget_Zotero.setItem(i, 1, year)
                    year_str = record['data']['date']
                    
                    author_list = ""
                    # Handle different athor types - Human has lastName, Corporate has name, Others get a blank because they are presumably blanks
                    for j, author in enumerate(record['data']['creators']):
                        if 'lastName' in author:
                            new_author = author['lastName']
                        elif 'name' in author:
                            new_author = author['name']
                        else:
                            new_author = ""
                            
                        author_list = author_list + ', ' + new_author
                    author_list = author_list[2 : len(author_list)]
                    self.dlgTable.tableWidget_Zotero.setItem(i, 2, QTableWidgetItem(author_list))
                    
                    title = QTableWidgetItem(record['data']['title'])
                    self.dlgTable.tableWidget_Zotero.setItem(i, 3, title)
                    title_str = record['data']['title']
                    
                    # pre-populate the table with anything already in the Extra field
                    if 'extra' in record['data']:
                        extra = QTableWidgetItem(record['data']['extra'])
                        
                        extra_str = record['data']['extra']
                        QgsMessageLog.logMessage("Extra String: %s" % extra_str, 'LiteratureMapper', QgsMessageLog.INFO)
                        check_point = '"type": "Point"'
                        check_multipoint = '"type": "Multip'
                        if extra_str[1:16] == check_point:
                            coords = extra_str[extra_str.find('['): extra_str.find(']')+1]
                            x = float(coords[1:coords.find(',')])
                            y = float(coords[coords.find(',')+1:coords.find(']')])
                            #put records with existing geometries into the virtual Point shapefile attribute table
                            self.fet = QgsFeature()
                            self.fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(x,y)))
                            self.fet.setAttributes([key_str, year_str, author_list, title_str, extra_str])
                            self.pointProvider.addFeatures([self.fet])
                            self.pointLayer.updateExtents()
                        elif extra_str[1:16] == check_multipoint:
                            #Alter to make a multipoint
                            #Needs a loop to run through all the points?
                            QgsMessageLog.logMessage("Made it into Multipoint Elif", 'LiteratureMapper', QgsMessageLog.INFO)
                            
                            # Coords needs to be formatted this way: gPolygon = QgsGeometry.fromPolygon([[QgsPoint(1, 1), QgsPoint(2, 2), QgsPoint(2, 1)]])
                            coords = extra_str[(extra_str.find('[')+1): (len(extra_str)-2)]
                            #looks like this: [-132.58038861948805, 36.36773760268237], [-126.90494519104253, 33.262306292778206], [-124.28139115336488, 36.84961487490887]
                            QgsMessageLog.logMessage("Coords: %s" % coords, 'LiteratureMapper', QgsMessageLog.INFO)
                            #Replace [ with [( and add QgsPoint
                            p=re.compile( '\[' )
                            c = p.sub('QgsPoint(', str(coords))
                            #Replace ] with )]
                            q = re.compile( '\]' )
                            coords_list = q.sub(')', str(c))
                            
                            coords_list = '['+coords_list+']'
                            QgsMessageLog.logMessage("Coords_List: %s" % coords_list, 'LiteratureMapper', QgsMessageLog.INFO)
                            
                            #put records with existing geometries into the virtual Multipoint shapefile attribute table
                            self.fet = QgsFeature()
                            #does QgsPoint make a multipoint or do you need another command?
                            self.fet.setGeometry(QgsGeometry.fromMultiPoint(eval(coords_list)))
                            #^change 1,1 back to x,y
                            self.fet.setAttributes([key_str, year_str, author_list, title_str, extra_str])
                            self.multipointProvider.addFeatures([self.fet])
                            self.multipointLayer.updateExtents()
                        else:
                            x = ''
                    else:
                        extra = QTableWidgetItem("")
                    self.dlgTable.tableWidget_Zotero.setItem(i, 4, extra)
                    

                
                # Reize the cells to fit the contents - behaves badly with the title column
                #self.dlgTable.tableWidget_Zotero.resizeRowsToContents()
                
                # Resize the Key and Year columns to fit the width of the contents
                self.dlgTable.tableWidget_Zotero.resizeColumnToContents(0)
                self.dlgTable.tableWidget_Zotero.resizeColumnToContents(1)
                
                # FUNCTIONALITY
                # TODO: Put points on the map canvas: http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/canvas.html#rubber-bands-and-vertex-markers  Memory Layers: http://gis.stackexchange.com/questions/72877/how-to-load-a-memory-layer-into-map-canvas-an-zoom-to-it-with-pyqgis  http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/vector.html#memory-provider
                # TODO: Transform coordinates if not in WGS84: http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/crs.html
                # TODO: update points in the memory shp don't just add new ones
                
                # USABILITY
                # TODO: Speed up saving to Zotero - will sending one query be quicker?  How does the version stuff work?
                # TODO: Make other table columns uneditable: http://stackoverflow.com/questions/2574115/qt-how-to-make-a-column-in-qtablewidget-read-only
                # TODO: Documentation
                
                
            else:
                self.iface.messageBar().pushMessage("Zotero cannot connect. Check the IDs you entered and try again.", level=1)


