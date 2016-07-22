import Tkinter as tk
import os
import platform

from browse import Browse
from varificator import varificator

root = tk.Tk()
root.title('Varificator')
root.resizable(width=False, height=False)
#root.minsize(width=300, height=300)

def xmlpath():
    if platform.system() == "Linux":
        return '/'
    else:
        return '\\'

ROOT_PATH=os.getcwd() + xmlpath()
body = tk.Frame(root, width=500, height=200)
niz = tk.Frame(root, width=500, height=150)
class But_start:
    def __init__(self):
        self.but = tk.Button(niz,
                            text="Start",
                            width=12, height=3,
                            bg="green", fg="white")
        self.but.bind("<Button-1>", self.start)
        self.but.pack()

    def start(self, event):
        varificator()

Browse(body)
But_start()




body.grid(row=1)
niz.grid(row=2)



root.mainloop()