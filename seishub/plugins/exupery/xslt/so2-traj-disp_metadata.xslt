<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/Trajectories">
        <metadata>
            <item title="Software">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="software" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Latitude [°]">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="latitude/value" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Longitude [°]">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="longitude/value" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Number of Trajectories">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="number_of_trajectories" />
                    </xsl:attribute>
                </text>
            </item>
        </metadata>
    </xsl:template>
</xsl:stylesheet>
