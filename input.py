import Tkinter as tk
import variables
import calendar
import datetime

def show_entry_fields():
    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
    print(variables.comparasURL)
    variables.comparasURL = e1.get()
    print(variables.comparasURL)

master = tk.Tk()

master.geometry("300x300+300+300")
tk.Label(master, text="First Name").grid(row=1)
tk.Label(master, text="Last Name").grid(row=2)

e1 = tk.Entry(master)
e2 = tk.Entry(master)

e1.grid(row=1, column=1)
e2.grid(row=2, column=1)

cal = calendar(master, font="Arial 14", selectmode='day', cursor="hand1", year=2018, month=2, day=5)
cal.pack(fill="both", expand=True)


tk.Button(master, text='Salir', command=master.quit).grid(row=7, column=2, sticky=tk.W, pady=4)
tk.Button(master, text='Mostrar', command=show_entry_fields).grid(row=7, column=1, sticky=tk.W, pady=4)

tk.mainloop()