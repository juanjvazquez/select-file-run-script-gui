import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import datetime
import webbrowser, os
#from tkinter import ttk
# tkinter.font as tkFont


class SelectAndRun(): #Selecting files and running simple scripts on them
    def __init__(self, master):
        #master
        self.master = master
        master.title('Select and Run - Tkinter')
        master.option_add('*tearOff', tk.FALSE)
        
        self.history_file = 'files/run_log.txt'
        self.downloadsFolder_path = "files/output_files"
        #menu
        self.menubar = tk.Menu(master)
        
        self.menu_home = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_home, label='Home')
        
        self.menu_test = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_test, label='Test')
        self.submenu_use_test_file = tk.Menu(self.menu_test)
        self.menu_test.add_cascade(menu=self.submenu_use_test_file, label='Use Test File')
        for f in os.listdir('files/test_files'):
            self.submenu_use_test_file.add_command(label=os.path.basename(f), command=lambda f=f: self.getTestFile(f))
        
        self.menu_directories = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_directories, label='Directories')
        self.menu_directories.add_command(label='Open Output Folder', command=self.openDownloadsFolder)
        self.menu_directories.add_command(label='Show Run Logs', command=self.openRunLogs)
        
        self.master.config(menu=self.menubar)
        
        #dropdown menu for script choices
        self.menu_var = tk.StringVar()
        self.menu_choices = sorted({'Sum', 'Multiply', 'All'})
        self.menu_var.set('Sum') # default value
        self.menu = tk.OptionMenu(master, self.menu_var, *self.menu_choices)
        
        #directory related variables - directory entry box, output files
            #self.directory_output= None
        self.filename = None
        self.browsedvar = tk.StringVar()
        self.textbox_var = tk.StringVar()
            #self.file_output = str(self.directory_output)+'/txt_output.txt'
        
        #information label
        self.label_title = tk.Label(master, text='Get the Sum/Product of Numbers in a txt file')
        
        #wrapping validate command
        vcmd = master.register(self.validate)
        
        #Entry boxes, buttons
        self.entry = tk.Entry(master, textvariable = self.browsedvar, validate='key', validatecommand=(vcmd,'%P'))
        self.textbox = tk.Entry(master, textvariable = self.textbox_var)
        self.selectFile = tk.Button(master, text='Select File', command=self.browseText)
        self.runScript = tk.Button(master, text='Run', command=lambda:[self.chooseScript(), self.runHistory()])
        self.downloadButton = tk.Button(master, text='Download', command=self.export_to_txt, state = tk.DISABLED)
        
        #GUI positiong of widgets
        self.label_title.grid(row=0, column=0, columnspan=2)
        self.entry.grid(row=1, column=1, columnspan=1, sticky="ew", padx=2, pady=2)
        self.menu.grid(row=2, column=1,columnspan=1, sticky="ew", padx=2, pady=2)
        self.selectFile.grid(row=1, column=0, columnspan=1, sticky="ew", padx=2, pady=2)
        self.runScript.grid(row=2, column=0, columnspan=1, sticky="ew", padx=2, pady=2)
        self.textbox.grid(row=3, column = 0, columnspan=2, sticky="ew", padx=2, pady=2)
        self.downloadButton.grid(row=4, column = 0, columnspan=2, sticky="ew", padx=2, pady=2)
        
    def validate(self, inputText): #This processes input in textbox
        if not inputText:
            self.filename = None
            return True
        try:
            filename = str(inputText)
            self.filename = filename
            return True
        except ValueError:
            return False
    
    def runHistory(self): #Produces a file <run_log.txt> containing all the times <Run> button has been pressed and the result
        if os.path.isfile(self.history_file):
            #print('exists')
            with open(self.history_file, 'ab') as outfile:
                outfile.write(('Date: '+str(datetime.datetime.now())+'\n').encode('utf-8'))
                outfile.write(('Input File: '+str(self.browsedvar.get())+'\n').encode('utf-8'))
                outfile.write(('Result: '+str(self.textbox_var.get())+'\n').encode('utf-8'))
                outfile.write((str('------------------------------\n')).encode('utf-8'))
        else:
            #print('doesn\'t exist')
            with open(self.history_file, 'wb') as outfile:
                outfile.write((str('------------------------------\n')).encode('utf-8'))
                outfile.write(('Date: '+str(datetime.datetime.now())+'\n').encode('utf-8'))
                outfile.write(('Input File: '+str(self.browsedvar.get())+'\n').encode('utf-8'))
                outfile.write(('Result: '+str(self.textbox_var.get())+'\n').encode('utf-8'))
                outfile.write((str('------------------------------\n')).encode('utf-8'))
                return 0
    
    def getTestFile(self, filename): #Helps user understand basic usage of the app using test files saved in app folder <test_files/>
        self.browsedvar.set('files/test_files/{}'.format(filename))
        
    def openDownloadsFolder(self): #Command to open Output/Downloads folder
        webbrowser.open(os.path.realpath(self.downloadsFolder_path))
        
    def openRunLogs(self): #Command to open txt file containing all run logs performed since its last creation
        if os.path.isfile(self.history_file):
            webbrowser.open(os.path.realpath(self.history_file))
        else:
            self.popup('runlogs')
        
    def export_to_txt(self): #Exports result to a txt file in folder <output_files/> once Download button is pressed
            #self.directory_output = str(os.path.dirname(self.filename))+'/SelectAndRun_output.txt'
        self.directory_output = 'files/output_files/'+'output_{}.txt'.format(datetime.datetime.now().strftime('%H-%M-%S_%d-%m-%Y'))
        output_file = self.directory_output
        with open(output_file, 'wb') as outfile:
                outfile.write((str(self.textbox_var.get())).encode())
                outfile.write(('\n').encode())
        self.popup('download')
        return 0
        
    def browseText(self): #Browses for a file, sets file path to self.filename
        file = tkinter.filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("txt","*.txt"), ("all files", "*.*")))
        self.browsedvar.set(file)

    def chooseScript(self): #Runs the script chosen with dropdown menu
        if self.menu_var.get()=='Sum':
            self.textbox_var.set('Sum is '+str(self.runSumOnFile()))
            
        if self.menu_var.get()=='Multiply':
            self.textbox_var.set('Product is '+str(self.runMultOnFile()))
            
        if self.menu_var.get()=='All':
            self.textbox_var.set('Sum is '+str(self.runSumOnFile())+', Product is '+str(self.runMultOnFile()))
        self.downloadButton.configure(state = tk.NORMAL)
    
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
            self.popup('warning')
    
    def runMultOnFile(self): #Runs a script (multiplying) on self.filename
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
            
    def popup(self, popup_type): #Produces different pop ups on screen
        if popup_type =='warning':
            tk.messagebox.showwarning('File Error', 'Script cannot be run on selected file. Check file path and try again.')
            
        if popup_type == 'download':
            tk.messagebox.showinfo('Download complete', 'Your result has been saved in the <output_files> folder. Please check the \'Open Downloads Folder\' button in the menu.')
            
        if popup_type == 'runlogs':
            tk.messagebox.showinfo('Run Logs file missing', 'It seems that you do not have a Run Logs file. Try running a script to create one.')

