# -*- coding: utf-8 -*-
"""
Exupery - WP3 - Seismic resources.

Contact:
 * 
"""

from lxml.etree import Element, SubElement as Sub
from seishub.core.core import Component, implements
from seishub.core.db import util
from seishub.core.packages.interfaces import ISQLView, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import sql
from obspy.db.db import WaveformChannel, Base
from seishub.core.xmldb.defaults import document_tab, document_meta_tab


class SeismicStationSQLView(Component):
    """
    Seismic station distribution layer.
    """
    implements(ISQLView)

    view_id = 'gis_seismic-station'

    def createView(self):
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes(package_id='seismology',
                                           resourcetype_id='station')

        filter = ['network_id', 'station_id', 'location_id', 'channel_id',
                  'latitude', 'longitude', 'start_datetime', 'end_datetime',
                  'quality']
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


class SeismicStationActivitySQLView(Component):
    """
    Seismic station activity layer.
    """
    implements(ISQLView)

    view_id = 'gis_seismic-station-activity'

    def createView(self):
        # make sure the relevant database tables exist!
        metadata = Base.metadata
        metadata.create_all(self.db.engine, checkfirst=True)
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes(package_id='seismology',
                                           resourcetype_id='station')

        filter = ['network_id', 'location_id', 'station_id', 'channel_id',
                  'latitude', 'longitude', 'start_datetime', 'end_datetime']
        xmlindex_list = [x for x in xmlindex_list if x.label in filter]
        if not xmlindex_list:
            return
        # build up query
        query, joins = catalog._createIndexView(xmlindex_list, compact=True)

        options = [
            sql.functions.max(WaveformChannel.endtime).label("latest_activity"),
            # XXX: not UTC!!!!
            (sql.func.now() - sql.functions.max(WaveformChannel.endtime)).label("latency"),
            (sql.literal_column("end_datetime.keyval") == None).label("active"),
            sql.func.random().label("random"),
            sql.func.GeomFromText(
                sql.text("'POINT(' || longitude.keyval || ' ' || " + \
                         "latitude.keyval || ')', 4326")).label('geom')
        ]
        for option in options:
            query.append_column(option)
        oncl = WaveformChannel.network == sql.literal_column("network_id.keyval")
        oncl = sql.and_(oncl, WaveformChannel.station == sql.literal_column("station_id.keyval"))
        oncl = sql.and_(oncl, WaveformChannel.channel == sql.literal_column("channel_id.keyval"))
        oncl = sql.and_(oncl, sql.or_(
            WaveformChannel.location == sql.literal_column("location_id.keyval"),
            sql.and_(
                WaveformChannel.location == None,
                sql.literal_column("location_id.keyval") == None
            )))
        oncl = sql.and_(oncl, WaveformChannel.endtime > sql.literal_column("start_datetime.keyval"))
        oncl = sql.and_(oncl, sql.or_(
            WaveformChannel.endtime <= sql.literal_column("end_datetime.keyval"),
            sql.literal_column("end_datetime.keyval") == None
            ))

        #joins = joins.join("default_waveform_channels", onclause=oncl)
        query = query.select_from(joins).group_by(
            document_tab.c['id'],
            document_meta_tab.c['datetime'],
            sql.literal_column("station_id.keyval"),
            sql.literal_column("channel_id.keyval"),
            sql.literal_column("network_id.keyval"),
            sql.literal_column("location_id.keyval"),
            sql.literal_column("latitude.keyval"),
            sql.literal_column("longitude.keyval"),
            sql.literal_column("start_datetime.keyval"),
            sql.literal_column("end_datetime.keyval"))
        return util.compileStatement(query)


