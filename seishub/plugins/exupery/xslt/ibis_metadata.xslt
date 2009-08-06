<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/GBSAR_IBIS">
        <metadata>
            <item title="Starttime of Master Image">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="image_information/master_image/start_time" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Starttime of Slave Image">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="image_information/slave_image/start_time" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="IBIS Station Lat [°]">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station/coords/latitude/value" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="IBIS Station Lon [°]">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station/coords/latitude/value" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="IBIS Station H [m]">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="station/coords/height/value" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Temporal Baseline [min]">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="image_information/temporal_baseline div 60" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Spatial Baseline [m]">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="image_information/spatial_baseline" />
                    </xsl:attribute>
                </text>
            </item>
        </metadata>
    </xsl:template>
</xsl:stylesheet>