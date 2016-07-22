import os
import tkMessageBox
import tkSimpleDialog
import Tkinter as tk
from tkFileDialog import askopenfilename
import platform
import xml.etree.ElementTree as ET

from xls2xml import toXML


def xmlpath():
    if platform.system() == "Linux":
        return '/'
    else:
        return '\\'

ROOT_PATH=os.getcwd() + xmlpath()


def open_file_handler():
    filePath = askopenfilename()

    doc = ET.parse(ROOT_PATH + 'file.xml')
    root = doc.getroot()
    django = doc.find('filePath')
    django.text = filePath
    doc.write(ROOT_PATH + 'file.xml', encoding="utf-8", xml_declaration=True)
    toXML(filename=filePath,node_name='node', cellsAs='attributes')
    tkMessageBox.showinfo(
    "Updated",
    "File added"
)


class Browse:
    def __init__(self, body):
        #butfont = font.Font(family='Ubuntu', size=10)
        self.but = tk.Button(body, command=open_file_handler, padx=100, text="Browse xls file", bg='#C0C0C0')
        self.but.pack()

        # title = tk.Label(body, text="Picture", font="Arial 12")
        # title.grid(row = 1, column = 1)



