<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output encoding="utf-8" indent="yes" media-type="text/xml" method="xml" />
  <xsl:template match="/Modis">
    <metadata>
      <item title="Satellite orbit 1">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of
              select="swath_aqua/swath_1/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Satellite orbit 2">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of
              select="swath_aqua/swath_2/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Satellite orbit 3">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of
              select="swath_aqua/swath_3/value" />
          </xsl:attribute>
        </text>
      </item>
    </metadata>
  </xsl:template>
</xsl:stylesheet>
