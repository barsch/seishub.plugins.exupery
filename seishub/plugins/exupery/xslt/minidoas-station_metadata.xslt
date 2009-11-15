<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output encoding="utf-8" indent="yes" media-type="text/xml" method="xml" />
  <xsl:template match="/MiniDOAS_Station">
    <metadata>
      <item title="Station ID">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="name" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Latitude (°)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="latitude/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Longitude (°)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="longitude/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Height (m)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="height/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Spectrometer">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="spectrometer" />
            <xsl:text> (</xsl:text>
            <xsl:value-of select="serial" />
            <xsl:text>)</xsl:text>
          </xsl:attribute>
        </text>
      </item>
    </metadata>
  </xsl:template>
</xsl:stylesheet>
