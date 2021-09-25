import os
import pythoncom
from win32com.shell import shell, shellcon

path =r'C:\Users\<username>\AppData\Roaming\Microsoft\Office\Recent'
path1 = r'C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Recent'
RecentLog = 'RecentFiles.txt'

list_of_files = []


def shortcut_target (shortcutfile):

    link = pythoncom.CoCreateInstance (
    shell.CLSID_ShellLink,
    None,
    pythoncom.CLSCTX_INPROC_SERVER,
    shell.IID_IShellLink
    )

    link.QueryInterface (pythoncom.IID_IPersistFile).Load (shortcutfile)
    target_path, _ = link.GetPath (shell.SLGP_UNCPRIORITY)
    return target_path


def list_all_files(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if f.upper().endswith(".LNK"):
            target_f = shortcut_target(f)
            #skip duplicates
            if os.path.exists(target_f):
                if os.path.isdir(target_f):
                    target_f = target_f + "\\"
                if target_f in list_of_files:
                    #print('duplicate : ' + f)
                    continue
                else:
                    list_of_files.append(target_f)
                    print('adding : ' + f)

    '''
    #out = []    
    for line in list_of_files:
        #if line.exists():
            #file.write(line + ',' + str(os.path.getctime(line)) + '\n')
        #print(line)
        if os.path.exists(line):
            if os.path.isdir(line):
                if not line.endswith("\\"):
                    line = line + "\\"
            out.append(line)
    '''
    
    # write the shortcuts target to the text file:
    file = open(RecentLog,'w')
    file.writelines("\n".join(list_of_files))
    file.close()


#----------------------------------------------------------------
# start main
#----------------------------------------------------------------

# read the existing RecentFiles.txt to list_of_files
if os.path.exists(RecentLog):
    f = open(RecentLog, 'r')
    # rstrip to remove newline
    list_of_files = [line.rstrip() for line in f.readlines()]
    f.close()
#print(list_of_files)

# get target for all the .lnk files in this path and only append them to RecentFiles.txt if they do not already exists in it.
list_all_files(path)
list_all_files(path1)

print("shortcut reader done")
