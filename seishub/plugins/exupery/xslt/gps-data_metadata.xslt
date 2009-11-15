<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output encoding="utf-8" indent="yes" media-type="text/xml" method="xml" />
  <xsl:template match="/GBSAR_GPS">
    <metadata>
      <item title="Station ID">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="station/name" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Date/Time">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="datetime/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Date/Time (Epoch 0)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="station/coords_epoch0/datetime" />
          </xsl:attribute>
        </text>
      </item>
      <item title="abs. Δ Latitude (m)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="data/absolute_displacement/dlat_m/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="abs. Δ Longitude (m)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="data/absolute_displacement/dlon_m/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="abs. Δ Height (m)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="data/absolute_displacement/dh_m/value" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Air Pressure (hPa)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="meteorology/air_pressure_hPa" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Air Humidity (%)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="meteorology/air_humidity_percent" />
          </xsl:attribute>
        </text>
      </item>
      <item title="Air Temperature (°C)">
        <text>
          <xsl:attribute name="text">
            <xsl:value-of select="meteorology/air_temperature_degC" />
          </xsl:attribute>
        </text>
      </item>
    </metadata>
  </xsl:template>
</xsl:stylesheet>
