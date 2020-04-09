import sys
from lxml import etree
from io import StringIO
import regex
from pprint import pprint as pp
from bs4 import BeautifulSoup
import html5lib
from utils import file_utils, setup_utils, html_utils


def main():
    global config
    config, base_dir_dict = setup_utils.setup()
    tag_omit_list = ['html', 'head', 'body', 'p', 'br', 'em', 'time', 'strong', 'i', 'b', 'code', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'table', 'thead', 'tbody', 'tr', 'td', 'tfoot']
    xml_parser = etree.HTMLParser(strip_cdata=False)

    # re_ulol = regex.compile(r'(\<(ul|ol)(?!href).*href[ ="]+https*\:\/\/[^=\>]+=http[^\>]+\>(?!</\2\>).*\<(\/\2)\>)')
    # re_li_a = regex.compile(r'(<li[^\>]*\>\s*\<a[^\>]+\shref\=("(javascript|http|\/)[^"]+")[^\>]*\>(?!\<\/a\>).*?\<\/a\>.*?\<\/li\>)')
    # re_href = regex.compile(r'(\<a[^\>]+\shref\=("http[^"]+")[^\>]*\>(?!\<\/a\>).*?\<\/a\>)')
    # re_tags = regex.compile(r'(\<(\w+)[^\>]*\>((?!</\2\>).*?)?\<(\/\2)\>)')
    re_reverse = regex.compile(r'((?r)\<(\w+)(?!\w).*?\/>)', regex.DOTALL)
    re_empty = regex.compile(r'(\<([^ /">]+)[^\>]*\>\s*\<\/\2\>)')
    re_cdata = regex.compile(r'(\/\/\s(\<|\&lt\;)\!\[CDATA\[(?!\/\/\]\](\>|\&gt\;)).*\/\/\]\](\>|\&gt\;))', regex.DOTALL)
    re_cdata_clean = regex.compile(r'\>(.*?\/\/\]\](\>|\&gt\;))')
    re_script_style = regex.compile(r'(\<(script|style|noscript)[^\>]*?\>((?!</\2\>).*?)?\<\/\2\>)', regex.DOTALL)
    re_button = regex.compile(r'(\<(button)[^\>]*?\>((?!</\2\>).*?)?\<\/\2\>)', regex.DOTALL)
    re_iframe = regex.compile(r'(\<(iframe)[^\>]*?\>((?!</\2\>).*?)?\<\/\2\>)', regex.DOTALL)
    re_head_foot = regex.compile(r'(\<(header|footer|aside|form|iframe|button)[^\>]*?\>((?!</\2\>).*?)?\<\/\2\>)')
    re_input = regex.compile(r'(\<(input)[^\>]*\>((?!</\2\>).*?)?\/>)')
    re_comment = regex.compile(r'(\<\!\-\-((?!\-\-\>).*?)?\-\-\>)')
    re_tag_name = regex.compile(r'^<([^ /">]+)')
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
                common_elements = None
                for pp_file in input_file_list:
                    print('Working with: ' + str(pp_file))
                    pp_string = html_utils.make_a_string(filename=str(pp_file))
                    pp_soup = html_utils.make_a_soup(html_doc_string=pp_string)
                    suff = '.html'
                    # base_string = html_utils.make_a_string(filename=pp_filename)
                    base_string = str(pp_soup).replace('\n', '')
                    rever = re_reverse.findall(base_string)
                    for r in rever:
                        r_str = r[0].replace('/>', '>' + '</' + r[1] + '>')
                        # print(r_str)
                        base_string = base_string.replace(r[0], r_str)

                    # base_string = re_cdata.sub('', base_string)
                    # cdata_clean = re_cdata_clean.match(base_string)
                    # if cdata_clean:
                    #     print('cdata_clean.')
                    #     base_string = base_string.replace(cdata_clean[0], '')
                    # base_xml_string = re_cdata.sub('', base_xml_string)
                    # while m4:
                    #     for m in m4:
                    #         print(m[0])
                    #         base_xml_string = base_xml_string.replace(m[0], '')
                    #     m4 = re_cdata.findall(base_xml_string)
                    #
                    # get rid of script, style, noscript tags
                    #
                    m4 = re_iframe.findall(base_string)
                    while m4:
                        for m in m4:
                            base_string = base_string.replace(m[0], '')
                        m4 = re_iframe.findall(base_string)
                    #
                    # get rid of script, style, noscript tags
                    #
                    m4 = re_button.findall(base_string)
                    while m4:
                        for m in m4:
                            base_string = base_string.replace(m[0], '')
                        m4 = re_button.findall(base_string)
                    #
                    # get rid of script, style, noscript tags
                    #
                    m4 = re_script_style.findall(base_string)
                    while m4:
                        for m in m4:
                            base_string = base_string.replace(m[0], '')
                        m4 = re_script_style.findall(base_string)

                    # base_xml = etree.parse(StringIO(base_string), xml_parser)
                    # base_xml_string = str(etree.tostring(base_xml.getroot(), pretty_print=True, method="xml"))
                    # base_soup = BeautifulSoup(base_xml_string, 'html5lib')
                    base_soup = html_utils.make_a_soup(html_doc_string=base_string)
                    tag_list = base_soup.find_all(True)
                    m3 = []
                    for item in tag_list:
                        item_string = str(item)
                        tag_name = re_tag_name.match(item_string)
                        tag_name_string = tag_name.group(1)
                        if tag_name_string not in tag_omit_list:
                            omit_flag = False
                            for omit in tag_omit_list:
                                if '<' + omit in item_string:
                                    omit_flag = True
                                    break
                            if not omit_flag:
                                m3.append((tag_name_string, item_string))

                    pp_filename = w_dir.joinpath(str(pp_file.stem) + '_pp' + suff)
                    working_file_list.append(pp_filename)
                    file_utils.write_file(fn=pp_filename,
                                                overwrite=True,
                                                content=base_soup.prettify())

                    print('Length of m3: ' + str(len(m3)))

                    if not common_elements:
                        common_elements = m3
                        print('common_elements set.')
                    else:
                        common_elements = list(set(common_elements) & set(m3)) 
                        break
                

                # common_elements = set(m3s[0]).intersection(*m3s[1:])

                # pp(common_elements)
                for working_filename in working_file_list:
                    working_string = html_utils.make_a_string(filename=working_filename)
                    # working_string = str(base_xml_string)
                    print('Common_element length: ' + str(len(common_elements)))
                    for common_element in common_elements:
                        # print(common_element[1])
                        working_string = working_string.replace(common_element[1], '')

                    #
                    # get rid of header, footer, form, script, button tags
                    #
                    m4 = re_head_foot.findall(working_string)
                    m4_iter = 0
                    while m4 and m4_iter < 3:
                        m4_iter += 1
                        for m in m4:
                            if tag_name_string not in tag_omit_list:
                                omit_flag = False
                                for omit in tag_omit_list:
                                    if '<' + omit in m[0]:
                                        omit_flag = True
                                        break
                            if not omit_flag:
                                working_string = working_string.replace(m[0], '')
                        m4 = re_head_foot.findall(working_string)
                    #
                    # get rid of <input /> tags
                    #
                    m4 = re_input.findall(working_string)
                    while m4:
                        for m in m4:
                            working_string = working_string.replace(m[0], '')
                        m4 = re_input.findall(working_string)
                    #
                    # get rid of comment tags
                    #
                    m4 = re_comment.findall(working_string)
                    # while m4:
                    for m in m4:
                        if tag_name_string not in tag_omit_list:
                            omit_flag = False
                            for omit in tag_omit_list:
                                if '<' + omit in m[0]:
                                    omit_flag = True
                                    break
                        if not omit_flag:
                            working_string = working_string.replace(m[0], '')
                        # m4 = re_comment.findall(working_string)
                    #
                    # get rid of empty tags
                    #
                    m4 = re_empty.findall(working_string)
                    while m4:
                        for m in m4:
                            working_string = working_string.replace(m[0], '')
                        m4 = re_empty.findall(working_string)

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