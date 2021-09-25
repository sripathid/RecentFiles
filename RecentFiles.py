# https://lawsie.github.io/guizero/alerts/

#-------------------------------------------------------------------------------
# Name:        Recent Files
# Purpose:     This program has 2 parts. 
#              First part, writes all the target of shortcuts in the recent files
#              folders to the RecentFile.txt. It will skip writing if the target 
#              already exists and only appends the newer ones.
#              Second Part, it will show the lines from recent files.txt file in a 
#              listbox, users can filter them by folders, files or partial text.
# Author:      Sripathi Dantuluri
#
# Created:     17/06/2021
# Copyright:   (c) Sripathi Dantuluri 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys
import os
# import shortcutreader

from guizero import App, Box, ListBox, Text, TextBox, PushButton, CheckBox
from shutil import copyfile

from subprocess import Popen
#Popen('python shortcutreader.py')

'''
To Do:
Find if a path is file or folder:
    Option 1: In RecentFiles.txt, append \ at the end of the folder and use that as indicator for file or folder
    Option 2: Create a list with same index as lines with file/folder checked https://pythonexamples.org/python-check-if-path-is-file-or-directory/

'''

folders_list = 'RecentFiles.txt'


with open(folders_list, 'r') as f:
    lines = f.readlines()

def enable_button():
   button1.enabled=True
   button2.enabled=True
   button3.enabled=True

def copy_file():
    print(filename)
    print(listbox.value)
    print('copy ', filename, ' to ', listbox.value)

def move_file():
    print(filename)
    print(listbox.value)
    print('move ', filename, ' to ', listbox.value)

def Refresh():
    tk_listbox.delete(0, len(lines))
    m.value = "Refresing.... Wait"
    p1 = Popen('python shortcutreader.py')
    p1.wait()
    #with open(folders_list, 'r') as f:
    #    lines = f.readlines()
    print("refresh done")
    m.value = "Refresing.... Done, close and reopen the app"
    filter_text()
    # ?? how to update lines array ??

def change_color(value):
    t.text_color = value

def open_folder():
    print(listbox.value)
    os.system(f'start {os.path.realpath(listbox.value)}')
    
def filter_text():
    print(s.value)
    tk_listbox.delete(0, len(lines))
    words = s.value.lower().split()

    for line in lines:
        line = line.rstrip()  # get rid of new line character, otherwise endswith won't work
        # xor : apply files folder filters only if one of them is not checked.
        if (checkbox1.value == 0) ^ (checkbox2.value == 0):
            # print(checkbox1.value, line.endswith("\\"), checkbox2.value, line)
            if (checkbox1.value == 0) and (line.endswith("\\") == True):
                continue
            if (checkbox2.value == 0) and (line.endswith("\\") == False):
                continue            

        if all(x in line.lower() for x in words):
            listbox.append(line)


app = App(title="Recent Files", width=800, height=720)

buttons_box = Box(app, width="fill", height=30, align="top", border=True)
button3 = PushButton(buttons_box, enabled=False,  text='Open', align="left", command=open_folder)
button2 = PushButton(buttons_box, enabled=False, text='Move', align="left", command=move_file)
button1 = PushButton(buttons_box, enabled=False, text='Copy', align="left", command=copy_file)
button0 = PushButton(buttons_box, enabled=True, text='Refresh', align="left", command=Refresh)

option_box = Box(app, width="fill", align="top", border=True)
opt_desc = Text(option_box, text="Filter by Files or Folders  ", color="black", align="left")
checkbox1 = CheckBox(option_box, text="Folders", align="left", command=filter_text)
opt_blank = Text(option_box, text="  ", color="black", align="left")
checkbox2 = CheckBox(option_box, text="Files", align="left", command=filter_text)
checkbox1.toggle()
checkbox2.toggle()

search_box = Box(app, width="fill", align="top", border=True)
t = Text(search_box, text="Search", color="black", align="left")
s = TextBox(search_box, align="left", width="fill", command=filter_text)
s.focus()

list_box = Box(app, height="fill", width="fill", border=True)
listbox = ListBox(list_box, items=[], command=enable_button, scrollbar=True, align="left", height="fill", width="fill")
tk_listbox = listbox.children[0].tk  #used for clearning the listbox

for line in reversed(lines):
   listbox.insert(0,line)

message_box = Box(app, width="fill", align="top", border=True)
m = Text(message_box, text="Status ...", align="left", color="black")

path = Text(app)
#print(path)

app.display()

