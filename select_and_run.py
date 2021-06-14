import tkinter as tk
import tkinter.filedialog
#from tkinter import ttk
# tkinter.font as tkFont
#import os

class SelectAndRun(): #Selecting files and running simple scripts on them
    def __init__(self, master):
        self.master = master
        master.title('Select and Run - Tkinter') 
        
        self.menu_var = tk.StringVar()
        self.menu_choices = sorted({'Sum', 'Multiply', 'All'})
        self.menu_var.set('Sum') # default value
        self.menu = tk.OptionMenu(master, self.menu_var, *self.menu_choices)
        
        self.filename = None
        self.browsedvar = tk.StringVar()
        self.textbox_var = tk.StringVar()
        
        self.label_title = tk.Label(master, text='Get the Sum/Product of Numbers in a txt file')
        
        vcmd = master.register(self.validate) # we have to wrap the command
        
        self.entry = tk.Entry(master, textvariable = self.browsedvar, validate='key', validatecommand=(vcmd,'%P'))
        self.textbox = tk.Entry(master, textvariable = self.textbox_var)
        #self.printButton = tk.Button(master, text='Print', command=self.printText)
        self.selectFile = tk.Button(master, text='Select File', command=self.browseText)
        self.runScript = tk.Button(master, text='Run', command=lambda:self.chooseScript())
        
        self.label_title.grid(row=0, column=0, columnspan=2)
        self.entry.grid(row=1, column=1, columnspan=1, sticky="ew", padx=2, pady=2)
        #self.printButton.grid(row=2, column=0, columnspan=5)
        self.menu.grid(row=2, column=1,columnspan=1, sticky="ew", padx=2, pady=2)
        self.selectFile.grid(row=1, column=0, columnspan=1, sticky="ew", padx=2, pady=2)
        self.runScript.grid(row=2, column=0, columnspan=1, sticky="ew", padx=2, pady=2)
        self.textbox.grid(row=3, column = 0, columnspan=2, sticky="ew", padx=2, pady=2)
    
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
        file = tkinter.filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("txt","*.txt"), ("all files", "*.*")))
        self.browsedvar.set(file)
        print(self.filename)

    def chooseScript(self):
        if self.menu_var.get()=='Sum':
            self.textbox_var.set('Sum is '+str(self.runSumOnFile()))
            
        if self.menu_var.get()=='Multiply':
            self.textbox_var.set('Product is '+str(self.runMultOnFile()))
            
        if self.menu_var.get()=='All':
            self.textbox_var.set('Sum is '+str(self.runSumOnFile())+', Product is '+str(self.runMultOnFile()))
    
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
            return count
        except FileNotFoundError:
            self.popup()
    
    def runMultOnFile(self): #Runs a script (counting) on self.filename
        try:
            directory= str(self.filename)
            file=open(directory,'r')
            info=file.readlines()
            prod=1
            for line in info:
                for i in line:
                    if i.isdigit():
                            prod=prod*int(i)
            return prod
        except FileNotFoundError:
            self.popup()
            
    def popup(self): #Produces 'file error' pop up on screen
        tk.messagebox.showwarning('File Error', 'Script cannot be run on selected file. Check file path and try again.')