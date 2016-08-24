# ./libmets.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:37b18ba845b72418ee8d15dde7fb53950cd4055d
# Generated 2016-03-03 17:55:40.722275 by PyXB version 1.2.4 using Python 2.7.10.final.0
# Namespace http://www.loc.gov/METS/

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six

# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:c2554b28-e160-11e5-b857-5c260a4b5ad7')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.4'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes
import _xlink as _ImportedBinding__xlink

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.loc.gov/METS/', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])
_Namespace_xlink = _ImportedBinding__xlink.Namespace
_Namespace_xlink.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    :rtype: object
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 292, 9)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.CREATOR = STD_ANON._CF_enumeration.addEnumeration(unicode_value='CREATOR', tag='CREATOR')
STD_ANON.EDITOR = STD_ANON._CF_enumeration.addEnumeration(unicode_value='EDITOR', tag='EDITOR')
STD_ANON.ARCHIVIST = STD_ANON._CF_enumeration.addEnumeration(unicode_value='ARCHIVIST', tag='ARCHIVIST')
STD_ANON.PRESERVATION = STD_ANON._CF_enumeration.addEnumeration(unicode_value='PRESERVATION', tag='PRESERVATION')
STD_ANON.DISSEMINATOR = STD_ANON._CF_enumeration.addEnumeration(unicode_value='DISSEMINATOR', tag='DISSEMINATOR')
STD_ANON.CUSTODIAN = STD_ANON._CF_enumeration.addEnumeration(unicode_value='CUSTODIAN', tag='CUSTODIAN')
STD_ANON.IPOWNER = STD_ANON._CF_enumeration.addEnumeration(unicode_value='IPOWNER', tag='IPOWNER')
STD_ANON.OTHER = STD_ANON._CF_enumeration.addEnumeration(unicode_value='OTHER', tag='OTHER')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 319, 9)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.INDIVIDUAL = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='INDIVIDUAL', tag='INDIVIDUAL')
STD_ANON_.ORGANIZATION = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='ORGANIZATION', tag='ORGANIZATION')
STD_ANON_.OTHER = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='OTHER', tag='OTHER')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 837, 3)
    _Documentation = None
STD_ANON_2._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_2, enum_prefix=None)
STD_ANON_2.RECT = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='RECT', tag='RECT')
STD_ANON_2.CIRCLE = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='CIRCLE', tag='CIRCLE')
STD_ANON_2.POLY = STD_ANON_2._CF_enumeration.addEnumeration(unicode_value='POLY', tag='POLY')
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 882, 3)
    _Documentation = None
STD_ANON_3._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_3, enum_prefix=None)
STD_ANON_3.BYTE = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='BYTE', tag='BYTE')
STD_ANON_3.IDREF = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='IDREF', tag='IDREF')
STD_ANON_3.SMIL = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='SMIL', tag='SMIL')
STD_ANON_3.MIDI = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='MIDI', tag='MIDI')
STD_ANON_3.SMPTE_25 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='SMPTE-25', tag='SMPTE_25')
STD_ANON_3.SMPTE_24 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='SMPTE-24', tag='SMPTE_24')
STD_ANON_3.SMPTE_DF30 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='SMPTE-DF30', tag='SMPTE_DF30')
STD_ANON_3.SMPTE_NDF30 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='SMPTE-NDF30', tag='SMPTE_NDF30')
STD_ANON_3.SMPTE_DF29_97 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='SMPTE-DF29.97', tag='SMPTE_DF29_97')
STD_ANON_3.SMPTE_NDF29_97 = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='SMPTE-NDF29.97', tag='SMPTE_NDF29_97')
STD_ANON_3.TIME = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='TIME', tag='TIME')
STD_ANON_3.TCF = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='TCF', tag='TCF')
STD_ANON_3.XPTR = STD_ANON_3._CF_enumeration.addEnumeration(unicode_value='XPTR', tag='XPTR')
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 922, 3)
    _Documentation = None
STD_ANON_4._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_4, enum_prefix=None)
STD_ANON_4.BYTE = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='BYTE', tag='BYTE')
STD_ANON_4.SMIL = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='SMIL', tag='SMIL')
STD_ANON_4.MIDI = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='MIDI', tag='MIDI')
STD_ANON_4.SMPTE_25 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='SMPTE-25', tag='SMPTE_25')
STD_ANON_4.SMPTE_24 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='SMPTE-24', tag='SMPTE_24')
STD_ANON_4.SMPTE_DF30 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='SMPTE-DF30', tag='SMPTE_DF30')
STD_ANON_4.SMPTE_NDF30 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='SMPTE-NDF30', tag='SMPTE_NDF30')
STD_ANON_4.SMPTE_DF29_97 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='SMPTE-DF29.97', tag='SMPTE_DF29_97')
STD_ANON_4.SMPTE_NDF29_97 = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='SMPTE-NDF29.97', tag='SMPTE_NDF29_97')
STD_ANON_4.TIME = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='TIME', tag='TIME')
STD_ANON_4.TCF = STD_ANON_4._CF_enumeration.addEnumeration(unicode_value='TCF', tag='TCF')
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1073, 6)
    _Documentation = None
STD_ANON_5._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_5, enum_prefix=None)
STD_ANON_5.ordered = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='ordered', tag='ordered')
STD_ANON_5.unordered = STD_ANON_5._CF_enumeration.addEnumeration(unicode_value='unordered', tag='unordered')
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1455, 8)
    _Documentation = None
STD_ANON_6._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_6, enum_prefix=None)
STD_ANON_6.BYTE = STD_ANON_6._CF_enumeration.addEnumeration(unicode_value='BYTE', tag='BYTE')
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_7 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1483, 8)
    _Documentation = None
STD_ANON_7._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_7, enum_prefix=None)
STD_ANON_7.decompression = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value='decompression', tag='decompression')
STD_ANON_7.decryption = STD_ANON_7._CF_enumeration.addEnumeration(unicode_value='decryption', tag='decryption')
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_8 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1577, 3)
    _Documentation = None
STD_ANON_8._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_8, enum_prefix=None)
STD_ANON_8.BYTE = STD_ANON_8._CF_enumeration.addEnumeration(unicode_value='BYTE', tag='BYTE')
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_enumeration)

# List simple type: {http://www.loc.gov/METS/}URIs
# superclasses pyxb.binding.datatypes.anySimpleType
class URIs (pyxb.binding.basis.STD_list):

    """Simple type that is a list of pyxb.binding.datatypes.anyURI."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'URIs')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1586, 1)
    _Documentation = None

    _ItemType = pyxb.binding.datatypes.anyURI
URIs._InitializeFacetMap()
Namespace.addCategoryObject('typeBinding', 'URIs', URIs)

# Atomic simple type: [anonymous]
class STD_ANON_9 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1639, 3)
    _Documentation = None
STD_ANON_9._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_9, enum_prefix=None)
STD_ANON_9.MARC = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='MARC', tag='MARC')
STD_ANON_9.MODS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='MODS', tag='MODS')
STD_ANON_9.EAD = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='EAD', tag='EAD')
STD_ANON_9.DC = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='DC', tag='DC')
STD_ANON_9.NISOIMG = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='NISOIMG', tag='NISOIMG')
STD_ANON_9.LC_AV = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='LC-AV', tag='LC_AV')
STD_ANON_9.VRA = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='VRA', tag='VRA')
STD_ANON_9.TEIHDR = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='TEIHDR', tag='TEIHDR')
STD_ANON_9.DDI = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='DDI', tag='DDI')
STD_ANON_9.FGDC = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='FGDC', tag='FGDC')
STD_ANON_9.LOM = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='LOM', tag='LOM')
STD_ANON_9.PREMIS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='PREMIS', tag='PREMIS')
STD_ANON_9.PREMISOBJECT = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='PREMIS:OBJECT', tag='PREMISOBJECT')
STD_ANON_9.PREMISAGENT = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='PREMIS:AGENT', tag='PREMISAGENT')
STD_ANON_9.PREMISRIGHTS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='PREMIS:RIGHTS', tag='PREMISRIGHTS')
STD_ANON_9.PREMISEVENT = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='PREMIS:EVENT', tag='PREMISEVENT')
STD_ANON_9.TEXTMD = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='TEXTMD', tag='TEXTMD')
STD_ANON_9.METSRIGHTS = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='METSRIGHTS', tag='METSRIGHTS')
STD_ANON_9.ISO_191152003_NAP = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='ISO 19115:2003 NAP', tag='ISO_191152003_NAP')
STD_ANON_9.EAC_CPF = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='EAC-CPF', tag='EAC_CPF')
STD_ANON_9.LIDO = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='LIDO', tag='LIDO')
STD_ANON_9.OTHER = STD_ANON_9._CF_enumeration.addEnumeration(unicode_value='OTHER', tag='OTHER')
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_10 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1691, 3)
    _Documentation = None
STD_ANON_10._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_10, enum_prefix=None)
STD_ANON_10.ARK = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='ARK', tag='ARK')
STD_ANON_10.URN = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='URN', tag='URN')
STD_ANON_10.URL = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='URL', tag='URL')
STD_ANON_10.PURL = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='PURL', tag='PURL')
STD_ANON_10.HANDLE = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='HANDLE', tag='HANDLE')
STD_ANON_10.DOI = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='DOI', tag='DOI')
STD_ANON_10.OTHER = STD_ANON_10._CF_enumeration.addEnumeration(unicode_value='OTHER', tag='OTHER')
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_11 (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1751, 3)
    _Documentation = None
STD_ANON_11._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_11, enum_prefix=None)
STD_ANON_11.Adler_32 = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='Adler-32', tag='Adler_32')
STD_ANON_11.CRC32 = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='CRC32', tag='CRC32')
STD_ANON_11.HAVAL = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='HAVAL', tag='HAVAL')
STD_ANON_11.MD5 = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='MD5', tag='MD5')
STD_ANON_11.MNP = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='MNP', tag='MNP')
STD_ANON_11.SHA_1 = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='SHA-1', tag='SHA_1')
STD_ANON_11.SHA_256 = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='SHA-256', tag='SHA_256')
STD_ANON_11.SHA_384 = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='SHA-384', tag='SHA_384')
STD_ANON_11.SHA_512 = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='SHA-512', tag='SHA_512')
STD_ANON_11.TIGER = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='TIGER', tag='TIGER')
STD_ANON_11.WHIRLPOOL = STD_ANON_11._CF_enumeration.addEnumeration(unicode_value='WHIRLPOOL', tag='WHIRLPOOL')
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_enumeration)

# Complex type {http://www.loc.gov/METS/}metsType with content type ELEMENT_ONLY
class metsType (pyxb.binding.basis.complexTypeDefinition):
    """metsType: Complex Type for METS Sections
			A METS document consists of seven possible subsidiary sections: metsHdr (METS document header), dmdSec (descriptive metadata section), amdSec (administrative metadata section), fileGrp (file inventory group), structLink (structural map linking), structMap (structural map) and behaviorSec (behaviors section).
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'metsType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 235, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}metsHdr uses Python identifier metsHdr
    __metsHdr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'metsHdr'), 'metsHdr', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSmetsHdr', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 242, 3), )

    
    metsHdr = property(__metsHdr.value, __metsHdr.set, None, ' \n\t\t\t\t\tThe mets header element <metsHdr> captures metadata about the METS document itself, not the digital object the METS document encodes. Although it records a more limited set of metadata, it is very similar in function and purpose to the headers employed in other schema such as the Text Encoding Initiative (TEI) or in the Encoded Archival Description (EAD).\n\t\t\t')

    
    # Element {http://www.loc.gov/METS/}dmdSec uses Python identifier dmdSec
    __dmdSec = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'dmdSec'), 'dmdSec', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSdmdSec', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 419, 3), )

    
    dmdSec = property(__dmdSec.value, __dmdSec.set, None, '\n\t\t\t\t\t\tA descriptive metadata section <dmdSec> records descriptive metadata pertaining to the METS object as a whole or one of its components. The <dmdSec> element conforms to same generic datatype as the <techMD>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes. A descriptive metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <dmdSec> elements; and descriptive metadata can be associated with any METS element that supports a DMDID attribute.  Descriptive metadata can be expressed according to many current description standards (i.e., MARC, MODS, Dublin Core, TEI Header, EAD, VRA, FGDC, DDI) or a locally produced XML schema. \n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}amdSec uses Python identifier amdSec
    __amdSec = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'amdSec'), 'amdSec', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSamdSec', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 426, 3), )

    
    amdSec = property(__amdSec.value, __amdSec.set, None, ' \n\t\t\t\t\t\tThe administrative metadata section <amdSec> contains the administrative metadata pertaining to the digital object, its components and any original source material from which the digital object is derived. The <amdSec> is separated into four sub-sections that accommodate technical metadata (techMD), intellectual property rights (rightsMD), analog/digital source metadata (sourceMD), and digital provenance metadata (digiprovMD). Each of these subsections can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both. Multiple instances of the <amdSec> element can occur within a METS document and multiple instances of its subsections can occur in one <amdSec> element. This allows considerable flexibility in the structuring of the administrative metadata. METS does not define a vocabulary or syntax for encoding administrative metadata. Administrative metadata can be expressed within the amdSec sub-elements according to many current community defined standards, or locally produced XML schemas. ')

    
    # Element {http://www.loc.gov/METS/}fileSec uses Python identifier fileSec
    __fileSec = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'fileSec'), 'fileSec', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSfileSec', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 432, 3), )

    
    fileSec = property(__fileSec.value, __fileSec.set, None, ' \n\t\t\t\t\t\tThe overall purpose of the content file section element <fileSec> is to provide an inventory of and the location for the content files that comprise the digital object being described in the METS document.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}structMap uses Python identifier structMap
    __structMap = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'structMap'), 'structMap', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSstructMap', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 470, 3), )

    
    structMap = property(__structMap.value, __structMap.set, None, ' \n\t\t\t\t\t\tThe structural map section <structMap> is the heart of a METS document. It provides a means for organizing the digital content represented by the <file> elements in the <fileSec> of the METS document into a coherent hierarchical structure. Such a hierarchical structure can be presented to users to facilitate their comprehension and navigation of the digital content. It can further be applied to any purpose requiring an understanding of the structural relationship of the content files or parts of the content files. The organization may be specified to any level of granularity (intellectual and or physical) that is desired. Since the <structMap> element is repeatable, more than one organization can be applied to the digital content represented by the METS document.  The hierarchical structure specified by a <structMap> is encoded as a tree of nested <div> elements. A <div> element may directly point to content via child file pointer <fptr> elements (if the content is represented in the <fileSec<) or child METS pointer <mptr> elements (if the content is represented by an external METS document). The <fptr> element may point to a single whole <file> element that manifests its parent <div<, or to part of a <file> that manifests its <div<. It can also point to multiple files or parts of files that must be played/displayed either in sequence or in parallel to reveal its structural division. In addition to providing a means for organizing content, the <structMap> provides a mechanism for linking content at any hierarchical level with relevant descriptive and administrative metadata.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}structLink uses Python identifier structLink
    __structLink = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'structLink'), 'structLink', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSstructLink', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 477, 3), )

    
    structLink = property(__structLink.value, __structLink.set, None, ' \n\t\t\t\t\t\tThe structural link section element <structLink> allows for the specification of hyperlinks between the different components of a METS structure that are delineated in a structural map. This element is a container for a single, repeatable element, <smLink> which indicates a hyperlink between two nodes in the structural map. The <structLink> section in the METS document is identified using its XML ID attributes.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}behaviorSec uses Python identifier behaviorSec
    __behaviorSec = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'behaviorSec'), 'behaviorSec', '__httpwww_loc_govMETS_metsType_httpwww_loc_govMETSbehaviorSec', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 489, 3), )

    
    behaviorSec = property(__behaviorSec.value, __behaviorSec.set, None, '\n\t\t\t\t\t\tA behavior section element <behaviorSec> associates executable behaviors with content in the METS document by means of a repeatable behavior <behavior> element. This element has an interface definition <interfaceDef> element that represents an abstract definition of the set of behaviors represented by a particular behavior section. A <behavior> element also has a <mechanism> element which is used to point to a module of executable code that implements and runs the behavior defined by the interface definition. The <behaviorSec> element, which is repeatable as well as nestable, can be used to group individual behaviors within the structure of the METS document. Such grouping can be useful for organizing families of behaviors together or to indicate other relationships between particular behaviors.')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_metsType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 496, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 496, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute OBJID uses Python identifier OBJID
    __OBJID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OBJID'), 'OBJID', '__httpwww_loc_govMETS_metsType_OBJID', pyxb.binding.datatypes.string)
    __OBJID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 502, 2)
    __OBJID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 502, 2)
    
    OBJID = property(__OBJID.value, __OBJID.set, None, 'OBJID (string/O): Is the primary identifier assigned to the METS object as a whole. Although this attribute is not required, it is strongly recommended. This identifier is used to tag the entire METS object to external systems, in contrast with the ID identifier.\n\t\t\t\t')

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_metsType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 508, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 508, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): Is a simple title string used to identify the object/entity being described in the METS document for the user.\n\t\t\t\t')

    
    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TYPE'), 'TYPE', '__httpwww_loc_govMETS_metsType_TYPE', pyxb.binding.datatypes.string)
    __TYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 514, 2)
    __TYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 514, 2)
    
    TYPE = property(__TYPE.value, __TYPE.set, None, 'TYPE (string/O): Specifies the class or type of the object, e.g.: book, journal, stereograph, dataset, video, etc.\n\t\t\t\t')

    
    # Attribute PROFILE uses Python identifier PROFILE
    __PROFILE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'PROFILE'), 'PROFILE', '__httpwww_loc_govMETS_metsType_PROFILE', pyxb.binding.datatypes.string)
    __PROFILE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 520, 2)
    __PROFILE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 520, 2)
    
    PROFILE = property(__PROFILE.value, __PROFILE.set, None, 'PROFILE (string/O): Indicates to which of the registered profile(s) the METS document conforms. For additional information about PROFILES see Chapter 5 of the METS Primer.\n\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __metsHdr.name() : __metsHdr,
        __dmdSec.name() : __dmdSec,
        __amdSec.name() : __amdSec,
        __fileSec.name() : __fileSec,
        __structMap.name() : __structMap,
        __structLink.name() : __structLink,
        __behaviorSec.name() : __behaviorSec
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __OBJID.name() : __OBJID,
        __LABEL.name() : __LABEL,
        __TYPE.name() : __TYPE,
        __PROFILE.name() : __PROFILE
    })
Namespace.addCategoryObject('typeBinding', 'metsType', metsType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """ 
					The mets header element <metsHdr> captures metadata about the METS document itself, not the digital object the METS document encodes. Although it records a more limited set of metadata, it is very similar in function and purpose to the headers employed in other schema such as the Text Encoding Initiative (TEI) or in the Encoded Archival Description (EAD).
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 248, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}agent uses Python identifier agent
    __agent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'agent'), 'agent', '__httpwww_loc_govMETS_CTD_ANON_httpwww_loc_govMETSagent', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 250, 6), )

    
    agent = property(__agent.value, __agent.set, None, 'agent: \n\t\t\t\t\t\t\t\tThe agent element <agent> provides for various parties and their roles with respect to the METS record to be documented.  \n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}altRecordID uses Python identifier altRecordID
    __altRecordID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'altRecordID'), 'altRecordID', '__httpwww_loc_govMETS_CTD_ANON_httpwww_loc_govMETSaltRecordID', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 335, 6), )

    
    altRecordID = property(__altRecordID.value, __altRecordID.set, None, '    \n\t\t\t\t\t\t\t\t\tThe alternative record identifier element <altRecordID> allows one to use alternative record identifier values for the digital object represented by the METS document; the primary record identifier is stored in the OBJID attribute in the root <mets> element.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}metsDocumentID uses Python identifier metsDocumentID
    __metsDocumentID = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'metsDocumentID'), 'metsDocumentID', '__httpwww_loc_govMETS_CTD_ANON_httpwww_loc_govMETSmetsDocumentID', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 360, 6), )

    
    metsDocumentID = property(__metsDocumentID.value, __metsDocumentID.set, None, '    \n\t\t\t\t\t\t\t\t\tThe metsDocument identifier element <metsDocumentID> allows a unique identifier to be assigned to the METS document itself.  This may be different from the OBJID attribute value in the root <mets> element, which uniquely identifies the entire digital object represented by the METS document.\n\t\t\t\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 386, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 386, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_CTD_ANON_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 392, 5)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 392, 5)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREFS/O): Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain administrative metadata pertaining to the METS document itself.  For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute CREATEDATE uses Python identifier CREATEDATE
    __CREATEDATE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CREATEDATE'), 'CREATEDATE', '__httpwww_loc_govMETS_CTD_ANON_CREATEDATE', pyxb.binding.datatypes.dateTime)
    __CREATEDATE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 398, 5)
    __CREATEDATE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 398, 5)
    
    CREATEDATE = property(__CREATEDATE.value, __CREATEDATE.set, None, 'CREATEDATE (dateTime/O): Records the date/time the METS document was created.\n\t\t\t\t\t\t\t')

    
    # Attribute LASTMODDATE uses Python identifier LASTMODDATE
    __LASTMODDATE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LASTMODDATE'), 'LASTMODDATE', '__httpwww_loc_govMETS_CTD_ANON_LASTMODDATE', pyxb.binding.datatypes.dateTime)
    __LASTMODDATE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 404, 5)
    __LASTMODDATE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 404, 5)
    
    LASTMODDATE = property(__LASTMODDATE.value, __LASTMODDATE.set, None, 'LASTMODDATE (dateTime/O): Is used to indicate the date/time the METS document was last modified.\n\t\t\t\t\t\t\t')

    
    # Attribute RECORDSTATUS uses Python identifier RECORDSTATUS
    __RECORDSTATUS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'RECORDSTATUS'), 'RECORDSTATUS', '__httpwww_loc_govMETS_CTD_ANON_RECORDSTATUS', pyxb.binding.datatypes.string)
    __RECORDSTATUS._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 410, 5)
    __RECORDSTATUS._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 410, 5)
    
    RECORDSTATUS = property(__RECORDSTATUS.value, __RECORDSTATUS.set, None, 'RECORDSTATUS (string/O): Specifies the status of the METS document. It is used for internal processing purposes.\n\t\t\t\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __agent.name() : __agent,
        __altRecordID.name() : __altRecordID,
        __metsDocumentID.name() : __metsDocumentID
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __ADMID.name() : __ADMID,
        __CREATEDATE.name() : __CREATEDATE,
        __LASTMODDATE.name() : __LASTMODDATE,
        __RECORDSTATUS.name() : __RECORDSTATUS
    })



# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """    
									The alternative record identifier element <altRecordID> allows one to use alternative record identifier values for the digital object represented by the METS document; the primary record identifier is stored in the OBJID attribute in the root <mets> element.
								"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 341, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON__ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 344, 10)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 344, 10)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t\t\t\t')

    
    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TYPE'), 'TYPE', '__httpwww_loc_govMETS_CTD_ANON__TYPE', pyxb.binding.datatypes.string)
    __TYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 350, 10)
    __TYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 350, 10)
    
    TYPE = property(__TYPE.value, __TYPE.set, None, 'TYPE (string/O): A description of the identifier type (e.g., OCLC record number, LCCN, etc.).\n\t\t\t\t\t\t\t\t\t\t\t\t')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __TYPE.name() : __TYPE
    })



# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """    
									The metsDocument identifier element <metsDocumentID> allows a unique identifier to be assigned to the METS document itself.  This may be different from the OBJID attribute value in the root <mets> element, which uniquely identifies the entire digital object represented by the METS document.
								"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 366, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_2_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 369, 10)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 369, 10)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t\t\t\t')

    
    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TYPE'), 'TYPE', '__httpwww_loc_govMETS_CTD_ANON_2_TYPE', pyxb.binding.datatypes.string)
    __TYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 375, 10)
    __TYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 375, 10)
    
    TYPE = property(__TYPE.value, __TYPE.set, None, 'TYPE (string/O): A description of the identifier type.\n\t\t\t\t\t\t\t\t\t\t\t\t')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __TYPE.name() : __TYPE
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """ 
						The overall purpose of the content file section element <fileSec> is to provide an inventory of and the location for the content files that comprise the digital object being described in the METS document.
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 438, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}fileGrp uses Python identifier fileGrp
    __fileGrp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'fileGrp'), 'fileGrp', '__httpwww_loc_govMETS_CTD_ANON_3_httpwww_loc_govMETSfileGrp', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 440, 6), )

    
    fileGrp = property(__fileGrp.value, __fileGrp.set, None, ' \n\t\t\t\t\t\t\t\t\tA sequence of file group elements <fileGrp> can be used group the digital files comprising the content of a METS object either into a flat arrangement or, because each file group element can itself contain one or more  file group elements,  into a nested (hierarchical) arrangement. In the case where the content files are images of different formats and resolutions, for example, one could group the image content files by format and create a separate <fileGrp> for each image format/resolution such as:\n-- one <fileGrp> for the thumbnails of the images\n-- one <fileGrp> for the higher resolution JPEGs of the image \n-- one <fileGrp> for the master archival TIFFs of the images \nFor a text resource with a variety of content file types one might group the content files at the highest level by type,  and then use the <fileGrp> element\u2019s nesting capabilities to subdivide a <fileGrp> by format within the type, such as:\n-- one <fileGrp> for all of the page images with nested <fileGrp> elements for each image format/resolution (tiff, jpeg, gif)\n-- one <fileGrp> for a PDF version of all the pages of the document \n-- one <fileGrp> for  a TEI encoded XML version of the entire document or each of its pages.\nA <fileGrp> may contain zero or more <fileGrp> elements and or <file> elements.\t\t\t\t\t\n\t\t\t\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_3_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 461, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 461, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __fileGrp.name() : __fileGrp
    })
    _AttributeMap.update({
        __ID.name() : __ID
    })



# Complex type {http://www.loc.gov/METS/}amdSecType with content type ELEMENT_ONLY
class amdSecType (pyxb.binding.basis.complexTypeDefinition):
    """amdSecType: Complex Type for Administrative Metadata Sections
			The administrative metadata section consists of four possible subsidiary sections: techMD (technical metadata for text/image/audio/video files), rightsMD (intellectual property rights metadata), sourceMD (analog/digital source metadata), and digiprovMD (digital provenance metadata, that is, the history of migrations/translations performed on a digital library object from it's original digital capture/encoding).
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'amdSecType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 528, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}techMD uses Python identifier techMD
    __techMD = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'techMD'), 'techMD', '__httpwww_loc_govMETS_amdSecType_httpwww_loc_govMETStechMD', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 535, 3), )

    
    techMD = property(__techMD.value, __techMD.set, None, ' \n\t\t\t\t\t\tA technical metadata element <techMD> records technical metadata about a component of the METS object, such as a digital content file. The <techMD> element conforms to same generic datatype as the <dmdSec>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes.  A technical metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <techMD> elements; and technical metadata can be associated with any METS element that supports an ADMID attribute. Technical metadata can be expressed according to many current technical description standards (such as MIX and textMD) or a locally produced XML schema.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}rightsMD uses Python identifier rightsMD
    __rightsMD = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'rightsMD'), 'rightsMD', '__httpwww_loc_govMETS_amdSecType_httpwww_loc_govMETSrightsMD', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 542, 3), )

    
    rightsMD = property(__rightsMD.value, __rightsMD.set, None, '\n\t\t\t\t\t\tAn intellectual property rights metadata element <rightsMD> records information about copyright and licensing pertaining to a component of the METS object. The <rightsMD> element conforms to same generic datatype as the <dmdSec>, <techMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes. A rights metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <rightsMD> elements; and rights metadata can be associated with any METS element that supports an ADMID attribute. Rights metadata can be expressed according current rights description standards (such as CopyrightMD and rightsDeclarationMD) or a locally produced XML schema.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}sourceMD uses Python identifier sourceMD
    __sourceMD = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'sourceMD'), 'sourceMD', '__httpwww_loc_govMETS_amdSecType_httpwww_loc_govMETSsourceMD', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 549, 3), )

    
    sourceMD = property(__sourceMD.value, __sourceMD.set, None, '\n\t\t\t\t\t\tA source metadata element <sourceMD> records descriptive and administrative metadata about the source format or media of a component of the METS object such as a digital content file. It is often used for discovery, data administration or preservation of the digital object. The <sourceMD> element conforms to same generic datatype as the <dmdSec>, <techMD>, <rightsMD>,  and <digiprovMD> elements, and supports the same sub-elements and attributes.  A source metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <sourceMD> elements; and source metadata can be associated with any METS element that supports an ADMID attribute. Source metadata can be expressed according to current source description standards (such as PREMIS) or a locally produced XML schema.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}digiprovMD uses Python identifier digiprovMD
    __digiprovMD = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'digiprovMD'), 'digiprovMD', '__httpwww_loc_govMETS_amdSecType_httpwww_loc_govMETSdigiprovMD', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 556, 3), )

    
    digiprovMD = property(__digiprovMD.value, __digiprovMD.set, None, '\n\t\t\t\t\t\tA digital provenance metadata element <digiprovMD> can be used to record any preservation-related actions taken on the various files which comprise a digital object (e.g., those subsequent to the initial digitization of the files such as transformation or migrations) or, in the case of born digital materials, the files\u2019 creation. In short, digital provenance should be used to record information that allows both archival/library staff and scholars to understand what modifications have been made to a digital object and/or its constituent parts during its life cycle. This information can then be used to judge how those processes might have altered or corrupted the object\u2019s ability to accurately represent the original item. One might, for example, record master derivative relationships and the process by which those derivations have been created. Or the <digiprovMD> element could contain information regarding the migration/transformation of a file from its original digitization (e.g., OCR, TEI, etc.,)to its current incarnation as a digital object (e.g., JPEG2000). The <digiprovMD> element conforms to same generic datatype as the <dmdSec>,  <techMD>, <rightsMD>, and <sourceMD> elements, and supports the same sub-elements and attributes. A digital provenance metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <digiprovMD> elements; and digital provenance metadata can be associated with any METS element that supports an ADMID attribute. Digital provenance metadata can be expressed according to current digital provenance description standards (such as PREMIS) or a locally produced XML schema.\n\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_amdSecType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 564, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 564, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __techMD.name() : __techMD,
        __rightsMD.name() : __rightsMD,
        __sourceMD.name() : __sourceMD,
        __digiprovMD.name() : __digiprovMD
    })
    _AttributeMap.update({
        __ID.name() : __ID
    })
Namespace.addCategoryObject('typeBinding', 'amdSecType', amdSecType)


# Complex type {http://www.loc.gov/METS/}fileGrpType with content type ELEMENT_ONLY
class fileGrpType (pyxb.binding.basis.complexTypeDefinition):
    """fileGrpType: Complex Type for File Groups
				The file group is used to cluster all of the digital files composing a digital library object in a hierarchical arrangement (fileGrp is recursively defined to enable the creation of the hierarchy).  Any file group may contain zero or more file elements.  File elements in turn can contain one or more FLocat elements (a pointer to a file containing content for this object) and/or a FContent element (the contents of the file, in either XML or  Base64 encoding).
				"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fileGrpType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 572, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}fileGrp uses Python identifier fileGrp
    __fileGrp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'fileGrp'), 'fileGrp', '__httpwww_loc_govMETS_fileGrpType_httpwww_loc_govMETSfileGrp', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 579, 3), )

    
    fileGrp = property(__fileGrp.value, __fileGrp.set, None, None)

    
    # Element {http://www.loc.gov/METS/}file uses Python identifier file
    __file = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'file'), 'file', '__httpwww_loc_govMETS_fileGrpType_httpwww_loc_govMETSfile', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 580, 3), )

    
    file = property(__file.value, __file.set, None, '\n\t\t\t\t\t\tThe file element <file> provides access to the content files for the digital object being described by the METS document. A <file> element may contain one or more <FLocat> elements which provide pointers to a content file and/or a <FContent> element which wraps an encoded version of the file. Embedding files using <FContent> can be a valuable feature for exchanging digital objects between repositories or for archiving versions of digital objects for off-site storage. All <FLocat> and <FContent> elements should identify and/or contain identical copies of a single file. The <file> element is recursive, thus allowing sub-files or component files of a larger file to be listed in the inventory. Alternatively, by using the <stream> element, a smaller component of a file or of a related file can be placed within a <file> element. Finally, by using the <transformFile> element, it is possible to include within a <file> element a different version of a file that has undergone a transformation for some reason, such as format migration.\n\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_fileGrpType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 588, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 588, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute VERSDATE uses Python identifier VERSDATE
    __VERSDATE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'VERSDATE'), 'VERSDATE', '__httpwww_loc_govMETS_fileGrpType_VERSDATE', pyxb.binding.datatypes.dateTime)
    __VERSDATE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 594, 2)
    __VERSDATE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 594, 2)
    
    VERSDATE = property(__VERSDATE.value, __VERSDATE.set, None, 'VERSDATE (dateTime/O): An optional dateTime attribute specifying the date this version/fileGrp of the digital object was created.\n\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_fileGrpType_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 600, 2)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 600, 2)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREF/O): Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> elements within the <amdSec> of the METS document applicable to all of the files in a particular file group. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute USE uses Python identifier USE
    __USE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'USE'), 'USE', '__httpwww_loc_govMETS_fileGrpType_USE', pyxb.binding.datatypes.string)
    __USE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 606, 2)
    __USE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 606, 2)
    
    USE = property(__USE.value, __USE.set, None, 'USE (string/O): A tagging attribute to indicate the intended use of files within this file group (e.g., master, reference, thumbnails for image files). A USE attribute can be expressed at the<fileGrp> level, the <file> level, the <FLocat> level and/or the <FContent> level.  A USE attribute value at the <fileGrp> level should pertain to all of the files in the <fileGrp>.  A USE attribute at the <file> level should pertain to all copies of the file as represented by subsidiary <FLocat> and/or <FContent> elements.  A USE attribute at the <FLocat> or <FContent> level pertains to the particular copy of the file that is either referenced (<FLocat>) or wrapped (<FContent>). \n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __fileGrp.name() : __fileGrp,
        __file.name() : __file
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __VERSDATE.name() : __VERSDATE,
        __ADMID.name() : __ADMID,
        __USE.name() : __USE
    })
Namespace.addCategoryObject('typeBinding', 'fileGrpType', fileGrpType)


# Complex type {http://www.loc.gov/METS/}structMapType with content type ELEMENT_ONLY
class structMapType (pyxb.binding.basis.complexTypeDefinition):
    """structMapType: Complex Type for Structural Maps
			The structural map (structMap) outlines a hierarchical structure for the original object being encoded, using a series of nested div elements.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'structMapType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 614, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}div uses Python identifier div
    __div = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'div'), 'div', '__httpwww_loc_govMETS_structMapType_httpwww_loc_govMETSdiv', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 621, 3), )

    
    div = property(__div.value, __div.set, None, " \n\t\t\t\t\t\tThe structural divisions of the hierarchical organization provided by a <structMap> are represented by division <div> elements, which can be nested to any depth. Each <div> element can represent either an intellectual (logical) division or a physical division. Every <div> node in the structural map hierarchy may be connected (via subsidiary <mptr> or <fptr> elements) to content files which represent that div's portion of the whole document. \n\t\t\t\t\t")

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_structMapType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 629, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 629, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TYPE'), 'TYPE', '__httpwww_loc_govMETS_structMapType_TYPE', pyxb.binding.datatypes.string)
    __TYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 635, 2)
    __TYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 635, 2)
    
    TYPE = property(__TYPE.value, __TYPE.set, None, 'TYPE (string/O): Identifies the type of structure represented by the <structMap>. For example, a <structMap> that represented a purely logical or intellectual structure could be assigned a TYPE value of \u201clogical\u201d whereas a <structMap> that represented a purely physical structure could be assigned a TYPE value of \u201cphysical\u201d. However, the METS schema neither defines nor requires a common vocabulary for this attribute. A METS profile, however, may well constrain the values for the <structMap> TYPE.\n\t\t\t\t')

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_structMapType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 641, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 641, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): Describes the <structMap> to viewers of the METS document. This would be useful primarily where more than one <structMap> is provided for a single object. A descriptive LABEL value, in that case, could clarify to users the purpose of each of the available structMaps.\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __div.name() : __div
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __TYPE.name() : __TYPE,
        __LABEL.name() : __LABEL
    })
Namespace.addCategoryObject('typeBinding', 'structMapType', structMapType)


# Complex type {http://www.loc.gov/METS/}parType with content type ELEMENT_ONLY
class parType (pyxb.binding.basis.complexTypeDefinition):
    """parType: Complex Type for Parallel Files
				The <par> or parallel files element aggregates pointers to files, parts of files, and/or sequences of files or parts of files that must be played or displayed simultaneously to manifest a block of digital content represented by an <fptr> element. 
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'parType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 773, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}area uses Python identifier area
    __area = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'area'), 'area', '__httpwww_loc_govMETS_parType_httpwww_loc_govMETSarea', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 780, 3), )

    
    area = property(__area.value, __area.set, None, None)

    
    # Element {http://www.loc.gov/METS/}seq uses Python identifier seq
    __seq = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'seq'), 'seq', '__httpwww_loc_govMETS_parType_httpwww_loc_govMETSseq', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 781, 3), )

    
    seq = property(__seq.value, __seq.set, None, None)

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_parType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 783, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 783, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute ORDER uses Python identifier ORDER
    __ORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ORDER'), 'ORDER', '__httpwww_loc_govMETS_parType_ORDER', pyxb.binding.datatypes.integer)
    __ORDER._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1591, 2)
    __ORDER._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1591, 2)
    
    ORDER = property(__ORDER.value, __ORDER.set, None, "ORDER (integer/O): A representation of the element's order among its siblings (e.g., its absolute, numeric sequence). For an example, and clarification of the distinction between ORDER and ORDERLABEL, see the description of the ORDERLABEL attribute.\n\t\t\t\t")

    
    # Attribute ORDERLABEL uses Python identifier ORDERLABEL
    __ORDERLABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ORDERLABEL'), 'ORDERLABEL', '__httpwww_loc_govMETS_parType_ORDERLABEL', pyxb.binding.datatypes.string)
    __ORDERLABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1597, 2)
    __ORDERLABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1597, 2)
    
    ORDERLABEL = property(__ORDERLABEL.value, __ORDERLABEL.set, None, "ORDERLABEL (string/O): A representation of the element's order among its siblings (e.g., \u201cxii\u201d), or of any non-integer native numbering system. It is presumed that this value will still be machine actionable (e.g., it would support \u2018go to page ___\u2019 function), and it should not be used as a replacement/substitute for the LABEL attribute. To understand the differences between ORDER, ORDERLABEL and LABEL, imagine a text with 10 roman numbered pages followed by 10 arabic numbered pages. Page iii would have an ORDER of \u201c3\u201d, an ORDERLABEL of \u201ciii\u201d and a LABEL of \u201cPage iii\u201d, while page 3 would have an ORDER of \u201c13\u201d, an ORDERLABEL of \u201c3\u201d and a LABEL of \u201cPage 3\u201d.\n\t\t\t\t")

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_parType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1603, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1603, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): An attribute used, for example, to identify a <div> to an end user viewing the document. Thus a hierarchical arrangement of the <div> LABEL values could provide a table of contents to the digital content represented by a METS document and facilitate the users\u2019 navigation of the digital object. Note that a <div> LABEL should be specific to its level in the structural map. In the case of a book with chapters, the book <div> LABEL should have the book title and the chapter <div>; LABELs should have the individual chapter titles, rather than having the chapter <div> LABELs combine both book title and chapter title . For further of the distinction between LABEL and ORDERLABEL see the description of the ORDERLABEL attribute.\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __area.name() : __area,
        __seq.name() : __seq
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __ORDER.name() : __ORDER,
        __ORDERLABEL.name() : __ORDERLABEL,
        __LABEL.name() : __LABEL
    })
Namespace.addCategoryObject('typeBinding', 'parType', parType)


# Complex type {http://www.loc.gov/METS/}seqType with content type ELEMENT_ONLY
class seqType (pyxb.binding.basis.complexTypeDefinition):
    """seqType: Complex Type for Sequences of Files
					The seq element should be used to link a div to a set of content files when those files should be played/displayed sequentially to deliver content to a user.  Individual <area> subelements within the seq element provide the links to the files or portions thereof.
				"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'seqType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 792, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}area uses Python identifier area
    __area = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'area'), 'area', '__httpwww_loc_govMETS_seqType_httpwww_loc_govMETSarea', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 799, 3), )

    
    area = property(__area.value, __area.set, None, None)

    
    # Element {http://www.loc.gov/METS/}par uses Python identifier par
    __par = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'par'), 'par', '__httpwww_loc_govMETS_seqType_httpwww_loc_govMETSpar', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 800, 3), )

    
    par = property(__par.value, __par.set, None, None)

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_seqType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 802, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 802, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute ORDER uses Python identifier ORDER
    __ORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ORDER'), 'ORDER', '__httpwww_loc_govMETS_seqType_ORDER', pyxb.binding.datatypes.integer)
    __ORDER._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1591, 2)
    __ORDER._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1591, 2)
    
    ORDER = property(__ORDER.value, __ORDER.set, None, "ORDER (integer/O): A representation of the element's order among its siblings (e.g., its absolute, numeric sequence). For an example, and clarification of the distinction between ORDER and ORDERLABEL, see the description of the ORDERLABEL attribute.\n\t\t\t\t")

    
    # Attribute ORDERLABEL uses Python identifier ORDERLABEL
    __ORDERLABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ORDERLABEL'), 'ORDERLABEL', '__httpwww_loc_govMETS_seqType_ORDERLABEL', pyxb.binding.datatypes.string)
    __ORDERLABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1597, 2)
    __ORDERLABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1597, 2)
    
    ORDERLABEL = property(__ORDERLABEL.value, __ORDERLABEL.set, None, "ORDERLABEL (string/O): A representation of the element's order among its siblings (e.g., \u201cxii\u201d), or of any non-integer native numbering system. It is presumed that this value will still be machine actionable (e.g., it would support \u2018go to page ___\u2019 function), and it should not be used as a replacement/substitute for the LABEL attribute. To understand the differences between ORDER, ORDERLABEL and LABEL, imagine a text with 10 roman numbered pages followed by 10 arabic numbered pages. Page iii would have an ORDER of \u201c3\u201d, an ORDERLABEL of \u201ciii\u201d and a LABEL of \u201cPage iii\u201d, while page 3 would have an ORDER of \u201c13\u201d, an ORDERLABEL of \u201c3\u201d and a LABEL of \u201cPage 3\u201d.\n\t\t\t\t")

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_seqType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1603, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1603, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): An attribute used, for example, to identify a <div> to an end user viewing the document. Thus a hierarchical arrangement of the <div> LABEL values could provide a table of contents to the digital content represented by a METS document and facilitate the users\u2019 navigation of the digital object. Note that a <div> LABEL should be specific to its level in the structural map. In the case of a book with chapters, the book <div> LABEL should have the book title and the chapter <div>; LABELs should have the individual chapter titles, rather than having the chapter <div> LABELs combine both book title and chapter title . For further of the distinction between LABEL and ORDERLABEL see the description of the ORDERLABEL attribute.\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __area.name() : __area,
        __par.name() : __par
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __ORDER.name() : __ORDER,
        __ORDERLABEL.name() : __ORDERLABEL,
        __LABEL.name() : __LABEL
    })
Namespace.addCategoryObject('typeBinding', 'seqType', seqType)


# Complex type {http://www.loc.gov/METS/}structLinkType with content type ELEMENT_ONLY
class structLinkType (pyxb.binding.basis.complexTypeDefinition):
    """structLinkType: Complex Type for Structural Map Linking
				The Structural Map Linking section allows for the specification of hyperlinks between different components of a METS structure delineated in a structural map.  structLink contains a single, repeatable element, smLink.  Each smLink element indicates a hyperlink between two nodes in the structMap.  The structMap nodes recorded in smLink are identified using their XML ID attribute	values.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'structLinkType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 953, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}smLink uses Python identifier smLink
    __smLink = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'smLink'), 'smLink', '__httpwww_loc_govMETS_structLinkType_httpwww_loc_govMETSsmLink', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 960, 3), )

    
    smLink = property(__smLink.value, __smLink.set, None, ' \n\t\t\t\t\t\tThe Structural Map Link element <smLink> identifies a hyperlink between two nodes in the structural map. You would use <smLink>, for instance, to note the existence of hypertext links between web pages, if you wished to record those links within METS. NOTE: <smLink> is an empty element. The location of the <smLink> element to which the <smLink> element is pointing MUST be stored in the xlink:href attribute.\n\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}smLinkGrp uses Python identifier smLinkGrp
    __smLinkGrp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'smLinkGrp'), 'smLinkGrp', '__httpwww_loc_govMETS_structLinkType_httpwww_loc_govMETSsmLinkGrp', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1017, 3), )

    
    smLinkGrp = property(__smLinkGrp.value, __smLinkGrp.set, None, '\n\t\t\t\t\t\tThe structMap link group element <smLinkGrp> provides an implementation of xlink:extendLink, and provides xlink compliant mechanisms for establishing xlink:arcLink type links between 2 or more <div> elements in <structMap> element(s) occurring within the same METS document or different METS documents.  The smLinkGrp could be used as an alternative to the <smLink> element to establish a one-to-one link between <div> elements in the same METS document in a fully xlink compliant manner.  However, it can also be used to establish one-to-many or many-to-many links between <div> elements. For example, if a METS document contains two <structMap> elements, one of which represents a purely logical structure and one of which represents a purely physical structure, the <smLinkGrp> element would provide a means of mapping a <div> representing a logical entity (for example, a newspaper article) with multiple <div> elements in the physical <structMap> representing the physical areas that  together comprise the logical entity (for example, the <div> elements representing the page areas that together comprise the newspaper article).\n\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_structLinkType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1084, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1084, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __smLink.name() : __smLink,
        __smLinkGrp.name() : __smLinkGrp
    })
    _AttributeMap.update({
        __ID.name() : __ID
    })
Namespace.addCategoryObject('typeBinding', 'structLinkType', structLinkType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """
									The structMap locator link element <smLocatorLink> is of xlink:type "locator".  It provides a means of identifying a <div> element that will participate in one or more of the links specified by means of <smArcLink> elements within the same <smLinkGrp>. The participating <div> element that is represented by the <smLocatorLink> is identified by means of a URI in the associate xlink:href attribute.  The lowest level of this xlink:href URI value should be a fragment identifier that references the ID value that identifies the relevant <div> element.  For example, "xlink:href='#div20'" where "div20" is the ID value that identifies the pertinent <div> in the current METS document. Although not required by the xlink specification, an <smLocatorLink> element will typically include an xlink:label attribute in this context, as the <smArcLink> elements will reference these labels to establish the from and to sides of each arc link.
								"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1031, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_4_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1032, 8)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1032, 8)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'href'), 'href', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI, required=True)
    __href._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 5, 2)
    __href._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 49, 4)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)
    __role._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 6, 2)
    __role._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 50, 4)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 8, 2)
    __title._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 51, 4)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'label'), 'label', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinklabel', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 30, 2)
    __label._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 52, 4)
    
    label = property(__label.value, __label.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_4_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default='locator')
    __type._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 48, 4)
    __type._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 48, 4)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __href.name() : __href,
        __role.name() : __role,
        __title.name() : __title,
        __label.name() : __label,
        __type.name() : __type
    })



