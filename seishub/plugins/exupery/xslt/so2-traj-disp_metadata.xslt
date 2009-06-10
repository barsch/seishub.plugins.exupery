<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/Trajectories">
        <metadata>
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
