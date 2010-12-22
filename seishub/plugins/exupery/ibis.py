# -*- coding: utf-8 -*-
"""
Exupery - WP1 - IBIS resources.

Contact:
 * Gwen Läufer (laeufer@ipg.tu-darmstadt.de)
 * Sabine Roedelsperger

GIS Layer:
(1) IBIS Displacement image (GeoTIFF)
 * Styles: Opaque, Semitransparent
 * Filters: time range
(2) IBIS Coherence image (GeoTIFF)
 * Styles: Opaque, Semitransparent
 * Filters: time range
"""

from lxml.etree import Element, SubElement as Sub
from obspy.core import UTCDateTime
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex, registerSchema, \
    registerStylesheet
from seishub.core.packages.interfaces import IResourceType, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import Table, sql
import os


class IBISResourceType(Component):
    """
    IBIS resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'ibis'

    registerSchema('xsd' + os.sep + 'ibis.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'ibis_metadata.xslt',
        'metadata')
    registerStylesheet('xslt' + os.sep + 'ibis_displacement_metadata.xslt',
        'metadata.displacement')

    registerIndex('project_id', '/GBSAR_IBIS/@project_id', 'text')
    registerIndex('volcano_id', '/GBSAR_IBIS/@volcano_id', 'text')
    registerIndex('start_datetime',
        '/GBSAR_IBIS/image_information/master_image/start_datetime/value',
        'datetime')
    registerIndex('end_datetime',
        '/GBSAR_IBIS/image_information/slave_image/start_datetime/value',
        'datetime')
    registerIndex('upperleft_latitude',
        '/GBSAR_IBIS/image_information/range_upperleft/latitude/value',
        'float')
    registerIndex('upperleft_longitude',
        '/GBSAR_IBIS/image_information/range_upperleft/longitude/value',
        'float')
    registerIndex('lowerright_latitude',
        '/GBSAR_IBIS/image_information/range_lowerright/latitude/value',
        'float')
    registerIndex('lowerright_longitude',
        '/GBSAR_IBIS/image_information/range_lowerright/longitude/value',
        'float')
    registerIndex('local_path_image_quality',
        '/GBSAR_IBIS/files/file/local_path[../@id="coherence"]', 'text')
    registerIndex('local_path_image_displacement',
        '/GBSAR_IBIS/files/file/local_path[../@id="losdisplacement"]', 'text')
    registerIndex('local_path_image_phase',
        '/GBSAR_IBIS/files/file/local_path[../@id="phase"]', 'text')


class _IBISGeoTIFFMapperBase(object):
    """
    A base mapper class where other IBIS mapper may inherit from.
    """
    implements(IMapper)

    def process_GET(self, request):
        tab = Table('/exupery/ibis', request.env.db.metadata, autoload=True)
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
                   tab.c[self.type_id]]
        query = sql.select(columns, oncl, limit=limit, distinct=True,
                           offset=offset, order_by=tab.c['start_datetime'])
        # process arguments
        try:
            temp = request.args0.get('project_id')
            if temp:
                query = query.where(tab.c['project_id'] == temp)
        except:
            pass
        try:
            temp = request.args0.get('start_datetime')
            if temp:
                temp = UTCDateTime(temp)
                query = query.where(tab.c['start_datetime'] >= temp.datetime)
        except:
            pass
        try:
            temp = request.args0.get('end_datetime')
            if temp:
                temp = UTCDateTime(temp)
                query = query.where(tab.c['end_datetime'] < temp.datetime)
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
            Sub(s, 'url').text = 'local://' + i[self.type_id]
        return toString(xml)


class IBISQualityGeoTIFFMapper(Component, _IBISGeoTIFFMapperBase):
    """
    Returns a list of filtered IBIS Quality GeoTiff files.
    """
    type_id = 'local_path_image_quality'
    mapping_url = '/exupery/wp1/ibis/quality/geotiff'


class IBISLosDisplacementGeoTIFFMapper(Component, _IBISGeoTIFFMapperBase):
    """
    Returns a list of filtered IBIS LosDisplacement GeoTiff files.
    """
    type_id = 'local_path_image_displacement'
    mapping_url = '/exupery/wp1/ibis/losdisplacement/geotiff'


class IBISPhaseGeoTIFFMapper(Component, _IBISGeoTIFFMapperBase):
    """
    Returns a list of filtered IBIS Phase GeoTiff files.
    """
    type_id = 'local_path_image_phase'
    mapping_url = '/exupery/wp1/ibis/phase/geotiff'
