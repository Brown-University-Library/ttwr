<xsl:stylesheet 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
  xmlns:xs="http://www.w3.org/2001/XMLSchema" 
  xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" 
  xmlns:TEI="http://www.tei-c.org/ns/1.0" 
  exclude-result-prefixes="xs xd" version="2.0">
<xd:doc scope="stylesheet">
<xd:desc>
<xd:p>
<xd:b>Created on:</xd:b>
Aug 19, 2011
</xd:p>
<xd:p>
<xd:b>Author:</xd:b>
elli
</xd:p>
<xd:p/>
</xd:desc>
</xd:doc>
<!--<xsl:output method="html" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN" encoding="utf-8" indent="yes"/>-->
<xsl:template match="/">
  <xsl:result-document href="#author_info" method="html">
  <xsl:apply-templates/>
</xsl:result-document>
</xsl:template>
<xsl:template match="TEI:teiHeader"/>
<xsl:template match="TEI:text/TEI:body">
<h2>
<xsl:apply-templates select="TEI:head/TEI:persName"/>
(
<xsl:apply-templates select="TEI:head/TEI:date"/>
)
</h2>
<xsl:apply-templates select="TEI:div/TEI:listPerson/TEI:person"/>
<xsl:apply-templates select="TEI:div[@type='history']"/>
<xsl:apply-templates select="TEI:div[@type='bibliography']"/>
<!--
 <p class="resp"><xsl:value-of select="//mads-note[@type='resp']" /></p> 
              need to match the person who wrote the bio. Info missing in XML right now. 
-->
</xsl:template>
<xsl:template match="TEI:person">
<h3>Variant Names</h3>
<ul>
<xsl:apply-templates select="TEI:persName[@type='variant']"/>
<xsl:if test="not(//TEI:persName[@type='variant'])">———</xsl:if>
</ul>
<h3>Dates</h3>
<xsl:apply-templates select="TEI:birth"/>
<xsl:if test="not(//TEI:birth)">———</xsl:if>
<xsl:apply-templates select="TEI:death"/>
<xsl:if test="not(//TEI:death)">———</xsl:if>
<h3>Occupation(s)</h3>
<ul>
<xsl:apply-templates select="TEI:occupation"/>
<xsl:if test="not(//TEI:occupation)">———</xsl:if>
</ul>
</xsl:template>
<xsl:template match="//TEI:persName[@type='variant']">
<li>
<span class="dark">
<xsl:apply-templates/>
</span>
</li>
</xsl:template>
<xsl:template match="//TEI:occupation">
<li>
<xsl:apply-templates/>
</li>
</xsl:template>
<xsl:template match="TEI:persName">
<!--<a href="{@ref}">-->
<xsl:apply-templates/>
<!--</a>-->
</xsl:template>
<xsl:template match="//TEI:birth">
<p>
<xsl:apply-templates/>
</p>
</xsl:template>
<xsl:template match="//TEI:death">
<p>
<xsl:apply-templates/>
</p>
</xsl:template>
<xsl:template match="TEI:div[@type='history']">
<xsl:apply-templates/>
</xsl:template>
<xsl:template match="TEI:div[@type='bibliography']">
<xsl:apply-templates/>
</xsl:template>
<xsl:template match="TEI:listBibl">
<ul>
<xsl:for-each select="TEI:bibl">
<li>
<span class="dark">
<xsl:apply-templates/>
</span>
</li>
</xsl:for-each>
</ul>
</xsl:template>
<xsl:template match="TEI:title">
<xsl:choose>
<xsl:when test="@ref">
<a href="{@ref}">
<i>
<xsl:apply-templates/>
</i>
</a>
</xsl:when>
<xsl:otherwise>
<i>
<xsl:apply-templates/>
</i>
</xsl:otherwise>
</xsl:choose>
</xsl:template>
<xsl:template match="TEI:head">
<h3>
<xsl:apply-templates/>
</h3>
</xsl:template>
<xsl:template match="TEI:p">
<p>
<xsl:apply-templates/>
</p>
</xsl:template>
<xsl:template match="TEI:hi">
<i>
<xsl:apply-templates/>
</i>
</xsl:template>
</xsl:stylesheet>
