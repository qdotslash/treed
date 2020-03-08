from bs4 import BeautifulSoup
from utils import file_utils

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
                print('Not a valid file: ' + filename + ' POSIX filename: ' + str(valid_path))
                return False
        else:
            print('Not a valid path: ' + filename + ' POSIX filename: ' + str(valid_path))
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
def rec_soup(ss, ind, tabs):
    ind += 1
    tabs += '\t'
    for x in range(0, len(ss.contents)):
        if ss.contents[x].name:
            print(tabs + ss.contents[x].name + '(' + str(len(ss.contents[x])) + ')')
            if len(ss.contents[x]) > 1:
                rec_soup(ss.contents[x], ind, tabs)

#
# find differences in soups to identify common parts such as headers, footers, sidebars
#
def diff_a_soup(s1, s2):
    # print(s1.prettify())
    print('length of s1.body: ' + str(len(s1.body.contents)))
    ind = 0
    tabs = ''
    rec_soup(s1.body, ind, tabs)


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
