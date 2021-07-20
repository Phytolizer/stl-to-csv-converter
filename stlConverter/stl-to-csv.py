import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from subprocess import Popen
import os, errno
import time

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def validate_filetype():
    files = filedialog.askopenfilenames(title = "Please Select One or More .stl Files to Convert")
    
    for file in files:
        file_type = file.split('.')[1]
        if (file_type != "stl"):
            msg = "The file " + file + " is not a .stl. Please Try Again" 
            popupmsg(msg)
            print("here")

    return files
        
def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = exit)
    B1.pack()
    popup.mainloop()

def append_csv(file, coords):
    csv_line = coords[0] + "," + coords[1] + "," + coords[2] + '\n'
    file.write(csv_line)

def build_csv(stl_path):
    last_slash = stl_path.rfind('/') + 1

    csv_path = stl_path[:last_slash]

    stl_name = stl_path[last_slash:]

    csv_name = stl_name.split('.')[0] + ".csv"
    
    csv = csv_path+csv_name

    silentremove(csv)

    return csv


def main():
    root = tk.Tk()
    root.withdraw()

    files = validate_filetype()

    for file in files:
        csv = build_csv(file)
        stl_file = open(file, 'r')
        list_of_lines = stl_file.readlines()

        csv_file = open(csv, 'a')
        csv_file.write("x_coord,y_coord,z_coord\n")

        for line in list_of_lines:
            if line.lstrip().startswith("vertex"):
                coords = line.split()[1:]
                append_csv(csv_file,coords)

        csv_file.close()
        stl_file.close()
        p = Popen(csv, shell=True)

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

if __name__ == "__main__":
    main()