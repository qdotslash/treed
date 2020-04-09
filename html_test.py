from lxml import etree
import regex
from io import StringIO
from bs4 import BeautifulSoup
import html5lib
from pprint import pprint as pp


broken_html = '<html><head><title>test<body><h1>page title<a class="alksjdf" href="kajdkf" /></h1><p><p>1111111<a href="_target" ><meta itemprop="zcmx" /><div /><br><p>akj<a href="_alkj">asdf</a>sdf<br><p>akdjf;akj'

parser = etree.HTMLParser()
tree = etree.parse(StringIO(broken_html), parser)

result = etree.tostring(tree.getroot(), pretty_print=True, method="xml")
# print(result)

soup = BeautifulSoup(result, 'html5lib')
ss = str(soup)
re_empty = regex.compile(r'(\<(w+)[^\>]*\>\s*\<\/\2\>)')
# print(soup.prettify())
t_list = soup.find_all(True)
for t in t_list:
    if len(t.contents) > 0:
        print(t.name + '\t' + str(len(t.contents)))
    else:
        t.decompose()
pp(soup.prettify())