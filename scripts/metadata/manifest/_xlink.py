# ./_xlink.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:b43cd366527ddb6a0e58594876e07421e0148f30
# Generated 2016-03-03 17:55:40.721802 by PyXB version 1.2.4 using Python 2.7.10.final.0
# Namespace http://www.w3.org/1999/xlink [xmlns:xlink]

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

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.w3.org/1999/xlink', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

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
    _XSDLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 10, 4)
    _Documentation = None
STD_ANON._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON, enum_prefix=None)
STD_ANON.new = STD_ANON._CF_enumeration.addEnumeration(unicode_value='new', tag='new')
STD_ANON.replace = STD_ANON._CF_enumeration.addEnumeration(unicode_value='replace', tag='replace')
STD_ANON.embed = STD_ANON._CF_enumeration.addEnumeration(unicode_value='embed', tag='embed')
STD_ANON.other = STD_ANON._CF_enumeration.addEnumeration(unicode_value='other', tag='other')
STD_ANON.none = STD_ANON._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
STD_ANON._InitializeFacetMap(STD_ANON._CF_enumeration)

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('http://www.loc.gov/standards/xlink/xlink.xsd', 21, 4)
    _Documentation = None
STD_ANON_._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=STD_ANON_, enum_prefix=None)
STD_ANON_.onLoad = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='onLoad', tag='onLoad')
STD_ANON_.onRequest = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='onRequest', tag='onRequest')
STD_ANON_.other = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='other', tag='other')
STD_ANON_.none = STD_ANON_._CF_enumeration.addEnumeration(unicode_value='none', tag='none')
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_enumeration)
