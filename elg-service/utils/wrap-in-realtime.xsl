<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <xsl:param name="gracefulTimeout" select="'5000'" />
  <xsl:param name="timeout" select="'10000'" />
  <xsl:param name="suppressExceptions" select="'false'" />

  <xsl:template match="@*|node()">
    <xsl:copy><xsl:apply-templates select="@*|node()"/></xsl:copy>
  </xsl:template>

  <xsl:template match="/*/application[resourceType != 'gate.creole.RealtimeCorpusController']" xml:space="preserve">
    <application class="gate.util.persistence.SerialAnalyserControllerPersistence">
      <prList class="gate.util.persistence.CollectionPersistence">
        <localList>
          <xsl:element name="{@class}">
            <xsl:apply-templates select="node()" />
          </xsl:element>
        </localList>
        <collectionType>java.util.ArrayList</collectionType>
      </prList>
      <resourceType>gate.creole.RealtimeCorpusController</resourceType>
      <resourceName><xsl:value-of select="resourceName" /> (RT)</resourceName>
      <initParams class="gate.util.persistence.MapPersistence">
        <mapType>gate.util.SimpleFeatureMapImpl</mapType>
        <localMap>
          <entry>
            <string>suppressExceptions</string>
            <boolean><xsl:value-of select="$suppressExceptions" /></boolean>
          </entry>
          <entry>
            <string>timeout</string>
            <long><xsl:value-of select="$timeout" /></long>
          </entry>
          <entry>
            <string>gracefulTimeout</string>
            <long><xsl:value-of select="$gracefulTimeout" /></long>
          </entry>
        </localMap>
      </initParams>
      <features class="gate.util.persistence.MapPersistence">
        <mapType>gate.util.SimpleFeatureMapImpl</mapType>
        <localMap/>
      </features>
    </application>
  </xsl:template>

</xsl:stylesheet>
