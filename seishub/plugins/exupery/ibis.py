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
from seishub.core import Component, implements
from seishub.packages.installer import registerIndex, registerSchema
from seishub.packages.interfaces import IResourceType, IMapper
from seishub.util.xmlwrapper import toString
from sqlalchemy import sql
import os


class IBISResourceType(Component):
    """
    IBIS resource type.
    """
    implements(IResourceType)
    
    package_id = 'exupery'
    resourcetype_id = 'ibis'
    
    registerSchema('xsd' + os.sep + 'ibis.xsd', 'XMLSchema')
    
    registerIndex('project_id', '/GBSAR_IBIS/@project_id', 'text')
    registerIndex('volcano_id', '/GBSAR_IBIS/@volcano_id', 'text')
    registerIndex('start_datetime', '/GBSAR_IBIS/image_information/master_image/start_datetime/value', 'datetime')
    registerIndex('end_datetime', '/GBSAR_IBIS/image_information/slave_image/start_datetime/value', 'datetime')
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
               %s
           FROM "/exupery/ibis"
           WHERE project_id = :pid 
           AND %s IS NOT NULL
        """ % (self.type, self.type))
        try:
            result = self.env.db.query(query, pid=pid)
        except:
            return toString(xml)
        
        for i in result:
            s = Sub(xml, "resource", document_id=str(i.document_id))
            Sub(s, 'start_datetime').text = (i.start_datetime).isoformat()
            Sub(s, 'end_datetime').text = (i.end_datetime).isoformat()
            Sub(s, 'url').text = 'local://' + i[self.type]
        return toString(xml)

class IBISQualityGeoTIFFMapper(Component, _IBISGeoTIFFMapperBase):
    """
    Returns a list of filtered IBIS Quality GeoTiff files.
    """
    type = 'local_path_image_quality'
    mapping_url = '/exupery/wp1/ibis/quality/geotiff'
    

class IBISLosDisplacementGeoTIFFMapper(Component, _IBISGeoTIFFMapperBase):
    """
    Returns a list of filtered IBIS LosDisplacement GeoTiff files.
    """
    type = 'local_path_image_displacement'
    mapping_url = '/exupery/wp1/ibis/losdisplacement/geotiff'


class IBISPhaseGeoTIFFMapper(Component, _IBISGeoTIFFMapperBase):
    """
    Returns a list of filtered IBIS Phase GeoTiff files.
    """
    type = 'local_path_image_phase'
    mapping_url = '/exupery/wp1/ibis/phase/geotiff'