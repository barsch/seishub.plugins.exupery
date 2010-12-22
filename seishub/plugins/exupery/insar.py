# -*- coding: utf-8 -*-
"""
Exupery - WP2 - InSAR resources.

Contact:
 * Xiaoying Cong (xiao.cong@dlr.de)
"""

from lxml.etree import Element, SubElement as Sub
from obspy.core.utcdatetime import UTCDateTime
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex, registerSchema, \
    registerStylesheet
from seishub.core.packages.interfaces import IResourceType, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import Table, sql
import os


class InSARResourceType(Component):
    """
    InSAR resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'insar'

    registerSchema('xsd' + os.sep + 'insar.xsd', 'XMLSchema')
    registerStylesheet('xslt' + os.sep + 'insar_displacement_metadata.xslt',
                       'metadata.displacement')
    registerStylesheet('xslt' + os.sep + 'insar_interferogram_metadata.xslt',
                       'metadata.interferogram')
    registerStylesheet('xslt' + os.sep + 'insar_differential_metadata.xslt',
                       'metadata.differential')

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
                  '/InSAR/files/file/local_path[../@id="coh_phase_image"]',
                  'text')
    registerIndex('satellite', '/InSAR/satellite', 'text')


class _InSARGeoTIFFMapperBase(object):
    """
    A base mapper class where other InSAR mapper may inherit from.
    """
    implements(IMapper)

    def process_GET(self, request):
        tab = Table('/exupery/insar', request.env.db.metadata, autoload=True)
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
                   tab.c['satellite'], tab.c[self.type_id]]
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
            Sub(s, 'satellite').text = i['satellite']
            Sub(s, 'url').text = 'local://' + i[self.type_id]
        return toString(xml)


class InSARAbsDPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR AbsDPhase GeoTiff files.
    """
    type_id = 'local_path_image_absdphase'
    mapping_url = '/exupery/wp2/insar/absdphase/geotiff'


class InSARDPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR DPhase GeoTiff files.
    """
    type_id = 'local_path_image_dphase'
    mapping_url = '/exupery/wp2/insar/dphase/geotiff'


class InSARPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR Phase GeoTiff files.
    """
    type_id = 'local_path_image_phase'
    mapping_url = '/exupery/wp2/insar/phase/geotiff'


class InSARCoherenceGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR Coherence GeoTiff files.
    """
    type_id = 'local_path_image_coherence'
    mapping_url = '/exupery/wp2/insar/coherence/geotiff'


class InSARAmplitudeGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR Amplitude GeoTiff files.
    """
    type_id = 'local_path_image_amplitude'
    mapping_url = '/exupery/wp2/insar/amplitude/geotiff'


class InSARCohAbsDPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR AbsDPhase GeoTiff files.
    """
    type_id = 'local_path_image_coh_absdphase'
    mapping_url = '/exupery/wp2/insar/cohabsdphase/geotiff'


class InSARCohDPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR DPhase GeoTiff files.
    """
    type_id = 'local_path_image_coh_dphase'
    mapping_url = '/exupery/wp2/insar/cohdphase/geotiff'


class InSARCohPhaseGeoTIFFMapper(Component, _InSARGeoTIFFMapperBase):
    """
    Returns a list of filtered InSAR Phase GeoTiff files.
    """
    type_id = 'local_path_image_coh_phase'
    mapping_url = '/exupery/wp2/insar/cohphase/geotiff'