# Complex type {http://www.loc.gov/METS/}behaviorSecType with content type ELEMENT_ONLY
class behaviorSecType (pyxb.binding.basis.complexTypeDefinition):
    """behaviorSecType: Complex Type for Behavior Sections
			Behaviors are executable code which can be associated with parts of a METS object.  The behaviorSec element is used to group individual behaviors within a hierarchical structure.  Such grouping can be useful to organize families of behaviors together or to indicate other relationships between particular behaviors.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'behaviorSecType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1092, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}behaviorSec uses Python identifier behaviorSec
    __behaviorSec = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'behaviorSec'), 'behaviorSec', '__httpwww_loc_govMETS_behaviorSecType_httpwww_loc_govMETSbehaviorSec', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1099, 3), )

    
    behaviorSec = property(__behaviorSec.value, __behaviorSec.set, None, None)

    
    # Element {http://www.loc.gov/METS/}behavior uses Python identifier behavior
    __behavior = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'behavior'), 'behavior', '__httpwww_loc_govMETS_behaviorSecType_httpwww_loc_govMETSbehavior', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1100, 3), )

    
    behavior = property(__behavior.value, __behavior.set, None, '\n\t\t\t\t\t\tA behavior element <behavior> can be used to associate executable behaviors with content in the METS document. This element has an interface definition <interfaceDef> element that represents an abstract definition of a set of behaviors represented by a particular behavior. A <behavior> element also has a behavior mechanism <mechanism> element, a module of executable code that implements and runs the behavior defined abstractly by the interface definition.\n\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_behaviorSecType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1108, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1108, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CREATED'), 'CREATED', '__httpwww_loc_govMETS_behaviorSecType_CREATED', pyxb.binding.datatypes.dateTime)
    __CREATED._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1114, 2)
    __CREATED._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1114, 2)
    
    CREATED = property(__CREATED.value, __CREATED.set, None, 'CREATED (dateTime/O): Specifies the date and time of creation for the <behaviorSec>\n\t\t\t\t')

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_behaviorSecType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1120, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1120, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): A text description of the behavior section.\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __behaviorSec.name() : __behaviorSec,
        __behavior.name() : __behavior
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __CREATED.name() : __CREATED,
        __LABEL.name() : __LABEL
    })
Namespace.addCategoryObject('typeBinding', 'behaviorSecType', behaviorSecType)


# Complex type {http://www.loc.gov/METS/}behaviorType with content type ELEMENT_ONLY
class behaviorType (pyxb.binding.basis.complexTypeDefinition):
    """behaviorType: Complex Type for Behaviors
			 A behavior can be used to associate executable behaviors with content in the METS object.  A behavior element has an interface definition element that represents an abstract definition  of the set  of behaviors represented by a particular behavior.  A behavior element also has an behavior  mechanism which is a module of executable code that implements and runs the behavior defined abstractly by the interface definition.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'behaviorType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1128, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}interfaceDef uses Python identifier interfaceDef
    __interfaceDef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'interfaceDef'), 'interfaceDef', '__httpwww_loc_govMETS_behaviorType_httpwww_loc_govMETSinterfaceDef', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1135, 3), )

    
    interfaceDef = property(__interfaceDef.value, __interfaceDef.set, None, '\n\t\t\t\t\t\tThe interface definition <interfaceDef> element contains a pointer to an abstract definition of a single behavior or a set of related behaviors that are associated with the content of a METS object. The interface definition object to which the <interfaceDef> element points using xlink:href could be another digital object, or some other entity, such as a text file which describes the interface or a Web Services Description Language (WSDL) file. Ideally, an interface definition object contains metadata that describes a set of behaviors or methods. It may also contain files that describe the intended usage of the behaviors, and possibly files that represent different expressions of the interface definition.\t\t\n\t\t\t')

    
    # Element {http://www.loc.gov/METS/}mechanism uses Python identifier mechanism
    __mechanism = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mechanism'), 'mechanism', '__httpwww_loc_govMETS_behaviorType_httpwww_loc_govMETSmechanism', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1142, 3), )

    
    mechanism = property(__mechanism.value, __mechanism.set, None, ' \n\t\t\t\t\tA mechanism element <mechanism> contains a pointer to an executable code module that implements a set of behaviors defined by an interface definition. The <mechanism> element will be a pointer to another object (a mechanism object). A mechanism object could be another METS object, or some other entity (e.g., a WSDL file). A mechanism object should contain executable code, pointers to executable code, or specifications for binding to network services (e.g., web services).\n\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_behaviorType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1150, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1150, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. In the case of a <behavior> element that applies to a <transformFile> element, the ID value must be present and would be referenced from the transformFile/@TRANSFORMBEHAVIOR attribute. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute STRUCTID uses Python identifier STRUCTID
    __STRUCTID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'STRUCTID'), 'STRUCTID', '__httpwww_loc_govMETS_behaviorType_STRUCTID', pyxb.binding.datatypes.IDREFS)
    __STRUCTID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1156, 2)
    __STRUCTID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1156, 2)
    
    STRUCTID = property(__STRUCTID.value, __STRUCTID.set, None, 'STRUCTID (IDREFS/O): An XML IDREFS attribute used to link a <behavior>  to one or more <div> elements within a <structMap> in the METS document. The content to which the STRUCTID points is considered input to the executable behavior mechanism defined for the behavior.  If the <behavior> applies to one or more <div> elements, then the STRUCTID attribute must be present.\n\t\t\t\t')

    
    # Attribute BTYPE uses Python identifier BTYPE
    __BTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'BTYPE'), 'BTYPE', '__httpwww_loc_govMETS_behaviorType_BTYPE', pyxb.binding.datatypes.string)
    __BTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1162, 2)
    __BTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1162, 2)
    
    BTYPE = property(__BTYPE.value, __BTYPE.set, None, 'BTYPE (string/O): The behavior type provides a means of categorizing the related behavior.')

    
    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CREATED'), 'CREATED', '__httpwww_loc_govMETS_behaviorType_CREATED', pyxb.binding.datatypes.dateTime)
    __CREATED._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1167, 2)
    __CREATED._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1167, 2)
    
    CREATED = property(__CREATED.value, __CREATED.set, None, 'CREATED (dateTime/O): The dateTime of creation for the behavior. \n\t\t\t\t')

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_behaviorType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1173, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1173, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): A text description of the behavior.  \n\t\t\t\t')

    
    # Attribute GROUPID uses Python identifier GROUPID
    __GROUPID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'GROUPID'), 'GROUPID', '__httpwww_loc_govMETS_behaviorType_GROUPID', pyxb.binding.datatypes.string)
    __GROUPID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1179, 2)
    __GROUPID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1179, 2)
    
    GROUPID = property(__GROUPID.value, __GROUPID.set, None, 'GROUPID (string/O): An identifier that establishes a correspondence between the given behavior and other behaviors, typically used to facilitate versions of behaviors.\n\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_behaviorType_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1185, 2)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1185, 2)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREFS/O): An optional attribute listing the XML ID values of administrative metadata sections within the METS document pertaining to this behavior.\n\t\t\t\t')

    _ElementMap.update({
        __interfaceDef.name() : __interfaceDef,
        __mechanism.name() : __mechanism
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __STRUCTID.name() : __STRUCTID,
        __BTYPE.name() : __BTYPE,
        __CREATED.name() : __CREATED,
        __LABEL.name() : __LABEL,
        __GROUPID.name() : __GROUPID,
        __ADMID.name() : __ADMID
    })
Namespace.addCategoryObject('typeBinding', 'behaviorType', behaviorType)


