import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from subprocess import Popen
import os, errno
import struct

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def validate_filetype():
    files = filedialog.askopenfilenames(title = "Please Select One or More .stl Files to Convert")
    
    for file in files:
        file_type = file.split('.')[1]
        if (file_type != "stl"):
            msg = "The file " + file + " is not a .stl. Please Try Again" 
            popup_msg(msg)
            print("here")

    return files
        
def popup_msg(msg):
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

def main():
    root = tk.Tk()
    root.withdraw()

    files = validate_filetype()

    for file in files:

        try: 
            csv = file.replace('.stl', '-table.csv')
            stl_file = open(file, 'r')
            list_of_lines = stl_file.readlines()
        except UnicodeDecodeError:
            list_of_lines = [""]

        if "solid" not in list_of_lines[0]:
            stl_file.close()
            stl_fileName = convert_binary(file)
            stl_file = open(stl_fileName, 'r')
            list_of_lines = stl_file.readlines()

        csv_file = open(csv, 'w')
        csv_file.write("x_coord,y_coord,z_coord\n")

        for line in list_of_lines:
            if line.lstrip().startswith("vertex"):
                coords = line.split()[1:]
                append_csv(csv_file,coords)

        csv_file.close()
        stl_file.close()
        p = Popen(csv, shell=True)

def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

def convert_binary(binaryFilename):
    binaryFile = open(binaryFilename, 'rb')
    asciiFileName = binaryFilename.replace('.stl', '-ascii.stl')
    asciiFile = open(asciiFileName, 'w')

    print(binaryFilename, "is in BINARY format, converting to ASCII:", asciiFileName)

    asciiFile.write("solid \n")

    binaryFile.seek(80, 0)

    triCount = struct.unpack('I', binaryFile.read(4))[0]

    for i in range(triCount):
        normal = struct.unpack('fff', binaryFile.read(12))
        vertexA = struct.unpack('fff', binaryFile.read(12))
        vertexB = struct.unpack('fff', binaryFile.read(12))
        vertexC = struct.unpack('fff', binaryFile.read(12))

        binaryFile.seek(2, 1)

        asciiFile.write("\tfacet normal {n0} {n1} {n2}\n".format(n0 = normal[0], n1 = normal[1], n2 = normal[2]))
        asciiFile.write("\t\touter loop\n")
        asciiFile.write("\t\t\tvertex {vA0} {vA1} {vA2}\n".format(vA0 = vertexA[0], vA1 = vertexA[1], vA2 = vertexA[2]))
        asciiFile.write("\t\t\tvertex {vB0} {vB1} {vB2}\n".format(vB0 = vertexB[0], vB1 = vertexB[1], vB2 = vertexB[2]))
        asciiFile.write("\t\t\tvertex {vC0} {vC1} {vC2}\n".format(vC0 = vertexC[0], vC1 = vertexC[1], vC2 = vertexC[2]))
        asciiFile.write("\t\tendloop\n")
        asciiFile.write("\tendfacet\n")

    asciiFile.write("endsolid\n")
    asciiFile.close()

    return asciiFileName

if __name__ == "__main__":
    main()