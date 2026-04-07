class Person:
    def __init__(self,name,age,id_number):
        self.name=name
        self.age=age
        self.id_number=id_number
    
class Doctor(Person):
    def __init__(self,name,id_number,age,specialization):
        super().__init__(name,id_number,age)
        self.specialization=specialization

class Patient(Person):
    def __init__(self, name, age,id_number, ailment):
        super().__init__(name, age,id_number)
        self.ailment = ailment
        self.medical_record = MedicalRecord()

class MedicalRecord:
    __history = []
    @staticmethod    
    def write_diagnosis (diagnosis):
        MedicalRecord.__history.append(diagnosis)
    @staticmethod
    def get_history():
        return MedicalRecord.__history
    
class Appointment:
    def __init__(self, doctor_name, patient_name, date_time):
        self.date_time = date_time
        self.doctor = doctor_name
        self.patient = patient_name


        



        

        
    