# Complex type {http://www.loc.gov/METS/}mdSecType with content type ELEMENT_ONLY
class mdSecType (pyxb.binding.basis.complexTypeDefinition):
    """mdSecType: Complex Type for Metadata Sections
			A generic framework for pointing to/including metadata within a METS document, a la Warwick Framework.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'mdSecType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1213, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}mdRef uses Python identifier mdRef
    __mdRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mdRef'), 'mdRef', '__httpwww_loc_govMETS_mdSecType_httpwww_loc_govMETSmdRef', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1220, 3), )

    
    mdRef = property(__mdRef.value, __mdRef.set, None, '\n\t\t\t\t\t\tThe metadata reference element <mdRef> element is a generic element used throughout the METS schema to provide a pointer to metadata which resides outside the METS document.  NB: <mdRef> is an empty element.  The location of the metadata must be recorded in the xlink:href attribute, supplemented by the XPTR attribute as needed.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}mdWrap uses Python identifier mdWrap
    __mdWrap = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mdWrap'), 'mdWrap', '__httpwww_loc_govMETS_mdSecType_httpwww_loc_govMETSmdWrap', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1251, 3), )

    
    mdWrap = property(__mdWrap.value, __mdWrap.set, None, ' \n\t\t\t\t\t\tA metadata wrapper element <mdWrap> provides a wrapper around metadata embedded within a METS document. The element is repeatable. Such metadata can be in one of two forms: 1) XML-encoded metadata, with the XML-encoding identifying itself as belonging to a namespace other than the METS document namespace. 2) Any arbitrary binary or textual form, PROVIDED that the metadata is Base64 encoded and wrapped in a <binData> element within the internal descriptive metadata element.\n\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_mdSecType_ID', pyxb.binding.datatypes.ID, required=True)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1295, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1295, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/R): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. The ID attribute on the <dmdSec>, <techMD>, <sourceMD>, <rightsMD> and <digiprovMD> elements (which are all of mdSecType) is required, and its value should be referenced from one or more DMDID attributes (when the ID identifies a <dmdSec> element) or ADMID attributes (when the ID identifies a <techMD>, <sourceMD>, <rightsMD> or <digiprovMD> element) that are associated with other elements in the METS document. The following elements support references to a <dmdSec> via a DMDID attribute: <file>, <stream>, <div>.  The following elements support references to <techMD>, <sourceMD>, <rightsMD> and <digiprovMD> elements via an ADMID attribute: <metsHdr>, <dmdSec>, <techMD>, <sourceMD>, <rightsMD>, <digiprovMD>, <fileGrp>, <file>, <stream>, <div>, <area>, <behavior>. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute GROUPID uses Python identifier GROUPID
    __GROUPID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'GROUPID'), 'GROUPID', '__httpwww_loc_govMETS_mdSecType_GROUPID', pyxb.binding.datatypes.string)
    __GROUPID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1301, 2)
    __GROUPID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1301, 2)
    
    GROUPID = property(__GROUPID.value, __GROUPID.set, None, 'GROUPID (string/O): This identifier is used to indicate that different metadata sections may be considered as part of a group. Two metadata sections with the same GROUPID value are to be considered part of the same group. For example this facility might be used to group changed versions of the same metadata if previous versions are maintained in a file for tracking purposes.\n\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_mdSecType_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1307, 2)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1307, 2)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREFS/O): Contains the ID attribute values of the <digiprovMD>, <techMD>, <sourceMD> and/or <rightsMD> elements within the <amdSec> of the METS document that contain administrative metadata pertaining to the current mdSecType element. Typically used in this context to reference preservation metadata (digiprovMD) which applies to the current metadata. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CREATED'), 'CREATED', '__httpwww_loc_govMETS_mdSecType_CREATED', pyxb.binding.datatypes.dateTime)
    __CREATED._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1313, 2)
    __CREATED._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1313, 2)
    
    CREATED = property(__CREATED.value, __CREATED.set, None, 'CREATED (dateTime/O): Specifies the date and time of creation for the metadata.\n\t\t\t\t')

    
    # Attribute STATUS uses Python identifier STATUS
    __STATUS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'STATUS'), 'STATUS', '__httpwww_loc_govMETS_mdSecType_STATUS', pyxb.binding.datatypes.string)
    __STATUS._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1319, 2)
    __STATUS._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1319, 2)
    
    STATUS = property(__STATUS.value, __STATUS.set, None, 'STATUS (string/O): Indicates the status of this metadata (e.g., superseded, current, etc.).\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __mdRef.name() : __mdRef,
        __mdWrap.name() : __mdWrap
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __GROUPID.name() : __GROUPID,
        __ADMID.name() : __ADMID,
        __CREATED.name() : __CREATED,
        __STATUS.name() : __STATUS
    })
Namespace.addCategoryObject('typeBinding', 'mdSecType', mdSecType)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """
									The xml data wrapper element <xmlData> is used to contain XML encoded metadata. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> is set to “lax”. Therefore, if the source schema and its location are identified by means of an XML schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element. 												
								"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1271, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """
						The file content element <FContent> is used to identify a content file contained internally within a METS document. The content file must be either Base64 encoded and contained within the subsidiary <binData> wrapper element, or consist of XML information and be contained within the subsidiary <xmlData> wrapper element.
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1364, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}binData uses Python identifier binData
    __binData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'binData'), 'binData', '__httpwww_loc_govMETS_CTD_ANON_6_httpwww_loc_govMETSbinData', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1366, 6), )

    
    binData = property(__binData.value, __binData.set, None, '\n\t\t\t\t\t\t\t\t\tA binary data wrapper element <binData> is used to contain a Base64 encoded file.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}xmlData uses Python identifier xmlData
    __xmlData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'xmlData'), 'xmlData', '__httpwww_loc_govMETS_CTD_ANON_6_httpwww_loc_govMETSxmlData', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1373, 6), )

    
    xmlData = property(__xmlData.value, __xmlData.set, None, '\n\t\t\t\t\t\t\t\t\tAn xml data wrapper element <xmlData> is used to contain  an XML encoded file. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> element is set to \u201clax\u201d. Therefore, if the source schema and its location are identified by means of an xsi:schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element.\n\t\t\t\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_6_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1386, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1386, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute USE uses Python identifier USE
    __USE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'USE'), 'USE', '__httpwww_loc_govMETS_CTD_ANON_6_USE', pyxb.binding.datatypes.string)
    __USE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1392, 5)
    __USE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1392, 5)
    
    USE = property(__USE.value, __USE.set, None, 'USE (string/O): A tagging attribute to indicate the intended use of the specific copy of the file represented by the <FContent> element (e.g., service master, archive master). A USE attribute can be expressed at the<fileGrp> level, the <file> level, the <FLocat> level and/or the <FContent> level.  A USE attribute value at the <fileGrp> level should pertain to all of the files in the <fileGrp>.  A USE attribute at the <file> level should pertain to all copies of the file as represented by subsidiary <FLocat> and/or <FContent> elements.  A USE attribute at the <FLocat> or <FContent> level pertains to the particular copy of the file that is either referenced (<FLocat>) or wrapped (<FContent>).\n\t\t\t\t\t\t\t')

    _ElementMap.update({
        __binData.name() : __binData,
        __xmlData.name() : __xmlData
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __USE.name() : __USE
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """
									An xml data wrapper element <xmlData> is used to contain  an XML encoded file. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> element is set to “lax”. Therefore, if the source schema and its location are identified by means of an xsi:schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element.
								"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1379, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_8 (metsType):
    """METS: Metadata Encoding and Transmission Standard.
				METS is intended to provide a standardized XML format for transmission of complex digital library objects between systems.  As such, it can be seen as filling a role similar to that defined for the Submission Information Package (SIP), Archival Information Package (AIP) and Dissemination Information Package (DIP) in the Reference Model for an Open Archival Information System. The root element <mets> establishes the container for the information being stored and/or transmitted by the standard.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 229, 2)
    _ElementMap = metsType._ElementMap.copy()
    _AttributeMap = metsType._AttributeMap.copy()
    # Base type is metsType
    
    # Element metsHdr ({http://www.loc.gov/METS/}metsHdr) inherited from {http://www.loc.gov/METS/}metsType
    
    # Element dmdSec ({http://www.loc.gov/METS/}dmdSec) inherited from {http://www.loc.gov/METS/}metsType
    
    # Element amdSec ({http://www.loc.gov/METS/}amdSec) inherited from {http://www.loc.gov/METS/}metsType
    
    # Element fileSec ({http://www.loc.gov/METS/}fileSec) inherited from {http://www.loc.gov/METS/}metsType
    
    # Element structMap ({http://www.loc.gov/METS/}structMap) inherited from {http://www.loc.gov/METS/}metsType
    
    # Element structLink ({http://www.loc.gov/METS/}structLink) inherited from {http://www.loc.gov/METS/}metsType
    
    # Element behaviorSec ({http://www.loc.gov/METS/}behaviorSec) inherited from {http://www.loc.gov/METS/}metsType
    
    # Attribute ID inherited from {http://www.loc.gov/METS/}metsType
    
    # Attribute OBJID inherited from {http://www.loc.gov/METS/}metsType
    
    # Attribute LABEL inherited from {http://www.loc.gov/METS/}metsType
    
    # Attribute TYPE inherited from {http://www.loc.gov/METS/}metsType
    
    # Attribute PROFILE inherited from {http://www.loc.gov/METS/}metsType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """agent: 
								The agent element <agent> provides for various parties and their roles with respect to the METS record to be documented.  
								"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 256, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'name'), 'name', '__httpwww_loc_govMETS_CTD_ANON_9_httpwww_loc_govMETSname', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 258, 9), )

    
    name = property(__name.value, __name.set, None, ' \n\t\t\t\t\t\t\t\t\t\t\tThe element <name> can be used to record the full name of the document agent.\n\t\t\t\t\t\t\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}note uses Python identifier note
    __note = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'note'), 'note', '__httpwww_loc_govMETS_CTD_ANON_9_httpwww_loc_govMETSnote', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 265, 9), )

    
    note = property(__note.value, __note.set, None, " \n\t\t\t\t\t\t\t\t\t\t\tThe <note> element can be used to record any additional information regarding the agent's activities with respect to the METS document.\n\t\t\t\t\t\t\t\t\t\t\t")

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_9_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 273, 8)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 273, 8)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t\t')

    
    # Attribute ROLE uses Python identifier ROLE
    __ROLE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ROLE'), 'ROLE', '__httpwww_loc_govMETS_CTD_ANON_9_ROLE', STD_ANON, required=True)
    __ROLE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 279, 8)
    __ROLE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 279, 8)
    
    ROLE = property(__ROLE.value, __ROLE.set, None, 'ROLE (string/R): Specifies the function of the agent with respect to the METS record. The allowed values are:\nCREATOR: The person(s) or institution(s) responsible for the METS document.\nEDITOR: The person(s) or institution(s) that prepares the metadata for encoding.\nARCHIVIST: The person(s) or institution(s) responsible for the document/collection.\nPRESERVATION: The person(s) or institution(s) responsible for preservation functions.\nDISSEMINATOR: The person(s) or institution(s) responsible for dissemination functions.\nCUSTODIAN: The person(s) or institution(s) charged with the oversight of a document/collection.\nIPOWNER: Intellectual Property Owner: The person(s) or institution holding copyright, trade or service marks or other intellectual property rights for the object.\nOTHER: Use OTHER if none of the preceding values pertains and clarify the type and location specifier being used in the OTHERROLE attribute (see below).\n\t\t\t\t\t\t\t\t\t\t')

    
    # Attribute OTHERROLE uses Python identifier OTHERROLE
    __OTHERROLE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OTHERROLE'), 'OTHERROLE', '__httpwww_loc_govMETS_CTD_ANON_9_OTHERROLE', pyxb.binding.datatypes.string)
    __OTHERROLE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 305, 8)
    __OTHERROLE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 305, 8)
    
    OTHERROLE = property(__OTHERROLE.value, __OTHERROLE.set, None, 'OTHERROLE (string/O): Denotes a role not contained in the allowed values set if OTHER is indicated in the ROLE attribute.\n\t\t\t\t\t\t\t\t\t\t')

    
    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TYPE'), 'TYPE', '__httpwww_loc_govMETS_CTD_ANON_9_TYPE', STD_ANON_)
    __TYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 311, 8)
    __TYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 311, 8)
    
    TYPE = property(__TYPE.value, __TYPE.set, None, 'TYPE (string/O): is used to specify the type of AGENT. It must be one of the following values:\nINDIVIDUAL: Use if an individual has served as the agent.\nORGANIZATION: Use if an institution, corporate body, association, non-profit enterprise, government, religious body, etc. has served as the agent.\nOTHER: Use OTHER if none of the preceding values pertain and clarify the type of agent specifier being used in the OTHERTYPE attribute\n\t\t\t\t\t\t\t\t\t\t')

    
    # Attribute OTHERTYPE uses Python identifier OTHERTYPE
    __OTHERTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OTHERTYPE'), 'OTHERTYPE', '__httpwww_loc_govMETS_CTD_ANON_9_OTHERTYPE', pyxb.binding.datatypes.string)
    __OTHERTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 327, 8)
    __OTHERTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 327, 8)
    
    OTHERTYPE = property(__OTHERTYPE.value, __OTHERTYPE.set, None, 'OTHERTYPE (string/O): Specifies the type of agent when the value OTHER is indicated in the TYPE attribute.\n\t\t\t\t\t\t\t\t\t\t')

    _ElementMap.update({
        __name.name() : __name,
        __note.name() : __note
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __ROLE.name() : __ROLE,
        __OTHERROLE.name() : __OTHERROLE,
        __TYPE.name() : __TYPE,
        __OTHERTYPE.name() : __OTHERTYPE
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (fileGrpType):
    """ 
									A sequence of file group elements <fileGrp> can be used group the digital files comprising the content of a METS object either into a flat arrangement or, because each file group element can itself contain one or more  file group elements,  into a nested (hierarchical) arrangement. In the case where the content files are images of different formats and resolutions, for example, one could group the image content files by format and create a separate <fileGrp> for each image format/resolution such as:
-- one <fileGrp> for the thumbnails of the images
-- one <fileGrp> for the higher resolution JPEGs of the image 
-- one <fileGrp> for the master archival TIFFs of the images 
For a text resource with a variety of content file types one might group the content files at the highest level by type,  and then use the <fileGrp> element’s nesting capabilities to subdivide a <fileGrp> by format within the type, such as:
-- one <fileGrp> for all of the page images with nested <fileGrp> elements for each image format/resolution (tiff, jpeg, gif)
-- one <fileGrp> for a PDF version of all the pages of the document 
-- one <fileGrp> for  a TEI encoded XML version of the entire document or each of its pages.
A <fileGrp> may contain zero or more <fileGrp> elements and or <file> elements.					
								"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 454, 7)
    _ElementMap = fileGrpType._ElementMap.copy()
    _AttributeMap = fileGrpType._AttributeMap.copy()
    # Base type is fileGrpType
    
    # Element fileGrp ({http://www.loc.gov/METS/}fileGrp) inherited from {http://www.loc.gov/METS/}fileGrpType
    
    # Element file ({http://www.loc.gov/METS/}file) inherited from {http://www.loc.gov/METS/}fileGrpType
    
    # Attribute ID inherited from {http://www.loc.gov/METS/}fileGrpType
    
    # Attribute VERSDATE inherited from {http://www.loc.gov/METS/}fileGrpType
    
    # Attribute ADMID inherited from {http://www.loc.gov/METS/}fileGrpType
    
    # Attribute USE inherited from {http://www.loc.gov/METS/}fileGrpType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_11 (structLinkType):
    """ 
						The structural link section element <structLink> allows for the specification of hyperlinks between the different components of a METS structure that are delineated in a structural map. This element is a container for a single, repeatable element, <smLink> which indicates a hyperlink between two nodes in the structural map. The <structLink> section in the METS document is identified using its XML ID attributes.
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 483, 4)
    _ElementMap = structLinkType._ElementMap.copy()
    _AttributeMap = structLinkType._AttributeMap.copy()
    # Base type is structLinkType
    
    # Element smLink ({http://www.loc.gov/METS/}smLink) inherited from {http://www.loc.gov/METS/}structLinkType
    
    # Element smLinkGrp ({http://www.loc.gov/METS/}smLinkGrp) inherited from {http://www.loc.gov/METS/}structLinkType
    
    # Attribute ID inherited from {http://www.loc.gov/METS/}structLinkType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })



# Complex type {http://www.loc.gov/METS/}divType with content type ELEMENT_ONLY
class divType (pyxb.binding.basis.complexTypeDefinition):
    """divType: Complex Type for Divisions
					The METS standard represents a document structurally as a series of nested div elements, that is, as a hierarchy (e.g., a book, which is composed of chapters, which are composed of subchapters, which are composed of text).  Every div node in the structural map hierarchy may be connected (via subsidiary mptr or fptr elements) to content files which represent that div's portion of the whole document.

SPECIAL NOTE REGARDING DIV ATTRIBUTE VALUES:
to clarify the differences between the ORDER, ORDERLABEL, and LABEL attributes for the <div> element, imagine a text with 10 roman numbered pages followed by 10 arabic numbered pages. Page iii would have an ORDER of "3", an ORDERLABEL of "iii" and a LABEL of "Page iii", while page 3 would have an ORDER of "13", an ORDERLABEL of "3" and a LABEL of "Page 3".
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'divType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 649, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}mptr uses Python identifier mptr
    __mptr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'mptr'), 'mptr', '__httpwww_loc_govMETS_divType_httpwww_loc_govMETSmptr', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 660, 3), )

    
    mptr = property(__mptr.value, __mptr.set, None, ' \n\t\t\t\t\t\tLike the <fptr> element, the METS pointer element <mptr> represents digital content that manifests its parent <div> element. Unlike the <fptr>, which either directly or indirectly points to content represented in the <fileSec> of the parent METS document, the <mptr> element points to content represented by an external METS document. Thus, this element allows multiple discrete and separate METS documents to be organized at a higher level by a separate METS document. For example, METS documents representing the individual issues in the series of a journal could be grouped together and organized by a higher level METS document that represents the entire journal series. Each of the <div> elements in the <structMap> of the METS document representing the journal series would point to a METS document representing an issue.  It would do so via a child <mptr> element. Thus the <mptr> element gives METS users considerable flexibility in managing the depth of the <structMap> hierarchy of individual METS documents. The <mptr> element points to an external METS document by means of an xlink:href attribute and associated XLink attributes. \t\t\t\t\t\t\t\t\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}fptr uses Python identifier fptr
    __fptr = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'fptr'), 'fptr', '__httpwww_loc_govMETS_divType_httpwww_loc_govMETSfptr', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 683, 3), )

    
    fptr = property(__fptr.value, __fptr.set, None, '\n\t\t\t\t\t\tThe <fptr> or file pointer element represents digital content that manifests its parent <div> element. The content represented by an <fptr> element must consist of integral files or parts of files that are represented by <file> elements in the <fileSec>. Via its FILEID attribute,  an <fptr> may point directly to a single integral <file> element that manifests a structural division. However, an <fptr> element may also govern an <area> element,  a <par>, or  a <seq>  which in turn would point to the relevant file or files. A child <area> element can point to part of a <file> that manifests a division, while the <par> and <seq> elements can point to multiple files or parts of files that together manifest a division. More than one <fptr> element can be associated with a <div> element. Typically sibling <fptr> elements represent alternative versions, or manifestations, of the same content\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}div uses Python identifier div
    __div = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'div'), 'div', '__httpwww_loc_govMETS_divType_httpwww_loc_govMETSdiv', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 734, 3), )

    
    div = property(__div.value, __div.set, None, None)

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_divType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 736, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 736, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute DMDID uses Python identifier DMDID
    __DMDID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'DMDID'), 'DMDID', '__httpwww_loc_govMETS_divType_DMDID', pyxb.binding.datatypes.IDREFS)
    __DMDID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 743, 2)
    __DMDID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 743, 2)
    
    DMDID = property(__DMDID.value, __DMDID.set, None, 'DMDID (IDREFS/O): Contains the ID attribute values identifying the <dmdSec>, elements in the METS document that contain or link to descriptive metadata pertaining to the structural division represented by the current <div> element.  For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_divType_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 749, 2)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 749, 2)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREFS/O): Contains the ID attribute values identifying the <rightsMD>, <sourceMD>, <techMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain or link to administrative metadata pertaining to the structural division represented by the <div> element. Typically the <div> ADMID attribute would be used to identify the <rightsMD> element or elements that pertain to the <div>, but it could be used anytime there was a need to link a <div> with pertinent administrative metadata. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute TYPE uses Python identifier TYPE
    __TYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TYPE'), 'TYPE', '__httpwww_loc_govMETS_divType_TYPE', pyxb.binding.datatypes.string)
    __TYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 755, 2)
    __TYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 755, 2)
    
    TYPE = property(__TYPE.value, __TYPE.set, None, 'TYPE (string/O): An attribute that specifies the type of structural division that the <div> element represents. Possible <div> TYPE attribute values include: chapter, article, page, track, segment, section etc. METS places no constraints on the possible TYPE values. Suggestions for controlled vocabularies for TYPE may be found on the METS website.\n\t\t\t\t')

    
    # Attribute CONTENTIDS uses Python identifier CONTENTIDS
    __CONTENTIDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CONTENTIDS'), 'CONTENTIDS', '__httpwww_loc_govMETS_divType_CONTENTIDS', URIs)
    __CONTENTIDS._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 761, 5)
    __CONTENTIDS._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 761, 5)
    
    CONTENTIDS = property(__CONTENTIDS.value, __CONTENTIDS.set, None, 'CONTENTIDS (URI/O): Content IDs for the content represented by the <div> (equivalent to DIDL DII or Digital Item Identifier, a unique external ID).\n\t\t\t\t')

    
    # Attribute ORDER uses Python identifier ORDER
    __ORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ORDER'), 'ORDER', '__httpwww_loc_govMETS_divType_ORDER', pyxb.binding.datatypes.integer)
    __ORDER._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1591, 2)
    __ORDER._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1591, 2)
    
    ORDER = property(__ORDER.value, __ORDER.set, None, "ORDER (integer/O): A representation of the element's order among its siblings (e.g., its absolute, numeric sequence). For an example, and clarification of the distinction between ORDER and ORDERLABEL, see the description of the ORDERLABEL attribute.\n\t\t\t\t")

    
    # Attribute ORDERLABEL uses Python identifier ORDERLABEL
    __ORDERLABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ORDERLABEL'), 'ORDERLABEL', '__httpwww_loc_govMETS_divType_ORDERLABEL', pyxb.binding.datatypes.string)
    __ORDERLABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1597, 2)
    __ORDERLABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1597, 2)
    
    ORDERLABEL = property(__ORDERLABEL.value, __ORDERLABEL.set, None, "ORDERLABEL (string/O): A representation of the element's order among its siblings (e.g., \u201cxii\u201d), or of any non-integer native numbering system. It is presumed that this value will still be machine actionable (e.g., it would support \u2018go to page ___\u2019 function), and it should not be used as a replacement/substitute for the LABEL attribute. To understand the differences between ORDER, ORDERLABEL and LABEL, imagine a text with 10 roman numbered pages followed by 10 arabic numbered pages. Page iii would have an ORDER of \u201c3\u201d, an ORDERLABEL of \u201ciii\u201d and a LABEL of \u201cPage iii\u201d, while page 3 would have an ORDER of \u201c13\u201d, an ORDERLABEL of \u201c3\u201d and a LABEL of \u201cPage 3\u201d.\n\t\t\t\t")

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_divType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1603, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1603, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): An attribute used, for example, to identify a <div> to an end user viewing the document. Thus a hierarchical arrangement of the <div> LABEL values could provide a table of contents to the digital content represented by a METS document and facilitate the users\u2019 navigation of the digital object. Note that a <div> LABEL should be specific to its level in the structural map. In the case of a book with chapters, the book <div> LABEL should have the book title and the chapter <div>; LABELs should have the individual chapter titles, rather than having the chapter <div> LABELs combine both book title and chapter title . For further of the distinction between LABEL and ORDERLABEL see the description of the ORDERLABEL attribute.\n\t\t\t\t')

    
    # Attribute {http://www.w3.org/1999/xlink}label uses Python identifier label
    __label = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'label'), 'label', '__httpwww_loc_govMETS_divType_httpwww_w3_org1999xlinklabel', pyxb.binding.datatypes.string)
    __label._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 30, 2)
    __label._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 767, 2)
    
    label = property(__label.value, __label.set, None, None)

    _ElementMap.update({
        __mptr.name() : __mptr,
        __fptr.name() : __fptr,
        __div.name() : __div
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __DMDID.name() : __DMDID,
        __ADMID.name() : __ADMID,
        __TYPE.name() : __TYPE,
        __CONTENTIDS.name() : __CONTENTIDS,
        __ORDER.name() : __ORDER,
        __ORDERLABEL.name() : __ORDERLABEL,
        __LABEL.name() : __LABEL,
        __label.name() : __label
    })
Namespace.addCategoryObject('typeBinding', 'divType', divType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """ 
						Like the <fptr> element, the METS pointer element <mptr> represents digital content that manifests its parent <div> element. Unlike the <fptr>, which either directly or indirectly points to content represented in the <fileSec> of the parent METS document, the <mptr> element points to content represented by an external METS document. Thus, this element allows multiple discrete and separate METS documents to be organized at a higher level by a separate METS document. For example, METS documents representing the individual issues in the series of a journal could be grouped together and organized by a higher level METS document that represents the entire journal series. Each of the <div> elements in the <structMap> of the METS document representing the journal series would point to a METS document representing an issue.  It would do so via a child <mptr> element. Thus the <mptr> element gives METS users considerable flexibility in managing the depth of the <structMap> hierarchy of individual METS documents. The <mptr> element points to an external METS document by means of an xlink:href attribute and associated XLink attributes. 								
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 666, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_12_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 667, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 667, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute CONTENTIDS uses Python identifier CONTENTIDS
    __CONTENTIDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CONTENTIDS'), 'CONTENTIDS', '__httpwww_loc_govMETS_CTD_ANON_12_CONTENTIDS', URIs)
    __CONTENTIDS._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 675, 8)
    __CONTENTIDS._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 675, 8)
    
    CONTENTIDS = property(__CONTENTIDS.value, __CONTENTIDS.set, None, 'CONTENTIDS (URI/O): Content IDs for the content represented by the <mptr> (equivalent to DIDL DII or Digital Item Identifier, a unique external ID).\n\t\t\t\t            ')

    
    # Attribute LOCTYPE uses Python identifier LOCTYPE
    __LOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LOCTYPE'), 'LOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_12_LOCTYPE', STD_ANON_10, required=True)
    __LOCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1679, 2)
    __LOCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1679, 2)
    
    LOCTYPE = property(__LOCTYPE.value, __LOCTYPE.set, None, 'LOCTYPE (string/R): Specifies the locator type used in the xlink:href attribute. Valid values for LOCTYPE are: \n\t\t\t\t\tARK\n\t\t\t\t\tURN\n\t\t\t\t\tURL\n\t\t\t\t\tPURL\n\t\t\t\t\tHANDLE\n\t\t\t\t\tDOI\n\t\t\t\t\tOTHER\n\t\t\t\t')

    
    # Attribute OTHERLOCTYPE uses Python identifier OTHERLOCTYPE
    __OTHERLOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OTHERLOCTYPE'), 'OTHERLOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_12_OTHERLOCTYPE', pyxb.binding.datatypes.string)
    __OTHERLOCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1703, 2)
    __OTHERLOCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1703, 2)
    
    OTHERLOCTYPE = property(__OTHERLOCTYPE.value, __OTHERLOCTYPE.set, None, 'OTHERLOCTYPE (string/O): Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although optional, it is strongly recommended when OTHER is used.\n\t\t\t\t')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'href'), 'href', '__httpwww_loc_govMETS_CTD_ANON_12_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    __href._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 5, 2)
    __href._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 35, 4)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_12_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)
    __role._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 6, 2)
    __role._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 36, 4)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_12_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)
    __arcrole._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 7, 2)
    __arcrole._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 37, 4)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_12_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 8, 2)
    __title._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 38, 4)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_12_httpwww_w3_org1999xlinkshow', _ImportedBinding__xlink.STD_ANON)
    __show._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 9, 2)
    __show._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 39, 4)
    
    show = property(__show.value, __show.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_12_httpwww_w3_org1999xlinkactuate', _ImportedBinding__xlink.STD_ANON_)
    __actuate._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 20, 2)
    __actuate._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 40, 4)
    
    actuate = property(__actuate.value, __actuate.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_12_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default='simple')
    __type._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 34, 4)
    __type._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 34, 4)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __CONTENTIDS.name() : __CONTENTIDS,
        __LOCTYPE.name() : __LOCTYPE,
        __OTHERLOCTYPE.name() : __OTHERLOCTYPE,
        __href.name() : __href,
        __role.name() : __role,
        __arcrole.name() : __arcrole,
        __title.name() : __title,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __type.name() : __type
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    """
						The <fptr> or file pointer element represents digital content that manifests its parent <div> element. The content represented by an <fptr> element must consist of integral files or parts of files that are represented by <file> elements in the <fileSec>. Via its FILEID attribute,  an <fptr> may point directly to a single integral <file> element that manifests a structural division. However, an <fptr> element may also govern an <area> element,  a <par>, or  a <seq>  which in turn would point to the relevant file or files. A child <area> element can point to part of a <file> that manifests a division, while the <par> and <seq> elements can point to multiple files or parts of files that together manifest a division. More than one <fptr> element can be associated with a <div> element. Typically sibling <fptr> elements represent alternative versions, or manifestations, of the same content
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 689, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}par uses Python identifier par
    __par = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'par'), 'par', '__httpwww_loc_govMETS_CTD_ANON_13_httpwww_loc_govMETSpar', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 691, 6), )

    
    par = property(__par.value, __par.set, None, ' \n\t\t\t\t\t\t\t\t\tThe <par> or parallel files element aggregates pointers to files, parts of files, and/or sequences of files or parts of files that must be played or displayed simultaneously to manifest a block of digital content represented by an <fptr> element. This might be the case, for example, with multi-media content, where a still image might have an accompanying audio track that comments on the still image. In this case, a <par> element would aggregate two <area> elements, one of which pointed to the image file and one of which pointed to the audio file that must be played in conjunction with the image. The <area> element associated with the image could be further qualified with SHAPE and COORDS attributes if only a portion of the image file was pertinent and the <area> element associated with the audio file could be further qualified with BETYPE, BEGIN, EXTTYPE, and EXTENT attributes if only a portion of the associated audio file should be played in conjunction with the image.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}seq uses Python identifier seq
    __seq = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'seq'), 'seq', '__httpwww_loc_govMETS_CTD_ANON_13_httpwww_loc_govMETSseq', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 698, 6), )

    
    seq = property(__seq.value, __seq.set, None, '  \n\t\t\t\t\t\t\t\t\tThe sequence of files element <seq> aggregates pointers to files,  parts of files and/or parallel sets of files or parts of files  that must be played or displayed sequentially to manifest a block of digital content. This might be the case, for example, if the parent <div> element represented a logical division, such as a diary entry, that spanned multiple pages of a diary and, hence, multiple page image files. In this case, a <seq> element would aggregate multiple, sequentially arranged <area> elements, each of which pointed to one of the image files that must be presented sequentially to manifest the entire diary entry. If the diary entry started in the middle of a page, then the first <area> element (representing the page on which the diary entry starts) might be further qualified, via its SHAPE and COORDS attributes, to specify the specific, pertinent area of the associated image file.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}area uses Python identifier area
    __area = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'area'), 'area', '__httpwww_loc_govMETS_CTD_ANON_13_httpwww_loc_govMETSarea', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 705, 6), )

    
    area = property(__area.value, __area.set, None, ' \n\t\t\t\t\t\t\t\t\tThe area element <area> typically points to content consisting of just a portion or area of a file represented by a <file> element in the <fileSec>. In some contexts, however, the <area> element can also point to content represented by an integral file. A single <area> element would appear as the direct child of a <fptr> element when only a portion of a <file>, rather than an integral <file>, manifested the digital content represented by the <fptr>. Multiple <area> elements would appear as the direct children of a <par> element or a <seq> element when multiple files or parts of files manifested the digital content represented by an <fptr> element. When used in the context of a <par> or <seq> element an <area> element can point either to an integral file or to a segment of a file as necessary.\n\t\t\t\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_13_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 713, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 713, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute FILEID uses Python identifier FILEID
    __FILEID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'FILEID'), 'FILEID', '__httpwww_loc_govMETS_CTD_ANON_13_FILEID', pyxb.binding.datatypes.IDREF)
    __FILEID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 719, 5)
    __FILEID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 719, 5)
    
    FILEID = property(__FILEID.value, __FILEID.set, None, 'FILEID (IDREF/O): An optional attribute that provides the XML ID identifying the <file> element that links to and/or contains the digital content represented by the <fptr>. A <fptr> element should only have a FILEID attribute value if it does not have a child <area>, <par> or <seq> element. If it has a child element, then the responsibility for pointing to the relevant content falls to this child element or its descendants.\n\t\t\t\t\t\t\t')

    
    # Attribute CONTENTIDS uses Python identifier CONTENTIDS
    __CONTENTIDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CONTENTIDS'), 'CONTENTIDS', '__httpwww_loc_govMETS_CTD_ANON_13_CONTENTIDS', URIs)
    __CONTENTIDS._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 725, 8)
    __CONTENTIDS._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 725, 8)
    
    CONTENTIDS = property(__CONTENTIDS.value, __CONTENTIDS.set, None, 'CONTENTIDS (URI/O): Content IDs for the content represented by the <fptr> (equivalent to DIDL DII or Digital Item Identifier, a unique external ID).\n\t\t\t\t            ')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __par.name() : __par,
        __seq.name() : __seq,
        __area.name() : __area
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __FILEID.name() : __FILEID,
        __CONTENTIDS.name() : __CONTENTIDS
    })



# Complex type {http://www.loc.gov/METS/}areaType with content type EMPTY
class areaType (pyxb.binding.basis.complexTypeDefinition):
    """areaType: Complex Type for Area Linking
				The area element provides for more sophisticated linking between a div element and content files representing that div, be they text, image, audio, or video files.  An area element can link a div to a point within a file, to a one-dimension segment of a file (e.g., text segment, image line, audio/video clip), or a two-dimensional section of a file 	(e.g, subsection of an image, or a subsection of the  video display of a video file.  The area element has no content; all information is recorded within its various attributes.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'areaType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 811, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_areaType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 817, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 817, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute FILEID uses Python identifier FILEID
    __FILEID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'FILEID'), 'FILEID', '__httpwww_loc_govMETS_areaType_FILEID', pyxb.binding.datatypes.IDREF, required=True)
    __FILEID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 823, 2)
    __FILEID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 823, 2)
    
    FILEID = property(__FILEID.value, __FILEID.set, None, 'FILEID (IDREF/R): An attribute which provides the XML ID value that identifies the <file> element in the <fileSec> that then points to and/or contains the digital content represented by the <area> element. It must contain an ID value represented in an ID attribute associated with a <file> element in the <fileSec> element in the same METS document.\n\t\t\t\t')

    
    # Attribute SHAPE uses Python identifier SHAPE
    __SHAPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'SHAPE'), 'SHAPE', '__httpwww_loc_govMETS_areaType_SHAPE', STD_ANON_2)
    __SHAPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 829, 2)
    __SHAPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 829, 2)
    
    SHAPE = property(__SHAPE.value, __SHAPE.set, None, 'SHAPE (string/O): An attribute that can be used as in HTML to define the shape of the relevant area within the content file pointed to by the <area> element. Typically this would be used with image content (still image or video frame) when only a portion of an integal image map pertains. If SHAPE is specified then COORDS must also be present. SHAPE should be used in conjunction with COORDS in the manner defined for the shape and coords attributes on an HTML4 <area> element. SHAPE must contain one of the following values: \nRECT \nCIRCLE\nPOLY\n\t\t\t\t')

    
    # Attribute COORDS uses Python identifier COORDS
    __COORDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'COORDS'), 'COORDS', '__httpwww_loc_govMETS_areaType_COORDS', pyxb.binding.datatypes.string)
    __COORDS._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 845, 2)
    __COORDS._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 845, 2)
    
    COORDS = property(__COORDS.value, __COORDS.set, None, 'COORDS (string/O): Specifies the coordinates in an image map for the shape of the pertinent area as specified in the SHAPE attribute. While technically optional, SHAPE and COORDS must both appear together to define the relevant area of image content. COORDS should be used in conjunction with SHAPE in the manner defined for the COORDs and SHAPE attributes on an HTML4 <area> element. COORDS must be a comma delimited string of integer value pairs representing coordinates (plus radius in the case of CIRCLE) within an image map. Number of coordinates pairs depends on shape: RECT: x1, y1, x2, y2; CIRC: x1, y1; POLY: x1, y1, x2, y2, x3, y3 . . .\n\t\t\t\t')

    
    # Attribute BEGIN uses Python identifier BEGIN
    __BEGIN = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'BEGIN'), 'BEGIN', '__httpwww_loc_govMETS_areaType_BEGIN', pyxb.binding.datatypes.string)
    __BEGIN._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 851, 2)
    __BEGIN._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 851, 2)
    
    BEGIN = property(__BEGIN.value, __BEGIN.set, None, 'BEGIN (string/O): An attribute that specifies the point in the content file where the relevant section of content begins. It can be used in conjunction with either the END attribute or the EXTENT attribute as a means of defining the relevant portion of the referenced file precisely. It can only be interpreted meaningfully in conjunction with the BETYPE or EXTTYPE, which specify the kind of beginning/ending point values or beginning/extent values that are being used. The BEGIN attribute can be used with or without a companion END or EXTENT element. In this case, the end of the content file is assumed to be the end point.\n\t\t\t\t')

    
    # Attribute END uses Python identifier END
    __END = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'END'), 'END', '__httpwww_loc_govMETS_areaType_END', pyxb.binding.datatypes.string)
    __END._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 857, 2)
    __END._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 857, 2)
    
    END = property(__END.value, __END.set, None, 'END (string/O): An attribute that specifies the point in the content file where the relevant section of content ends. It can only be interpreted meaningfully in conjunction with the BETYPE, which specifies the kind of ending point values being used. Typically the END attribute would only appear in conjunction with a BEGIN element.\n\t\t\t\t')

    
    # Attribute BETYPE uses Python identifier BETYPE
    __BETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'BETYPE'), 'BETYPE', '__httpwww_loc_govMETS_areaType_BETYPE', STD_ANON_3)
    __BETYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 863, 2)
    __BETYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 863, 2)
    
    BETYPE = property(__BETYPE.value, __BETYPE.set, None, 'BETYPE: Begin/End Type.\n\t\t\t\t\tBETYPE (string/O): An attribute that specifies the kind of BEGIN and/or END values that are being used. For example, if BYTE is specified, then the BEGIN and END point values represent the byte offsets into a file. If IDREF is specified, then the BEGIN element specifies the ID value that identifies the element in a structured text file where the relevant section of the file begins; and the END value (if present) would specify the ID value that identifies the element with which the relevant section of the file ends. Must be one of the following values: \nBYTE\nIDREF\nSMIL\nMIDI\nSMPTE-25\nSMPTE-24\nSMPTE-DF30\nSMPTE-NDF30\nSMPTE-DF29.97\nSMPTE-NDF29.97\nTIME\nTCF\nXPTR\n\t\t\t\t')

    
    # Attribute EXTENT uses Python identifier EXTENT
    __EXTENT = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'EXTENT'), 'EXTENT', '__httpwww_loc_govMETS_areaType_EXTENT', pyxb.binding.datatypes.string)
    __EXTENT._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 900, 2)
    __EXTENT._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 900, 2)
    
    EXTENT = property(__EXTENT.value, __EXTENT.set, None, 'EXTENT (string/O): An attribute that specifies the extent of the relevant section of the content file. Can only be interpreted meaningfully in conjunction with the EXTTYPE which specifies the kind of value that is being used. Typically the EXTENT attribute would only appear in conjunction with a BEGIN element and would not be used if the BEGIN point represents an IDREF.\n\t\t\t\t')

    
    # Attribute EXTTYPE uses Python identifier EXTTYPE
    __EXTTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'EXTTYPE'), 'EXTTYPE', '__httpwww_loc_govMETS_areaType_EXTTYPE', STD_ANON_4)
    __EXTTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 906, 2)
    __EXTTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 906, 2)
    
    EXTTYPE = property(__EXTTYPE.value, __EXTTYPE.set, None, 'EXTTYPE (string/O): An attribute that specifies the kind of EXTENT values that are being used. For example if BYTE is specified then EXTENT would represent a byte count. If TIME is specified the EXTENT would represent a duration of time. EXTTYPE must be one of the following values: \nBYTE\nSMIL\nMIDI\nSMPTE-25\nSMPTE-24\nSMPTE-DF30\nSMPTE-NDF30\nSMPTE-DF29.97\nSMPTE-NDF29.97\nTIME\nTCF.\n\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_areaType_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 938, 2)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 938, 2)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREFS/O): Contains the ID attribute values identifying the <rightsMD>, <sourceMD>, <techMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain or link to administrative metadata pertaining to the content represented by the <area> element. Typically the <area> ADMID attribute would be used to identify the <rightsMD> element or elements that pertain to the <area>, but it could be used anytime there was a need to link an <area> with pertinent administrative metadata. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer\n\t\t\t\t')

    
    # Attribute CONTENTIDS uses Python identifier CONTENTIDS
    __CONTENTIDS = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CONTENTIDS'), 'CONTENTIDS', '__httpwww_loc_govMETS_areaType_CONTENTIDS', URIs)
    __CONTENTIDS._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 944, 5)
    __CONTENTIDS._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 944, 5)
    
    CONTENTIDS = property(__CONTENTIDS.value, __CONTENTIDS.set, None, 'CONTENTIDS (URI/O): Content IDs for the content represented by the <area> (equivalent to DIDL DII or Digital Item Identifier, a unique external ID).\n\t\t\t\t')

    
    # Attribute ORDER uses Python identifier ORDER
    __ORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ORDER'), 'ORDER', '__httpwww_loc_govMETS_areaType_ORDER', pyxb.binding.datatypes.integer)
    __ORDER._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1591, 2)
    __ORDER._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1591, 2)
    
    ORDER = property(__ORDER.value, __ORDER.set, None, "ORDER (integer/O): A representation of the element's order among its siblings (e.g., its absolute, numeric sequence). For an example, and clarification of the distinction between ORDER and ORDERLABEL, see the description of the ORDERLABEL attribute.\n\t\t\t\t")

    
    # Attribute ORDERLABEL uses Python identifier ORDERLABEL
    __ORDERLABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ORDERLABEL'), 'ORDERLABEL', '__httpwww_loc_govMETS_areaType_ORDERLABEL', pyxb.binding.datatypes.string)
    __ORDERLABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1597, 2)
    __ORDERLABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1597, 2)
    
    ORDERLABEL = property(__ORDERLABEL.value, __ORDERLABEL.set, None, "ORDERLABEL (string/O): A representation of the element's order among its siblings (e.g., \u201cxii\u201d), or of any non-integer native numbering system. It is presumed that this value will still be machine actionable (e.g., it would support \u2018go to page ___\u2019 function), and it should not be used as a replacement/substitute for the LABEL attribute. To understand the differences between ORDER, ORDERLABEL and LABEL, imagine a text with 10 roman numbered pages followed by 10 arabic numbered pages. Page iii would have an ORDER of \u201c3\u201d, an ORDERLABEL of \u201ciii\u201d and a LABEL of \u201cPage iii\u201d, while page 3 would have an ORDER of \u201c13\u201d, an ORDERLABEL of \u201c3\u201d and a LABEL of \u201cPage 3\u201d.\n\t\t\t\t")

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_areaType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1603, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1603, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): An attribute used, for example, to identify a <div> to an end user viewing the document. Thus a hierarchical arrangement of the <div> LABEL values could provide a table of contents to the digital content represented by a METS document and facilitate the users\u2019 navigation of the digital object. Note that a <div> LABEL should be specific to its level in the structural map. In the case of a book with chapters, the book <div> LABEL should have the book title and the chapter <div>; LABELs should have the individual chapter titles, rather than having the chapter <div> LABELs combine both book title and chapter title . For further of the distinction between LABEL and ORDERLABEL see the description of the ORDERLABEL attribute.\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __FILEID.name() : __FILEID,
        __SHAPE.name() : __SHAPE,
        __COORDS.name() : __COORDS,
        __BEGIN.name() : __BEGIN,
        __END.name() : __END,
        __BETYPE.name() : __BETYPE,
        __EXTENT.name() : __EXTENT,
        __EXTTYPE.name() : __EXTTYPE,
        __ADMID.name() : __ADMID,
        __CONTENTIDS.name() : __CONTENTIDS,
        __ORDER.name() : __ORDER,
        __ORDERLABEL.name() : __ORDERLABEL,
        __LABEL.name() : __LABEL
    })
