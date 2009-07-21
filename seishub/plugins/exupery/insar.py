# -*- coding: utf-8 -*-
"""
Exupery - WP2 - InSAR resources.

Contact:
 * Xiaoying Cong (xiao.cong@dlr.de)
"""

from lxml.etree import Element, SubElement as Sub
from seishub.core import Component, implements
from seishub.packages.installer import registerIndex, registerSchema
from seishub.packages.interfaces import IResourceType, IMapper
from seishub.util.xmlwrapper import toString
from sqlalchemy import sql
import os


class InSARResourceType(Component):
    """
    InSAR resource type.
    """
    implements(IResourceType)
    
    package_id = 'exupery'
    resourcetype_id = 'insar'
    
    registerSchema('xsd' + os.sep + 'insar.xsd', 'XMLSchema')
    
    registerIndex('project_id', '/InSAR/@project_id', 'text')
    registerIndex('volcano_id', '/InSAR/@volcano_id', 'text')
    registerIndex('start_datetime', '/InSAR/start_datetime/value', 'date')
    registerIndex('end_datetime', '/InSAR/end_datetime/value', 'date')
    registerIndex('upperleft_latitude', 
                  '/InSAR/range_upperleft/latitude/value', 'float')
    registerIndex('upperleft_longitude', 
                  '/InSAR/range_upperleft/longitude/value', 'float')
    registerIndex('lowerright_latitude',
                  '/InSAR/range_lowerright/latitude/value', 'float')
    registerIndex('lowerright_longitude', 
                  '/InSAR/range_lowerright/longitude/value', 'float')
    registerIndex('local_path_image_absdphase', 
                  '/InSAR/files/file/local_path[../@id="absdphase_image"]', 
                  'text')
    registerIndex('local_path_image_dphase', 
                  '/InSAR/files/file/local_path[../@id="dphase_image"]', 
                  'text')
    registerIndex('local_path_image_phase', 
                  '/InSAR/files/file/local_path[../@id="phase_image"]', 'text')
    registerIndex('local_path_image_coherence', 
                  '/InSAR/files/file/local_path[../@id="coherence_image"]', 
                  'text')
    registerIndex('local_path_image_amplitude', 
                  '/InSAR/files/file/local_path[../@id="amplitude_image"]', 
                  'text')
    registerIndex('local_path_image_coh_absdphase', 
                  '/InSAR/files/file/local_path[../@id="coh_absdphase_image"]', 
                  'text')
    registerIndex('local_path_image_coh_dphase', 
                  '/InSAR/files/file/local_path[../@id="coh_dphase_image"]', 
                  'text')
    registerIndex('local_path_image_coh_phase', 
                  '/InSAR/files/file/local_path[../@id="coh_phase_image"]', 'text')


class _InSARGeoTIFFMapperBase(object):
    """
    A base mapper class where other InSAR mapper may inherit from.
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
           FROM "/exupery/insar"
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


class InSARAbsDPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR AbsDPhase GeoTiff files.
    """
    type = 'local_path_image_absdphase'
    mapping_url = '/exupery/wp2/insar/absdphase/geotiff'


class InSARDPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR DPhase GeoTiff files.
    """
    type = 'local_path_image_dphase'
    mapping_url = '/exupery/wp2/insar/dphase/geotiff'


class InSARPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR Phase GeoTiff files.
    """
    type = 'local_path_image_phase'
    mapping_url = '/exupery/wp2/insar/phase/geotiff'


class InSARCoherenceGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR Coherence GeoTiff files.
    """
    type = 'local_path_image_coherence'
    mapping_url = '/exupery/wp2/insar/coherence/geotiff'


class InSARAmplitudeGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR Amplitude GeoTiff files.
    """
    type = 'local_path_image_amplitude'
    mapping_url = '/exupery/wp2/insar/amplitude/geotiff'
