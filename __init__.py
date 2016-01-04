# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Ellipse
                                 A QGIS plugin
 Create ellipse based on minor and major radius widths and a rotation angle
                             -------------------
        begin                : 2015-12-15
        copyright            : (C) 2015 by Script: Pete Wells (Lutra Consulting); Plugin: Ali Moyle (Ecotricity)
        email                : ali.moyle@ecotricity.co.uk
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Ellipse class from file Ellipse.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .GIS41_01_Ellipse import Ellipse
    return Ellipse(iface)
