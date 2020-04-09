import sys
import regex
from pprint import pprint as pp
from utils import file_utils, setup_utils, html_utils


def main():
    global config
    config, base_dir_dict = setup_utils.setup()
    tag_omit_list = ['html', 'head', 'body', 'p', 'br', 'em', 'time', 'strong', 'i', 'b', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'table', 'thead', 'tbody', 'tr', 'td', 'tfoot']
    # re_ulol = regex.compile(r'(\<(ul|ol)(?!href).*href[ ="]+https*\:\/\/[^=\>]+=http[^\>]+\>(?!</\2\>).*\<(\/\2)\>)')
    re_li_a = regex.compile(r'(<li[^\>]*\>\s*\<a[^\>]+\shref\=("(javascript|http|\/)[^"]+")[^\>]*\>(?!\<\/a\>).*?\<\/a\>.*?\<\/li\>)')
    # re_href = regex.compile(r'(\<a[^\>]+\shref\=("http[^"]+")[^\>]*\>(?!\<\/a\>).*?\<\/a\>)')
    re_tags = regex.compile(r'(\<(\w+)[^\>]*\>((?!</\2\>).*?)?\<(\/\2)\>)')
    re_empty = regex.compile(r'(\<(div)[^\>]*\>\s*\<\/\2\>)')
    re_head_foot = regex.compile(r'(\<(header|footer|form|script)[^\>]*\>((?!</\2\>).*?)?\<\/\2\>)')
    re_input = regex.compile(r'(\<(input)[^\>]*\>((?!</\2\>).*?)?\/>)')
    re_comment = regex.compile(r'(\<\!\-\-((?!\-\-\>).*?)?\-\-\>)')
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
                pp_file_list = file_utils.get_file_list(root_path_str=str(i_dir))
                for pp_file in pp_file_list:
                    pp_soup = html_utils.make_a_soup(filename=pp_file)
                    # if not pp_file.suffix:
                    #         suff = '.html'
                    # else:
                    #     suff = pp_file.suffix
                    suff = '.html'
                    pp_filename = w_dir.joinpath(str(pp_file.stem) + '_pp' + suff)
                    file_utils.write_file(fn=pp_filename,
                                                overwrite=True,
                                                content=pp_soup.prettify())
                print('Done pretty printing in: ' + str(i_dir))

                print('Working in: ' + str(w_dir))
                html_file_list = file_utils.get_file_list(root_path_str=str(w_dir), file_stem_str='*_pp', file_ext_str='html')
                base_filename = html_file_list[0]
                base_string = html_utils.make_a_string(filename=base_filename)
                m2 = re_tags.findall(base_string, overlapped=True)
                # m2 = regex.findall(, base_string, overlapped=True)
                m3 = []
                for tup in m2:
                    if tup[1] not in tag_omit_list:
                        omit_flag = False
                        for omit in tag_omit_list:
                            if '<' + omit in tup[1]:
                                omit_flag = True
                                break
                        if not omit_flag:
                            m3.append(tup)

                for next_filename in html_file_list:
                    next_string = html_utils.make_a_string(filename=next_filename)
                    for tup in m3:
                        next_string = next_string.replace(tup[0], '')

                    m4 = re_comment.findall(next_string)
                    while m4:
                        for m in m4:
                            # print(m)
                            # sys.exit()
                            next_string = next_string.replace(m[0], '')
                            m4 = re_comment.findall(next_string)
                    
                    m4 = re_li_a.findall(next_string)
                    while m4:
                        for m in m4:
                            # print(m)
                            # sys.exit()
                            next_string = next_string.replace(m[0], '')
                            m4 = re_li_a.findall(next_string)
                    #
                    # m4 = re_href.findall(next_string)
                    # while m4:
                    #     for m in m4:
                    #         # print(m)
                    #         # sys.exit()
                    #         next_string = next_string.replace(m[0], '')
                    #         m4 = re_href.findall(next_string)
                    #
                    m4 = re_head_foot.findall(next_string)
                    while m4:
                        for m in m4:
                            next_string = next_string.replace(m[0], '')
                            m4 = re_head_foot.findall(next_string)
                    #
                    m4 = re_input.findall(next_string)
                    while m4:
                        for m in m4:
                            next_string = next_string.replace(m[0], '')
                            m4 = re_input.findall(next_string)
                    #
                    m4 = re_empty.findall(next_string, overlapped=True)
                    while m4:
                        for m in m4:
                            next_string = next_string.replace(m[0], '')
                            m4 = re_empty.findall(next_string, overlapped=True)
                            
                    next_soup = html_utils.make_a_soup(html_doc_string=next_string)
                    next_fn = o_dir.joinpath('minimized_' + next_filename.stem.replace('_pp', '') + '.html')
                    print('next fn: ' + str(next_fn))
                    file_utils.write_file(fn=next_fn,
                                                overwrite=True,
                                                content=next_soup.prettify())
                    # break
                print('Done with: ' + str(w_dir))
                # break
        else:
            print('data list not in config.')
    # #
    # #
if __name__ == "__main__":
    main()