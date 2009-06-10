<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/Trajectories/data/point">
        <Placemark xmlns="http://www.opengis.net/kml/2.2">
            <description>
                <item name="Height" type="Double">
                    <xsl:value-of select="height" />
                </item>
            </description>
            <Point>
                <coordinates>
                    <xsl:value-of select="longitude" />
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="latitude" />
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="height" />
                </coordinates>
            </Point>
        </Placemark>
    </xsl:template>
    <xsl:template match="/Trajectories">
        <kml xmlns="http://www.opengis.net/kml/2.2">
            <xsl:apply-templates select="/Trajectories/data/point" />
        </kml>
    </xsl:template>
</xsl:stylesheet>
