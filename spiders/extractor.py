import sys
from cStringIO import StringIO
from itertools import chain
import socket

from lxml import etree #http://codespeak.net/lxml/

socket.setdefaulttimeout(10)

IGNORABLE_TAGS = set(['script', 'a'])
MIN_TEXT_LEN = 50
STATUS_OK = 200
STATUS_NOT_FOUND = 404

def remove_node(node):
    node.getparent().remove(node)

def get_text(node):
    '''
    Given a XML node, extract all the text it contains.
    (does not recurse into children)
    '''
    text = [node.text or '']
    for cnode in node.getchildren():
        tail = cnode.tail
        if tail is not None:
            text.append(cnode.tail)

    text = '\n'.join(text).strip()
    return text

def get_xml(node):
    '''
    Convert the sub-tree from node downwards
    into string XML representation.
    '''
    return etree.tostring(node)

def create_doc(data):
    '''
    Construct XML tree datastructure from xml string representation.
    '''
    parser = etree.HTMLParser()
    doc = etree.parse(StringIO(data), parser)
    return doc


def get_meta_info(html_page):
    meta_desc = html_page.xpath('//meta[@name = "description"]/@content')
    meta_title =html_page.xpath('//meta[@name = "title"]/@content')
    meta_keywords = html_page.xpath('//meta[@name = "keywords"]/@content')

    if not meta_desc:
        meta_desc = [""]

    if not meta_title:
        meta_title = [""]

    if not meta_keywords:
        meta_keywords = [""]

    return meta_desc,meta_title,meta_keywords

def get_content_nodes(doc):
    '''
    Identify nodes in the XML document that
    have substantial text.
    '''
    nodes = []

    for n in doc.xpath('//*'):
        tag = n.tag

        if tag.lower() in IGNORABLE_TAGS:
            continue

        text = get_text(n)
        if not text:
            continue

        if len(text) < MIN_TEXT_LEN:
            continue

        nodes.append(n)

    return nodes

def make_pruned_tree(content_nodes):
    '''
    Prune the whole XML tree by remnoving nodes
    other than content nodes and their ancestors.
    '''
    nodes = {}
    links = {}
    for node in content_nodes:

        nodes[id(node)] = node

        parent = node.getparent()
        if parent is not None:
            links[id(node)] = id(parent)

        for anode in node.iterancestors():
            _id = id(anode)
            parent = anode.getparent()
            if parent is not None:
                links[_id] = id(parent)

            if _id not in nodes:
                nodes[_id] = anode
    return nodes, links

def get_inlink_counts(links):
    '''
    Given the inter-node links, find out which
    node has maximum number of links coming into it.
    '''
    counts = {}

    for from_id, to_id in links.iteritems():
        count = counts.setdefault(to_id, 0)
        counts[to_id] = count + 1

    return counts

def get_most_linked_node(nodes, links):
    '''
    Identify the node which is most linked.
    (i,e) has most number of inlinks.
    '''
    inlink_counts = get_inlink_counts(links)

    mcount, mid = max([(count, _id) for _id, count in inlink_counts.iteritems()])
    node = nodes[mid]
    return node

def make_dot_graph(nodes, links, chosen_node, stream):
    '''
    Construct the dot format graph representation
    so that graphviz can render the tree for visualization.
    '''
    o = stream
    graph_code = ''
    graph_code += "digraph G {\n"

    for _id, node in nodes.iteritems():

        tlen = len(get_text(node))
        tag = node.tag

        if tlen:
            text = '%s (%d)' % (tag, tlen)
        else:
            text = tag

        if _id == chosen_node:
            attrs = 'style=filled color=lightblue'
        else:
            attrs = ''

        graph_code += "%s [label=\"%s\" %s];\n" % (_id, text, attrs)

    for fid, tid in links.iteritems():
        graph_code += "%d -> %d;\n" % (fid, tid)

    graph_code += "}"
    return graph_code


def _process(html_page):
    # make doc from html data (cleans html)
    #html_page is the data in the page i.e. page_source
    doc = create_doc(html_page)

    # remove all script/style nodes
    for tag in ('script', 'style'):
        for node in doc.xpath('.//%s' % tag):
            remove_node(node)

    #get meta title, description, keywords
    meta_desc, meta_title, meta_keywords = get_meta_info(doc)

    # identify content nodes
    content_nodes = get_content_nodes(doc)

    if not content_nodes:
        return ''

    # prune xml tree to remove irrelevant nodes
    nodes, links = make_pruned_tree(content_nodes)

    # get the most linked node from pruned tree
    mnode = get_most_linked_node(nodes, links)

    # make the dot graph
    graph_code = make_dot_graph(nodes, links, id(mnode), sys.stdout)

    text = '\n'.join([x.strip() for x in mnode.xpath('.//text()') if x.strip()])
    meta_info = {}
    meta_info['description'] = meta_desc[0]
    meta_info['title'] = meta_title[0]
    meta_info['keywords'] = meta_keywords[0]

    #text = text.encode('utf8')
    data = {'text':text, 'meta':meta_info, 'graph':graph_code}
    return data

def process_text(page):
    page = page.encode('utf8')
    data = _process(page)
    if not data:
        return dict(status=STATUS_NOT_FOUND)

    return dict(status=STATUS_OK, data=data)

def process_url(url):
    import urllib2;
    page = urllib2.build_opener()
    page.addheaders = [('User-agent', 'Mozilla/5.0')]
    page = page.open(url)
    #page = urllib.urlopen(url).read()
    #page = urllib.urlopen(url)
    con_type = page.info().getheader('Content-Type')
    if not 'text/html' in con_type:
        return dict(status=STATUS_NOT_FOUND)

    page = page.read()
    #page = page.encode('utf8')
    data = _process(page)

    return data
