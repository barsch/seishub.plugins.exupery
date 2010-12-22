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
from seishub.core.core import Component, implements
from seishub.core.db import util
from seishub.core.packages.installer import registerIndex, registerSchema, \
    registerStylesheet
from seishub.core.packages.interfaces import IResourceType, ISQLView, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import sql, Table
import os


class InfraredResourceType(Component):
    """
    Infrared resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'infrared'

    registerSchema('xsd' + os.sep + 'infrared.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'infrared_hotspots_metadata.xslt',
                       'metadata')

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
    registerIndex('percentage_area_hotspot',
                  '/infrared/hotspots/hotspot#percentage_of_area_of_thermal_anomaly',
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
        xmlindex_list = catalog.getIndexes(package_id='exupery',
                                           resourcetype_id='infrared')

        filter = ['project_id', 'volcano_id', 'latitude_hotspot',
                  'longitude_hotspot', 'start_datetime', 'end_datetime',
                  'radiant_flux_hotspot', 'temperature_hotspot',
                  'area_hotspot', 'percentage_area_hotspot',
                  'effusion_hotspot']
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
        # don't show rows without hotspots
        query = query.where(sql.column('latitude_hotspot') != None)
        return util.compileStatement(query)


class InfraredGeoTIFFMapper(Component):
    """
    Returns a list of filtered Infrared GeoTiff files.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp2/infrared/geotiff'

    def process_GET(self, request):
        tab = Table('/exupery/infrared', request.env.db.metadata,
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
        columns = [tab.c['document_id'], tab.c['project_id'],
                   tab.c['start_datetime'], tab.c['end_datetime'],
                   tab.c['local_path_image'], tab.c['local_path_image_16bit']]
        query = sql.select(columns, oncl, limit=limit, distinct=True,
                           offset=offset, order_by=tab.c['start_datetime'])
        query = query.where(tab.c['local_path_image'] != None)
        # process arguments
        try:
            temp = request.args0.get('project_id', '')
            query = query.where(tab.c['project_id'] == temp)
        except:
            pass
        # generate XML result
        xml = Element("query")
        # execute query
        try:
            results = request.env.db.query(query)
        except:
            return toString(xml)
        for i in results:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            try:
                temp = i.start_datetime.isoformat()
            except:
                temp = ''
            Sub(s, 'start_datetime').text = temp
            try:
                temp = i.end_datetime.isoformat()
            except:
                temp = ''
            Sub(s, 'end_datetime').text = temp
            Sub(s, 'url').text = 'local://' + i.local_path_image
            if i.local_path_image_16bit:
                path = 'local://' + i.local_path_image_16bit
            else:
                path = ''
            Sub(s, 'url16').text = path
        return toString(xml)
