<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/SO2">
        <metadata>
            <item title="Number of measurements">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="number_of_measurements" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Latitude of max SO2">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="latitude_of_max_SO2" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Longitude of max SO2">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="longitude_of_max_SO2" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Time of max SO2">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="time_of_max_SO2" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="SO2 &lt; 0.5 DU">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="measurements_with_SO2_under_0.5DU" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="SO2 0.5 - 1.0 DU">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="measurements_with_SO2_between_0.5DU_and_1DU"
                         />
                    </xsl:attribute>
                </text>
            </item>
            <item title="SO2 1.0 - 1.5 DU">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="measurements_with_SO2_between_1DU_and_1.5DU"
                         />
                    </xsl:attribute>
                </text>
            </item>
            <item title="SO2 &gt; 1.5 DU">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of
                            select="measurements_with_SO2_above_1.5DU" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="SO2 Alert Level">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="SO2_alert_level" />
                    </xsl:attribute>
                </text>
            </item>
        </metadata>
    </xsl:template>
</xsl:stylesheet>
