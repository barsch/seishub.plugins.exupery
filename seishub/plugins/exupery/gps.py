# -*- coding: utf-8 -*-
"""
Exupery - WP1 - GPS resources.

Contact:
 * Gwen Läufer (laeufer@ipg.tu-darmstadt.de)

GIS Layer:
(1) GPS Station network (PostGIS)
 * Color: active (green), not active (red)
 * Symbol: dependent of receiver type (trimble/ublox)
 * Filters: time range
(2) GPS Data (PostGIS)
 * Style: absolute and relative displacements as vectors + confidence ellipse
 * Filters: time range

URL to external program to display time series
"""

from lxml.etree import Element, SubElement as Sub
from obspy.core import UTCDateTime
from seishub.core.core import Component, implements
from seishub.core.db import util
from seishub.core.packages.installer import registerIndex, registerSchema, \
    registerStylesheet
from seishub.core.packages.interfaces import IResourceType, ISQLView, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import Table, sql
import os


class GPSStationResourceType(Component):
    """
    GPS Station resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'gps-station'

    registerSchema('xsd' + os.sep + 'gps-station.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'gps-station_metadata.xslt',
        'metadata')
    registerIndex('project_id', '/GBSAR_GPS_Station/@project_id', 'text')
    registerIndex('volcano_id', '/GBSAR_GPS_Station/@volcano_id', 'text')
    registerIndex('receiver_type',
        '/GBSAR_GPS_Station/instruments/gps_receiver/type', 'text')
    registerIndex('start_datetime', '/GBSAR_GPS_Station/start_datetime/value',
        'datetime')
    registerIndex('end_datetime', '/GBSAR_GPS_Station/end_datetime/value',
        'datetime')
    registerIndex('station_id', '/GBSAR_GPS_Station/station/name', 'text')
    registerIndex('latitude',
        '/GBSAR_GPS_Station/station/coords_epoch0/latitude/value', 'float')
    registerIndex('longitude',
        '/GBSAR_GPS_Station/station/coords_epoch0/longitude/value', 'float')


class GPSDataResourceType(Component):
    """
    GPS Data resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'gps-data'

    registerSchema('xsd' + os.sep + 'gps-data.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'gps-data_metadata.xslt', 'metadata')
    registerStylesheet('xslt' + os.sep + 'gps-data_displacement.xslt',
                       'displacement')
    registerIndex('project_id', '/GBSAR_GPS/@project_id', 'text')
    registerIndex('volcano_id', '/GBSAR_GPS/@volcano_id', 'text')
    registerIndex('start_datetime',
        '/GBSAR_GPS/data/epoch/start_datetime/value', 'datetime')
    registerIndex('end_datetime', '/GBSAR_GPS/data/epoch/end_datetime/value',
        'datetime')
    registerIndex('station_id', '/GBSAR_GPS/station/name', 'text')
    registerIndex('epoch0_latitude',
        '/GBSAR_GPS/station/coords_epoch0/latitude/value', 'float')
    registerIndex('epoch0_longitude',
        '/GBSAR_GPS/station/coords_epoch0/longitude/value', 'float')
    registerIndex('epoch0_height',
        '/GBSAR_GPS/station/coords_epoch0/height/value', 'float')
    registerIndex('abs_latitude',
        '/GBSAR_GPS/data/absolute_displacement/dlat_m/value', 'float')
    registerIndex('abs_longitude',
        '/GBSAR_GPS/data/absolute_displacement/dlon_m/value', 'float')
    registerIndex('abs_height',
        '/GBSAR_GPS/data/absolute_displacement/dh_m/value', 'float')
    registerIndex('abs_height_conf',
        '/GBSAR_GPS/data/absolute_displacement/dh_m/conf', 'float')
    registerIndex('abs_conf_ellipse_a',
        '/GBSAR_GPS/data/absolute_displacement/conf_ellipse/a', 'float')
    registerIndex('abs_conf_ellipse_b',
        '/GBSAR_GPS/data/absolute_displacement/conf_ellipse/b', 'float')
    registerIndex('abs_conf_azimuth_a',
        '/GBSAR_GPS/data/absolute_displacement/conf_ellipse/azimuth_a',
        'float')
    registerIndex('rel_latitude',
        '/GBSAR_GPS/data/relative_displacement/dlat_m/value', 'float')
    registerIndex('rel_longitude',
        '/GBSAR_GPS/data/relative_displacement/dlon_m/value', 'float')
    registerIndex('rel_height',
        '/GBSAR_GPS/data/relative_displacement/dh_m/value', 'float')
    registerIndex('rel_height_conf',
        '/GBSAR_GPS/data/relative_displacement/dh_m/conf', 'float')
    registerIndex('rel_conf_ellipse_a',
        '/GBSAR_GPS/data/relative_displacement/conf_ellipse/a', 'float')
    registerIndex('rel_conf_ellipse_b',
        '/GBSAR_GPS/data/relative_displacement/conf_ellipse/b', 'float')
    registerIndex('rel_conf_azimuth_a',
        '/GBSAR_GPS/data/relative_displacement/conf_ellipse/azimuth_a',
        'float')


class GPSStationSQLView(Component):
    """
    Creates SQL View for GPS station distribution.
    """
    implements(ISQLView)

    view_id = 'gis_gps-station'

    def createView(self):
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes(package_id='exupery',
                                           resourcetype_id='gps-station')
        filter = ['project_id', 'volcano_id', 'station_id', 'receiver_type',
                  'start_datetime', 'end_datetime', 'longitude', 'latitude']
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


class GPSDataSQLView(Component):
    """
    Creates SQL View for GPS Data components.
    """
    implements(ISQLView)

    view_id = 'gis_gps-data'

    def createView(self):
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes(package_id='exupery',
                                           resourcetype_id='gps-data')
        filter = ['project_id', 'volcano_id', 'station_id',
                  'start_datetime', 'end_datetime', 'epoch0_longitude',
                  'epoch0_latitude']
        xmlindex_list = [x for x in xmlindex_list if x.label in filter]
        if not xmlindex_list:
            return
        # build up query
        query, joins = catalog._createIndexView(xmlindex_list, compact=True)
        options = [
            sql.literal_column("epoch0_latitude.keyval").label("latitude"),
            sql.literal_column("epoch0_longitude.keyval").label("longitude"),
            sql.func.GeomFromText(
                sql.text("'POINT(' || epoch0_longitude.keyval || ' ' || " + \
                         "epoch0_latitude.keyval || ')', 4326")).label('geom')
        ]
        for option in options:
            query.append_column(option)
        query = query.select_from(joins)
        return util.compileStatement(query)


class GPSStationActivityMapper(Component):
    """
    Returns a last datetime entry for a given GPS Station ID.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp1/gps/station/activity'

    def process_GET(self, request):
        # parse input arguments
        args = {}
        args['sid'] = request.args0.get('station_id', '')
        args['end'] = request.args0.get('datetime', 'NOW()')

        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
            SELECT document_id, end_datetime
            FROM "gis_gps-data"
            WHERE station_id = :sid
            AND end_datetime <= :end
            ORDER BY end_datetime DESC
            LIMIT 1;
        """)
        try:
            result = self.env.db.query(query, **args).fetchone()
            if not result:
                return toString(xml)
        except:
            return toString(xml)

        s = Sub(xml, "resource", document_id=str(result.document_id))
        Sub(s, 'station_id').text = args['sid']
        Sub(s, 'last_datetime').text = (result.end_datetime).isoformat()
        return toString(xml)


