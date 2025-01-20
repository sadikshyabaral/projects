import json
from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder

class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave):
        self.autosave = autosave
        self.patients = [] 
        if self.autosave:
            self.load_patients()

    # load patients from a file
    def load_patients(self):
        try:
            with open("clinic/patients.json", 'r') as file:
                self.patients = json.load(file, cls=PatientDecoder)
        except (FileNotFoundError, json.JSONDecodeError):
            self.patients = []
    
    # save patients to file
    def save_patients(self):
        with open("clinic/patients.json", 'w') as file:
            json.dump(self.patients, file, cls=PatientEncoder)

    # search a patient by phn and returns the patient
    def search_patient(self, key):
        for element in self.patients:
            if (element.phn == key):
                return element
        return None

    # create a patient with the given information
    def create_patient(self, patient):
        self.patients.append(patient)
        
        if self.autosave:
            self.save_patients()
        return patient

    # search patient by name
    # returns a list of patients that have name as part of their name
    def retrieve_patients(self, search_string):
        retrieved = []
        
        for patient in self.patients:
            if search_string in patient.name:
                retrieved.append(patient)
        
        return retrieved

    # search patient by phn, and update patient data
    def update_patient(self, key, patient):
        
        # find patient to update
        updating_patient = self.search_patient(key)

        updating_patient.phn = patient.phn
        updating_patient.name = patient.name
        updating_patient.date_of_birth = patient.birth_date
        updating_patient.phone = patient.phone
        updating_patient.email = patient.email
        updating_patient.address = patient.address
        
        if self.autosave:
            self.save_patients()
        
        return True

    # user searches the patient by PHN and deletes the patient from the system
    def delete_patient(self, key):
        
        patient = self.search_patient(key)
        self.patients.remove(patient)
        
        if self.autosave:
            self.save_patients()
        
        return True
    
    # user recovers a list of all the patients
    def list_patients(self):
        patients_list = []
        for patient in self.patients:
            patients_list.append(patient)
        return patients_list