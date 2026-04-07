from person import *
from tkinter import *
from tkinter import ttk, messagebox 
from PIL import Image, ImageTk
from tkcalendar import Calendar
import sqlite3
import datetime

file=sqlite3.connect("hospital.db")
cursor=file.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS doctors (name TEXT, age INTEGER, specialization TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS patients (name TEXT, age INTEGER, ailment TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS appointments (doctor_name TEXT, patient_name TEXT, date_time TEXT, booking_date TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS medical_records (patient_name TEXT, diagnosis TEXT)")

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()//2
    screen_height = root.winfo_screenheight()//2
    x = (screen_width ) - (width // 2)
    y = (screen_height ) - (height // 2)
    return (f'{width}x{height}+{x}+{y}')

class HospitalApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Hospital Management System")
        self.window.geometry(center_window(self.window, 800, 500))
        self.window.resizable(False, False)
    
        self.sidebar = Frame(self.window, bg="black", width=200)
        self.sidebar.pack(side=LEFT, fill=Y)

        self.content_frame = Frame(self.window, bg="white")
        self.content_frame.pack(side=RIGHT, fill=BOTH, expand=True)
        self.window.iconphoto(False,ImageTk.PhotoImage(file="photos\\download-_1_.png")  )
        self.bg_img = Image.open("photos\\download.png")
        self.bg_img = self.bg_img.resize((700, 500))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        Label(self.content_frame, image=self.bg_img).place(x=0, y=0)

        self.doctor_list = []
        self.patient_list = []
        self.appointments = []
        Button(self.sidebar, text="Exit", command=self.on_closing,bg="red",fg="white",width=15,height=2,pady=10).pack(side=BOTTOM)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()    
    
    def clear_content(self):
        for _ in self.content_frame.winfo_children():
            _.destroy()  
        Label(self.content_frame, image=self.bg_img).place(x=0, y=0)
    def on_closing(self):
        if messagebox.askokcancel("خروج", "هل تريد إغلاق البرنامج وقاعدة البيانات؟"):
            file.close()
            self.window.destroy() 
    def create_widgets(self):
        Label(self.content_frame, text="Welcome to HospitalApp", font=("Arial", 25, "bold"), bg="black", fg="white").place(x=120, y=50)
        Label(self.sidebar, text="تسجيل الدخول ك", font=("Arial", 12, "bold"), bg="black", fg="white").pack(pady=20)
        Button(self.sidebar, text="طبيب", width=15, bg="white", fg="black", command=self.doctor_login).pack(pady=10)
        Button(self.sidebar, text="مريض", width=15, bg="white", fg="black", command=self.patient_login).pack(pady=10)
        Button(self.sidebar, text="احجز موعد", width=15, bg="white", fg="black", command=self.book_appointment).pack(pady=10)
    
    def doctor_login(self):
        self.clear_content()

        Label(self.content_frame,text='اسم الطبيب',font=("Arial",12,"bold"),bg="black",fg="white").pack(pady=10,)
        self.doctor_name=Entry(self.content_frame,justify="center",relief="solid",font=("Arial",12,"bold"))
        self.doctor_name.pack(pady=10)

        Label(self.content_frame,text='متخصص في',font=("Arial",12,"bold"),bg="black",fg="white").pack(pady=10)
        self.specialization=Entry(self.content_frame,justify="center",relief="solid",font=("Arial",12,"bold"))
        self.specialization.pack(pady=10)
        
        Label(self.content_frame, text="عمر الطبيب",font=("Arial",12,"bold"),bg="black",fg="white").pack(pady=10)
        self.doctor_age=Entry(self.content_frame,justify="center",relief="solid",font=("Arial",12,"bold"))
        self.doctor_age.pack(pady=10)

        Button(self.content_frame, text="Save", command=self.save_doctor_info,font=("Arial",12,"bold"),bg="green",fg="white",width=10).pack(pady=10)
    
    def save_doctor_info(self):
        doctor_name=self.doctor_name.get()
        specialization=self.specialization.get()
        doctor_age=self.doctor_age.get()
        
        if specialization and doctor_age and doctor_name:
            if doctor_age.isdigit():
                doctor_age=int(doctor_age)
                self.doctor_list.append((doctor_name, specialization, doctor_age))
                cursor.execute("INSERT INTO doctors (name, age, specialization) VALUES (?, ?, ?)", (doctor_name, doctor_age, specialization))
                file.commit()
                doctor_id_number=cursor.lastrowid
                messagebox.showinfo("Success", "تمت الاضافه بنجاح")
                return Doctor(doctor_name, doctor_id_number, doctor_age, specialization)            
            else:
                messagebox.showwarning("warning","يجب ان يكون العمر رقم صحيح")
                self.doctor_age.delete(0,END)
        else:
            messagebox.showwarning("Warning","لم يتم ملء جميع الحقول ")    
    
    def patient_login(self):
        self.clear_content()
       
        Label(self.content_frame, text="اسم المريض", font=("Arial", 12, "bold"), bg="blue", fg="white").pack(pady=10)
        self.patient_name = Entry(self.content_frame, justify="center")
        self.patient_name.pack()
       
        Label(self.content_frame, text="عمر المريض", font=("Arial", 12, "bold"), bg="blue", fg="white").pack(pady=10)
        self.patient_age = Entry(self.content_frame, justify="center")
        self.patient_age.pack()

        Label(self.content_frame,text="اعراض المرض",font=("Arial",12,"bold"),bg="blue",fg="white").pack(pady=10)
        self.patient_ailment=Text(self.content_frame,width=46,height=5)
        self.patient_ailment.pack()
       
        Button(self.content_frame, text="Save", command=self.save_patient_info, width=10).pack(pady=10)

    def save_patient_info(self):
        patient_name=self.patient_name.get()
        patient_age=self.patient_age.get()
        patient_ailment=self.patient_ailment.get("1.0", "end-1c")

        if patient_name and patient_age and patient_ailment:
            if patient_age.isdigit():
                patient_age=int(patient_age)
                self.patient_list.append((patient_name, patient_age, patient_ailment))
                cursor.execute("INSERT INTO patients (name, age, ailment) VALUES (?, ?, ?)", (patient_name, patient_age, patient_ailment))
                file.commit()
                patient_id_number=cursor.lastrowid
                messagebox.showinfo("Success", "تمت الاضافه بنجاح")
                return Patient(patient_name, patient_age, patient_id_number, patient_ailment)
            else:
                messagebox.showwarning("warning","يجب ان يكون رقم الهوية رقم صحيح")
                self.patient_id_number.delete(0,END)
        else:
            messagebox.showwarning("Warning", "لم يتم ملء جميع الحقول ")

    def book_appointment(self):
        self.clear_content()
        Label(self.content_frame, image=self.bg_img).place(x=0, y=0)

        doctor_list_name=cursor.execute("SELECT name FROM doctors")
        doctor_list_name=doctor_list_name.fetchall()
        patient_list_name=cursor.execute("SELECT name FROM patients")
        patient_list_name=patient_list_name.fetchall()
        
        self.left_frame=Frame(self.content_frame,width=300,height=300,relief="groove",bd=2)
        self.left_frame.pack(side=RIGHT,anchor="w",padx=20)

        Label(self.left_frame, text="اختر اسم الطبيب", font=("Arial", 12, "bold")).pack(pady=5)
        self.choose_doctor=ttk.Combobox(self.left_frame, state="readonly",values=doctor_list_name)
        self.choose_doctor.pack(pady=5)

        Label(self.left_frame, text="اسم المريض", font=("Arial", 12, "bold")).pack(pady=5)
        self.choose_patient =ttk.Combobox(self.left_frame, state="readonly",values=patient_list_name)
        self.choose_patient.pack(pady=5)

        Label(self.left_frame, text="التاريخ",font=("Arial", 12, "bold")).pack(pady=5)
        self.date_time=Calendar(self.left_frame, selectmode="day", year=2026, month=4, day=1, date_pattern="yyyy-mm-dd")
        self.date_time.pack(pady=20)

        Button(self.left_frame, text="Save appointment", command=self.save_appointment, width=55,height=2,bg="green").pack(side=BOTTOM,pady=20,anchor="e")

    def save_appointment(self):
        doctor_name=self.choose_doctor.get()
        patient_name=self.choose_patient.get()
        date=self.date_time.get_date()
        booking_date=str(datetime.datetime.now().date())


        if date and doctor_name and patient_name:
            self.appointments.append((doctor_name, patient_name, date, booking_date))
            cursor.execute("INSERT INTO appointments (doctor_name, patient_name, date_time, booking_date) VALUES (?, ?, ?, ?)", (doctor_name, patient_name, date, booking_date))
            file.commit()
            messagebox.showinfo("Success", "تم الحجز بنجاح")
            return Appointment(doctor_name,patient_name,self.date_time)

        else:
            messagebox.showwarning("Warning", "لم يتم ملء جميع الحقول")
    
    def show_patients(self):
        self.clear_content()
        patients_frame=Frame(self.content_frame,width=400,height=400,relief="groove",bd=2)
        patients_frame.pack(side=RIGHT,anchor="w",padx=20)
        Label(patients_frame,text="قائمة المرضى",font=("Arial",12,"bold")).pack(pady=10)
        patient_listbox=Listbox(patients_frame,width=50,height=20)
        patient_listbox.pack(pady=10)
        S=Scrollbar(patients_frame, orient="vertical", command=patient_listbox.yview)
        S.pack(side=RIGHT, fill=Y)
        patient_listbox.config(yscrollcommand=S.set)
        cursor.execute("SELECT rowid,* FROM patients")
        patients = cursor.fetchall()
        for patient in patients:
            patient_listbox.insert(END, f"ID : {patient[0]} | Name : {patient[1]} | Age : {patient[2]} | Ailment : {patient[3]}")

    def show_doctors(self):
        self.clear_content()
        doctors_frame=Frame(self.content_frame,width=400,height=400,relief="groove",bd=2)
        doctors_frame.pack(side=RIGHT,anchor="w",padx=20)
        Label(doctors_frame,text="قائمة الاطباء",font=("Arial",12,"bold")).pack(pady=10)
        doctor_listbox=Listbox(doctors_frame,width=50,height=20)
        doctor_listbox.pack(pady=10)
        S=Scrollbar(doctors_frame, orient="vertical", command=doctor_listbox.yview)
        S.pack(side=RIGHT, fill=Y)
        doctor_listbox.config(yscrollcommand=S.set)
        cursor.execute("SELECT rowid,* FROM doctors")
        doctors = cursor.fetchall()
        for doctor in doctors:
            doctor_listbox.insert(END, f"ID : {doctor[0]} | Name : {doctor[1]} | Specialization : {doctor[2]} | Age : {doctor[3]}")
    
    def show_appointments(self):
        self.clear_content()
        appointments_frame=Frame(self.content_frame,width=400,height=400,relief="groove",bd=2)
        appointments_frame.pack(side=RIGHT,anchor="w",padx=20)
        Label(appointments_frame,text="قائمة الحجز",font=("Arial",12,"bold")).pack(pady=10)
        appointment_listbox=Listbox(appointments_frame,width=50,height=20)
        appointment_listbox.pack(pady=10)
        S=Scrollbar(appointments_frame, orient="vertical", command=appointment_listbox.yview)
        S.pack(side=RIGHT, fill=Y)
        appointment_listbox.config(yscrollcommand=S.set)
        cursor.execute("SELECT rowid,* FROM appointments")
        appointments = cursor.fetchall()
        for appointment in appointments:
            appointment_listbox.insert(END, f"Doctor Name : {appointment[1]} | Patient Name : {appointment[2]} | Date : {appointment[3]} | Booking Date : {appointment[4]}")
    
    def edit_patient(self):
        self.clear_content()
        self.Edit_frame=Frame(self.content_frame,width=400,height=400,relief="groove",bd=2)
        self.Edit_frame.place(x=150,y=50)
        Label(self.Edit_frame, text="Edit Patient", font=("Arial", 12, "bold")).pack(pady=10)
        self.Edit_patient=ttk.Combobox(self.Edit_frame,state="readonly",values=cursor.execute("SELECT name FROM patients").fetchall())
        self.Edit_patient.pack(pady=10)
        self.choise=IntVar()
        Radiobutton(self.Edit_frame,text="Add Medical Record",variable=self.choise,value=1).pack(pady=5)
        Radiobutton(self.Edit_frame,text="View Medical Record",variable=self.choise,value=2).pack(pady=5)
        Button(self.Edit_frame,text="Submit",command=self.add_medical_record).pack(pady=10)
        self.dynamic_frame = Frame(self.Edit_frame,)
        self.dynamic_frame.pack(pady=10, fill=BOTH, expand=True)

    def add_medical_record(self):
        patient_name_choise=self.Edit_patient.get()
        choise=self.choise.get()
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        if patient_name_choise:
            if choise==1:
                self.medical=Text(self.dynamic_frame,width=40,height=10)
                self.medical.pack(pady=10)
                def save_medical_record():
                    diagnosis = self.medical.get("1.0", "end-1c")
                    if diagnosis:
                        cursor.execute("CREATE TABLE IF NOT EXISTS medical_records (patient_name TEXT, diagnosis TEXT)")
                        cursor.execute("INSERT INTO medical_records (patient_name, diagnosis) VALUES (?, ?)", (patient_name_choise, self.medical.get("1.0", "end-1c")))
                        file.commit()
                        MedicalRecord.write_diagnosis(diagnosis)
                        messagebox.showinfo("Success", "تمت الاضافه بنجاح")
                    else:
                        messagebox.showwarning("Warning", "لم يتم كتابة التشخيص")
                Button(self.dynamic_frame,text="Save",width=10,bg="green",command=save_medical_record).pack(pady=10)
            elif choise==2:
                cursor.execute("SELECT diagnosis FROM medical_records WHERE patient_name=?", (patient_name_choise,))
                diagnosis = cursor.fetchall()
                diagnosis_text = "\n".join([d[0] for d in diagnosis])
                if not diagnosis:diagnosis=["لا يوجد تشخيص لهذا المريض"]
                self.view_medical=Label(self.dynamic_frame,text=diagnosis_text,width=40,height=10,bg="lightgray",wraplength=300,font=("Arial",12,"bold"),relief="groove",bd=2)
                self.view_medical.pack(pady=10,fill=BOTH,expand=True)




        