Namespace.addCategoryObject('typeBinding', 'areaType', areaType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    """ 
						The Structural Map Link element <smLink> identifies a hyperlink between two nodes in the structural map. You would use <smLink>, for instance, to note the existence of hypertext links between web pages, if you wished to record those links within METS. NOTE: <smLink> is an empty element. The location of the <smLink> element to which the <smLink> element is pointing MUST be stored in the xlink:href attribute.
				"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 966, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_14_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 967, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 967, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_14_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)
    __arcrole._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 7, 2)
    __arcrole._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 973, 5)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_14_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 8, 2)
    __title._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 980, 5)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_14_httpwww_w3_org1999xlinkshow', _ImportedBinding__xlink.STD_ANON)
    __show._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 9, 2)
    __show._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 987, 5)
    
    show = property(__show.value, __show.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_14_httpwww_w3_org1999xlinkactuate', _ImportedBinding__xlink.STD_ANON_)
    __actuate._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 20, 2)
    __actuate._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 994, 5)
    
    actuate = property(__actuate.value, __actuate.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}from uses Python identifier from_
    __from = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'from'), 'from_', '__httpwww_loc_govMETS_CTD_ANON_14_httpwww_w3_org1999xlinkfrom', pyxb.binding.datatypes.string, required=True)
    __from._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 31, 2)
    __from._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1008, 5)
    
    from_ = property(__from.value, __from.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}to uses Python identifier to
    __to = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'to'), 'to', '__httpwww_loc_govMETS_CTD_ANON_14_httpwww_w3_org1999xlinkto', pyxb.binding.datatypes.string, required=True)
    __to._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 32, 2)
    __to._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1001, 5)
    
    to = property(__to.value, __to.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __arcrole.name() : __arcrole,
        __title.name() : __title,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __from.name() : __from,
        __to.name() : __to
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    """
						The structMap link group element <smLinkGrp> provides an implementation of xlink:extendLink, and provides xlink compliant mechanisms for establishing xlink:arcLink type links between 2 or more <div> elements in <structMap> element(s) occurring within the same METS document or different METS documents.  The smLinkGrp could be used as an alternative to the <smLink> element to establish a one-to-one link between <div> elements in the same METS document in a fully xlink compliant manner.  However, it can also be used to establish one-to-many or many-to-many links between <div> elements. For example, if a METS document contains two <structMap> elements, one of which represents a purely logical structure and one of which represents a purely physical structure, the <smLinkGrp> element would provide a means of mapping a <div> representing a logical entity (for example, a newspaper article) with multiple <div> elements in the physical <structMap> representing the physical areas that  together comprise the logical entity (for example, the <div> elements representing the page areas that together comprise the newspaper article).
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1023, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}smLocatorLink uses Python identifier smLocatorLink
    __smLocatorLink = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'smLocatorLink'), 'smLocatorLink', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_loc_govMETSsmLocatorLink', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1025, 6), )

    
    smLocatorLink = property(__smLocatorLink.value, __smLocatorLink.set, None, '\n\t\t\t\t\t\t\t\t\tThe structMap locator link element <smLocatorLink> is of xlink:type "locator".  It provides a means of identifying a <div> element that will participate in one or more of the links specified by means of <smArcLink> elements within the same <smLinkGrp>. The participating <div> element that is represented by the <smLocatorLink> is identified by means of a URI in the associate xlink:href attribute.  The lowest level of this xlink:href URI value should be a fragment identifier that references the ID value that identifies the relevant <div> element.  For example, "xlink:href=\'#div20\'" where "div20" is the ID value that identifies the pertinent <div> in the current METS document. Although not required by the xlink specification, an <smLocatorLink> element will typically include an xlink:label attribute in this context, as the <smArcLink> elements will reference these labels to establish the from and to sides of each arc link.\n\t\t\t\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}smArcLink uses Python identifier smArcLink
    __smArcLink = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'smArcLink'), 'smArcLink', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_loc_govMETSsmArcLink', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1040, 6), )

    
    smArcLink = property(__smArcLink.value, __smArcLink.set, None, None)

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_15_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1068, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1068, 5)
    
    ID = property(__ID.value, __ID.set, None, None)

    
    # Attribute ARCLINKORDER uses Python identifier ARCLINKORDER
    __ARCLINKORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ARCLINKORDER'), 'ARCLINKORDER', '__httpwww_loc_govMETS_CTD_ANON_15_ARCLINKORDER', STD_ANON_5, unicode_default='unordered')
    __ARCLINKORDER._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1069, 5)
    __ARCLINKORDER._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1069, 5)
    
    ARCLINKORDER = property(__ARCLINKORDER.value, __ARCLINKORDER.set, None, 'ARCLINKORDER (enumerated string/O): ARCLINKORDER is used to indicate whether the order of the smArcLink elements aggregated by the smLinkGrp element is significant. If the order is significant, then a value of "ordered" should be supplied.  Value defaults to "unordered" Note that the ARLINKORDER attribute has no xlink specified meaning.')

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)
    __role._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 6, 2)
    __role._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 44, 4)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 8, 2)
    __title._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 45, 4)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_15_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default='extended')
    __type._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 43, 4)
    __type._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 43, 4)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        __smLocatorLink.name() : __smLocatorLink,
        __smArcLink.name() : __smArcLink
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __ARCLINKORDER.name() : __ARCLINKORDER,
        __role.name() : __role,
        __title.name() : __title,
        __type.name() : __type
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    """
										The structMap arc link element <smArcLink> is of xlink:type "arc" It can be used to establish a traversal link between two <div> elements as identified by <smLocatorLink> elements within the same smLinkGrp element. The associated xlink:from and xlink:to attributes identify the from and to sides of the arc link by referencing the xlink:label attribute values on the participating smLocatorLink elements.
									"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1041, 7)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_16_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1047, 8)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1047, 8)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.')

    
    # Attribute ARCTYPE uses Python identifier ARCTYPE
    __ARCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ARCTYPE'), 'ARCTYPE', '__httpwww_loc_govMETS_CTD_ANON_16_ARCTYPE', pyxb.binding.datatypes.string)
    __ARCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1053, 8)
    __ARCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1053, 8)
    
    ARCTYPE = property(__ARCTYPE.value, __ARCTYPE.set, None, 'ARCTYPE (string/O):The ARCTYPE attribute provides a means of specifying the relationship between the <div> elements participating in the arc link, and hence the purpose or role of the link.  While it can be considered analogous to the xlink:arcrole attribute, its type is a simple string, rather than anyURI.  ARCTYPE has no xlink specified meaning, and the xlink:arcrole attribute should be used instead of or in addition to the ARCTYPE attribute when full xlink compliance is desired with respect to specifying the role or purpose of the arc link. \n\t\t\t\t\t\t\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_CTD_ANON_16_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1059, 8)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1059, 8)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREFS/O): Contains the ID attribute values identifying the <sourceMD>, <techMD>, <digiprovMD> and/or <rightsMD> elements within the <amdSec> of the METS document that contain or link to administrative metadata pertaining to <smArcLink>. Typically the <smArcLink> ADMID attribute would be used to identify one or more <sourceMD> and/or <techMD> elements that refine or clarify the relationship between the xlink:from and xlink:to sides of the arc. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t\t')

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)
    __arcrole._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 7, 2)
    __arcrole._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 56, 4)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 8, 2)
    __title._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 57, 4)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_w3_org1999xlinkshow', _ImportedBinding__xlink.STD_ANON)
    __show._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 9, 2)
    __show._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 58, 4)
    
    show = property(__show.value, __show.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_w3_org1999xlinkactuate', _ImportedBinding__xlink.STD_ANON_)
    __actuate._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 20, 2)
    __actuate._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 59, 4)
    
    actuate = property(__actuate.value, __actuate.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}from uses Python identifier from_
    __from = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'from'), 'from_', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_w3_org1999xlinkfrom', pyxb.binding.datatypes.string)
    __from._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 31, 2)
    __from._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 60, 4)
    
    from_ = property(__from.value, __from.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}to uses Python identifier to
    __to = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'to'), 'to', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_w3_org1999xlinkto', pyxb.binding.datatypes.string)
    __to._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 32, 2)
    __to._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 61, 4)
    
    to = property(__to.value, __to.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_16_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default='arc')
    __type._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 55, 4)
    __type._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 55, 4)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __ARCTYPE.name() : __ARCTYPE,
        __ADMID.name() : __ADMID,
        __arcrole.name() : __arcrole,
        __title.name() : __title,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __from.name() : __from,
        __to.name() : __to,
        __type.name() : __type
    })



# Complex type {http://www.loc.gov/METS/}objectType with content type EMPTY
class objectType (pyxb.binding.basis.complexTypeDefinition):
    """objectType: complexType for interfaceDef and mechanism elements
				The mechanism and behavior elements point to external objects--an interface definition object or an executable code object respectively--which together constitute a behavior that can be applied to one or more <div> elements in a <structMap>.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'objectType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1192, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_objectType_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1198, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1198, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_objectType_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1204, 2)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1204, 2)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): A text description of the entity represented.\n\t\t\t\t')

    
    # Attribute LOCTYPE uses Python identifier LOCTYPE
    __LOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LOCTYPE'), 'LOCTYPE', '__httpwww_loc_govMETS_objectType_LOCTYPE', STD_ANON_10, required=True)
    __LOCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1679, 2)
    __LOCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1679, 2)
    
    LOCTYPE = property(__LOCTYPE.value, __LOCTYPE.set, None, 'LOCTYPE (string/R): Specifies the locator type used in the xlink:href attribute. Valid values for LOCTYPE are: \n\t\t\t\t\tARK\n\t\t\t\t\tURN\n\t\t\t\t\tURL\n\t\t\t\t\tPURL\n\t\t\t\t\tHANDLE\n\t\t\t\t\tDOI\n\t\t\t\t\tOTHER\n\t\t\t\t')

    
    # Attribute OTHERLOCTYPE uses Python identifier OTHERLOCTYPE
    __OTHERLOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OTHERLOCTYPE'), 'OTHERLOCTYPE', '__httpwww_loc_govMETS_objectType_OTHERLOCTYPE', pyxb.binding.datatypes.string)
    __OTHERLOCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1703, 2)
    __OTHERLOCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1703, 2)
    
    OTHERLOCTYPE = property(__OTHERLOCTYPE.value, __OTHERLOCTYPE.set, None, 'OTHERLOCTYPE (string/O): Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although optional, it is strongly recommended when OTHER is used.\n\t\t\t\t')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'href'), 'href', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    __href._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 5, 2)
    __href._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 35, 4)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'role'), 'role', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)
    __role._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 6, 2)
    __role._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 36, 4)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'arcrole'), 'arcrole', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)
    __arcrole._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 7, 2)
    __arcrole._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 37, 4)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'title'), 'title', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 8, 2)
    __title._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 38, 4)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'show'), 'show', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkshow', _ImportedBinding__xlink.STD_ANON)
    __show._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 9, 2)
    __show._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 39, 4)
    
    show = property(__show.value, __show.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'actuate'), 'actuate', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinkactuate', _ImportedBinding__xlink.STD_ANON_)
    __actuate._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 20, 2)
    __actuate._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 40, 4)
    
    actuate = property(__actuate.value, __actuate.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'type'), 'type', '__httpwww_loc_govMETS_objectType_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default='simple')
    __type._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 34, 4)
    __type._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 34, 4)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __LABEL.name() : __LABEL,
        __LOCTYPE.name() : __LOCTYPE,
        __OTHERLOCTYPE.name() : __OTHERLOCTYPE,
        __href.name() : __href,
        __role.name() : __role,
        __arcrole.name() : __arcrole,
        __title.name() : __title,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __type.name() : __type
    })
