# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LiteratureMapperDialog
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

import os

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
#from PyQt.QtCore import QObject

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'literature_mapper_dialog_base.ui'))

FORM_CLASS_Table, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'table_interface.ui'))
    
class LiteratureMapperDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(LiteratureMapperDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

class TableInterface(QDialog, FORM_CLASS_Table):
    def __init__(self, parent=None):
        super(TableInterface, self).__init__(parent)
        self.setupUi(self)
