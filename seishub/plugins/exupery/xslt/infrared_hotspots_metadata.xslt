<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output encoding="utf-8" indent="yes" media-type="text/xml" method="xml" />
  <xsl:template match="/infrared">
    <metadata>
      <item title="Satellite">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of
              select="processing/satellite" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Satellite zenith angle (°)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of
              select="processing/satellite_zenith_deg" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Solar zenith angle (°)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="processing/solar_zenith_deg" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Satellite azimut (°)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="processing/satellite_azimuth_deg" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Solar azimut (°)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="processing/solar_azimuth_deg" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Cloud coverage (%)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="processing/cloud_coverage_percentage" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Sun glint angle (°)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="hotspots_overview/sun_glint_degrees"
             />
          </xsl:attribute>
        </text>
      </item>
      <item title="Background temperature (K)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="hotspots_overview/background_temperature_K"
            />
          </xsl:attribute>
        </text>
      </item>
      <item title="Emissivity in MIR spectra">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="processing/emissivity_MIR" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Emissivity in TIR spectra">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="processing/emissivity_TIR" />
          </xsl:attribute>
        </text>
      </item>
    </metadata>
  </xsl:template>
</xsl:stylesheet>
