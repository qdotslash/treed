from bs4 import BeautifulSoup
from utils import file_utils
from pprint import PrettyPrinter as pp
from pprint import pprint, pformat
from difflib import SequenceMatcher

#
# Simple pretty print html code
#
def write_ppsoup(soup, file_out):
    success = file_utils.write_file(fn=file_out, content=soup.prettify())
    if success:
        return True
    else:
        return False
#
# make a soup from file or string
#
def make_a_soup(filename=None, html_doc_string=None, html_parser='html5lib'):
    if filename:
        valid_path = file_utils.validate_path(filename=filename)
        if valid_path:
            if valid_path.is_file():
                print('Returning a soup from file: ' + str(valid_path))
                with valid_path.open('r') as fi:
                    return BeautifulSoup(fi, html_parser)
            else:
                print('Not a valid file: ' + str(filename) + ' POSIX filename: ' + str(valid_path))
                return False
        else:
            print('Not a valid path: ' + str(filename) + ' POSIX filename: ' + str(valid_path))
            return False
    elif html_doc_string:
        if len(html_doc_string) < 1:
            print('No html doc provided, returning False')
            return False
        else:
            return BeautifulSoup(html_doc_string, html_parser)
    else:
        print('Neither filename nor html_doc_string provided, returning False')        
        return False
#
# recursive dif
#
def rec_soup(ss, ind, ind_max, ind_limit, tabs, ss_list):
    
    ind += 1
    if ind > ind_max:
        ind_max = ind
    if ind_limit and ind > ind_limit:
        return ss_list, ind_max
    tabs += '\t'
    for x in range(0, len(ss.contents)):
        if ss.contents[x].name:
            # ss_list.append(tabs + ss.contents[x].name + '(' + str(len(ss.contents[x])) + ')')
            if ss.contents[x].name == 'script':
                ss_list.append(tabs + ss.contents[x].name)
            elif ss.contents[x].name == 'style':
                ss_list.append(tabs + ss.contents[x].name)
            elif ss.contents[x].has_attr('class'):
                if ss.contents[x].string:
                    ss_string = ss.contents[x].string.strip().replace('\r', '').replace('\n','  ')
                    # ss_list.append(tabs + ss.contents[x].name + '--' + ss_string)
                    ss_list.append(tabs + ss.contents[x].name + '-c-' + ss.contents[x]['class'][0] + '-s-' + ''.join(ss_string))
                else:
                    ss_list.append(tabs + ss.contents[x].name + '-c-' + ss.contents[x]['class'][0])
            # elif ss.contents[x].string:
            #     ss_string = ss.contents[x].string.replace('\n', ' ').strip()
            #     ss_list.append(tabs + ss.contents[x].name + '--' + ss_string)
            else:
                if ss.contents[x].string:
                    ss_string = ss.contents[x].string.strip().replace('\r', '').replace('\n','  ')
                    # ss_list.append(tabs + ss.contents[x].name + '--' + ss_string)
                    ss_list.append(tabs + ss.contents[x].name + '-s-' + ''.join(ss_string))
                else:
                    ss_list.append(tabs + ss.contents[x].name)

                # ss_list.append(tabs + ss.contents[x].name)
            
            # print(tabs + ss.contents[x].name + '(' + str(len(ss.contents[x])) + ')')
            if len(ss.contents[x]) > 0:
                ss_list, ind_max = rec_soup(ss.contents[x], ind, ind_max, ind_limit, tabs, ss_list)
    ind = 0
    clean_ss_list = []
    for s in ss_list:
        if s.startswith('\t'):
            clean_ss_list.append(s)
    return clean_ss_list, ind_max
#
# find differences in soups to identify common parts such as headers, footers, sidebars
#
def diff_a_soup(s1, s2):
    # print(s1.prettify())
    sx_ind_limit = None
    ind = 0
    tabs = ''
    s1_list = []
    s1_ind_max = 0
    s1_list, s1_ind_max = rec_soup(s1, ind, s1_ind_max, sx_ind_limit, tabs, s1_list)
    s1_list_len = len(s1_list)
    ind = 0
    tabs = ''
    s2_list = []
    s2_ind_max = 0
    s2_list, s2_ind_max = rec_soup(s2, ind, s2_ind_max, sx_ind_limit, tabs, s2_list)
    s2_list_len = len(s2_list)
    seq = SequenceMatcher(None, s1_list, s2_list)
    # if s1_list_len <= s2_list_len:
    #     seq = SequenceMatcher(None, s1_list, s2_list)
    # else:
    #     seq = SequenceMatcher(None, s2_list, s1_list)
    match_block = seq.get_matching_blocks()
    print('Length of s1: ' + str(s1_list_len))
    print('s1 ind max: ' + str(s1_ind_max))
    print('Length of s2: ' + str(s2_list_len))
    print('s2 ind max: ' + str(s2_ind_max))
    print('Number of matched blocks: ' + str(len(match_block)))
    # pprint(match_block)
    return s1_list, s2_list, match_block


def diff_a_list(l1, l2):
    s1 = []
    for l in l1:
        s1.append(l.split(',')[-1].strip())
    s2 = []
    for l in l2:
        s2.append(l.split(',')[-1].strip())
    print(s1)
    print(s2)
    seq = SequenceMatcher(s1, s2)
    seq_blocks = seq.get_matching_blocks()
    return seq_blocks


# if __name__ == "__main__":
#     html_doc = """
#     <html><head><title>The Dormouse's story</title></head>
#     <body>
#     <p class="title"><b>The Dormouse's story</b></p>
#     <p class="story">Once upon a time there were three little sisters; and their names were
#     <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
#     <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
#     <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
#     and they lived at the bottom of a well.</p>
#     <p class="story">...</p>
#     """
#     soup = make_a_soup(html_doc_string=html_doc)
#     print(soup.prettify())
#     save = write_ppsoup(soup=soup, file_out='./test/pp_example.html')
