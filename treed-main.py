import re
import collections
import os
import sys
from io import StringIO
from lxml import etree
import lxml.html
import yaml
from xmldiff import main as xd
import pprint

from utils import file_utils, yaml_utils


def get_html_file_list(html_dir):
    file_list = file_utils.get_file_list(root_path_str=html_dir, file_stem_str='*', file_ext_str='*', recursive_bool=False, rtn_abs_path_bool=True, rtn_uri=False)
    if 0 < len(file_list) < 2:
        print('Only one file found, exiting.')
        return None
        # xml = file_list[0].read_text()
    elif 1 < len(file_list) :
        # print(file_list[0])
        return file_list
    else:
        print('File not found, exiting.')
        return None


def make_tree(fn):
    try:
        print('Reading file: ' + str(fn))
        html_text = fn.read_text()
    except:
        print('Could not read: ' + str(fn))
    html = etree.parse(StringIO(html_text), parser=html_parser)
    return html


def compare_trees():
    if 'dirlist' in config:
        for html_dir in config['dirlist']:
            html_file_list = get_html_file_list(html_dir=html_dir)
            base_html_tree = make_tree(fn=html_file_list.pop(0))
            for html_filename in html_file_list:
                html_tree = make_tree(fn=html_filename)
                # diff_formatter = xd.formatting.XMLFormatter(pretty_print=True)
                # diff_formatter = xd.formatting.XmlDiffFormatter(normalize='WS_TAGS', pretty_print=True)
                diff_formatter = xd.formatting.DiffFormatter(pretty_print=True)
                diff_o = {"F": 0.5}
                html_diff = xd.diff_trees(left=base_html_tree,
                                          right=html_tree,
                                          diff_options=diff_o,
                                          formatter=diff_formatter)
                with open(str(html_filename).replace('html', 'diff'), 'w') as diff_out:
                    diff_out.write(html_diff)





def setup():
    global html_parser, config
    html_parser = etree.HTMLParser()
    config = yaml_utils.load_config()
    return True


if __name__ == "__main__":
    success = setup()
    if not success:
        print('Failed to complete setup, exiting.')
        sys.exit()
    
    compare_trees()

# raw_tree = etree.ElementTree(html)
# nice_tree = collections.OrderedDict()
 
# print(html.body)
# tag_body_flag = False
# for tag in html.iter():
#     #print(tag)
#     path = re.sub('\[[0-9]+\]', '', html.getpath(tag))
#     if path not in nice_tree:
#         nice_tree[path] = []
#     if len(tag.keys()) > 0:
#         nice_tree[path].extend(attrib for attrib in tag.keys() if attrib not in nice_tree[path])            
 
# for path, attribs in nice_tree.items():
#     indent = int(path.count('/') - 1)
#     print('{0}{1}: {2} [{3}]'.format('    ' * indent, indent, path.split('/')[-1], ', '.join(attribs) if len(attribs) > 0 else '-'))
    
