import tkinter as tk
# tkinter.font as tkFont
#import os

class SelectAndRun(): #Selecting files and running simple scripts on them
    def __init__(self, master):
        self.master = master
        master.title('Select and Run - Tkinter') 
        
        self.filename = None
        self.browsedvar = tk.StringVar()
        
        self.label_title = tk.Label(master, text='Title')
        
        vcmd = master.register(self.validate) # we have to wrap the command
        
        self.entry = tk.Entry(master, textvariable = self.browsedvar, validate='key', validatecommand=(vcmd,'%P'))
        #self.printButton = tk.Button(master, text='Print', command=self.printText)
        self.selectFile = tk.Button(master, text='Select File', command=self.browseText)
        self.runScript = tk.Button(master, text='Run Script on File', command=self.runSumOnFile)
        
        self.label_title.grid(row=0, column=0, columnspan=2)
        self.entry.grid(row=1, column=0, columnspan=2)
        #self.printButton.grid(row=2, column=0, columnspan=5)
        self.selectFile.grid(row=3, column=0, columnspan=2)
        self.runScript.grid(row=4, column=0, columnspan=2)
    
    def validate(self, inputText): #This processes input, validates it
        if not inputText:
            self.filename = None
            return True
        try:
            filename = str(inputText)
            self.filename = filename
            return True
        except ValueError:
            return False
    
    def printText(self): #Prints text in console
        print(self.filename)
        self.entry.delete(0, tk.END)
        
    def browseText(self): #Browses for a file, sets file path to self.filename
        file = tk.filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("txt","*.txt"), ("all files", "*.*")))
        self.browsedvar.set(file)
        print(self.filename)
        
    def runSumOnFile(self): #Runs a script (counting) on self.filename
        try:
            directory= str(self.filename)
            file=open(directory,'r')
            info=file.readlines()
            count=0
            for line in info:
                for i in line:
                    if i.isdigit():
                        count=count+int(i)
            print(count)
        except FileNotFoundError:
            self.popup()
            
    def popup(self): #Produces 'file error' pop up on screen
        tk.messagebox.showwarning('File Error', 'Script cannot be run on selected file. Check file path and try again.')