class GPSDisplacementMapper(Component):
    """
    Returns a XML with displacement information for a given document_id.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp1/gps/data/displacement'

    def process_GET(self, request):
        # parse input arguments
        try:
            document_id = int(request.args0.get('document_id'))
        except:
            return "<query />"
        # fetch document from catalog
        res = self.env.catalog.getResource(document_id=document_id)
        data = res.document.data
        # fetch a XSLT document object
        reg = request.env.registry
        xslt = reg.stylesheets.get(
            package_id=res.package.package_id,
            resourcetype_id=res.resourcetype.resourcetype_id,
            type='displacement'
        )
        if not xslt or not len(xslt):
            return "<query />"
        xslt = xslt[0]
        xmldoc = xslt.transform(data)
        return str(xmldoc)


class GPSTimeSeriesMapper(Component):
    """
    Returns a filtered list of GPS data for displaying as time series.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp1/gps/data/timeseries'

    def process_GET(self, request):
        # parse input arguments
        args = {}
        args['sid'] = request.args0.get('station_id', '')
        args['start'] = request.args0.get('start_datetime', 'NOW()')
        args['end'] = request.args0.get('end_datetime', 'NOW()')

        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
            SELECT *
            FROM "/exupery/gps-data"
            WHERE station_id = :sid
            AND start_datetime >= :start
            AND end_datetime <= :end;
        """)
        try:
            result = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for res in result:
            s = Sub(xml, "resource", document_id=str(res.document_id))
            for id, value in res.items():
                if id in ['start_datetime', 'end_datetime']:
                    Sub(s, id).text = (value).isoformat()
                else:
                    Sub(s, id).text = str(value)
        return toString(xml)


class GPSTimeSeriesMapper2(Component):
    """
    Returns a filtered list of GPS data for displaying as time series.
    Creates also a second SQL View for GPS Data components.
    """
    implements(IMapper, ISQLView)

    package_id = 'exupery'
    mapping_url = '/exupery/wp1/gps/data/timeseries2'
    view_id = 'gis_gps-absdata'

    def process_GET(self, request):
        tab = Table('gis_gps-absdata', request.env.db.metadata,
                    autoload=True)
        # fetch arguments
        try:
            limit = int(request.args0.get('limit'))
            offset = int(request.args0.get('offset', 0))
        except:
            limit = None
            offset = 0
        oncl = sql.and_(1 == 1)
        # build up query
        query = sql.select([tab], oncl, limit=limit, distinct=True,
                           offset=offset, order_by=tab.c['start_datetime'])
        # process arguments
        try:
            temp = request.args0.get('station_id', '')
            query = query.where(tab.c['station_id'] == temp)
        except:
            pass
        try:
            temp = UTCDateTime(request.args0.get('start_datetime'))
        except:
            temp = UTCDateTime()
        query = query.where(tab.c['start_datetime'] >= temp.datetime)
        try:
            temp = UTCDateTime(request.args0.get('end_datetime'))
        except:
            temp = UTCDateTime()
        query = query.where(tab.c['end_datetime'] <= temp.datetime)
        # generate XML result
        xml = Element("query")
        # execute query
        try:
            results = request.env.db.query(query)
        except:
            return toString(xml)
        for res in results:
            s = Sub(xml, "resource", document_id=str(res.document_id))
            for id, value in res.items():
                if id in ['start_datetime', 'end_datetime']:
                    Sub(s, id).text = (value).isoformat()
                else:
                    Sub(s, id).text = str(value)
        return toString(xml)

    def createView(self):
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes(package_id='exupery',
                                           resourcetype_id='gps-data')
        filter = ['station_id', 'start_datetime', 'end_datetime',
                  'abs_conf_azimuth_a', 'abs_conf_ellipse_b',
                  'abs_conf_ellipse_a', 'abs_height_conf', 'abs_height',
                  'abs_longitude', 'abs_latitude']
        xmlindex_list = [x for x in xmlindex_list if x.label in filter]
        if not xmlindex_list:
            return
        # build up query
        query, joins = catalog._createIndexView(xmlindex_list, compact=True)
        query = query.select_from(joins)
        return util.compileStatement(query)
