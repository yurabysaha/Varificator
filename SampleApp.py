import Tkinter as tk
import os
import platform
import subprocess

import tkMessageBox
import ttk

import re
from urlparse import urlparse

import requests
import sys
import xlsxwriter

from browse import Browse


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        body = tk.Frame(self, width=500, height=200)
        niz = tk.Frame(self, width=500, height=150)
        body.grid(row=1)
        niz.grid(row=2)
        Browse(body)
        self.but = tk.Button(niz,
                        text="Start",
                        width=12, height=3,
                        bg="green", fg="white", command=lambda :self.start())
        self.but.pack()
        self.progressBar = ttk.Progressbar(self, orient='horizontal', length=200, mode='determinate')
        self.progressBar.grid(row=3)


    def start(self):
        line_number = 0
        koppelbaar_find = 0
        good_line = 1
        fail_line = 1
        no_link_line = 1
        self.progressBar.start()

        def xmlpath():
            if platform.system() == "Linux":
                return '/'
            else:
                return '\\'

        ROOT_PATH = os.getcwd() + xmlpath()
        with open(ROOT_PATH + "Link.txt") as a_file:
                workbook = xlsxwriter.Workbook('result.xls')
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
                        self.progressBar.update()
                        self.progressBar["maximum"]=762
                        self.progressBar["value"]=line_number

                        d = re.search('Domein=\"(.+?)\"', a_line).group(1)
                        el = re.search('Exit_link=\"(.+?)\"', a_line).group(1)

                        try:
                            www = requests.get(el).url
                            o = urlparse(www)
                            if o.netloc == 'www.' + d:
                                # print "GOOD: Expected: " + d + ' Actually: ' + o.netloc + ' link ' + el
                                good_line += 1
                                Good.write('A' + good_line.__str__(), d)
                                Good.write('B' + good_line.__str__(), o.netloc)
                                Good.write('C' + good_line.__str__(), el)
                            else:
                                # print "Not Good: Expected: " + d + ' Actually: ' + o.netloc + ' link: ' + el
                                fail_line += 1
                                Fail.write('A' + fail_line.__str__(), d)
                                Fail.write('B' + fail_line.__str__(), o.netloc)
                                Fail.write('C' + fail_line.__str__(), el)
                        except:
                            # print 'No Link: ' + el + ' != ' + d
                            no_link_line += 1
                            No_link.write('A' + no_link_line.__str__(), d)
                            No_link.write('B' + no_link_line.__str__(), 'Missing Link')

                    else:
                        pass
                print "Finish OK"
                self.progressBar.stop()

                workbook.close()
                result = tkMessageBox.askquestion("Result", "Do you want open result.xls?", icon='warning')
                if result == 'yes':
                    filename = 'result.xls'

                    if sys.platform == "win32":
                        os.startfile(filename)
                    else:
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.call([opener, filename])
                else:
                    pass


app = SampleApp()
app.mainloop()

