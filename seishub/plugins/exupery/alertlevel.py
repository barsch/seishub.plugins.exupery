# -*- coding: utf-8 -*-
"""
Exupery - WP3 - Alert Level resources.

Contact:
 * Moritz Beyreuther (beyreuth@geophysik.uni-muenchen.de)

GIS Layer:
 The Alert level (a single integer value in the XML file) refers to a whole 
 region instead of a single point. Therefore it should not appear in the layer 
 tree, but be available separately (e.g. in the GIS menu). The alert level 
 should be displayed as a color (green, yellow, red). Additional information 
 (e.g. confidence) is available in the XML file. It may be displayed in an 
 info box. URL to display an image (preferably created "on the fly" by an 
 external program) in a new window.
"""

from lxml.etree import Element, SubElement as Sub
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex, registerStylesheet
from seishub.core.packages.interfaces import IResourceType, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import sql
import os


class AlertLevelResourceType(Component):
    """
    Alert Level resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'alert-level'

    registerStylesheet('xslt' + os.sep + 'alert-level_metadata.xslt',
                       'metadata')
    registerStylesheet('xslt' + os.sep + 'alert-level_smile.xslt',
                       'smile')
    registerIndex('project_id', '/alert_level/@project_id', 'text')
    registerIndex('volcano_id', '/alert_level/@volcano_id', 'text')
    registerIndex('datetime', '/alert_level/datetime/value', 'datetime')
    registerIndex('level', '/alert_level/alert/level', 'integer')
    registerIndex('probability', '/alert_level/alert/probability', 'float')
    registerIndex('comment', '/alert_level/alert/comment', 'text')


class AlertLevelMapper(Component):
    """
    Returns a list of alert levels.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/alert'

    def process_GET(self, request):
        # parse input arguments
        pid = request.args0.get('project_id', '')

        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
           SELECT DISTINCT 
               document_id, 
               volcano_id, 
               datetime,
               level, 
               comment
           FROM "/exupery/alert-level"
           WHERE project_id = :pid
        """)
        try:
            result = self.env.db.query(query, pid=pid)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'volcano_id').text = i.volcano_id
            Sub(s, 'datetime').text = (i.datetime).isoformat()
            Sub(s, 'level').text = str(i.level)
            Sub(s, 'comment').text = i.comment
        return toString(xml)


class S024AlertMapper(Component):
    """
    Returns a list of SO2_range3 values in a given time range.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/so24alert'

    def process_GET(self, request):
        # parse input arguments
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['start'] = request.args0.get('start_datetime', '')
        args['end'] = request.args0.get('end_datetime', '')

        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
           SELECT DISTINCT
               document_id,
               SO2_range3
           FROM "/exupery/so2-gome2"
           WHERE project_id = :pid 
           AND start_datetime > :start 
           AND end_datetime < :end
        """)
        try:
            result = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'SO2_range3').text = str(i.SO2_range3)
        return toString(xml)

class Event4AlertMapper(Component):
    """
    Returns a list of Events depending on type
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/event4alert'

    def process_GET(self, request):
        # parse input arguments
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['start'] = request.args0.get('start_datetime', '')
        args['end'] = request.args0.get('end_datetime', '')
        args['event'] = request.args0.get('event', '')

        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
           SELECT DISTINCT
               document_id,
               event_type
           FROM "/seismology/event"
           WHERE event_type = :event
           AND datetime > :start
           AND datetime < :end
        """)
        #XXX project_id is missing in seismic events!!!
        # AND project_id = :pid
        try:
            result = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'event_type').text = str(i.event_type)
        return toString(xml)


class Infrared4AlertMapper(Component):
    """
    Returns a list of temperature hotspot values in a given time range.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/infrared4alert'

    def process_GET(self, request):
        # parse input arguments
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['start'] = request.args0.get('start_datetime', '')
        args['end'] = request.args0.get('end_datetime', '')

        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
           SELECT DISTINCT
               document_id ,
               temperature_hotspot
           FROM "/exupery/infrared"
           WHERE project_id = :pid 
           AND start_datetime > :start 
           AND end_datetime < :end
        """)
        try:
            result = self.env.db.query(query, **args)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'temperature_hotspot').text = str(i.temperature_hotspot)
        return toString(xml)


class GPS4AlertMapper(Component):
    """
    Returns a dictionary of absolute height values per station. 
    
    Therefore several SQL queries are necessary. First query all available 
    station IDs. Then for each station retrieve the absolute height and
    confidence for the latest measurement and for the measurements a 
    specified time range before and commit this result. (???)
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp3/alert-level/gps4alert'

    def process_GET(self, request):
        # parse input arguments
        args = {}
        args['pid'] = request.args0.get('project_id', '')
        args['start'] = request.args0.get('start_datetime', '')
        args['end'] = request.args0.get('end_datetime', '')

        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
           SELECT DISTINCT 
               document_id,
               station_id 
           FROM "/exupery/gps-station"
           WHERE project_id = :pid 
           AND start_datetime < :start 
           AND end_datetime > :end
        """)
        try:
            available_stations = self.env.db.query(query, **args)
        except:
            return toString(xml)

        # extracts the absolute height and height confidence for each station
        for s in available_stations:
            # MONITOR
            sid = s.station_id
            query = sql.text("""
               SELECT DISTINCT 
                   document_id,
                   abs_height,
                   abs_height_conf,
                   start_datetime
               FROM "/exupery/gps-data"
               WHERE project_id = :pid
               AND station_id = :sid
               ORDER BY start_datetime ASC
               LIMIT 1
            """)
            try:
                monitor = self.env.db.query(query, sid=sid, **args)
            except:
                print "Exception Monitor"
                continue

            #BASELINE
            query = sql.text("""
               SELECT DISTINCT 
                   document_id,
                   abs_height,
                   abs_height_conf,
                   start_datetime
               FROM "/exupery/gps-data"
               WHERE project_id = :pid
               AND station_id = :sid
               ORDER BY start_datetime DESC
               LIMIT 1
            """)
            try:
                baseline = self.env.db.query(query, sid=sid, **args)
            except:
                print "Exception BASELINE"
                continue
            # We only get this far if we have a valid baseline and monitor 
            s = Sub(xml, "station", id=str(sid),
                    document_id=str(s.document_id))
            for j in monitor:
                t = Sub(s, "monitor", document_id=str(j.document_id))
                Sub(t, 'start_datetime').text = (j.start_datetime).isoformat()
                Sub(t, 'abs_height').text = str(j.abs_height)
                Sub(t, 'abs_height_conf').text = str(j.abs_height_conf)
            for k in baseline:
                u = Sub(s, "baseline", document_id=str(k.document_id))
                Sub(u, 'start_datetime').text = (k.start_datetime).isoformat()
                Sub(u, 'abs_height').text = str(k.abs_height)
                Sub(u, 'abs_height_conf').text = str(k.abs_height_conf)
        return toString(xml)
