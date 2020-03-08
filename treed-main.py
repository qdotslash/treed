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
import utils
# from utils import file_utils
# from utils import html_utils
# from utils import yaml_utils
#
# main function
#
def main():
    success = setup()
    if not success:
        print('Failed to complete setup, exiting.')
        sys.exit()
    else:
        if 'dirlist' in config:
            for html_dir in config['dirlist']:
                # root_path_str, file_stem_str='*', file_ext_str='*', recursive_bool=False, xclude_hidden_paths=True, rtn_abs_path_bool=True, rtn_uri=False
                html_file_list = utils.file_utils.get_file_list(root_path_str=html_dir)
                base_soup = utils.html_utils.make_a_soup(filename=html_file_list.pop(0))
                # success = utils.html_utils.write_ppsoup(base_soup, 'test/base_soup.html')
                for file in html_file_list:
                    next_soup = utils.html_utils.make_a_soup(filename=file)
                    diff = utils.html_utils.diff_a_soup(s1=base_soup, s2= next_soup)
                    print('********************')
                    diff = utils.html_utils.diff_a_soup(s1=next_soup, s2=base_soup)
                break
#
#
def get_html_file_list(html_dir):
    file_list = utils.file_utils.get_file_list(root_path_str=html_dir, file_stem_str='*', file_ext_str='*', recursive_bool=False, rtn_abs_path_bool=True, rtn_uri=False)
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
#
#
def setup():
    global config
    config = utils.yaml_utils.load_config()
    return True
#
#
if __name__ == "__main__":
    main()