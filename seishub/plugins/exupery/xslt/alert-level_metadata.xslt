<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet exclude-result-prefixes="xlink" version="1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output encoding="utf-8" indent="yes" media-type="text/xml"
        method="xml" />
    <xsl:template match="/alert_level">
        <metadata>
            <item title="Level">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="alert/level" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Probability">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="alert/probability" />
                    </xsl:attribute>
                </text>
            </item>
            <item title="Comment">
                <text>
                    <xsl:attribute name="text">
                        <xsl:value-of select="alert/comment" />
                    </xsl:attribute>
                </text>
            </item>
        </metadata>
    </xsl:template>
</xsl:stylesheet>
