"""
Functions that communicate with OBS API
and work with related XML data.
"""


from .. import connection as osc_connection
from .. import core as osc_core


def get(apiurl, path, query=None):
    """
    Send a GET request to OBS.

    :param apiurl: OBS apiurl.
    :type  apiurl: str
    :param path: URL path segments.
    :type  path: list(str)
    :param query: URL query values.
    :type  query: dict(str, str)
    :returns: Parsed XML root.
    :rtype:   xml.etree.ElementTree.Element
    """
    assert apiurl
    assert path

    if not isinstance(path, (list, tuple)):
        raise TypeError("Argument `path` expects a list of strings")

    url = osc_core.makeurl(apiurl, path, query)
    with osc_connection.http_GET(url) as f:
        root = osc_core.ET.parse(f).getroot()
    return root


def find_nodes(root, root_name, node_name):
    """
    Find nodes with given `node_name`.
    Also, verify that the root tag matches the `root_name`.

    :param root: Root node.
    :type  root: xml.etree.ElementTree.Element
    :param root_name: Expected (tag) name of the root node.
    :type  root_name: str
    :param node_name: Name of the nodes we're looking for.
    :type  node_name: str
    :returns: List of nodes that match the given `node_name`.
    :rtype:   list(xml.etree.ElementTree.Element)
    """
    assert root.tag == root_name
    return root.findall(node_name)


def find_node(root, root_name, node_name=None):
    """
    Find a single node with given `node_name`.
    If `node_name` is not specified, the root node is returned.
    Also, verify that the root tag matches the `root_name`.

    :param root: Root node.
    :type  root: xml.etree.ElementTree.Element
    :param root_name: Expected (tag) name of the root node.
    :type  root_name: str
    :param node_name: Name of the nodes we're looking for.
    :type  node_name: str
    :returns: The node that matches the given `node_name`
              or the root node if `node_name` is not specified.
    :rtype:   xml.etree.ElementTree.Element
    """

    assert root.tag == root_name
    if node_name:
        return root.find(node_name)
    return root


def write_xml_node_to_file(node, path, indent=True):
    """
    Write a XML node to a file.

    :param node: Node to write.
    :type  node: xml.etree.ElementTree.Element
    :param path: Path to a file that will be written to.
    :type  path: str
    :param indent: Whether to indent (pretty-print) the written XML.
    :type  indent: bool
    """
    if indent:
        osc_core.xmlindent(node)
    osc_core.ET.ElementTree(node).write(path)
