import requests
from urlparse import urlparse
import platform
import os
import re
import xlsxwriter

def xmlpath():
    if platform.system() == "Linux":
        return '/'
    else:
        return '\\'

ROOT_PATH=os.getcwd() + xmlpath()


def varificator():
    line_number = 0
    koppelbaar_find = 0
    good_line = 1
    fail_line = 1
    no_link_line = 1
    with open(ROOT_PATH + "Link.txt") as a_file:
        workbook = xlsxwriter.Workbook('result.xlsx')
        Good = workbook.add_worksheet('Pass')
        bold = workbook.add_format({'bold': True})
        Good.write('A1', 'Expected', bold)
        Good.write('B1', 'Actually', bold)
        Good.write('C1', 'Exit_link', bold)
        Fail = workbook.add_worksheet('Fail')
        Fail.write('A1', 'Expected', bold)
        Fail.write('B1', 'Actually', bold)
        Fail.write('C1', 'Exit_link', bold)
        No_link = workbook.add_worksheet('No Link')
        No_link.write('A1', 'Domein', bold)
        No_link.write('B1', 'Link', bold)

        for a_line in a_file:
            line_number += 1
            if a_line.find("Koppelbaar=\"1\"") != -1:
                koppelbaar_find += 1

                #print('{:>4} {}'.format(line_number, a_line.rstrip()))
                #z = re.search('|Exit_link=(.*)', a_line).group()
                d = re.search('Domein=\"(.+?)\"', a_line).group(1)
                el = re.search('Exit_link=\"(.+?)\"', a_line).group(1)


                try:
                    www = requests.get(el).url
                    o = urlparse(www)
                    if o.netloc == 'www.' + d:
                        #print "GOOD: Expected: " + d + ' Actually: ' + o.netloc + ' link ' + el
                        good_line +=1
                        Good.write('A'+ good_line.__str__(), d)
                        Good.write('B' + good_line.__str__(), o.netloc)
                        Good.write('C' + good_line.__str__(), el)
                    else:
                        #print "Not Good: Expected: " + d + ' Actually: ' + o.netloc + ' link: ' + el
                        fail_line += 1
                        Fail.write('A' + fail_line.__str__(), d)
                        Fail.write('B' + fail_line.__str__(), o.netloc)
                        Fail.write('C' + fail_line.__str__(), el)
                except:
                    #print 'No Link: ' + el + ' != ' + d
                    no_link_line += 1
                    No_link.write('A' + no_link_line.__str__(), d)
                    No_link.write('B' + no_link_line.__str__(), 'Missing Link')

            else:
                pass
        print "Finish OK"
        workbook.close()