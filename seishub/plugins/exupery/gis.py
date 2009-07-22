# -*- coding: utf-8 -*-
"""
Exupery - GIS resources.
"""

from seishub.core import Component, implements
from seishub.packages.installer import registerIndex
from seishub.packages.interfaces import IMapper, IResourceType
from sqlalchemy import sql


METADATA_RESOURCE_LINK = """
    <item title="XML Resource">
      <link href="%s/xml%s" text="%s" />
    </item>
  </metadata>
"""

METADATA_ALLOWED_VIEWS = {
    'gis_seismic-station': 0,
    'gis_gps-data': 0, 
    'gis_gps-station': 0, 
    'gis_infrared-hotspot': 0,
    'gis_seismic-event': 1,
    'gis_minidoas-station': 0
}

METADATA_EMPTY_XML = """
  <metadata>
  </metadata>
"""

# stations
# input: discrete time stamp (start==end) 
# data: time range with possible open end
SQL_QUERY_0 = """
    SELECT document_id
    FROM "%s"
    WHERE Distance(GeomFromText('POINT(:x :y)', 4326), geom) <= :d
    AND start_datetime <= :now
    AND (end_datetime >= :now OR end_datetime IS NULL)
    ORDER BY 
        Distance(GeomFromText('POINT(:x :y)', 4326), geom),
        start_datetime DESC
    LIMIT 1
"""

# events
# input: time range
# data: discrete value
SQL_QUERY_1 = """
    SELECT document_id
    FROM "%s"
    WHERE Distance(GeomFromText('POINT(:x :y)', 4326), geom) <= :d
    AND datetime >= :start
    AND datetime <= :end
    ORDER BY 
        Distance(GeomFromText('POINT(:x :y)', 4326), geom),
        datetime DESC
    LIMIT 1
"""



class GISSessionResourceType(Component):
    """
    GIS Session resource type.
    """
    implements(IResourceType)
    
    package_id = 'exupery'
    resourcetype_id = 'gis-session'
    
    registerIndex('global', '/save/@global', 'boolean')
    registerIndex('project_id', '/save/@project_id', 'text')
    registerIndex('user_id', '/save/@user', 'text')


class GISMetadataMapper(Component):
    """
    Returns GIS Metadata for various GIS layers.
    """
    implements(IMapper)
    
    package_id = 'exupery'
    mapping_url = '/exupery/gis/metadata'
    
    
    def process_GET(self, request):
        # parse input arguments
        try:
            document_id = int(request.args0.get('document_id', 0))
            # process further arguments if no document_id is given
            if not document_id:
                args = {}
                #project_id = request.args0.get('project_id', '')
                args['x'] = float(request.args0.get('longitude', 0))
                args['y'] = float(request.args0.get('latitude', 0))
                args['d'] = float(request.args0.get('delta', 0))
                view_id = request.args0.get('view', 'gis_seismic-station')
                args['start'] = request.args0.get('start_datetime', 'NOW()')
                args['end'] = request.args0.get('end_datetime', 'NOW()')
                if args['end']==args['start']:
                    args['now'] = args['start']
        except:
            return ""
        
        if not document_id:
            # only known view_ids are allowed
            if view_id not in METADATA_ALLOWED_VIEWS.keys():
                return "<metadata />"
            type = METADATA_ALLOWED_VIEWS.get(view_id)
            # build up and execute query
            if type==0:
                query = sql.text(SQL_QUERY_0 % view_id)
            else:
                query = sql.text(SQL_QUERY_1 % view_id)
            try:
                result = self.env.db.query(query, **args).fetchone()
                if not result or len(result)!=1:
                    return "<metadata />"
            except:
                # nothing found
                return "<metadata />"
            # now we got a document ID
            document_id=result[0]
        
        # fetch document from catalog
        res = self.env.catalog.getResource(document_id=document_id)
        data = res.document.data
        # fetch a XSLT document object
        reg = request.env.registry
        xslt = reg.stylesheets.get(
            package_id = res.package.package_id,
            resourcetype_id = res.resourcetype.resourcetype_id,
            type = 'metadata'
        )
        if not xslt or not len(xslt):
            xmldoc = METADATA_EMPTY_XML
        else:
            xslt = xslt[0]
            xmldoc = xslt.transform(data)
        # append resource a XML to metadata
        res_link = METADATA_RESOURCE_LINK % (self.env.getRestUrl(), str(res),
                                             res.name)
        xmldoc = xmldoc.replace('</metadata>', str(res_link))
        return str(xmldoc)


class GISKMLMapper(Component):
    """
    Returns a KML document from a given document_id.
    """
    implements(IMapper)
    
    package_id = 'exupery'
    mapping_url = '/exupery/gis/kml'
    
    
    def process_GET(self, request):
        # parse input arguments
        try:
            document_id = int(request.args0.get('document_id', 0))
        except:
            return ""
        
        if not document_id:
            return "<kml />"
        
        # fetch document from catalog
        res = self.env.catalog.getResource(document_id=document_id)
        data = res.document.data
        # fetch a XSLT document object
        reg = request.env.registry
        xslt = reg.stylesheets.get(
            package_id = res.package.package_id,
            resourcetype_id = res.resourcetype.resourcetype_id,
            type = 'kml'
        )
        if not xslt or not len(xslt):
            return "<kml />"
        xslt = xslt[0]
        xmldoc = xslt.transform(data)
        return str(xmldoc)


class GISSessionMapper(Component):
    """
    Returns a list of current GIS Session objects.
    """
    implements(IMapper)
    
    package_id = 'exupery'
    mapping_url = '/exupery/gis/session'
    
    def process_GET(self, request):
        # generate a plain text file
        request.setHeader('content-type', 'text/plain; charset=UTF-8')
        
        # parse input arguments
        uid = request.args0.get('user', '')
        gid = request.args0.get('global', 'true')
        pid = request.args0.get('project_id', '')
        
        if gid=='true':
            gid = True
            uid = ""
        else:
            gid = False
            if not uid:
                return ""
        
        # build up query
        SQL_QUERY = """
            SELECT document_id 
            FROM "/exupery/gis-session"
            WHERE global = :gid 
            AND project_id = :pid
        """
        if uid:
            SQL_QUERY += " AND user_id = :uid"
        query = sql.text(SQL_QUERY)
        # execute query
        try:
            result = self.env.db.query(query, gid=gid, pid=pid, 
                                       uid=uid).fetchall()
        except:
            return ""
        
        # format output
        out = ''
        for res in result:
            res = self.env.catalog.getResource(document_id=res[0])
            data = res.document.data
            # get only save tag
            data = data.split('>', 1)[0]
            out+=data + ' />\n'
        return out


class GISUserAuthMapper(Component):
    """
    Checks if given user and encoded password are correct.
    """
    implements(IMapper)
    
    package_id = 'exupery'
    mapping_url = '/exupery/gis/auth'
    
    def process_GET(self, request):
        # generate a plain text file
        request.setHeader('content-type', 'text/plain; charset=UTF-8')
        
        # process args
        user = request.args0.get('user', '')
        hash = request.args0.get('hash', '')
        # check password
        try:
            if self.env.auth.checkPasswordHash(user, hash):
                return "True"
            else:
                return "WRONG PASSWORD"
        except:
            return "WRONG USER"
