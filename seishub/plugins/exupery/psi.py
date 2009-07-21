# -*- coding: utf-8 -*-
"""
Exupery - WP2 - PSI resources.

Contact:
 * Xiaoying Cong (Xiao.Cong@dlr.de)
"""

from lxml.etree import Element, SubElement as Sub
from seishub.core import Component, implements
from seishub.packages.installer import registerIndex, registerSchema
from seishub.packages.interfaces import IResourceType, IMapper
from seishub.util.xmlwrapper import toString
from sqlalchemy import sql
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
                local_path_kml
            FROM "/exupery/psi"
            WHERE local_path_kml IS NOT NULL
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
            Sub(s, 'url').text = 'local://' + i.local_path_kml
        return toString(xml)
