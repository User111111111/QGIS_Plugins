# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Ellipse
                                 A QGIS plugin
 Create ellipses based on minor and major axis diameter widths and a rotation angle in degrees
                              -------------------
        begin                : 2015-12-15
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Script: Pete Wells (Lutra Consulting); Plugin: Ali Moyle (Ecotricity)
        email                : ali.moyle@ecotricity.co.uk
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
import resources
# Import the code for the dialog
from GIS41_01_Ellipse_dialog import EllipseDialog
import os.path
from qgis.core import *


class Ellipse:
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
            'Ellipse_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = EllipseDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Ellipse')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Ellipse')
        self.toolbar.setObjectName(u'Ellipse')

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
        return QCoreApplication.translate('Ellipse', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=False,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

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

        icon_path = ':/plugins/Ellipse/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Create Ellipse'),
            callback=self.run,
            parent=self.iface.mainWindow())
        self.iface.addPluginToVectorMenu("Ellipse", self.actions[0])


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Ellipse'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
        self.iface.removePluginVectorMenu("Ellipse", self.actions[0])


    def run(self):
        """Run method that performs all the real work"""
        from PyQt4.QtGui import QMessageBox

        # Get the current layer
        cur_layer = self.iface.mapCanvas().currentLayer()

        #Ensure that the layer exists
        if cur_layer is None:
            problem = 'No layer selected'
            QMessageBox.information(None, "Invalid target layer:", problem)
            return False

        # Ensure it's a vector layer
        if cur_layer.type() != QgsMapLayer.VectorLayer:
            problem = 'Selected layer is not a vector layer'
            QMessageBox.information(None, "Invalid target layer:", problem)
            return False

        #Ensure it's a polygon layer
        if cur_layer.geometryType() != QGis.Polygon:
            problem = 'Selected layer is not a polygon vector layer'
            QMessageBox.information(None, "Invalid target layer:", problem)
            return False

        # Ensure it's editable
        if not cur_layer.isEditable():
            problem = 'Selected layer is not editable'
            QMessageBox.information(None, "Invalid target layer:", problem)
            return False

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            #"""
            #A function for working with ellipses
            #"""
            import math
            import sys
            def draw_ellipse(min_diam=150, maj_diam=250, angle_deg=45):
                #"""
                #
                #Adds an ellipse to the current layer
                #
                #:param iface:       A QgsInterface object
                #:param min_diam:     Minor ellipse axis diameter (float, map units)
                #:param maj_diam:     Major ellipse axis diameter (float, map units)
                #:param angle_deg:   Angle of rotation (float, degrees, clockwise)
                #:return:
                #"""

                # Draw the ellipse around 0, 0
                vert_count = 100
                coords = []
                for i in range(vert_count):
                    angle = i * 2 * math.pi / vert_count
                    x = (min_diam/2) * math.cos(angle)
                    y = (maj_diam/2) * math.sin(angle)
                    coords.append( QgsPoint(x, y) )
                coords.append( QgsPoint(x, y) )

                # Make a geometry from the points
                ellipse_geom = QgsGeometry().fromPolygon( [coords] )
                ellipse_geom.rotate( angle_deg, QgsPoint(0,0) )

                # Get the canvas centroid position
                # Translate (shift) the new geometry to that location
                canvas_center = self.iface.mapCanvas().center()
                ellipse_geom.translate( canvas_center.x(),
                                        canvas_center.y())

                # Create and add the new feature
                new_f = QgsFeature()
                new_f.setGeometry( ellipse_geom )
                cur_layer.dataProvider().addFeatures( [ new_f ] )

                cur_layer.updateExtents()
                self.iface.mapCanvas().refresh()

                return True

            #Validate ellipse dimensions entered by user and call the ellipse function if dimensions are valid
            if self.dlg.txtMinDiameter.text().replace('.','',1).isdigit() and self.dlg.txtMajDiameter.text().replace('.','',1).isdigit() and self.dlg.txtRotation.text().replace('.','',1).isdigit():
                draw_ellipse(float(self.dlg.txtMinDiameter.text()), float(self.dlg.txtMajDiameter.text()), float(self.dlg.txtRotation.text()))
            else:
                QMessageBox.information(None, "Invalid ellipse dimensions:", "Please enter valid ellipse dimensions")