import regex
from pprint import pprint as pp
from utils import file_utils, setup_utils, html_utils


def main():
    global config
    config, base_dir_dict = setup_utils.setup()
    re_tags = regex.compile(r'(\<(\w+)[^\>]*\>((?!</\2\>).*?)?\<(\/\2)\>)')
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
                
                print('\nWorking in: ' + str(w_dir))
                html_file_list = file_utils.get_file_list(root_path_str=str(w_dir), file_stem_str='*_pp', file_ext_str='html')
                base_filename = html_file_list.pop(0)
                base_string = html_utils.make_a_string(filename=base_filename)
                if not base_filename.suffix:
                    suff = ''
                else:
                    suff = base_filename.suffix
                base_string = html_utils.make_a_string(filename=base_filename)
                m2 = re_tags.findall(base_string, overlapped=True)
                # m2 = regex.findall(, base_string, overlapped=True)
                m3 = []
                for tup in m2:
                    if tup[1] not in ['html', 'head', 'body', 'p', 'em', 'i', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7']:
                        m3.append(tup)

                for next_filename in html_file_list:
                    next_string = html_utils.make_a_string(filename=next_filename)
                    for tup in m3:
                        next_string = next_string.replace(tup[0], '')
                    next_soup = html_utils.make_a_soup(html_doc_string=next_string)
                    next_fn = o_dir.joinpath('minimized_' + next_filename.stem.replace('_pp', '') + '.html')
                    print('next fn: ' + str(next_fn))
                    file_utils.write_file(fn=next_fn,
                                                overwrite=True,
                                                content=next_soup.prettify())
                # print('Done.')
                # break
        else:
            print('data list not in config.')

    # s = '<tag0>a01bbba<tag01><tag1>a10</bb>ba</tag1>"a02bbba"<tag2><tag21>a21bbba</tag21><tag22>a22bbba</tag22>a20bbba</tag2>a03bbba<tag3>a31bbba</tag3><tag4></tag4></tag01>a04bbba</tag0>'

    # # m = regex.match(r'<(\w++)>(?:[^<>]|(?R))*+</\1>', s).groups()
    # # b(?:m|(?R))*e
    # # m = regex.findall(r'\<(\w+)\>(?:([^\<]*)|(?R))*\<(\/\2)\>)\<(\/\1\)>', s)
    # # m = regex.findall(r'\<(\w+)\>([^\<]*)(?:([^\<]*)|(?R))*([^\<]*)\<(\/\1)\>', s)
    # # m0 = regex.findall(r'(\<(\w+)\>([^\<]*)*(\<(\w+)\>([^\<]*)\<(\/\5)\>)*([^\<]*)\<(\/\2)\>)+', s)
    # # m1 = regex.match(r'((\<(\w+)\>(.*?)?\<(\/\3)\>)|(?R))', s)
    # m2 = regex.findall(r'(\<(\w+)\>((?!</\2\>).*?)?\<(\/\2)\>)', s, overlapped=True)
    # # m10 = regex.findall(r'(\<(\w+)\>([^\<]*)?\<(/\2)\>)(([^\<]*)?(\<(\w+)\>([^\<]*)?\<(/\8)\>))+', s)

    # # m20 = regex.match(r'(\<(\w+)\>)([^\<]*)?((\<(\w+)\>([^\<]*)\<(\/\6)\>([^\<]*)?)|(?R))*(\<(\/\2)\>)', s).groups()

    # # print(m0)
    # # print(m1.groups())
    # pp(m2)
    # # print(m10)
    # # print(m20)
    # #
    # #
if __name__ == "__main__":
    main()