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
        if 'site_list' in config:
            for site_dir in config['site_list']:
                if 'input_dir' in config:
                    i_dir = utils.file_utils.make_pure(p=config['input_dir'])
                    if 'data_dir' in config:
                        i_dir = i_dir.joinpath(config['data_dir'])
                    i_dir = i_dir.joinpath(config['site_dir'])
                elif 'data_dir' in config:
                    i_dir = utils.file_utils.make_pure(p=config['data_dir'])
                    i_dir = i_dir.joinpath(config['site_dir'])
                else:
                    i_dir = i_dir.joinpath(config['site_dir'])
                   

                # root_path_str, file_stem_str='*', file_ext_str='*', recursive_bool=False, xclude_hidden_paths=True, rtn_abs_path_bool=True, rtn_uri=False
                html_file_list = utils.file_utils.get_file_list(root_path_str=html_dir)
                base_filename = html_file_list.pop(0)
                base_soup = utils.html_utils.make_a_soup(filename=base_filename)
                if not base_filename.suffix:
                    suff = ''
                else:
                    suff = base_filename.suffix
                pp_filename = base_filename.parent.joinpath('list', str(base_filename.stem) + '_pp' + suff)
                utils.file_utils.write_file(fn=pp_filename,
                                            overwrite=True,
                                            content=base_soup.prettify())
                # success = utils.html_utils.write_ppsoup(base_soup, 'test/base_soup.html')
                for next_filename in html_file_list:
                    next_soup = utils.html_utils.make_a_soup(filename=next_filename)
                    if not next_filename.suffix:
                        suff = ''
                    else:
                        suff = next_filename.suffix
                    pp_filename = next_filename.parent.joinpath('list', str(next_filename.stem) + '_pp' + suff)
                    utils.file_utils.write_file(fn=pp_filename,
                                                overwrite=True,
                                                content=next_soup.prettify())

                    base_list, next_list, block_match = utils.html_utils.diff_a_soup(s1=base_soup, s2=next_soup)
                    base_list_filename = base_filename.parent.joinpath('list', base_filename.name)
                    if not base_list_filename.parent.is_dir():
                        base_list_filename.parent.mkdir()
                    next_list_filename = next_filename.parent.joinpath('list', next_filename.name)
                    utils.file_utils.write_file(fn=base_list_filename,
                                                overwrite=True,
                                                # content=pprint.pformat(base_list))
                                                content=base_list)

                    utils.file_utils.write_file(fn=next_list_filename,
                                                overwrite=True,
                                                # content=pprint.pformat(next_list))
                                                content=next_list)
                    block_list_filename = base_list_filename.with_name(base_filename.stem + '__' + next_filename.stem + '.txt')
                    utils.file_utils.write_file(fn=block_list_filename,
                                                overwrite=True,
                                                content=pprint.pformat(block_match))

                #break
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