Namespace.addCategoryObject('typeBinding', 'objectType', objectType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    """
						The metadata reference element <mdRef> element is a generic element used throughout the METS schema to provide a pointer to metadata which resides outside the METS document.  NB: <mdRef> is an empty element.  The location of the metadata must be recorded in the xlink:href attribute, supplemented by the XPTR attribute as needed.
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1226, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_17_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1227, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1227, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_CTD_ANON_17_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1237, 5)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1237, 5)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL (string/O): Provides a label to display to the viewer of the METS document that identifies the associated metadata.\n\t\t\t\t\t\t\t')

    
    # Attribute XPTR uses Python identifier XPTR
    __XPTR = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'XPTR'), 'XPTR', '__httpwww_loc_govMETS_CTD_ANON_17_XPTR', pyxb.binding.datatypes.string)
    __XPTR._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1243, 5)
    __XPTR._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1243, 5)
    
    XPTR = property(__XPTR.value, __XPTR.set, None, 'XPTR (string/O): Locates the point within a file to which the <mdRef> element refers, if applicable.\n\t\t\t\t\t\t\t')

    
    # Attribute MDTYPE uses Python identifier MDTYPE
    __MDTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'MDTYPE'), 'MDTYPE', '__httpwww_loc_govMETS_CTD_ANON_17_MDTYPE', STD_ANON_9, required=True)
    __MDTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1612, 2)
    __MDTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1612, 2)
    
    MDTYPE = property(__MDTYPE.value, __MDTYPE.set, None, 'MDTYPE (string/R): Is used to indicate the type of the associated metadata. It must have one of the following values:\nMARC: any form of MARC record\nMODS: metadata in the Library of Congress MODS format\nEAD: Encoded Archival Description finding aid\nDC: Dublin Core\nNISOIMG: NISO Technical Metadata for Digital Still Images\nLC-AV: technical metadata specified in the Library of Congress A/V prototyping project\nVRA: Visual Resources Association Core\nTEIHDR: Text Encoding Initiative Header\nDDI: Data Documentation Initiative\nFGDC: Federal Geographic Data Committee metadata\nLOM: Learning Object Model\nPREMIS:  PREservation Metadata: Implementation Strategies\nPREMIS:OBJECT: PREMIS Object entiry\nPREMIS:AGENT: PREMIS Agent entity\nPREMIS:RIGHTS: PREMIS Rights entity\nPREMIS:EVENT: PREMIS Event entity\nTEXTMD: textMD Technical metadata for text\nMETSRIGHTS: Rights Declaration Schema\nISO 19115:2003 NAP: North American Profile of ISO 19115:2003 descriptive metadata\nEAC-CPF: Encoded Archival Context - Corporate Bodies, Persons, and Families\nLIDO: Lightweight Information Describing Objects\nOTHER: metadata in a format not specified above\n\t\t\t\t')

    
    # Attribute OTHERMDTYPE uses Python identifier OTHERMDTYPE
    __OTHERMDTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OTHERMDTYPE'), 'OTHERMDTYPE', '__httpwww_loc_govMETS_CTD_ANON_17_OTHERMDTYPE', pyxb.binding.datatypes.string)
    __OTHERMDTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1666, 2)
    __OTHERMDTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1666, 2)
    
    OTHERMDTYPE = property(__OTHERMDTYPE.value, __OTHERMDTYPE.set, None, 'OTHERMDTYPE (string/O): Specifies the form of metadata in use when the value OTHER is indicated in the MDTYPE attribute.\n\t\t\t\t')

    
    # Attribute MDTYPEVERSION uses Python identifier MDTYPEVERSION
    __MDTYPEVERSION = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'MDTYPEVERSION'), 'MDTYPEVERSION', '__httpwww_loc_govMETS_CTD_ANON_17_MDTYPEVERSION', pyxb.binding.datatypes.string)
    __MDTYPEVERSION._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1672, 2)
    __MDTYPEVERSION._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1672, 2)
    
    MDTYPEVERSION = property(__MDTYPEVERSION.value, __MDTYPEVERSION.set, None, 'MDTYPEVERSION(string/O): Provides a means for recording the version of the type of metadata (as recorded in the MDTYPE or OTHERMDTYPE attribute) that is being used.  This may represent the version of the underlying data dictionary or metadata model rather than a schema version. ')

    
    # Attribute LOCTYPE uses Python identifier LOCTYPE
    __LOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LOCTYPE'), 'LOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_17_LOCTYPE', STD_ANON_10, required=True)
    __LOCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1679, 2)
    __LOCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1679, 2)
    
    LOCTYPE = property(__LOCTYPE.value, __LOCTYPE.set, None, 'LOCTYPE (string/R): Specifies the locator type used in the xlink:href attribute. Valid values for LOCTYPE are: \n\t\t\t\t\tARK\n\t\t\t\t\tURN\n\t\t\t\t\tURL\n\t\t\t\t\tPURL\n\t\t\t\t\tHANDLE\n\t\t\t\t\tDOI\n\t\t\t\t\tOTHER\n\t\t\t\t')

    
    # Attribute OTHERLOCTYPE uses Python identifier OTHERLOCTYPE
    __OTHERLOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OTHERLOCTYPE'), 'OTHERLOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_17_OTHERLOCTYPE', pyxb.binding.datatypes.string)
    __OTHERLOCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1703, 2)
    __OTHERLOCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1703, 2)
    
    OTHERLOCTYPE = property(__OTHERLOCTYPE.value, __OTHERLOCTYPE.set, None, 'OTHERLOCTYPE (string/O): Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although optional, it is strongly recommended when OTHER is used.\n\t\t\t\t')

    
    # Attribute MIMETYPE uses Python identifier MIMETYPE
    __MIMETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'MIMETYPE'), 'MIMETYPE', '__httpwww_loc_govMETS_CTD_ANON_17_MIMETYPE', pyxb.binding.datatypes.string)
    __MIMETYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1711, 2)
    __MIMETYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1711, 2)
    
    MIMETYPE = property(__MIMETYPE.value, __MIMETYPE.set, None, 'MIMETYPE (string/O): The IANA MIME media type for the associated file or wrapped content. Some values for this attribute can be found on the IANA website.\n\t\t\t\t')

    
    # Attribute SIZE uses Python identifier SIZE
    __SIZE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'SIZE'), 'SIZE', '__httpwww_loc_govMETS_CTD_ANON_17_SIZE', pyxb.binding.datatypes.long)
    __SIZE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1717, 2)
    __SIZE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1717, 2)
    
    SIZE = property(__SIZE.value, __SIZE.set, None, 'SIZE (long/O): Specifies the size in bytes of the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CREATED'), 'CREATED', '__httpwww_loc_govMETS_CTD_ANON_17_CREATED', pyxb.binding.datatypes.dateTime)
    __CREATED._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1723, 2)
    __CREATED._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1723, 2)
    
    CREATED = property(__CREATED.value, __CREATED.set, None, 'CREATED (dateTime/O): Specifies the date and time of creation for the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CHECKSUM uses Python identifier CHECKSUM
    __CHECKSUM = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CHECKSUM'), 'CHECKSUM', '__httpwww_loc_govMETS_CTD_ANON_17_CHECKSUM', pyxb.binding.datatypes.string)
    __CHECKSUM._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1729, 2)
    __CHECKSUM._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1729, 2)
    
    CHECKSUM = property(__CHECKSUM.value, __CHECKSUM.set, None, 'CHECKSUM (string/O): Provides a checksum value for the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CHECKSUMTYPE uses Python identifier CHECKSUMTYPE
    __CHECKSUMTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CHECKSUMTYPE'), 'CHECKSUMTYPE', '__httpwww_loc_govMETS_CTD_ANON_17_CHECKSUMTYPE', STD_ANON_11)
    __CHECKSUMTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1735, 2)
    __CHECKSUMTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1735, 2)
    
    CHECKSUMTYPE = property(__CHECKSUMTYPE.value, __CHECKSUMTYPE.set, None, 'CHECKSUMTYPE (enumerated string/O): Specifies the checksum algorithm used to produce the value contained in the CHECKSUM attribute.  CHECKSUMTYPE must contain one of the following values:\n\t\t\t\t\tAdler-32\n\t\t\t\t\tCRC32\n\t\t\t\t\tHAVAL\n\t\t\t\t\tMD5\n\t\t\t\t\tMNP\n\t\t\t\t\tSHA-1\n\t\t\t\t\tSHA-256\n\t\t\t\t\tSHA-384\n\t\t\t\t\tSHA-512\n\t\t\t\t\tTIGER\n\t\t\t\t\tWHIRLPOOL\n\t\t\t\t')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'href'), 'href', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    __href._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 5, 2)
    __href._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 35, 4)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)
    __role._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 6, 2)
    __role._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 36, 4)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)
    __arcrole._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 7, 2)
    __arcrole._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 37, 4)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 8, 2)
    __title._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 38, 4)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkshow', _ImportedBinding__xlink.STD_ANON)
    __show._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 9, 2)
    __show._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 39, 4)
    
    show = property(__show.value, __show.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinkactuate', _ImportedBinding__xlink.STD_ANON_)
    __actuate._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 20, 2)
    __actuate._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 40, 4)
    
    actuate = property(__actuate.value, __actuate.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_17_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default='simple')
    __type._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 34, 4)
    __type._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 34, 4)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __LABEL.name() : __LABEL,
        __XPTR.name() : __XPTR,
        __MDTYPE.name() : __MDTYPE,
        __OTHERMDTYPE.name() : __OTHERMDTYPE,
        __MDTYPEVERSION.name() : __MDTYPEVERSION,
        __LOCTYPE.name() : __LOCTYPE,
        __OTHERLOCTYPE.name() : __OTHERLOCTYPE,
        __MIMETYPE.name() : __MIMETYPE,
        __SIZE.name() : __SIZE,
        __CREATED.name() : __CREATED,
        __CHECKSUM.name() : __CHECKSUM,
        __CHECKSUMTYPE.name() : __CHECKSUMTYPE,
        __href.name() : __href,
        __role.name() : __role,
        __arcrole.name() : __arcrole,
        __title.name() : __title,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __type.name() : __type
    })



# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    """ 
						A metadata wrapper element <mdWrap> provides a wrapper around metadata embedded within a METS document. The element is repeatable. Such metadata can be in one of two forms: 1) XML-encoded metadata, with the XML-encoding identifying itself as belonging to a namespace other than the METS document namespace. 2) Any arbitrary binary or textual form, PROVIDED that the metadata is Base64 encoded and wrapped in a <binData> element within the internal descriptive metadata element.
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1257, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}binData uses Python identifier binData
    __binData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'binData'), 'binData', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_loc_govMETSbinData', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1259, 6), )

    
    binData = property(__binData.value, __binData.set, None, ' \n\t\t\t\t\t\t\t\t\tThe binary data wrapper element <binData> is used to contain Base64 encoded metadata.\t\t\t\t\t\t\t\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}xmlData uses Python identifier xmlData
    __xmlData = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'xmlData'), 'xmlData', '__httpwww_loc_govMETS_CTD_ANON_18_httpwww_loc_govMETSxmlData', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1265, 6), )

    
    xmlData = property(__xmlData.value, __xmlData.set, None, '\n\t\t\t\t\t\t\t\t\tThe xml data wrapper element <xmlData> is used to contain XML encoded metadata. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> is set to \u201clax\u201d. Therefore, if the source schema and its location are identified by means of an XML schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element. \t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t')

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_18_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1278, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1278, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute LABEL uses Python identifier LABEL
    __LABEL = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LABEL'), 'LABEL', '__httpwww_loc_govMETS_CTD_ANON_18_LABEL', pyxb.binding.datatypes.string)
    __LABEL._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1286, 5)
    __LABEL._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1286, 5)
    
    LABEL = property(__LABEL.value, __LABEL.set, None, 'LABEL: an optional string attribute providing a label to display to the viewer of the METS document identifying the metadata.\n\t\t\t\t\t\t\t')

    
    # Attribute MDTYPE uses Python identifier MDTYPE
    __MDTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'MDTYPE'), 'MDTYPE', '__httpwww_loc_govMETS_CTD_ANON_18_MDTYPE', STD_ANON_9, required=True)
    __MDTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1612, 2)
    __MDTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1612, 2)
    
    MDTYPE = property(__MDTYPE.value, __MDTYPE.set, None, 'MDTYPE (string/R): Is used to indicate the type of the associated metadata. It must have one of the following values:\nMARC: any form of MARC record\nMODS: metadata in the Library of Congress MODS format\nEAD: Encoded Archival Description finding aid\nDC: Dublin Core\nNISOIMG: NISO Technical Metadata for Digital Still Images\nLC-AV: technical metadata specified in the Library of Congress A/V prototyping project\nVRA: Visual Resources Association Core\nTEIHDR: Text Encoding Initiative Header\nDDI: Data Documentation Initiative\nFGDC: Federal Geographic Data Committee metadata\nLOM: Learning Object Model\nPREMIS:  PREservation Metadata: Implementation Strategies\nPREMIS:OBJECT: PREMIS Object entiry\nPREMIS:AGENT: PREMIS Agent entity\nPREMIS:RIGHTS: PREMIS Rights entity\nPREMIS:EVENT: PREMIS Event entity\nTEXTMD: textMD Technical metadata for text\nMETSRIGHTS: Rights Declaration Schema\nISO 19115:2003 NAP: North American Profile of ISO 19115:2003 descriptive metadata\nEAC-CPF: Encoded Archival Context - Corporate Bodies, Persons, and Families\nLIDO: Lightweight Information Describing Objects\nOTHER: metadata in a format not specified above\n\t\t\t\t')

    
    # Attribute OTHERMDTYPE uses Python identifier OTHERMDTYPE
    __OTHERMDTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OTHERMDTYPE'), 'OTHERMDTYPE', '__httpwww_loc_govMETS_CTD_ANON_18_OTHERMDTYPE', pyxb.binding.datatypes.string)
    __OTHERMDTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1666, 2)
    __OTHERMDTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1666, 2)
    
    OTHERMDTYPE = property(__OTHERMDTYPE.value, __OTHERMDTYPE.set, None, 'OTHERMDTYPE (string/O): Specifies the form of metadata in use when the value OTHER is indicated in the MDTYPE attribute.\n\t\t\t\t')

    
    # Attribute MDTYPEVERSION uses Python identifier MDTYPEVERSION
    __MDTYPEVERSION = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'MDTYPEVERSION'), 'MDTYPEVERSION', '__httpwww_loc_govMETS_CTD_ANON_18_MDTYPEVERSION', pyxb.binding.datatypes.string)
    __MDTYPEVERSION._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1672, 2)
    __MDTYPEVERSION._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1672, 2)
    
    MDTYPEVERSION = property(__MDTYPEVERSION.value, __MDTYPEVERSION.set, None, 'MDTYPEVERSION(string/O): Provides a means for recording the version of the type of metadata (as recorded in the MDTYPE or OTHERMDTYPE attribute) that is being used.  This may represent the version of the underlying data dictionary or metadata model rather than a schema version. ')

    
    # Attribute MIMETYPE uses Python identifier MIMETYPE
    __MIMETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'MIMETYPE'), 'MIMETYPE', '__httpwww_loc_govMETS_CTD_ANON_18_MIMETYPE', pyxb.binding.datatypes.string)
    __MIMETYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1711, 2)
    __MIMETYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1711, 2)
    
    MIMETYPE = property(__MIMETYPE.value, __MIMETYPE.set, None, 'MIMETYPE (string/O): The IANA MIME media type for the associated file or wrapped content. Some values for this attribute can be found on the IANA website.\n\t\t\t\t')

    
    # Attribute SIZE uses Python identifier SIZE
    __SIZE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'SIZE'), 'SIZE', '__httpwww_loc_govMETS_CTD_ANON_18_SIZE', pyxb.binding.datatypes.long)
    __SIZE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1717, 2)
    __SIZE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1717, 2)
    
    SIZE = property(__SIZE.value, __SIZE.set, None, 'SIZE (long/O): Specifies the size in bytes of the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CREATED'), 'CREATED', '__httpwww_loc_govMETS_CTD_ANON_18_CREATED', pyxb.binding.datatypes.dateTime)
    __CREATED._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1723, 2)
    __CREATED._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1723, 2)
    
    CREATED = property(__CREATED.value, __CREATED.set, None, 'CREATED (dateTime/O): Specifies the date and time of creation for the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CHECKSUM uses Python identifier CHECKSUM
    __CHECKSUM = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CHECKSUM'), 'CHECKSUM', '__httpwww_loc_govMETS_CTD_ANON_18_CHECKSUM', pyxb.binding.datatypes.string)
    __CHECKSUM._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1729, 2)
    __CHECKSUM._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1729, 2)
    
    CHECKSUM = property(__CHECKSUM.value, __CHECKSUM.set, None, 'CHECKSUM (string/O): Provides a checksum value for the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CHECKSUMTYPE uses Python identifier CHECKSUMTYPE
    __CHECKSUMTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CHECKSUMTYPE'), 'CHECKSUMTYPE', '__httpwww_loc_govMETS_CTD_ANON_18_CHECKSUMTYPE', STD_ANON_11)
    __CHECKSUMTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1735, 2)
    __CHECKSUMTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1735, 2)
    
    CHECKSUMTYPE = property(__CHECKSUMTYPE.value, __CHECKSUMTYPE.set, None, 'CHECKSUMTYPE (enumerated string/O): Specifies the checksum algorithm used to produce the value contained in the CHECKSUM attribute.  CHECKSUMTYPE must contain one of the following values:\n\t\t\t\t\tAdler-32\n\t\t\t\t\tCRC32\n\t\t\t\t\tHAVAL\n\t\t\t\t\tMD5\n\t\t\t\t\tMNP\n\t\t\t\t\tSHA-1\n\t\t\t\t\tSHA-256\n\t\t\t\t\tSHA-384\n\t\t\t\t\tSHA-512\n\t\t\t\t\tTIGER\n\t\t\t\t\tWHIRLPOOL\n\t\t\t\t')

    _ElementMap.update({
        __binData.name() : __binData,
        __xmlData.name() : __xmlData
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __LABEL.name() : __LABEL,
        __MDTYPE.name() : __MDTYPE,
        __OTHERMDTYPE.name() : __OTHERMDTYPE,
        __MDTYPEVERSION.name() : __MDTYPEVERSION,
        __MIMETYPE.name() : __MIMETYPE,
        __SIZE.name() : __SIZE,
        __CREATED.name() : __CREATED,
        __CHECKSUM.name() : __CHECKSUM,
        __CHECKSUMTYPE.name() : __CHECKSUMTYPE
    })



