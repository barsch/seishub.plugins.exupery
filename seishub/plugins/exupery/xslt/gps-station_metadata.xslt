<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/GBSAR_GPS_Station">
        <metadata>
            <item title="Station ID">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="station/name" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Latitude (°)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station/coords_epoch0/latitude/value" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Longitude (°)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station/coords_epoch0/longitude/value" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Height (m)">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station/coords_epoch0/height/value" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="GPS Receiver">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="instruments/gps_receiver/type" />
                        <xsl:text> - </xsl:text>
                        <xsl:value-of select="instruments/gps_receiver/name" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="GPS Antenna">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="instruments/gps_antenna/type" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Mesh Node">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="instruments/meshnode/name" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Weather Station">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="instruments/weather_station/name"
                         />
                    </xsl:attribute>
                </text>
            </item>
        </metadata>
    </xsl:template>
</xsl:stylesheet>
