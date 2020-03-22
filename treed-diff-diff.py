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
            for diff_dir in config['dirlist']:
                # root_path_str, file_stem_str='*__*', file_ext_str='*', recursive_bool=False, xclude_hidden_paths=True, rtn_abs_path_bool=True, rtn_uri=False
                diff_file_list = utils.file_utils.get_file_list(root_path_str=diff_dir,
                                                                file_stem_str='*__*',
                                                                file_ext_str='*',
                                                                recursive_bool=True)
                base_filename = diff_file_list.pop(0)
                base_list = utils.file_utils.return_list(fn=base_filename)
                # print(base_list)
                # break
                base_list_filename = base_filename.parent.joinpath('diff', base_filename.name)
                if not base_list_filename.parent.is_dir():
                    base_list_filename.parent.mkdir()
                else:
                    utils.file_utils.delete_folder(pth=base_list_filename.parent)
                    base_list_filename.parent.mkdir()

                for next_filename in diff_file_list:
                    next_list = utils.file_utils.return_list(fn=next_filename)
                    diff_list = utils.html_utils.diff_a_list(l1=base_list, l2=next_list)
                    diff_list_filename = base_list_filename.with_name(base_filename.stem + '__' + next_filename.stem + '__diff.txt')
                    utils.file_utils.write_file(fn=diff_list_filename,
                                                overwrite=True,
                                                content=pprint.pformat(diff_list))

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