# Complex type {http://www.loc.gov/METS/}fileType with content type ELEMENT_ONLY
class fileType (pyxb.binding.basis.complexTypeDefinition):
    """fileType: Complex Type for Files
				The file element provides access to content files for a METS object.  A file element may contain one or more FLocat elements, which provide pointers to a content file, and/or an FContent element, which wraps an encoded version of the file. Note that ALL FLocat and FContent elements underneath a single file element should identify/contain identical copies of a single file.
			"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'fileType')
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1327, 1)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.loc.gov/METS/}FLocat uses Python identifier FLocat
    __FLocat = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FLocat'), 'FLocat', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETSFLocat', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1335, 3), )

    
    FLocat = property(__FLocat.value, __FLocat.set, None, ' \n\t\t\t\t\t\tThe file location element <FLocat> provides a pointer to the location of a content file. It uses the XLink reference syntax to provide linking information indicating the actual location of the content file, along with other attributes specifying additional linking information. NOTE: <FLocat> is an empty element. The location of the resource pointed to MUST be stored in the xlink:href attribute.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}FContent uses Python identifier FContent
    __FContent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'FContent'), 'FContent', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETSFContent', False, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1358, 3), )

    
    FContent = property(__FContent.value, __FContent.set, None, '\n\t\t\t\t\t\tThe file content element <FContent> is used to identify a content file contained internally within a METS document. The content file must be either Base64 encoded and contained within the subsidiary <binData> wrapper element, or consist of XML information and be contained within the subsidiary <xmlData> wrapper element.\n\t\t\t\t\t')

    
    # Element {http://www.loc.gov/METS/}stream uses Python identifier stream
    __stream = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'stream'), 'stream', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETSstream', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1400, 3), )

    
    stream = property(__stream.value, __stream.set, None, ' \n\t\t\t\t\t\tA component byte stream element <stream> may be composed of one or more subsidiary streams. An MPEG4 file, for example, might contain separate audio and video streams, each of which is associated with technical metadata. The repeatable <stream> element provides a mechanism to record the existence of separate data streams within a particular file, and the opportunity to associate <dmdSec> and <amdSec> with those subsidiary data streams if desired. ')

    
    # Element {http://www.loc.gov/METS/}transformFile uses Python identifier transformFile
    __transformFile = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'transformFile'), 'transformFile', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETStransformFile', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1465, 3), )

    
    transformFile = property(__transformFile.value, __transformFile.set, None, '\n\t\t\t\t\t\tThe transform file element <transformFile> provides a means to access any subsidiary files listed below a <file> element by indicating the steps required to "unpack" or transform the subsidiary files. This element is repeatable and might provide a link to a <behavior> in the <behaviorSec> that performs the transformation.')

    
    # Element {http://www.loc.gov/METS/}file uses Python identifier file
    __file = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'file'), 'file', '__httpwww_loc_govMETS_fileType_httpwww_loc_govMETSfile', True, pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1514, 3), )

    
    file = property(__file.value, __file.set, None, None)

    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_fileType_ID', pyxb.binding.datatypes.ID, required=True)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1516, 2)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1516, 2)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/R): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. Typically, the ID attribute value on a <file> element would be referenced from one or more FILEID attributes (which are of type IDREF) on <fptr>and/or <area> elements within the <structMap>.  Such references establish links between  structural divisions (<div> elements) and the specific content files or parts of content files that manifest them. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute SEQ uses Python identifier SEQ
    __SEQ = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'SEQ'), 'SEQ', '__httpwww_loc_govMETS_fileType_SEQ', pyxb.binding.datatypes.int)
    __SEQ._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1522, 2)
    __SEQ._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1522, 2)
    
    SEQ = property(__SEQ.value, __SEQ.set, None, 'SEQ (integer/O): Indicates the sequence of this <file> relative to the others in its <fileGrp>.\n\t\t\t\t')

    
    # Attribute OWNERID uses Python identifier OWNERID
    __OWNERID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OWNERID'), 'OWNERID', '__httpwww_loc_govMETS_fileType_OWNERID', pyxb.binding.datatypes.string)
    __OWNERID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1529, 2)
    __OWNERID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1529, 2)
    
    OWNERID = property(__OWNERID.value, __OWNERID.set, None, 'OWNERID (string/O): A unique identifier assigned to the file by its owner.  This may be a URI which differs from the URI used to retrieve the file.\n\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_fileType_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1535, 2)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1535, 2)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREFS/O): Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain administrative metadata pertaining to the file. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute DMDID uses Python identifier DMDID
    __DMDID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'DMDID'), 'DMDID', '__httpwww_loc_govMETS_fileType_DMDID', pyxb.binding.datatypes.IDREFS)
    __DMDID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1541, 2)
    __DMDID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1541, 2)
    
    DMDID = property(__DMDID.value, __DMDID.set, None, 'DMDID (IDREFS/O): Contains the ID attribute values identifying the <dmdSec>, elements in the METS document that contain or link to descriptive metadata pertaining to the content file represented by the current <file> element.  For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t')

    
    # Attribute GROUPID uses Python identifier GROUPID
    __GROUPID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'GROUPID'), 'GROUPID', '__httpwww_loc_govMETS_fileType_GROUPID', pyxb.binding.datatypes.string)
    __GROUPID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1547, 2)
    __GROUPID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1547, 2)
    
    GROUPID = property(__GROUPID.value, __GROUPID.set, None, 'GROUPID (string/O): An identifier that establishes a correspondence between this file and files in other file groups. Typically, this will be used to associate a master file in one file group with the derivative files made from it in other file groups.\n\t\t\t\t')

    
    # Attribute USE uses Python identifier USE
    __USE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'USE'), 'USE', '__httpwww_loc_govMETS_fileType_USE', pyxb.binding.datatypes.string)
    __USE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1553, 2)
    __USE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1553, 2)
    
    USE = property(__USE.value, __USE.set, None, 'USE (string/O): A tagging attribute to indicate the intended use of all copies of the file aggregated by the <file> element (e.g., master, reference, thumbnails for image files). A USE attribute can be expressed at the<fileGrp> level, the <file> level, the <FLocat> level and/or the <FContent> level.  A USE attribute value at the <fileGrp> level should pertain to all of the files in the <fileGrp>.  A USE attribute at the <file> level should pertain to all copies of the file as represented by subsidiary <FLocat> and/or <FContent> elements.  A USE attribute at the <FLocat> or <FContent> level pertains to the particular copy of the file that is either referenced (<FLocat>) or wrapped (<FContent>).\n\t\t\t\t')

    
    # Attribute BEGIN uses Python identifier BEGIN
    __BEGIN = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'BEGIN'), 'BEGIN', '__httpwww_loc_govMETS_fileType_BEGIN', pyxb.binding.datatypes.string)
    __BEGIN._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1559, 2)
    __BEGIN._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1559, 2)
    
    BEGIN = property(__BEGIN.value, __BEGIN.set, None, 'BEGIN (string/O): An attribute that specifies the point in the parent <file> where the current <file> begins.  When used in conjunction with a <file> element, this attribute is only meaningful when this element is nested, and its parent <file> element represents a container file. It can be used in conjunction with the END attribute as a means of defining the location of the current file within its parent file. However, the BEGIN attribute can be used with or without a companion END attribute. When no END attribute is specified, the end of the parent file is assumed also to be the end point of the current file. The BEGIN and END attributes can only be interpreted meaningfully in conjunction with a BETYPE attribute, which specifies the kind of beginning/ending point values that are being used. \n\t\t\t\t')

    
    # Attribute END uses Python identifier END
    __END = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'END'), 'END', '__httpwww_loc_govMETS_fileType_END', pyxb.binding.datatypes.string)
    __END._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1565, 2)
    __END._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1565, 2)
    
    END = property(__END.value, __END.set, None, 'END (string/O): An attribute that specifies the point in the parent <file> where the current, nested <file> ends. It can only be interpreted meaningfully in conjunction with the BETYPE, which specifies the kind of ending point values being used. Typically the END attribute would only appear in conjunction with a BEGIN attribute.\n\t\t\t\t')

    
    # Attribute BETYPE uses Python identifier BETYPE
    __BETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'BETYPE'), 'BETYPE', '__httpwww_loc_govMETS_fileType_BETYPE', STD_ANON_8)
    __BETYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1571, 2)
    __BETYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1571, 2)
    
    BETYPE = property(__BETYPE.value, __BETYPE.set, None, 'BETYPE: Begin/End Type.\n\t\t\t\t\tBETYPE (string/O): An attribute that specifies the kind of BEGIN and/or END values that are being used. Currently BYTE is the only valid value that can be used in conjunction with nested <file> or <stream> elements. \n\t\t\t\t')

    
    # Attribute MIMETYPE uses Python identifier MIMETYPE
    __MIMETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'MIMETYPE'), 'MIMETYPE', '__httpwww_loc_govMETS_fileType_MIMETYPE', pyxb.binding.datatypes.string)
    __MIMETYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1711, 2)
    __MIMETYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1711, 2)
    
    MIMETYPE = property(__MIMETYPE.value, __MIMETYPE.set, None, 'MIMETYPE (string/O): The IANA MIME media type for the associated file or wrapped content. Some values for this attribute can be found on the IANA website.\n\t\t\t\t')

    
    # Attribute SIZE uses Python identifier SIZE
    __SIZE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'SIZE'), 'SIZE', '__httpwww_loc_govMETS_fileType_SIZE', pyxb.binding.datatypes.long)
    __SIZE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1717, 2)
    __SIZE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1717, 2)
    
    SIZE = property(__SIZE.value, __SIZE.set, None, 'SIZE (long/O): Specifies the size in bytes of the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CREATED uses Python identifier CREATED
    __CREATED = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CREATED'), 'CREATED', '__httpwww_loc_govMETS_fileType_CREATED', pyxb.binding.datatypes.dateTime)
    __CREATED._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1723, 2)
    __CREATED._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1723, 2)
    
    CREATED = property(__CREATED.value, __CREATED.set, None, 'CREATED (dateTime/O): Specifies the date and time of creation for the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CHECKSUM uses Python identifier CHECKSUM
    __CHECKSUM = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CHECKSUM'), 'CHECKSUM', '__httpwww_loc_govMETS_fileType_CHECKSUM', pyxb.binding.datatypes.string)
    __CHECKSUM._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1729, 2)
    __CHECKSUM._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1729, 2)
    
    CHECKSUM = property(__CHECKSUM.value, __CHECKSUM.set, None, 'CHECKSUM (string/O): Provides a checksum value for the associated file or wrapped content.\n\t\t\t\t')

    
    # Attribute CHECKSUMTYPE uses Python identifier CHECKSUMTYPE
    __CHECKSUMTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CHECKSUMTYPE'), 'CHECKSUMTYPE', '__httpwww_loc_govMETS_fileType_CHECKSUMTYPE', STD_ANON_11)
    __CHECKSUMTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1735, 2)
    __CHECKSUMTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1735, 2)
    
    CHECKSUMTYPE = property(__CHECKSUMTYPE.value, __CHECKSUMTYPE.set, None, 'CHECKSUMTYPE (enumerated string/O): Specifies the checksum algorithm used to produce the value contained in the CHECKSUM attribute.  CHECKSUMTYPE must contain one of the following values:\n\t\t\t\t\tAdler-32\n\t\t\t\t\tCRC32\n\t\t\t\t\tHAVAL\n\t\t\t\t\tMD5\n\t\t\t\t\tMNP\n\t\t\t\t\tSHA-1\n\t\t\t\t\tSHA-256\n\t\t\t\t\tSHA-384\n\t\t\t\t\tSHA-512\n\t\t\t\t\tTIGER\n\t\t\t\t\tWHIRLPOOL\n\t\t\t\t')

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.loc.gov/METS/'))
    _ElementMap.update({
        __FLocat.name() : __FLocat,
        __FContent.name() : __FContent,
        __stream.name() : __stream,
        __transformFile.name() : __transformFile,
        __file.name() : __file
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __SEQ.name() : __SEQ,
        __OWNERID.name() : __OWNERID,
        __ADMID.name() : __ADMID,
        __DMDID.name() : __DMDID,
        __GROUPID.name() : __GROUPID,
        __USE.name() : __USE,
        __BEGIN.name() : __BEGIN,
        __END.name() : __END,
        __BETYPE.name() : __BETYPE,
        __MIMETYPE.name() : __MIMETYPE,
        __SIZE.name() : __SIZE,
        __CREATED.name() : __CREATED,
        __CHECKSUM.name() : __CHECKSUM,
        __CHECKSUMTYPE.name() : __CHECKSUMTYPE
    })
Namespace.addCategoryObject('typeBinding', 'fileType', fileType)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    """ 
						The file location element <FLocat> provides a pointer to the location of a content file. It uses the XLink reference syntax to provide linking information indicating the actual location of the content file, along with other attributes specifying additional linking information. NOTE: <FLocat> is an empty element. The location of the resource pointed to MUST be stored in the xlink:href attribute.
					"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1341, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_19_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1342, 5)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1342, 5)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t')

    
    # Attribute USE uses Python identifier USE
    __USE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'USE'), 'USE', '__httpwww_loc_govMETS_CTD_ANON_19_USE', pyxb.binding.datatypes.string)
    __USE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1349, 5)
    __USE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1349, 5)
    
    USE = property(__USE.value, __USE.set, None, 'USE (string/O): A tagging attribute to indicate the intended use of the specific copy of the file  represented by the <FLocat> element (e.g., service master, archive master). A USE attribute can be expressed at the<fileGrp> level, the <file> level, the <FLocat> level and/or the <FContent> level.  A USE attribute value at the <fileGrp> level should pertain to all of the files in the <fileGrp>.  A USE attribute at the <file> level should pertain to all copies of the file as represented by subsidiary <FLocat> and/or <FContent> elements.  A USE attribute at the <FLocat> or <FContent> level pertains to the particular copy of the file that is either referenced (<FLocat>) or wrapped (<FContent>).\n\t\t\t\t\t\t\t')

    
    # Attribute LOCTYPE uses Python identifier LOCTYPE
    __LOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'LOCTYPE'), 'LOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_19_LOCTYPE', STD_ANON_10, required=True)
    __LOCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1679, 2)
    __LOCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1679, 2)
    
    LOCTYPE = property(__LOCTYPE.value, __LOCTYPE.set, None, 'LOCTYPE (string/R): Specifies the locator type used in the xlink:href attribute. Valid values for LOCTYPE are: \n\t\t\t\t\tARK\n\t\t\t\t\tURN\n\t\t\t\t\tURL\n\t\t\t\t\tPURL\n\t\t\t\t\tHANDLE\n\t\t\t\t\tDOI\n\t\t\t\t\tOTHER\n\t\t\t\t')

    
    # Attribute OTHERLOCTYPE uses Python identifier OTHERLOCTYPE
    __OTHERLOCTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OTHERLOCTYPE'), 'OTHERLOCTYPE', '__httpwww_loc_govMETS_CTD_ANON_19_OTHERLOCTYPE', pyxb.binding.datatypes.string)
    __OTHERLOCTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1703, 2)
    __OTHERLOCTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1703, 2)
    
    OTHERLOCTYPE = property(__OTHERLOCTYPE.value, __OTHERLOCTYPE.set, None, 'OTHERLOCTYPE (string/O): Specifies the locator type when the value OTHER is used in the LOCTYPE attribute. Although optional, it is strongly recommended when OTHER is used.\n\t\t\t\t')

    
    # Attribute {http://www.w3.org/1999/xlink}href uses Python identifier href
    __href = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'href'), 'href', '__httpwww_loc_govMETS_CTD_ANON_19_httpwww_w3_org1999xlinkhref', pyxb.binding.datatypes.anyURI)
    __href._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 5, 2)
    __href._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 35, 4)
    
    href = property(__href.value, __href.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}role uses Python identifier role
    __role = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'role'), 'role', '__httpwww_loc_govMETS_CTD_ANON_19_httpwww_w3_org1999xlinkrole', pyxb.binding.datatypes.string)
    __role._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 6, 2)
    __role._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 36, 4)
    
    role = property(__role.value, __role.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}arcrole uses Python identifier arcrole
    __arcrole = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'arcrole'), 'arcrole', '__httpwww_loc_govMETS_CTD_ANON_19_httpwww_w3_org1999xlinkarcrole', pyxb.binding.datatypes.string)
    __arcrole._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 7, 2)
    __arcrole._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 37, 4)
    
    arcrole = property(__arcrole.value, __arcrole.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}title uses Python identifier title
    __title = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'title'), 'title', '__httpwww_loc_govMETS_CTD_ANON_19_httpwww_w3_org1999xlinktitle', pyxb.binding.datatypes.string)
    __title._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 8, 2)
    __title._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 38, 4)
    
    title = property(__title.value, __title.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}show uses Python identifier show
    __show = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'show'), 'show', '__httpwww_loc_govMETS_CTD_ANON_19_httpwww_w3_org1999xlinkshow', _ImportedBinding__xlink.STD_ANON)
    __show._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 9, 2)
    __show._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 39, 4)
    
    show = property(__show.value, __show.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}actuate uses Python identifier actuate
    __actuate = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'actuate'), 'actuate', '__httpwww_loc_govMETS_CTD_ANON_19_httpwww_w3_org1999xlinkactuate', _ImportedBinding__xlink.STD_ANON_)
    __actuate._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 20, 2)
    __actuate._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 40, 4)
    
    actuate = property(__actuate.value, __actuate.set, None, None)

    
    # Attribute {http://www.w3.org/1999/xlink}type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(_Namespace_xlink, 'type'), 'type', '__httpwww_loc_govMETS_CTD_ANON_19_httpwww_w3_org1999xlinktype', pyxb.binding.datatypes.string, fixed=True, unicode_default='simple')
    __type._DeclarationLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 34, 4)
    __type._UseLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 34, 4)
    
    type = property(__type.value, __type.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __USE.name() : __USE,
        __LOCTYPE.name() : __LOCTYPE,
        __OTHERLOCTYPE.name() : __OTHERLOCTYPE,
        __href.name() : __href,
        __role.name() : __role,
        __arcrole.name() : __arcrole,
        __title.name() : __title,
        __show.name() : __show,
        __actuate.name() : __actuate,
        __type.name() : __type
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    """ 
						A component byte stream element <stream> may be composed of one or more subsidiary streams. An MPEG4 file, for example, might contain separate audio and video streams, each of which is associated with technical metadata. The repeatable <stream> element provides a mechanism to record the existence of separate data streams within a particular file, and the opportunity to associate <dmdSec> and <amdSec> with those subsidiary data streams if desired. """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1405, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_20_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1408, 7)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1408, 7)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t')

    
    # Attribute streamType uses Python identifier streamType
    __streamType = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'streamType'), 'streamType', '__httpwww_loc_govMETS_CTD_ANON_20_streamType', pyxb.binding.datatypes.string)
    __streamType._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1414, 7)
    __streamType._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1414, 7)
    
    streamType = property(__streamType.value, __streamType.set, None, 'streamType (string/O): The IANA MIME media type for the bytestream.')

    
    # Attribute OWNERID uses Python identifier OWNERID
    __OWNERID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'OWNERID'), 'OWNERID', '__httpwww_loc_govMETS_CTD_ANON_20_OWNERID', pyxb.binding.datatypes.string)
    __OWNERID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1419, 7)
    __OWNERID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1419, 7)
    
    OWNERID = property(__OWNERID.value, __OWNERID.set, None, 'OWNERID (string/O): Used to provide a unique identifier (which could include a URI) assigned to the file. This identifier may differ from the URI used to retrieve the file.\n\t\t\t\t\t\t\t\t\t')

    
    # Attribute ADMID uses Python identifier ADMID
    __ADMID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ADMID'), 'ADMID', '__httpwww_loc_govMETS_CTD_ANON_20_ADMID', pyxb.binding.datatypes.IDREFS)
    __ADMID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1425, 7)
    __ADMID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1425, 7)
    
    ADMID = property(__ADMID.value, __ADMID.set, None, 'ADMID (IDREFS/O): Contains the ID attribute values of the <techMD>, <sourceMD>, <rightsMD> and/or <digiprovMD> elements within the <amdSec> of the METS document that contain administrative metadata pertaining to the bytestream. For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t')

    
    # Attribute DMDID uses Python identifier DMDID
    __DMDID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'DMDID'), 'DMDID', '__httpwww_loc_govMETS_CTD_ANON_20_DMDID', pyxb.binding.datatypes.IDREFS)
    __DMDID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1431, 7)
    __DMDID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1431, 7)
    
    DMDID = property(__DMDID.value, __DMDID.set, None, 'DMDID (IDREFS/O): Contains the ID attribute values identifying the <dmdSec>, elements in the METS document that contain or link to descriptive metadata pertaining to the content file stream represented by the current <stream> element.  For more information on using METS IDREFS and IDREF type attributes for internal linking, see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t')

    
    # Attribute BEGIN uses Python identifier BEGIN
    __BEGIN = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'BEGIN'), 'BEGIN', '__httpwww_loc_govMETS_CTD_ANON_20_BEGIN', pyxb.binding.datatypes.string)
    __BEGIN._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1437, 7)
    __BEGIN._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1437, 7)
    
    BEGIN = property(__BEGIN.value, __BEGIN.set, None, 'BEGIN (string/O): An attribute that specifies the point in the parent <file> where the current <stream> begins. It can be used in conjunction with the END attribute as a means of defining the location of the stream within its parent file. However, the BEGIN attribute can be used with or without a companion END attribute. When no END attribute is specified, the end of the parent file is assumed also to be the end point of the stream. The BEGIN and END attributes can only be interpreted meaningfully in conjunction with a BETYPE attribute, which specifies the kind of beginning/ending point values that are being used. \n\t\t\t\t\t\t\t\t\t')

    
    # Attribute END uses Python identifier END
    __END = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'END'), 'END', '__httpwww_loc_govMETS_CTD_ANON_20_END', pyxb.binding.datatypes.string)
    __END._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1443, 7)
    __END._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1443, 7)
    
    END = property(__END.value, __END.set, None, 'END (string/O): An attribute that specifies the point in the parent <file> where the <stream> ends. It can only be interpreted meaningfully in conjunction with the BETYPE, which specifies the kind of ending point values being used. Typically the END attribute would only appear in conjunction with a BEGIN attribute.\n\t\t\t\t\t\t\t\t\t')

    
    # Attribute BETYPE uses Python identifier BETYPE
    __BETYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'BETYPE'), 'BETYPE', '__httpwww_loc_govMETS_CTD_ANON_20_BETYPE', STD_ANON_6)
    __BETYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1449, 7)
    __BETYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1449, 7)
    
    BETYPE = property(__BETYPE.value, __BETYPE.set, None, 'BETYPE: Begin/End Type.\n\t\t\t\t\t\t\t\t\t\tBETYPE (string/O): An attribute that specifies the kind of BEGIN and/or END values that are being used. Currently BYTE is the only valid value that can be used in conjunction with nested <file> or <stream> elements. \n\t\t\t\t\t\t\t\t\t')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __streamType.name() : __streamType,
        __OWNERID.name() : __OWNERID,
        __ADMID.name() : __ADMID,
        __DMDID.name() : __DMDID,
        __BEGIN.name() : __BEGIN,
        __END.name() : __END,
        __BETYPE.name() : __BETYPE
    })