#class SeismicStationQualitySQLView(Component):
#    """
#    Seismic station quality layer.
#    """
#    implements(ISQLView)
#
#    view_id = 'gis_seismic-station-activity'
#
#    def createView(self):
#        # filter indexes
#        catalog = self.env.catalog.index_catalog
#        xmlindex_list = catalog.getIndexes('seismology', 'station')
#
#        filter = ['network_id', 'location_id', 'station_id', 'channel_id',
#                  'latitude', 'longitude', 'start_datetime', 'end_datetime']
#        xmlindex_list = [x for x in xmlindex_list if x.label in filter]
#        if not xmlindex_list:
#            return
#        # build up query
#        query, joins = catalog._createIndexView(xmlindex_list, compact=True)
#
#        options = [
#            sql.functions.max(miniseed_tab.c.end_datetime).label("latest_activity"),
#            (sql.func.now() - sql.functions.max(miniseed_tab.c.end_datetime)).label("latency"),
#            sql.func.random().label("random"),
#            sql.func.GeomFromText(
#                sql.text("'POINT(' || longitude.keyval || ' ' || " + \
#                         "latitude.keyval || ')', 4326")).label('geom')
#        ]
#        for option in options:
#            query.append_column(option)
#        oncl = miniseed_tab.c['network_id'] == sql.literal_column("network_id.keyval")
#        oncl = sql.and_(oncl, miniseed_tab.c['station_id'] == sql.literal_column("station_id.keyval"))
#        oncl = sql.and_(oncl, miniseed_tab.c['channel_id'] == sql.literal_column("channel_id.keyval"))
#        oncl = sql.and_(oncl, sql.or_(
#            miniseed_tab.c['location_id'] == sql.literal_column("location_id.keyval"),
#            sql.and_(
#                miniseed_tab.c['location_id'] == None,
#                sql.literal_column("location_id.keyval") == None
#            )))
#        oncl = sql.and_(oncl, miniseed_tab.c['end_datetime'] > sql.literal_column("start_datetime.keyval"))
#        oncl = sql.and_(oncl, sql.or_(
#            miniseed_tab.c['end_datetime'] <= sql.literal_column("end_datetime.keyval"),
#            sql.literal_column("end_datetime.keyval") == None
#            ))
#
#
#        joins = joins.join(miniseed_tab, onclause=oncl)
#        query = query.select_from(joins).group_by(
#            document_tab.c.id,
#            sql.literal_column("station_id.keyval"),
#            sql.literal_column("channel_id.keyval"),
#            sql.literal_column("network_id.keyval"),
#            sql.literal_column("location_id.keyval"),
#            sql.literal_column("latitude.keyval"),
#            sql.literal_column("longitude.keyval"),
#            sql.literal_column("start_datetime.keyval"),
#            sql.literal_column("end_datetime.keyval"))
#        return util.compileStatement(query)


class SeismicEventSQLView(Component):
    """
    Creates SQL View for seismic events.
    """
    implements(ISQLView)

    view_id = 'gis_seismic-event'

    def createView(self):
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes(package_id='seismology',
                                           resourcetype_id='event')
        filter = ['datetime', 'latitude', 'longitude', 'depth',
                  'magnitude', 'magnitude_type', 'event_type', 'np1_strike',
                  'np1_dip', 'np1_rake', 'mt_mrr', 'mt_mtt', 'mt_mpp',
                  'mt_mrt', 'mt_mrp', 'mt_mtp', 'localisation_method']
        xmlindex_list = [x for x in xmlindex_list if x.label in filter]
        if not xmlindex_list:
            return
        # build up query
        query, joins = catalog._createIndexView(xmlindex_list, compact=True)
        options = [
            sql.literal_column("datetime.keyval").label("end_datetime"),
            sql.literal_column("datetime.keyval").label("start_datetime"),
            sql.case(
                value=sql.literal_column("localisation_method.keyval"),
                whens={'manual': 'circle'},
                else_='square').label('gis_localisation_method'),
            sql.func.GeomFromText(
                sql.text("'POINT(' || longitude.keyval || ' ' || " + \
                         "latitude.keyval || ')', 4326")).label('geom')
        ]
        for option in options:
            query.append_column(option)
        query = query.select_from(joins)
        return util.compileStatement(query)


class BeachballMapper(Component):
    """
    Returns a beachball image for the given parameters.
    """
    implements(IMapper)

    mapping_url = '/exupery/wp3/seismic/event/beachball'

    def process_GET(self, request):
        from obspy.imaging.beachball import Beachball
        # parse input arguments
        try:
            fm = request.args0.get('fm', '235, 80, 35')
            size = int(request.args0.get('size', 100))
            alpha = float(request.args0.get('alpha', 0.8))
            linewidth = float(request.args0.get('linewidth', 2))
            # try to parse fm
            if fm.count(',') == 2:
                fm = fm.split(',')
                fm = [float(fm[0]), float(fm[1]), float(fm[2])]
            elif fm.count(',') == 5:
                fm = fm.split(',')
                fm = [float(fm[0]), float(fm[1]), float(fm[2]),
                      float(fm[3]), float(fm[4]), float(fm[5])]
            else:
                return ''
        except:
            return ''
        if alpha < 0 or alpha > 1:
            alpha = 1
        if linewidth < 0 or linewidth > 10:
            linewidth = 2
        if size < 100 or size > 1000:
            size = 100
        # generate correct header
        request.setHeader('content-type', 'image/svg+xml; charset=UTF-8')
        # create beachball
        return Beachball(fm, size, format='svg', alpha=alpha,
                         linewidth=linewidth)


class SeismicEventTypeMapper(Component):
    """
    Returns a list of seismic event types over a certain time span.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp3/seismic/event/eventtype'

    def process_GET(self, request):
        # parse input arguments
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['vid'] = request.args0.get('volcano_id', '')
        args['start'] = request.args0.get('start_datetime', 'NOW()')
        args['end'] = request.args0.get('end_datetime', 'NOW()')
        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
            SELECT event_type, count(event_type) AS event_count
            FROM "/seismology/event"
            WHERE datetime >= :start
            AND datetime <= :end
            GROUP BY event_type;
        """)
        try:
            result = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for res in result:
            if not res.event_type:
                continue
            s = Sub(xml, "eventcount", type=res.event_type)
            s.text = str(res.event_count)
        return toString(xml)
