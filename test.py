from tkinter import *
from appGUI import HospitalApp



window=Tk()
app=HospitalApp(window)
m=Menu(window)
file_menu=Menu(m,tearoff=0)
file_menu.add_command(label="show patients",command=lambda: app.show_patients())
file_menu.add_command(label="show doctors",command=lambda: app.show_doctors())
file_menu.add_command(label="show appointments",command=lambda: app.show_appointments())
m.add_cascade(label="Files",menu=file_menu)
window.config(menu=m)
edit_menu=Menu(m,tearoff=0)
edit_menu.add_command(label="Add-MedicalRecord",command=lambda: app.edit_patient())
m.add_cascade(label="Edit",menu=edit_menu)
window.config(menu=m)



window.mainloop()

