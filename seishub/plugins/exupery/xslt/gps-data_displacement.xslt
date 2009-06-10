<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/GBSAR_GPS">
        <query>
            <xsl:copy-of select="data/absolute_displacement" />
            <xsl:copy-of select="data/relative_displacement" />
        </query>
    </xsl:template>
</xsl:stylesheet>
