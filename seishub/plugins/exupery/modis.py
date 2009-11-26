# -*- coding: utf-8 -*-
"""
Exupery - WP2 - Modis resources.

Contact:
 * Cordelia Maerker (Cordelia.Maerker@dlr.de)
"""

from lxml.etree import Element, SubElement as Sub
from obspy.core import UTCDateTime
from seishub.core import Component, implements
from seishub.packages.installer import registerIndex, registerStylesheet
from seishub.packages.interfaces import IResourceType, IMapper
from seishub.util.xmlwrapper import toString
from sqlalchemy import Table, sql
import os


class ModisResourceType(Component):
    """
    Modis resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'modis'

    registerStylesheet('xslt' + os.sep + 'modis_aqua_metadata.xslt',
        'metadata.aqua')
    registerStylesheet('xslt' + os.sep + 'modis_terra_metadata.xslt',
        'metadata.terra')
    registerIndex('project_id', '/Modis/@project_id', 'text')
    registerIndex('volcano_id', '/Modis/@volcano_id', 'text')
    registerIndex('datetime', '/Modis/time_of_creation', 'datetime')
    registerIndex('upperleft_latitude',
        '/Modis/range_upperleft/latitude/value', 'float')
    registerIndex('upperleft_longitude',
        '/Modis/range_upperleft/longitude/value', 'float')
    registerIndex('lowerright_latitude',
        '/Modis/range_lowerright/latitude/value', 'float')
    registerIndex('lowerright_longitude',
        '/Modis/range_lowerright/longitude/value', 'float')
    registerIndex('local_path_image_aqua',
        '/Modis/files/file/local_path[../@id="MODIS Aqua True Color image 250m"]',
        'text')
    registerIndex('local_path_image_terra',
        '/Modis/files/file/local_path[../@id="MODIS Terra True Color image 250m"]',
        'text')


class _ModisGeoTIFFMapperBase(object):
    """
    A base mapper class where other Modis mapper may inherit from.
    """
    implements(IMapper)

    def process_GET(self, request):
        tab = Table('/exupery/modis', request.env.db.metadata, autoload=True)
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
                   tab.c['volcano_id'], tab.c['datetime'], tab.c[self.type_id]]
        query = sql.select(columns, oncl, limit=limit, distinct=True,
                           offset=offset, order_by=tab.c['datetime'])
        # process arguments
        try:
            temp = request.args0.get('project_id')
            if temp:
                query = query.where(tab.c['project_id'] == temp)
        except:
            pass
        try:
            temp = request.args0.get('volcano_id')
            if temp:
                query = query.where(tab.c['volcano_id'] == temp)
        except:
            pass
        try:
            temp = request.args0.get('start_datetime')
            if temp:
                temp = UTCDateTime(temp)
                query = query.where(tab.c['datetime'] >= temp.datetime)
        except:
            pass
        try:
            temp = request.args0.get('end_datetime')
            if temp:
                temp = UTCDateTime(temp)
                query = query.where(tab.c['datetime'] <= temp.datetime)
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
                temp = i.datetime.isoformat()
            except:
                temp = ''
            Sub(s, 'project_id').text = i['project_id']
            Sub(s, 'volcano_id').text = i['volcano_id']
            Sub(s, 'datetime').text = temp
            Sub(s, 'url').text = 'local://' + i[self.type_id]
        return toString(xml)


class AquaGeoTIFFMapper(Component, _ModisGeoTIFFMapperBase):
    """
    Returns a list of filtered Aqua GeoTiff files.
    """
    type_id = 'local_path_image_aqua'
    mapping_url = '/exupery/wp2/modis/aqua/geotiff'


class TerraGeoTIFFMapper(Component, _ModisGeoTIFFMapperBase):
    """
    Returns a list of filtered Terra GeoTiff files.
    """
    type_id = 'local_path_image_terra'
    mapping_url = '/exupery/wp2/modis/terra/geotiff'
