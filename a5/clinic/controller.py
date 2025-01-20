from .patient import Patient
from clinic.dao.patient_dao_json import PatientDAOJSON  
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

import hashlib

class Controller:
    
    def __init__(self, autosave):
        self.patient_dao = PatientDAOJSON(autosave)
        self.current_patient = None
        self.users = self.load_users()
        self.logged_in = False
        self.autosave = autosave

    # load usernames from a text file
    def load_users(self):
        file = 'clinic/users.txt'

        with open(file, 'r') as file:
            lines = file.readlines()

        users = {}
        
        for line in lines:
            key, value = line.strip().split(',')
            users[key.strip()] = value.strip()
        
        return users
    
    def get_password_hash(self, password):
        # Learn a bit about password hashes by reading this code
        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
        return hex_dig

    def login(self, username, password):
        # convert the password into a password hash before
        # comparing it with the password hash that came from the file
        if self.logged_in:
            raise DuplicateLoginException()
        
        if self.users.get(username):
            password_hash = self.get_password_hash(password)
            if self.users.get(username) == password_hash:
                self.logged_in = True
                return True
            else:
                raise InvalidLoginException()
        else:
            raise InvalidLoginException()

    # user logout and unset current patient
    def logout(self):
        
        if self.logged_in:
            self.unset_current_patient()
            self.logged_in = False
            return True
        else:
            raise InvalidLogoutException()
    
    # search a patient by phn and returns the patient
    def search_patient(self, phn):
        if self.logged_in == False:
            raise IllegalAccessException()
        
        else:
            return self.patient_dao.search_patient(phn)
    
    # create a patient with the given information
    def create_patient(self, phn, name, birth_date, phone, email, address):
        if self.logged_in == False:
            raise IllegalAccessException()
        
        patient = self.search_patient(phn)
        if patient is not None:
            raise IllegalOperationException(f"Patient with PHN {phn} already exists.")
        return self.patient_dao.create_patient(Patient(phn, name, birth_date, phone, email, address, self.autosave))
    
    def set_current_patient(self, phn):
        if self.logged_in == False:
            raise IllegalAccessException() 
        
        # find patient with phn and set it as current patient
        for element in self.patient_dao.patients:
            if element.phn == phn:
                self.current_patient = element
                return
        self.current_patient = None
        raise IllegalOperationException()
                
    def get_current_patient(self):
        if self.logged_in == False:
            raise IllegalAccessException() 
        
        return self.current_patient

    def unset_current_patient(self):
        if self.logged_in == False:
            raise IllegalAccessException()
        self.current_patient = None
    
    # search patient by name
    # returns a list of patients that have name as part of their name
    def retrieve_patients(self, name):
        
        if self.logged_in == False:
            raise IllegalAccessException()

        return self.patient_dao.retrieve_patients(name)
    
    # search patient by phn, and update patient data
    def update_patient(self, search_phn, phn, name, birth_date, phone, email, address):
        if self.logged_in == False:
            raise IllegalAccessException()
       
       # check if patient already exists with the new phn
       # cannot update if another patient has the new phn
        if self.search_patient(phn) and search_phn != phn:
            raise IllegalOperationException()
        
        # find patient to update
        patient = self.search_patient(search_phn)
        
        if not patient:
            raise IllegalOperationException()
        
        # need to unset current_patient before updating
        if self.current_patient:
            if patient == self.current_patient:
                raise IllegalOperationException
        else:
            return self.patient_dao.update_patient(search_phn, Patient(phn, name, birth_date, phone, email, address, self.autosave))
            
    # user searches the patient by PHN and deletes the patient from the system
    def delete_patient(self, phn):        
        if self.logged_in == False:
            raise IllegalAccessException()
        
        patient = self.search_patient(phn)
        
        # need to unset current_patient before deleting
        if self.current_patient is not None:
            if self.current_patient.phn == phn:
                #return IllegalOperationException() # there is no exception in the integration tests for this
                raise IllegalOperationException
        
        # if patient exists, delete
        if not patient:
            raise IllegalOperationException() # there is no exception in the integration tests for this
        
        return self.patient_dao.delete_patient(phn)
                
    # user recovers a list of all the patients
    def list_patients(self):
        
        if not self.logged_in:
            raise IllegalAccessException() 
        
        return self.patient_dao.list_patients();
            
    # patient record calls
    def create_note(self, text):
        
        if self.logged_in == False:
            raise IllegalAccessException() 
        
        if self.current_patient != None:
            return self.current_patient.record.create_note(text)
        else:
            raise NoCurrentPatientException()
        
    def delete_note(self, code):
        if self.logged_in == False:
            raise IllegalAccessException()

        if self.current_patient != None:
            # checking to only call delete note if notes is not empty
            if len(self.current_patient.record.note_dao.notes) != 0:
                self.current_patient.record.delete_note(code)
                return True
            else:
                return False
        else:
            raise NoCurrentPatientException()
        
    def update_note(self, key, text):
        if self.logged_in == False:
            raise IllegalAccessException()

        if self.current_patient != None:
            # checking to only call update_note if notes is not empty
            if len(self.current_patient.record.note_dao.notes) != 0:
                self.current_patient.record.update_note(key, text)
                return True
            else:
                return False
        else:
            raise NoCurrentPatientException()
    
    def retrieve_notes(self, text):
        if self.logged_in == False:
            raise IllegalAccessException()

        if self.current_patient != None:
            return self.current_patient.record.retrieve_notes(text)
        else:
            raise NoCurrentPatientException()
        
    def search_note(self, code):
        if self.logged_in == False:
            raise IllegalAccessException()

        if self.current_patient != None:
            return self.current_patient.record.search_note(code)
        else:
            raise NoCurrentPatientException()
        
    def list_notes(self):
        if self.logged_in == False:
            raise IllegalAccessException()

        if self.current_patient != None:
            return self.current_patient.record.list_notes()
        else:
            raise NoCurrentPatientException()
