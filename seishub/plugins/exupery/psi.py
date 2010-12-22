# -*- coding: utf-8 -*-
"""
Exupery - WP2 - PSI resources.

Contact:
 * Xiaoying Cong (Xiao.Cong@dlr.de)
"""

from lxml.etree import Element, SubElement as Sub
from seishub.core.core import Component, implements
from seishub.core.packages.installer import registerIndex, registerSchema
from seishub.core.packages.interfaces import IResourceType, IMapper
from seishub.core.util.xmlwrapper import toString
from sqlalchemy import sql, Table
import os


class PSIResourceType(Component):
    """
    PSI resource type.
    """
    implements(IResourceType)

    package_id = 'exupery'
    resourcetype_id = 'psi'

    registerSchema('xsd' + os.sep + 'psi.xsd', 'XMLSchema')

    registerIndex('project_id', '/PSI/@project_id', 'text')
    registerIndex('volcano_id', '/PSI/@volcano_id', 'text')
    registerIndex('start_datetime', '/PSI/start_datetime/value', 'date')
    registerIndex('end_datetime', '/PSI/end_datetime/value', 'date')
    registerIndex('upperleft_latitude', '/PSI/range_upperleft/latitude/value',
                  'float')
    registerIndex('upperleft_longitude',
                  '/PSI/range_upperleft/longitude/value', 'float')
    registerIndex('lowerright_latitude',
                  '/PSI/range_lowerright/latitude/value', 'float')
    registerIndex('lowerright_longitude',
                  '/PSI/range_lowerright/longitude/value', 'float')
    registerIndex('local_path_kml',
                  '/PSI/files/file/local_path[../@id="PSI_Stack"]', 'text')


class PSIKMLMapper(Component):
    """
    Returns a list of filtered PSI KML files.
    """
    implements(IMapper)

    package_id = 'exupery'
    mapping_url = '/exupery/wp2/insar/psi/kml'

    def process_GET(self, request):
        tab = Table('/exupery/psi', request.env.db.metadata, autoload=True)
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
                   tab.c['volcano_id'], tab.c['start_datetime'],
                   tab.c['end_datetime'], tab.c['local_path_kml']]
        query = sql.select(columns, oncl, limit=limit, distinct=True,
                           offset=offset, order_by=tab.c['start_datetime'])
        # only with non empty local_path_kml
        query = query.where(tab.c['local_path_kml'] != None)
        # process arguments
        try:
            temp = request.args0.get('project_id')
            if temp:
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
                start = i.start_datetime.isoformat()
            except:
                start = ''
            try:
                end = i.end_datetime.isoformat()
            except:
                end = ''
            Sub(s, 'project_id').text = i['project_id']
            Sub(s, 'volcano_id').text = i['volcano_id']
            Sub(s, 'start_datetime').text = start
            Sub(s, 'end_datetime').text = end
            Sub(s, 'url').text = 'local://' + i.local_path_kml
        return toString(xml)
