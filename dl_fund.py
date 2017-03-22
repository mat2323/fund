#!/usr/bin/python
from HTMLParser import HTMLParser
import urllib2

g_fund_files = []

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.items = []
        self.newLine = False

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.newLine = True

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.newLine = False
            self.items.append('\n')
            
    def handle_data(self, data):
        if self.newLine:
            self.items.append(data + ',')

def read_fund(s_fund, pos, total):
    parser = MyHTMLParser()
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&page=1&per=300&sdate=&edate=&code=' + s_fund
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req)
    parser.feed(fd.read())
    fd.close()
    f_output = open(s_fund + '.fund', 'w')
    f_output.writelines(parser.items)
    f_output.close()
    print '(%d'%pos + '/' + '%d'%total + ') fund ' + s_fund + " read complete"

if __name__ == '__main__':
    f_fund = open("funds")
    funds = f_fund.readlines()
    total = len(funds)
    i = 0
    for fund in funds:
        i = i + 1
        if fund:
            read_fund(fund.strip('\n'), i, total)
    f_fund.close()
