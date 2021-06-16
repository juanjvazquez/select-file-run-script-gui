import tkinter as tk
from select_and_run import SelectAndRun

app=tk.Tk()
GUI = SelectAndRun(app)
app.option_add('*tearOff', tk.FALSE)
app.mainloop()


    