# -*- coding: utf-8 -*-
"""
Exupery - WP1 - MiniDOAS resources.

Contact:
 * Thor Hansteen (thansteen@ifm-geomar.de)

GIS Layer:
(1) MiniDOAS Station network (PostGIS)
 * Styles: quality
 * Filters: time range, ?

URL to external program to display time series
"""

from seishub.core.core import Component, implements
from seishub.core.db import util
from seishub.core.packages.installer import registerIndex, registerStylesheet, \
    registerSchema
from seishub.core.packages.interfaces import IResourceType, ISQLView
from sqlalchemy import sql
import os


class MiniDOASStationResourceType(Component):
    """
    MiniDOAS Station resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'minidoas-station'

    registerStylesheet('xslt' + os.sep + 'minidoas-station_metadata.xslt',
                       'metadata')
    registerIndex('project_id', '/MiniDOAS_Station/@project_id', 'text')
    registerIndex('volcano_id', '/MiniDOAS_Station/@volcano_id', 'text')
    registerIndex('start_datetime', '/MiniDOAS_Station/start_datetime/value',
                  'datetime')
    registerIndex('end_datetime', '/MiniDOAS_Station/end_datetime/value',
                  'datetime')
    registerIndex('station_id', '/MiniDOAS_Station/name', 'text')
    registerIndex('latitude', '/MiniDOAS_Station/latitude/value', 'float')
    registerIndex('longitude', '/MiniDOAS_Station/longitude/value', 'float')


class MiniDOASDataResourceType(Component):
    """
    MiniDOAS data resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'minidoas-data'

    registerSchema('xsd' + os.sep + 'minidoas-data.xsd', 'XMLSchema')
    registerIndex('project_id', '/MiniDOAS_data/@project_id', 'text')
    registerIndex('volcano_id', '/MiniDOAS_data/@volcano_id', 'text')
    registerIndex('start_datetime', '/MiniDOAS_data/start_datetime/value',
                  'datetime')
    registerIndex('end_datetime', '/MiniDOAS_data/end_datetime/value',
                  'datetime')
    registerIndex('flux', '/MiniDOAS_data/flux', 'float')


class MiniDOASStationLayer(Component):
    """
    Creates a MiniDOAS Station distribution layer.
    """
    implements(ISQLView)

    view_id = 'gis_minidoas-station'

    def createView(self):
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes(package_id='exupery',
                                           resourcetype_id='minidoas-station')

        filter = ['project_id', 'volcano_id', 'station_id', 'latitude',
                  'longitude', 'start_datetime', 'end_datetime']
        xmlindex_list = [x for x in xmlindex_list if x.label in filter]
        if not xmlindex_list:
            return
        # build up query
        query, joins = catalog._createIndexView(xmlindex_list, compact=True)

        options = [
            sql.func.random().label("random"),
            sql.func.GeomFromText(
                sql.text("'POINT(' || longitude.keyval || ' ' || " + \
                         "latitude.keyval || ')', 4326")).label('geom')
        ]
        for option in options:
            query.append_column(option)
        query = query.select_from(joins)
        return util.compileStatement(query)
