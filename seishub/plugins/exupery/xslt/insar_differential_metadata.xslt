<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output encoding="utf-8" indent="yes" media-type="text/xml" method="xml" />
  <xsl:template match="/InSAR">
    <metadata>
      <item title="Effective Baseline">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of
              select="effective_baseline" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Orig. Azimuth resolution/Pixel">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="original_azimuth_resolution_per_pixel" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Orig. Range resolution/Pixel">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="original_range_resolution_per_pixel" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Looks of Azimuth">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="looks_of_azimuth" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Looks of Range">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="looks_of_range"
            />
          </xsl:attribute>
        </text>
      </item>
      <item title="External DEM">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="external_DEM"
            />
          </xsl:attribute>
        </text>
      </item>
    </metadata>
  </xsl:template>
</xsl:stylesheet>
