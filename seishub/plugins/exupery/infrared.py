# -*- coding: utf-8 -*-
"""
Exupery - WP2 - Infrared resources.

Contact:
 * Klemen Zaksek (klemen.zaksek@zmaw.de)

GIS Layer:
(1) Infrared image (GeoTIFF)
 * Styles:  Opaque, Semitransparent
 * Filters: time range, volcano id, satellite(?)
(2) Hotspots (PostGIS)
 * Styles:  temperature, hotspot area, radiant flux, emission rate
 * Filters: time range, volcano id, radiant flux, satellite(?), 
            satellite zenith angle 
"""

from lxml.etree import Element, SubElement as Sub
from seishub.core import Component, implements
from seishub.db import util
from seishub.packages.installer import registerSchema, registerIndex
from seishub.packages.interfaces import IResourceType, ISQLView, IMapper
from seishub.util.xmlwrapper import toString
from sqlalchemy import sql
import os


class InfraredResourceType(Component):
    """
    Infrared resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'infrared'

    registerSchema('xsd' + os.sep + 'infrared.xsd', 'XMLSchema')

    registerIndex('project_id', '/infrared/@project_id', 'text')
    registerIndex('volcano_id', '/infrared/@volcano_id', 'text')
    registerIndex('start_datetime',
                  '/infrared/start_datetime/value', 'datetime')
    registerIndex('end_datetime', '/infrared/end_datetime/value', 'datetime')
    registerIndex('upperleft_latitude',
                  '/infrared/range_upperleft/latitude/value', 'float')
    registerIndex('upperleft_longitude',
                  '/infrared/range_upperleft/longitude/value', 'float')
    registerIndex('lowerright_latitude',
                  '/infrared/range_lowerright/latitude/value', 'float')
    registerIndex('lowerright_longitude',
                  '/infrared/range_lowerright/longitude/value', 'float')
    registerIndex('satellite', '/infrared/processing/satellite', 'text')
    registerIndex('satellite_zenith_deg',
                  '/infrared/processing/satellite_zenith_deg', 'float')
    registerIndex('alert_level',
                  '/infrared/hotspots_overview/thermal_anomaly_alert_level',
                  'numeric')
    registerIndex('radiant_flux_overview',
                  '/infrared/hotspots_overview/radiant_flux_MW', 'float')
    registerIndex('latitude_hotspot',
                  '/infrared/hotspots/hotspot#latitude/value', 'float')
    registerIndex('longitude_hotspot',
                  '/infrared/hotspots/hotspot#longitude/value', 'float')
    registerIndex('radiant_flux_hotspot',
                  '/infrared/hotspots/hotspot#radiant_flux_MW', 'float')
    registerIndex('temperature_hotspot',
                  '/infrared/hotspots/hotspot#temperature_of_thermal_anomaly_K',
                  'float')
    registerIndex('area_hotspot',
                  '/infrared/hotspots/hotspot#area_of_thermal_anomaly_ha',
                  'float')
    registerIndex('effusion_hotspot',
                  '/infrared/hotspots/hotspot#effusion_rate_m3_s', 'float')
    registerIndex('local_path_image',
                  '/infrared/files/file/local_path[../@id="IRimage_8bit"]',
                  'text')
    registerIndex('local_path_image_16bit',
                  '/infrared/files/file/local_path[../@id="IRimage_16bit"]',
                  'text')


class InfraredHotspotSQLView(Component):
    """
    Creates SQL View for Infrared Hotspot distribution.
    """
    implements(ISQLView)

    view_id = 'gis_infrared_hotspot'

    def createView(self):
        # filter indexes
        catalog = self.env.catalog.index_catalog
        xmlindex_list = catalog.getIndexes('exupery', 'infrared')

        filter = ['project_id', 'volcano_id', 'latitude_hotspot',
                  'longitude_hotspot', 'start_datetime', 'end_datetime',
                  'radiant_flux_hotspot', 'temperature_hotspot',
                  'area_hotspot', 'effusion_hotspot']
        xmlindex_list = [x for x in xmlindex_list if x.label in filter]
        if not xmlindex_list:
            return
        # build up query
        query, joins = catalog._createIndexView(xmlindex_list, compact=True)

        options = [
            sql.func.GeomFromText(
                sql.text("'POINT(' || longitude_hotspot.keyval || ' ' || " + \
                         "latitude_hotspot.keyval || ')', 4326")).label('geom')
        ]
        for option in options:
            query.append_column(option)
        query = query.select_from(joins)
        return util.compileStatement(query)


class InfraredGeoTIFFMapper(Component):
    """
    Returns a list of filtered Infrared GeoTiff files.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp2/infrared/geotiff'

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
           FROM "/exupery/infrared"
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
            Sub(s, 'url16').text = 'local://' + i.local_path_image_16bit
        return toString(xml)
