# -*- coding: utf-8 -*-
"""
Exupery - WP2 - SO2 resources.

Contact:
 * Pieter Valks (pieter.valks@dlr.de)
 * Thilo Erbertseder (thilo.erbertseder@dlr.de)
 * Cordelia Märker (cordelia.maerker@dlr.de)

GIS Layer:
(1) GOME2 SO2 concentrations (GeoTIFF)
 * Styles: Opaque, Semitransparent
 * Filters: time range, volcano id
(2) Hypothetical volcanic trajectories (KML)
 * Styles: ?
 * Filters: time range, volcano id
(3) Plume dispersion probability (GeoTIFF)
 * Styles: Opaque, Semitransparent
 * Filters: time range, volcano id 
"""

from lxml.etree import Element, SubElement as Sub
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerSchema, registerIndex, \
    registerStylesheet
from seishub.core.packages.interfaces import IMapper, IResourceType
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import sql
import os


class SO2GOME2ResourceType(Component):
    """
    SO2 GOME2 resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'so2-gome2'

    registerSchema('xsd' + os.sep + 'so2-gome2.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'so2-gome2_metadata.xslt', 'metadata')
    registerIndex('project_id', '/SO2/@project_id', 'text')
    registerIndex('volcano_id', '/SO2/@volcano_id', 'text')
    registerIndex('start_datetime', '/SO2/start_datetime/value', 'datetime')
    registerIndex('end_datetime', '/SO2/end_datetime/value', 'datetime')
    registerIndex('upperleft_latitude',
                  '/SO2/range_upperleft/latitude/value', 'float')
    registerIndex('upperleft_longitude',
                  '/SO2/range_upperleft/longitude/value', 'float')
    registerIndex('lowerright_latitude',
                  '/SO2/range_lowerright/latitude/value', 'float')
    registerIndex('lowerright_longitude',
                  '/SO2/range_lowerright/longitude/value', 'float')
    registerIndex('max_SO2_value', '/SO2/max_SO2_value', 'float')
    registerIndex('SO2_range1',
                  '/SO2/measurements_with_SO2_between_0.5DU_and_1DU',
                  'numeric')
    registerIndex('SO2_range2',
                  '/SO2/measurements_with_SO2_between_1DU_and_1.5DU',
                  'numeric')
    registerIndex('SO2_range3',
                  '/SO2/measurements_with_SO2_above_1.5DU', 'numeric')
    registerIndex('alert_level', '/SO2/SO2_alert_level', 'numeric')
    registerIndex('local_path_image',
                  '/SO2/files/file/local_path[../@id="GOME2_SO2 image"]',
                  'text')
    registerIndex('local_path_grid',
                  '/SO2/files/file/local_path[../@id="GOME2_SO2 data"]',
                  'text')


class SO2TrajectoriesResourceType(Component):
    """
    SO2 Trajectories resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'so2-traj-disp'

    registerSchema('xsd' + os.sep + 'so2-traj-disp.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'so2-traj-disp_kml.xslt', 'kml')
    registerStylesheet('xslt' + os.sep + 'so2-traj-disp_metadata.xslt',
                       'metadata')
    registerIndex('project_id', '/Trajectories/@project_id', 'text')
    registerIndex('volcano_id', '/Trajectories/@volcano_id', 'text')
    registerIndex('start_datetime', '/Trajectories/start_datetime/value',
                  'datetime')
    registerIndex('end_datetime', '/Trajectories/end_datetime/value',
                  'datetime')
    registerIndex('upperleft_latitude',
                  '/Trajectories/range_upperleft/latitude/value', 'float')
    registerIndex('upperleft_longitude',
                  '/Trajectories/range_upperleft/longitude/value', 'float')
    registerIndex('lowerright_latitude',
                  '/Trajectories/range_lowerright/latitude/value', 'float')
    registerIndex('lowerright_longitude',
                  '/Trajectories/range_lowerright/longitude/value', 'float')
    registerIndex('latitude', '/Trajectories/latitude/value', 'float')
    registerIndex('longitude', '/Trajectories/longitude/value', 'float')
    registerIndex('local_path_image',
                  '/Trajectories/files/file/local_path[../@format="GeoTIFF"]',
                  'text')


class SO2GOME2GeoTIFFMapper(Component):
    """
    Returns a list of filtered SO2 GOME2 GeoTiff files.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp2/so2/gome2/geotiff'

    def process_GET(self, request):
        # parse input arguments
        pid = request.args0.get('project_id', '')
        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
            SELECT
                document_id, 
                start_datetime, 
                end_datetime, 
                local_path_image 
            FROM "/exupery/so2-gome2"
            WHERE local_path_image IS NOT NULL
            AND project_id = :pid
        """)
        try:
            result = self.env.db.query(query, pid=pid)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'start_datetime').text = (i.start_datetime).isoformat()
            Sub(s, 'end_datetime').text = (i.end_datetime).isoformat()
            Sub(s, 'url').text = 'local://' + i.local_path_image
        return toString(xml)


class SO2GOME2GridMapper(Component):
    """
    Returns a list of filtered SO2 GOME2 Grid files.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp2/so2/gome2/grid'

    def process_GET(self, request):
        # parse input arguments
        pid = request.args0.get('project_id', '')
        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
            SELECT
                document_id, 
                start_datetime, 
                end_datetime, 
                local_path_grid 
            FROM "/exupery/so2-gome2"
            WHERE local_path_grid IS NOT NULL
            AND project_id = :pid
        """)
        try:
            result = self.env.db.query(query, pid=pid)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'start_datetime').text = (i.start_datetime).isoformat()
            Sub(s, 'end_datetime').text = (i.end_datetime).isoformat()
            Sub(s, 'url').text = 'local://' + i.local_path_grid
        return toString(xml)


class SO2TrajectoriesKMLMapper(Component):
    """
    Returns a list of filtered SO2 Trajectories KML files.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp2/so2/trajectories/kml'

    def process_GET(self, request):
        # parse input arguments
        pid = request.args0.get('project_id', '')
        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
            SELECT
                document_id, 
                start_datetime, 
                end_datetime
            FROM "/exupery/so2-traj-disp"
            WHERE project_id = :pid
        """)
        try:
            result = self.env.db.query(query, pid=pid)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'start_datetime').text = (i.start_datetime).isoformat()
            Sub(s, 'end_datetime').text = (i.end_datetime).isoformat()
            Sub(s, 'url').text = "seishub://exupery/gis/kml?document_id=%s" % \
                (str(i.document_id))
        return toString(xml)


class SO2DispersionGeoTIFFMapper(Component):
    """
    Returns a list of filtered SO2 Dispersion GeoTiff files.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp2/so2/dispersion/geotiff'

    def process_GET(self, request):
        # parse input arguments
        pid = request.args0.get('project_id', '')
        # generate XML result
        xml = Element("query")
        # build up and execute query
        query = sql.text("""
            SELECT
                document_id, 
                start_datetime, 
                end_datetime, 
                local_path_image 
            FROM "/exupery/so2-traj-disp"
            WHERE local_path_image IS NOT NULL
            AND project_id = :pid
        """)
        try:
            result = self.env.db.query(query, pid=pid)
        except:
            return toString(xml)

        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'start_datetime').text = (i.start_datetime).isoformat()
            Sub(s, 'end_datetime').text = (i.end_datetime).isoformat()
            Sub(s, 'url').text = 'local://' + i.local_path_image
        return toString(xml)