# Complex type [anonymous] with content type EMPTY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    """
						The transform file element <transformFile> provides a means to access any subsidiary files listed below a <file> element by indicating the steps required to "unpack" or transform the subsidiary files. This element is repeatable and might provide a link to a <behavior> in the <behaviorSec> that performs the transformation."""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1470, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute ID uses Python identifier ID
    __ID = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ID'), 'ID', '__httpwww_loc_govMETS_CTD_ANON_21_ID', pyxb.binding.datatypes.ID)
    __ID._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1473, 7)
    __ID._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1473, 7)
    
    ID = property(__ID.value, __ID.set, None, 'ID (ID/O): This attribute uniquely identifies the element within the METS document, and would allow the element to be referenced unambiguously from another element or document via an IDREF or an XPTR. For more information on using ID attributes for internal and external linking see Chapter 4 of the METS Primer.\n\t\t\t\t\t\t\t\t\t')

    
    # Attribute TRANSFORMTYPE uses Python identifier TRANSFORMTYPE
    __TRANSFORMTYPE = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TRANSFORMTYPE'), 'TRANSFORMTYPE', '__httpwww_loc_govMETS_CTD_ANON_21_TRANSFORMTYPE', STD_ANON_7, required=True)
    __TRANSFORMTYPE._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1479, 7)
    __TRANSFORMTYPE._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1479, 7)
    
    TRANSFORMTYPE = property(__TRANSFORMTYPE.value, __TRANSFORMTYPE.set, None, 'TRANSFORMTYPE (string/R): Is used to indicate the type of transformation needed to render content of a file accessible. This may include unpacking a file into subsidiary files/streams. The controlled value constraints for this XML string include \u201cdecompression\u201d and \u201cdecryption\u201d. Decompression is defined as the action of reversing data compression, i.e., the process of encoding information using fewer bits than an unencoded representation would use by means of specific encoding schemas. Decryption is defined as the process of restoring data that has been obscured to make it unreadable without special knowledge (encrypted data) to its original form. ')

    
    # Attribute TRANSFORMALGORITHM uses Python identifier TRANSFORMALGORITHM
    __TRANSFORMALGORITHM = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TRANSFORMALGORITHM'), 'TRANSFORMALGORITHM', '__httpwww_loc_govMETS_CTD_ANON_21_TRANSFORMALGORITHM', pyxb.binding.datatypes.string, required=True)
    __TRANSFORMALGORITHM._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1490, 7)
    __TRANSFORMALGORITHM._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1490, 7)
    
    TRANSFORMALGORITHM = property(__TRANSFORMALGORITHM.value, __TRANSFORMALGORITHM.set, None, 'TRANSFORM-ALGORITHM (string/R): Specifies the decompression or decryption routine used to access the contents of the file. Algorithms for compression can be either loss-less or lossy.')

    
    # Attribute TRANSFORMKEY uses Python identifier TRANSFORMKEY
    __TRANSFORMKEY = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TRANSFORMKEY'), 'TRANSFORMKEY', '__httpwww_loc_govMETS_CTD_ANON_21_TRANSFORMKEY', pyxb.binding.datatypes.string)
    __TRANSFORMKEY._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1495, 7)
    __TRANSFORMKEY._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1495, 7)
    
    TRANSFORMKEY = property(__TRANSFORMKEY.value, __TRANSFORMKEY.set, None, 'TRANSFORMKEY (string/O): A key to be used with the transform algorithm for accessing the file\u2019s contents.')

    
    # Attribute TRANSFORMBEHAVIOR uses Python identifier TRANSFORMBEHAVIOR
    __TRANSFORMBEHAVIOR = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TRANSFORMBEHAVIOR'), 'TRANSFORMBEHAVIOR', '__httpwww_loc_govMETS_CTD_ANON_21_TRANSFORMBEHAVIOR', pyxb.binding.datatypes.IDREF)
    __TRANSFORMBEHAVIOR._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1500, 7)
    __TRANSFORMBEHAVIOR._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1500, 7)
    
    TRANSFORMBEHAVIOR = property(__TRANSFORMBEHAVIOR.value, __TRANSFORMBEHAVIOR.set, None, 'TRANSFORMBEHAVIOR (string/O): An IDREF to a behavior element for this transformation.')

    
    # Attribute TRANSFORMORDER uses Python identifier TRANSFORMORDER
    __TRANSFORMORDER = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'TRANSFORMORDER'), 'TRANSFORMORDER', '__httpwww_loc_govMETS_CTD_ANON_21_TRANSFORMORDER', pyxb.binding.datatypes.positiveInteger, required=True)
    __TRANSFORMORDER._DeclarationLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1505, 7)
    __TRANSFORMORDER._UseLocation = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1505, 7)
    
    TRANSFORMORDER = property(__TRANSFORMORDER.value, __TRANSFORMORDER.set, None, 'TRANSFORMORDER (postive-integer/R): The order in which the instructions must be followed in order to unpack or transform the container file.')

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ID.name() : __ID,
        __TRANSFORMTYPE.name() : __TRANSFORMTYPE,
        __TRANSFORMALGORITHM.name() : __TRANSFORMALGORITHM,
        __TRANSFORMKEY.name() : __TRANSFORMKEY,
        __TRANSFORMBEHAVIOR.name() : __TRANSFORMBEHAVIOR,
        __TRANSFORMORDER.name() : __TRANSFORMORDER
    })



mets = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mets'), CTD_ANON_8, documentation='METS: Metadata Encoding and Transmission Standard.\n\t\t\t\tMETS is intended to provide a standardized XML format for transmission of complex digital library objects between systems.  As such, it can be seen as filling a role similar to that defined for the Submission Information Package (SIP), Archival Information Package (AIP) and Dissemination Information Package (DIP) in the Reference Model for an Open Archival Information System. The root element <mets> establishes the container for the information being stored and/or transmitted by the standard.\n\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 223, 1))
Namespace.addCategoryObject('elementBinding', mets.name().localName(), mets)



metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'metsHdr'), CTD_ANON, scope=metsType, documentation=' \n\t\t\t\t\tThe mets header element <metsHdr> captures metadata about the METS document itself, not the digital object the METS document encodes. Although it records a more limited set of metadata, it is very similar in function and purpose to the headers employed in other schema such as the Text Encoding Initiative (TEI) or in the Encoded Archival Description (EAD).\n\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 242, 3)))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'dmdSec'), mdSecType, scope=metsType, documentation='\n\t\t\t\t\t\tA descriptive metadata section <dmdSec> records descriptive metadata pertaining to the METS object as a whole or one of its components. The <dmdSec> element conforms to same generic datatype as the <techMD>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes. A descriptive metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <dmdSec> elements; and descriptive metadata can be associated with any METS element that supports a DMDID attribute.  Descriptive metadata can be expressed according to many current description standards (i.e., MARC, MODS, Dublin Core, TEI Header, EAD, VRA, FGDC, DDI) or a locally produced XML schema. \n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 419, 3)))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'amdSec'), amdSecType, scope=metsType, documentation=' \n\t\t\t\t\t\tThe administrative metadata section <amdSec> contains the administrative metadata pertaining to the digital object, its components and any original source material from which the digital object is derived. The <amdSec> is separated into four sub-sections that accommodate technical metadata (techMD), intellectual property rights (rightsMD), analog/digital source metadata (sourceMD), and digital provenance metadata (digiprovMD). Each of these subsections can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both. Multiple instances of the <amdSec> element can occur within a METS document and multiple instances of its subsections can occur in one <amdSec> element. This allows considerable flexibility in the structuring of the administrative metadata. METS does not define a vocabulary or syntax for encoding administrative metadata. Administrative metadata can be expressed within the amdSec sub-elements according to many current community defined standards, or locally produced XML schemas. ', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 426, 3)))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fileSec'), CTD_ANON_3, scope=metsType, documentation=' \n\t\t\t\t\t\tThe overall purpose of the content file section element <fileSec> is to provide an inventory of and the location for the content files that comprise the digital object being described in the METS document.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 432, 3)))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'structMap'), structMapType, scope=metsType, documentation=' \n\t\t\t\t\t\tThe structural map section <structMap> is the heart of a METS document. It provides a means for organizing the digital content represented by the <file> elements in the <fileSec> of the METS document into a coherent hierarchical structure. Such a hierarchical structure can be presented to users to facilitate their comprehension and navigation of the digital content. It can further be applied to any purpose requiring an understanding of the structural relationship of the content files or parts of the content files. The organization may be specified to any level of granularity (intellectual and or physical) that is desired. Since the <structMap> element is repeatable, more than one organization can be applied to the digital content represented by the METS document.  The hierarchical structure specified by a <structMap> is encoded as a tree of nested <div> elements. A <div> element may directly point to content via child file pointer <fptr> elements (if the content is represented in the <fileSec<) or child METS pointer <mptr> elements (if the content is represented by an external METS document). The <fptr> element may point to a single whole <file> element that manifests its parent <div<, or to part of a <file> that manifests its <div<. It can also point to multiple files or parts of files that must be played/displayed either in sequence or in parallel to reveal its structural division. In addition to providing a means for organizing content, the <structMap> provides a mechanism for linking content at any hierarchical level with relevant descriptive and administrative metadata.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 470, 3)))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'structLink'), CTD_ANON_11, scope=metsType, documentation=' \n\t\t\t\t\t\tThe structural link section element <structLink> allows for the specification of hyperlinks between the different components of a METS structure that are delineated in a structural map. This element is a container for a single, repeatable element, <smLink> which indicates a hyperlink between two nodes in the structural map. The <structLink> section in the METS document is identified using its XML ID attributes.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 477, 3)))

metsType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'behaviorSec'), behaviorSecType, scope=metsType, documentation='\n\t\t\t\t\t\tA behavior section element <behaviorSec> associates executable behaviors with content in the METS document by means of a repeatable behavior <behavior> element. This element has an interface definition <interfaceDef> element that represents an abstract definition of the set of behaviors represented by a particular behavior section. A <behavior> element also has a <mechanism> element which is used to point to a module of executable code that implements and runs the behavior defined by the interface definition. The <behaviorSec> element, which is repeatable as well as nestable, can be used to group individual behaviors within the structure of the METS document. Such grouping can be useful for organizing families of behaviors together or to indicate other relationships between particular behaviors.', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 489, 3)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 242, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 419, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 426, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 432, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 477, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 489, 3))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'metsHdr')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 242, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dmdSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 419, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'amdSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 426, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'fileSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 432, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'structMap')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 470, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'structLink')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 477, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(metsType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'behaviorSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 489, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
metsType._Automaton = _BuildAutomaton()




CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'agent'), CTD_ANON_9, scope=CTD_ANON, documentation='agent: \n\t\t\t\t\t\t\t\tThe agent element <agent> provides for various parties and their roles with respect to the METS record to be documented.  \n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 250, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'altRecordID'), CTD_ANON_, scope=CTD_ANON, documentation='    \n\t\t\t\t\t\t\t\t\tThe alternative record identifier element <altRecordID> allows one to use alternative record identifier values for the digital object represented by the METS document; the primary record identifier is stored in the OBJID attribute in the root <mets> element.\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 335, 6)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'metsDocumentID'), CTD_ANON_2, scope=CTD_ANON, documentation='    \n\t\t\t\t\t\t\t\t\tThe metsDocument identifier element <metsDocumentID> allows a unique identifier to be assigned to the METS document itself.  This may be different from the OBJID attribute value in the root <mets> element, which uniquely identifies the entire digital object represented by the METS document.\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 360, 6)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 250, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 335, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 360, 6))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'agent')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 250, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'altRecordID')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 335, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'metsDocumentID')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 360, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton_()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fileGrp'), CTD_ANON_10, scope=CTD_ANON_3, documentation=' \n\t\t\t\t\t\t\t\t\tA sequence of file group elements <fileGrp> can be used group the digital files comprising the content of a METS object either into a flat arrangement or, because each file group element can itself contain one or more  file group elements,  into a nested (hierarchical) arrangement. In the case where the content files are images of different formats and resolutions, for example, one could group the image content files by format and create a separate <fileGrp> for each image format/resolution such as:\n-- one <fileGrp> for the thumbnails of the images\n-- one <fileGrp> for the higher resolution JPEGs of the image \n-- one <fileGrp> for the master archival TIFFs of the images \nFor a text resource with a variety of content file types one might group the content files at the highest level by type,  and then use the <fileGrp> element\u2019s nesting capabilities to subdivide a <fileGrp> by format within the type, such as:\n-- one <fileGrp> for all of the page images with nested <fileGrp> elements for each image format/resolution (tiff, jpeg, gif)\n-- one <fileGrp> for a PDF version of all the pages of the document \n-- one <fileGrp> for  a TEI encoded XML version of the entire document or each of its pages.\nA <fileGrp> may contain zero or more <fileGrp> elements and or <file> elements.\t\t\t\t\t\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 440, 6)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'fileGrp')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 440, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_2()




amdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'techMD'), mdSecType, scope=amdSecType, documentation=' \n\t\t\t\t\t\tA technical metadata element <techMD> records technical metadata about a component of the METS object, such as a digital content file. The <techMD> element conforms to same generic datatype as the <dmdSec>, <rightsMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes.  A technical metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <techMD> elements; and technical metadata can be associated with any METS element that supports an ADMID attribute. Technical metadata can be expressed according to many current technical description standards (such as MIX and textMD) or a locally produced XML schema.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 535, 3)))

amdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'rightsMD'), mdSecType, scope=amdSecType, documentation='\n\t\t\t\t\t\tAn intellectual property rights metadata element <rightsMD> records information about copyright and licensing pertaining to a component of the METS object. The <rightsMD> element conforms to same generic datatype as the <dmdSec>, <techMD>, <sourceMD> and <digiprovMD> elements, and supports the same sub-elements and attributes. A rights metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <rightsMD> elements; and rights metadata can be associated with any METS element that supports an ADMID attribute. Rights metadata can be expressed according current rights description standards (such as CopyrightMD and rightsDeclarationMD) or a locally produced XML schema.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 542, 3)))

amdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'sourceMD'), mdSecType, scope=amdSecType, documentation='\n\t\t\t\t\t\tA source metadata element <sourceMD> records descriptive and administrative metadata about the source format or media of a component of the METS object such as a digital content file. It is often used for discovery, data administration or preservation of the digital object. The <sourceMD> element conforms to same generic datatype as the <dmdSec>, <techMD>, <rightsMD>,  and <digiprovMD> elements, and supports the same sub-elements and attributes.  A source metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <sourceMD> elements; and source metadata can be associated with any METS element that supports an ADMID attribute. Source metadata can be expressed according to current source description standards (such as PREMIS) or a locally produced XML schema.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 549, 3)))

amdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'digiprovMD'), mdSecType, scope=amdSecType, documentation='\n\t\t\t\t\t\tA digital provenance metadata element <digiprovMD> can be used to record any preservation-related actions taken on the various files which comprise a digital object (e.g., those subsequent to the initial digitization of the files such as transformation or migrations) or, in the case of born digital materials, the files\u2019 creation. In short, digital provenance should be used to record information that allows both archival/library staff and scholars to understand what modifications have been made to a digital object and/or its constituent parts during its life cycle. This information can then be used to judge how those processes might have altered or corrupted the object\u2019s ability to accurately represent the original item. One might, for example, record master derivative relationships and the process by which those derivations have been created. Or the <digiprovMD> element could contain information regarding the migration/transformation of a file from its original digitization (e.g., OCR, TEI, etc.,)to its current incarnation as a digital object (e.g., JPEG2000). The <digiprovMD> element conforms to same generic datatype as the <dmdSec>,  <techMD>, <rightsMD>, and <sourceMD> elements, and supports the same sub-elements and attributes. A digital provenance metadata element can either wrap the metadata  (mdWrap) or reference it in an external location (mdRef) or both.  METS allows multiple <digiprovMD> elements; and digital provenance metadata can be associated with any METS element that supports an ADMID attribute. Digital provenance metadata can be expressed according to current digital provenance description standards (such as PREMIS) or a locally produced XML schema.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 556, 3)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 535, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 542, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 549, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 556, 3))
    counters.add(cc_3)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(amdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'techMD')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 535, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(amdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'rightsMD')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 542, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(amdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'sourceMD')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 549, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(amdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'digiprovMD')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 556, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
amdSecType._Automaton = _BuildAutomaton_3()




fileGrpType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fileGrp'), fileGrpType, scope=fileGrpType, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 579, 3)))

fileGrpType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'file'), fileType, scope=fileGrpType, documentation='\n\t\t\t\t\t\tThe file element <file> provides access to the content files for the digital object being described by the METS document. A <file> element may contain one or more <FLocat> elements which provide pointers to a content file and/or a <FContent> element which wraps an encoded version of the file. Embedding files using <FContent> can be a valuable feature for exchanging digital objects between repositories or for archiving versions of digital objects for off-site storage. All <FLocat> and <FContent> elements should identify and/or contain identical copies of a single file. The <file> element is recursive, thus allowing sub-files or component files of a larger file to be listed in the inventory. Alternatively, by using the <stream> element, a smaller component of a file or of a related file can be placed within a <file> element. Finally, by using the <transformFile> element, it is possible to include within a <file> element a different version of a file that has undergone a transformation for some reason, such as format migration.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 580, 3)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 579, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 580, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(fileGrpType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'fileGrp')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 579, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(fileGrpType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'file')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 580, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
fileGrpType._Automaton = _BuildAutomaton_4()




structMapType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'div'), divType, scope=structMapType, documentation=" \n\t\t\t\t\t\tThe structural divisions of the hierarchical organization provided by a <structMap> are represented by division <div> elements, which can be nested to any depth. Each <div> element can represent either an intellectual (logical) division or a physical division. Every <div> node in the structural map hierarchy may be connected (via subsidiary <mptr> or <fptr> elements) to content files which represent that div's portion of the whole document. \n\t\t\t\t\t", location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 621, 3)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(structMapType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'div')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 621, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
structMapType._Automaton = _BuildAutomaton_5()




parType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'area'), areaType, scope=parType, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 780, 3)))

parType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'seq'), seqType, scope=parType, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 781, 3)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 780, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 781, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(parType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'area')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 780, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(parType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'seq')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 781, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
parType._Automaton = _BuildAutomaton_6()




seqType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'area'), areaType, scope=seqType, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 799, 3)))

seqType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'par'), parType, scope=seqType, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 800, 3)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 799, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 800, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(seqType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'area')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 799, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(seqType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'par')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 800, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
seqType._Automaton = _BuildAutomaton_7()




structLinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'smLink'), CTD_ANON_14, scope=structLinkType, documentation=' \n\t\t\t\t\t\tThe Structural Map Link element <smLink> identifies a hyperlink between two nodes in the structural map. You would use <smLink>, for instance, to note the existence of hypertext links between web pages, if you wished to record those links within METS. NOTE: <smLink> is an empty element. The location of the <smLink> element to which the <smLink> element is pointing MUST be stored in the xlink:href attribute.\n\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 960, 3)))

structLinkType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'smLinkGrp'), CTD_ANON_15, scope=structLinkType, documentation='\n\t\t\t\t\t\tThe structMap link group element <smLinkGrp> provides an implementation of xlink:extendLink, and provides xlink compliant mechanisms for establishing xlink:arcLink type links between 2 or more <div> elements in <structMap> element(s) occurring within the same METS document or different METS documents.  The smLinkGrp could be used as an alternative to the <smLink> element to establish a one-to-one link between <div> elements in the same METS document in a fully xlink compliant manner.  However, it can also be used to establish one-to-many or many-to-many links between <div> elements. For example, if a METS document contains two <structMap> elements, one of which represents a purely logical structure and one of which represents a purely physical structure, the <smLinkGrp> element would provide a means of mapping a <div> representing a logical entity (for example, a newspaper article) with multiple <div> elements in the physical <structMap> representing the physical areas that  together comprise the logical entity (for example, the <div> elements representing the page areas that together comprise the newspaper article).\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1017, 3)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(structLinkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'smLink')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 960, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(structLinkType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'smLinkGrp')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1017, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
structLinkType._Automaton = _BuildAutomaton_8()




behaviorSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'behaviorSec'), behaviorSecType, scope=behaviorSecType, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1099, 3)))

behaviorSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'behavior'), behaviorType, scope=behaviorSecType, documentation='\n\t\t\t\t\t\tA behavior element <behavior> can be used to associate executable behaviors with content in the METS document. This element has an interface definition <interfaceDef> element that represents an abstract definition of a set of behaviors represented by a particular behavior. A <behavior> element also has a behavior mechanism <mechanism> element, a module of executable code that implements and runs the behavior defined abstractly by the interface definition.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1100, 3)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1099, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1100, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(behaviorSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'behaviorSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1099, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(behaviorSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'behavior')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1100, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
behaviorSecType._Automaton = _BuildAutomaton_9()




behaviorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'interfaceDef'), objectType, scope=behaviorType, documentation='\n\t\t\t\t\t\tThe interface definition <interfaceDef> element contains a pointer to an abstract definition of a single behavior or a set of related behaviors that are associated with the content of a METS object. The interface definition object to which the <interfaceDef> element points using xlink:href could be another digital object, or some other entity, such as a text file which describes the interface or a Web Services Description Language (WSDL) file. Ideally, an interface definition object contains metadata that describes a set of behaviors or methods. It may also contain files that describe the intended usage of the behaviors, and possibly files that represent different expressions of the interface definition.\t\t\n\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1135, 3)))

behaviorType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mechanism'), objectType, scope=behaviorType, documentation=' \n\t\t\t\t\tA mechanism element <mechanism> contains a pointer to an executable code module that implements a set of behaviors defined by an interface definition. The <mechanism> element will be a pointer to another object (a mechanism object). A mechanism object could be another METS object, or some other entity (e.g., a WSDL file). A mechanism object should contain executable code, pointers to executable code, or specifications for binding to network services (e.g., web services).\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1142, 3)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1135, 3))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(behaviorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'interfaceDef')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1135, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(behaviorType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mechanism')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1142, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
behaviorType._Automaton = _BuildAutomaton_10()




mdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mdRef'), CTD_ANON_17, scope=mdSecType, documentation='\n\t\t\t\t\t\tThe metadata reference element <mdRef> element is a generic element used throughout the METS schema to provide a pointer to metadata which resides outside the METS document.  NB: <mdRef> is an empty element.  The location of the metadata must be recorded in the xlink:href attribute, supplemented by the XPTR attribute as needed.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1220, 3)))

mdSecType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mdWrap'), CTD_ANON_18, scope=mdSecType, documentation=' \n\t\t\t\t\t\tA metadata wrapper element <mdWrap> provides a wrapper around metadata embedded within a METS document. The element is repeatable. Such metadata can be in one of two forms: 1) XML-encoded metadata, with the XML-encoding identifying itself as belonging to a namespace other than the METS document namespace. 2) Any arbitrary binary or textual form, PROVIDED that the metadata is Base64 encoded and wrapped in a <binData> element within the internal descriptive metadata element.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1251, 3)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1220, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(mdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mdRef')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1220, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1251, 3))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(mdSecType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mdWrap')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1251, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=st_0)

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1220, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1251, 3))
    counters.add(cc_1)
    states = []
    sub_automata = []
    sub_automata.append(_BuildAutomaton_12())
    sub_automata.append(_BuildAutomaton_13())
    final_update = set()
    symbol = pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1219, 2)
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=True)
    st_0._set_subAutomata(*sub_automata)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
mdSecType._Automaton = _BuildAutomaton_11()




def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1273, 9))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_14()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'binData'), pyxb.binding.datatypes.base64Binary, scope=CTD_ANON_6, documentation='\n\t\t\t\t\t\t\t\t\tA binary data wrapper element <binData> is used to contain a Base64 encoded file.\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1366, 6)))

CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'xmlData'), CTD_ANON_7, scope=CTD_ANON_6, documentation='\n\t\t\t\t\t\t\t\t\tAn xml data wrapper element <xmlData> is used to contain  an XML encoded file. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> element is set to \u201clax\u201d. Therefore, if the source schema and its location are identified by means of an xsi:schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element.\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1373, 6)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1366, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1373, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'binData')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1366, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'xmlData')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1373, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_15()




def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=pyxb.binding.content.Wildcard.NC_any), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1381, 9))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_16()




def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 242, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 419, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 426, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 432, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 477, 3))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 489, 3))
    counters.add(cc_5)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'metsHdr')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 242, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'dmdSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 419, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'amdSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 426, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'fileSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 432, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'structMap')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 470, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'structLink')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 477, 3))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'behaviorSec')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 489, 3))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_8._Automaton = _BuildAutomaton_17()




CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'name'), pyxb.binding.datatypes.string, scope=CTD_ANON_9, documentation=' \n\t\t\t\t\t\t\t\t\t\t\tThe element <name> can be used to record the full name of the document agent.\n\t\t\t\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 258, 9)))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'note'), pyxb.binding.datatypes.string, scope=CTD_ANON_9, documentation=" \n\t\t\t\t\t\t\t\t\t\t\tThe <note> element can be used to record any additional information regarding the agent's activities with respect to the METS document.\n\t\t\t\t\t\t\t\t\t\t\t", location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 265, 9)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 265, 9))
    counters.add(cc_0)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'name')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 258, 9))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'note')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 265, 9))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_9._Automaton = _BuildAutomaton_18()




def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 579, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 580, 3))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'fileGrp')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 579, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'file')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 580, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_19()




def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'smLink')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 960, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'smLinkGrp')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1017, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_11._Automaton = _BuildAutomaton_20()




divType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'mptr'), CTD_ANON_12, scope=divType, documentation=' \n\t\t\t\t\t\tLike the <fptr> element, the METS pointer element <mptr> represents digital content that manifests its parent <div> element. Unlike the <fptr>, which either directly or indirectly points to content represented in the <fileSec> of the parent METS document, the <mptr> element points to content represented by an external METS document. Thus, this element allows multiple discrete and separate METS documents to be organized at a higher level by a separate METS document. For example, METS documents representing the individual issues in the series of a journal could be grouped together and organized by a higher level METS document that represents the entire journal series. Each of the <div> elements in the <structMap> of the METS document representing the journal series would point to a METS document representing an issue.  It would do so via a child <mptr> element. Thus the <mptr> element gives METS users considerable flexibility in managing the depth of the <structMap> hierarchy of individual METS documents. The <mptr> element points to an external METS document by means of an xlink:href attribute and associated XLink attributes. \t\t\t\t\t\t\t\t\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 660, 3)))

divType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'fptr'), CTD_ANON_13, scope=divType, documentation='\n\t\t\t\t\t\tThe <fptr> or file pointer element represents digital content that manifests its parent <div> element. The content represented by an <fptr> element must consist of integral files or parts of files that are represented by <file> elements in the <fileSec>. Via its FILEID attribute,  an <fptr> may point directly to a single integral <file> element that manifests a structural division. However, an <fptr> element may also govern an <area> element,  a <par>, or  a <seq>  which in turn would point to the relevant file or files. A child <area> element can point to part of a <file> that manifests a division, while the <par> and <seq> elements can point to multiple files or parts of files that together manifest a division. More than one <fptr> element can be associated with a <div> element. Typically sibling <fptr> elements represent alternative versions, or manifestations, of the same content\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 683, 3)))

divType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'div'), divType, scope=divType, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 734, 3)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 660, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 683, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 734, 3))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(divType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'mptr')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 660, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(divType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'fptr')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 683, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(divType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'div')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 734, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
divType._Automaton = _BuildAutomaton_21()




CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'par'), parType, scope=CTD_ANON_13, documentation=' \n\t\t\t\t\t\t\t\t\tThe <par> or parallel files element aggregates pointers to files, parts of files, and/or sequences of files or parts of files that must be played or displayed simultaneously to manifest a block of digital content represented by an <fptr> element. This might be the case, for example, with multi-media content, where a still image might have an accompanying audio track that comments on the still image. In this case, a <par> element would aggregate two <area> elements, one of which pointed to the image file and one of which pointed to the audio file that must be played in conjunction with the image. The <area> element associated with the image could be further qualified with SHAPE and COORDS attributes if only a portion of the image file was pertinent and the <area> element associated with the audio file could be further qualified with BETYPE, BEGIN, EXTTYPE, and EXTENT attributes if only a portion of the associated audio file should be played in conjunction with the image.\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 691, 6)))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'seq'), seqType, scope=CTD_ANON_13, documentation='  \n\t\t\t\t\t\t\t\t\tThe sequence of files element <seq> aggregates pointers to files,  parts of files and/or parallel sets of files or parts of files  that must be played or displayed sequentially to manifest a block of digital content. This might be the case, for example, if the parent <div> element represented a logical division, such as a diary entry, that spanned multiple pages of a diary and, hence, multiple page image files. In this case, a <seq> element would aggregate multiple, sequentially arranged <area> elements, each of which pointed to one of the image files that must be presented sequentially to manifest the entire diary entry. If the diary entry started in the middle of a page, then the first <area> element (representing the page on which the diary entry starts) might be further qualified, via its SHAPE and COORDS attributes, to specify the specific, pertinent area of the associated image file.\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 698, 6)))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'area'), areaType, scope=CTD_ANON_13, documentation=' \n\t\t\t\t\t\t\t\t\tThe area element <area> typically points to content consisting of just a portion or area of a file represented by a <file> element in the <fileSec>. In some contexts, however, the <area> element can also point to content represented by an integral file. A single <area> element would appear as the direct child of a <fptr> element when only a portion of a <file>, rather than an integral <file>, manifested the digital content represented by the <fptr>. Multiple <area> elements would appear as the direct children of a <par> element or a <seq> element when multiple files or parts of files manifested the digital content represented by an <fptr> element. When used in the context of a <par> or <seq> element an <area> element can point either to an integral file or to a segment of a file as necessary.\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 705, 6)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 691, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 698, 6))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 705, 6))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'par')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 691, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'seq')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 698, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'area')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 705, 6))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_13._Automaton = _BuildAutomaton_22()




CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'smLocatorLink'), CTD_ANON_4, scope=CTD_ANON_15, documentation='\n\t\t\t\t\t\t\t\t\tThe structMap locator link element <smLocatorLink> is of xlink:type "locator".  It provides a means of identifying a <div> element that will participate in one or more of the links specified by means of <smArcLink> elements within the same <smLinkGrp>. The participating <div> element that is represented by the <smLocatorLink> is identified by means of a URI in the associate xlink:href attribute.  The lowest level of this xlink:href URI value should be a fragment identifier that references the ID value that identifies the relevant <div> element.  For example, "xlink:href=\'#div20\'" where "div20" is the ID value that identifies the pertinent <div> in the current METS document. Although not required by the xlink specification, an <smLocatorLink> element will typically include an xlink:label attribute in this context, as the <smArcLink> elements will reference these labels to establish the from and to sides of each arc link.\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1025, 6)))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'smArcLink'), CTD_ANON_16, scope=CTD_ANON_15, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1040, 6)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=2, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1025, 6))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'smLocatorLink')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1025, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'smArcLink')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1040, 6))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_15._Automaton = _BuildAutomaton_23()




CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'binData'), pyxb.binding.datatypes.base64Binary, scope=CTD_ANON_18, documentation=' \n\t\t\t\t\t\t\t\t\tThe binary data wrapper element <binData> is used to contain Base64 encoded metadata.\t\t\t\t\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1259, 6)))

CTD_ANON_18._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'xmlData'), CTD_ANON_5, scope=CTD_ANON_18, documentation='\n\t\t\t\t\t\t\t\t\tThe xml data wrapper element <xmlData> is used to contain XML encoded metadata. The content of an <xmlData> element can be in any namespace or in no namespace. As permitted by the XML Schema Standard, the processContents attribute value for the metadata in an <xmlData> is set to \u201clax\u201d. Therefore, if the source schema and its location are identified by means of an XML schemaLocation attribute, then an XML processor will validate the elements for which it can find declarations. If a source schema is not identified, or cannot be found at the specified schemaLocation, then an XML validator will check for well-formedness, but otherwise skip over the elements appearing in the <xmlData> element. \t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1265, 6)))

def _BuildAutomaton_24 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_24
    del _BuildAutomaton_24
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1259, 6))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1265, 6))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'binData')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1259, 6))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_18._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'xmlData')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1265, 6))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_18._Automaton = _BuildAutomaton_24()




fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FLocat'), CTD_ANON_19, scope=fileType, documentation=' \n\t\t\t\t\t\tThe file location element <FLocat> provides a pointer to the location of a content file. It uses the XLink reference syntax to provide linking information indicating the actual location of the content file, along with other attributes specifying additional linking information. NOTE: <FLocat> is an empty element. The location of the resource pointed to MUST be stored in the xlink:href attribute.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1335, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'FContent'), CTD_ANON_6, scope=fileType, documentation='\n\t\t\t\t\t\tThe file content element <FContent> is used to identify a content file contained internally within a METS document. The content file must be either Base64 encoded and contained within the subsidiary <binData> wrapper element, or consist of XML information and be contained within the subsidiary <xmlData> wrapper element.\n\t\t\t\t\t', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1358, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'stream'), CTD_ANON_20, scope=fileType, documentation=' \n\t\t\t\t\t\tA component byte stream element <stream> may be composed of one or more subsidiary streams. An MPEG4 file, for example, might contain separate audio and video streams, each of which is associated with technical metadata. The repeatable <stream> element provides a mechanism to record the existence of separate data streams within a particular file, and the opportunity to associate <dmdSec> and <amdSec> with those subsidiary data streams if desired. ', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1400, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'transformFile'), CTD_ANON_21, scope=fileType, documentation='\n\t\t\t\t\t\tThe transform file element <transformFile> provides a means to access any subsidiary files listed below a <file> element by indicating the steps required to "unpack" or transform the subsidiary files. This element is repeatable and might provide a link to a <behavior> in the <behaviorSec> that performs the transformation.', location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1465, 3)))

fileType._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'file'), fileType, scope=fileType, location=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1514, 3)))

def _BuildAutomaton_25 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_25
    del _BuildAutomaton_25
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1335, 3))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1358, 3))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1400, 3))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1465, 3))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1514, 3))
    counters.add(cc_4)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FLocat')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1335, 3))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'FContent')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1358, 3))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'stream')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1400, 3))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'transformFile')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1465, 3))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(fileType._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'file')), pyxb.utils.utility.Location('/home/claudio/Applications/eudat/b2safe/manifest/mets.xsd', 1514, 3))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
fileType._Automaton = _BuildAutomaton_25()

