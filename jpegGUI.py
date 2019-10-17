from tkinter import filedialog
from tkinter import *
from subprocess import call
import numpy

root = Tk()
root.title("JPEG Compression Tool")
root.geometry("210x400")
root.configure(background = "gray")

def Getfilename():
    root.filename =  filedialog.askopenfilename(initialdir = "/home/" ,title = "Select file",filetypes = (("Img files",(("*.jpg"),("*.png"))),("png files","*.png")))
    print ("filepath is:",root.filename, Output['text'])
    if ((Output['text'] == "\nImport IMG and set QF\n") and root.filename != ""):
        Output.configure(text = "\nSet QF\n")
    if (Output['text'] == "\nImport IMG\n"):
        Output.configure(text = "\nReady To Compress\n")
def saveQF():
    try:
        QF = int(numentry.get())
    except:
        QFoutput.configure(text = "\nInput must be an INT\n")
        numentry.delete(0,'end')
        return None
    if (0 < QF < 101):
        SAVE = True
    else:
        SAVE = False 
    if SAVE:
        QFoutput.configure(text = "\nQF = " + str(QF)+"\n")
        if (Output['text'] == "\nImport IMG and set QF\n"):
            Output.configure(text = "\nImport IMG\n")
        if (Output['text'] == "\nSet QF\n"):
            Output.configure(text = "\nReady To Compress\n")            
    else:
        QFoutput.configure(text = "\nQF Must be [1,100]\n")
        numentry.delete(0,'end')
def callEncoder():
    if (Output['text'] == "\nReady To Compress\n"):
        QF = int(numentry.get())
        File = root.filename
        param1 = ["-qf",str(QF)]
        param2 = ["-F",File]
        #print("printin", call( ["python", "JPEGEncoderFinal.py"] + param1+param2, shell=False ))
        #MAY NEED TO CHANGE THIS TO PYTHON INSTEAD OF PYTHON3 IF NOT RUNNING PYTHON3
        call( ["python3", "JPEGEncoderFinal.py"] + param1+param2, shell=False )
    else:
        # if(Output['text'][0] != 'P'):
        #     Output.configure(text =  "Please "+ Output['text'])
        # else: pass
        pass
# Frame = Frame(root, width = 400, height = 400)
# Frame.pack_propagate(0)
# Frame.pack()
button = Button(root, text='Import File', command=Getfilename)
button.grid(row = 1, column=1, sticky = N)
Label(root, text = "\nEnter your Quality Factor (1-100)\n", bg = "gray", font = "none 10 bold").grid(row = 2, column = 1, sticky = S)
numentry = Entry(root, width = 20, bg = "white" )
numentry.grid(row=3, column = 1, sticky = N)
QFoutput = Label(root, text = "\nQF = \n", background = "gray")
QFoutput.grid(row = 4, column = 1, sticky = S)
Button(root, text = "SAVE QF", width = 6, command = saveQF).grid(row=5, column = 1, sticky = N)
Label(root, text = "", bg = "gray", font = "none 10 bold").grid(row = 6, column = 1, sticky = S)
Button(root, text = "COMPRESS AND DISPLAY", width = 20, command = callEncoder).grid(row=7, column = 1,columnspan = 2 , sticky = N)
Label(root, text = "", bg = "gray", font = "none 10 bold").grid(row = 8, column = 1, sticky = S)
Output = Label(root, text = "\nImport IMG and set QF\n", background = "gray")
Output.grid(row = 0, column = 1, sticky = N)
# Output = Label(root, text = "Import IMG and set QF", background = "gray")
# Output.grid(row = 8, column = 1, sticky = S)
root.mainloop()