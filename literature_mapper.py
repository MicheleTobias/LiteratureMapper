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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from literature_mapper_dialog import LiteratureMapperDialog
import os.path
import json #json parsing library  simplejson simplejson.load(json string holding variable)
import requests


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



    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Literature Mapper'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        
        if result == 1:
            # send the API request
            #function to send a get request
            def api_get(userID, collectionID):
                api_url = 'https://api.zotero.org/users/%s/collections/%s/items?v=3' % (userID, collectionID)
                zotero_response = requests.get(api_url)
                #print zotero_response.status_code
                return zotero_response
            
            # *if* the server response = 200, start the window that records geometry from map canvas clicks.
            userID = '2338633'
            collectionID = '7VGCKIXX'
            apiKey = 'RBdQF6QREuQGvjXezOgqHiQO'
            data = api_get('2338633', '7VGCKIXX')
            if data.status_code == 200:
                #self.objectfrominterface.content <-- how to access the user input
                self.iface.messageBar().pushMessage("Zotero is ready!", level=1)
            else:
                self.iface.messageBar().pushMessage("Try again...", level=1)
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            #from urllib2 import urlopen #API library?
            #import json #json parsing library
            # arrange the input into an API call that checks with Zotero 
            #response = requests.get(URL GOES HERE!)
            #if response.status_code = 200:
             #   PROCEED
                
            # Pull in a list of citations from the collection specified
            # Put the citations into a table
            # Select a citation in the table, then let the user click to add the geometry to the appropriate column.
            
        
            #pass
