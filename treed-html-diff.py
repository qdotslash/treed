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
# import utils
from utils import file_utils
from utils import html_utils
from utils import yaml_utils
from utils import setup_utils
#
# main function
#
def main():
    global config
    config, base_dir_dict = setup_utils.setup()
    if not config:
        print('Failed to complete setup, exiting.')
        sys.exit()
    else:
        if 'data_list' in config:
            for data_dir in config['data_list']:
                if 'input' in base_dir_dict:
                    i_dir = base_dir_dict['input'].joinpath(data_dir).resolve()
                if 'work' in base_dir_dict:
                    w_dir = base_dir_dict['work'].joinpath(data_dir).resolve()
                if 'output' in base_dir_dict:
                    o_dir = base_dir_dict['output'].joinpath(data_dir).resolve()
                if not w_dir.is_dir():
                    w_dir.mkdir(parents=True)
                if not o_dir.is_dir():
                    o_dir.mkdir(parents=True)

                # root_path_str, file_stem_str='*', file_ext_str='*', recursive_bool=False, xclude_hidden_paths=True, rtn_abs_path_bool=True, rtn_uri=False
                print('Working in: ' + str(i_dir))
                html_file_list = file_utils.get_file_list(root_path_str=str(i_dir))
                base_filename = html_file_list.pop(0)
                #
                #
                #

                base_soup = html_utils.make_a_soup(filename=base_filename)
                if not base_filename.suffix:
                    suff = '.html'
                else:
                    suff = base_filename.suffix
                pp_filename = w_dir.joinpath(str(base_filename.stem) + '_pp' + suff)
                file_utils.write_file(fn=pp_filename,
                                            overwrite=True,
                                            content=base_soup.prettify())
                # success = utils.html_write_ppsoup(base_soup, 'test/base_soup.html')
                for next_filename in html_file_list:
                    next_soup = html_utils.make_a_soup(filename=next_filename)
                    if not next_filename.suffix:
                        suff = '.html'
                    else:
                        suff = next_filename.suffix
                    pp_filename = w_dir.joinpath(str(next_filename.stem) + '_pp' + suff)
                    file_utils.write_file(fn=pp_filename,
                                                overwrite=True,
                                                content=next_soup.prettify())

                    base_list, next_list, block_match = html_utils.diff_a_soup(s1=base_soup, s2=next_soup)
                    base_list_filename = w_dir.joinpath(base_filename.stem + '_tabs' + '.txt')
                    next_list_filename = w_dir.joinpath(next_filename.stem + '_tabs' + '.txt')
                    file_utils.write_file(fn=base_list_filename,
                                                overwrite=True,
                                                # content=pprint.pformat(base_list))
                                                content=base_list)

                    file_utils.write_file(fn=next_list_filename,
                                                overwrite=True,
                                                # content=pprint.pformat(next_list))
                                                content=next_list)
                    block_list_filename = o_dir.joinpath(base_filename.stem + '__' + next_filename.stem + '.txt')
                    file_utils.write_file(fn=block_list_filename,
                                                overwrite=True,
                                                content=pprint.pformat(block_match))

                #break
#
#
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
#
#
def setup():
    global config
    config = yaml_utils.load_config()
    return True
#
#
if __name__ == "__main__":
    main()