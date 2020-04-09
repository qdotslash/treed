import sys
from lxml import etree
from io import StringIO
from difflib import SequenceMatcher
import regex
from pprint import pprint as pp
from bs4 import BeautifulSoup
import html5lib
from utils import file_utils, setup_utils, html_utils


def main():
    global config
    config, base_dir_dict = setup_utils.setup()
    tag_omit_list = ['html', 'head', 'body', 'p', 'br', 'em', 'time', 'strong', 'i', 'b', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'table', 'thead', 'tbody', 'tr', 'td', 'tfoot']
    xml_parser = etree.HTMLParser()

    # re_ulol = regex.compile(r'(\<(ul|ol)(?!href).*href[ ="]+https*\:\/\/[^=\>]+=http[^\>]+\>(?!</\2\>).*\<(\/\2)\>)')
    # re_li_a = regex.compile(r'(<li[^\>]*\>\s*\<a[^\>]+\shref\=("(javascript|http|\/)[^"]+")[^\>]*\>(?!\<\/a\>).*?\<\/a\>.*?\<\/li\>)')
    # re_href = regex.compile(r'(\<a[^\>]+\shref\=("http[^"]+")[^\>]*\>(?!\<\/a\>).*?\<\/a\>)')
    # re_tags = regex.compile(r'(\<(\w+)[^\>]*\>((?!</\2\>).*?)?\<(\/\2)\>)')
    re_empty = regex.compile(r'(\<([^ /">]+)[^\>]*\>\s*\<\/\2\>)')
    re_head_foot = regex.compile(r'(\<(header|footer|form|script|noscript|iframe|button)[^\>]*\>((?!</\2\>).*?)?\<\/\2\>)')
    re_input = regex.compile(r'(\<(input)[^\>]*\>((?!</\2\>).*?)?\/>)')
    re_comment = regex.compile(r'(\<\!\-\-((?!\-\-\>).*?)?\-\-\>)')
    re_tag_name = regex.compile(r'^<([^ /">]+)')
    re_reverse = regex.compile(r'((?r)\<(\w+)(?!\w).*?\/>)', regex.DOTALL)
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
                #
                #
                #
                print('\nPretty printing in: ' + str(i_dir))
                input_file_list = file_utils.get_file_list(root_path_str=str(i_dir))
                working_file_list = []
                seq_2 = None
                common_elements = None
                for pp_file in input_file_list:
                    print('Working with: ' + str(pp_file))
                    pp_soup = html_utils.make_a_soup(filename=pp_file)
                    base_string = str(pp_soup).replace('\n', '')
                    rever = re_reverse.findall(base_string)
                    for r in rever:
                        print(r[0].replace('/>', '>' + '</' + r[1] + '>'))
                    break
                    working_soup = html_utils.make_a_soup(html_doc_string=working_string)
                    output_filename = o_dir.joinpath('minimized_' + working_filename.stem.replace('_pp', '') + '.html')
                    print('output filename: ' + str(output_filename))
                    file_utils.write_file(fn=output_filename,
                                                overwrite=True,
                                                content=working_soup.prettify())
                    
                print('Done with: ' + str(w_dir))
                # break
        else:
            print('data list not in config.')
    # #
    # #
if __name__ == "__main__":
    main()