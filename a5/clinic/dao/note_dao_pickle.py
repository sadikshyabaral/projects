from clinic.note import Note
from datetime import date, datetime
from clinic.dao.note_dao import NoteDAO  # Import the abstract NoteDAO class
from pickle import dump, load

class NoteDAOPickle(NoteDAO):
    def __init__(self, phn, autosave):
        self.phn = phn
        self.autosave = autosave
        self.auto_counter = 0
        self.notes = [] 
        self.filepath = f"clinic/records/{self.phn}.dat"
        
        if self.autosave:
            self.load_notes()
    
    # load notes from the patient record file
    def load_notes(self):
        
        # check if file exists
        try:
            with open(self.filepath, 'rb') as file:
                self.notes = load(file)
                
                # update auto_counter
                if self.notes:
                    self.auto_counter = len(self.notes)
        except (FileNotFoundError, EOFError):
            self.notes = [] 
            self.auto_counter = 0;
    
    # make the notes to file
    def save_notes(self):
        with open(self.filepath, 'wb') as file:
            dump(self.notes, file)
      
    # finds and return note with the key
    def search_note(self, key):
        for element in self.notes:
           if (element.code == key):
              return element
        return None
    
    # creates a note with given text
    def create_note(self, text):
        # increment auto_counter whenever you create a note
        self.auto_counter += 1
         
        note = Note(self.auto_counter, text)
        self.notes.append(note)
        
        if self.autosave:
            self.save_notes()
            
        return note
    
    # returns a list of notes that contain the text given
    def retrieve_notes(self, search_string):
        if (len(self.notes) == 0):
           return None
        
        retrieved = []

        for note in self.notes:
          if search_string in note.text:
             retrieved.append(note)
        
        return retrieved
    
    # updates a note's text with given text
    def update_note(self, key, text):
        for note in self.notes:
            
            # note is searched by the note's code and the timestamp updates to current time
            if (key == note.code):
               note.text = text
               note.time_stamp = date.today()
               
               if self.autosave:
                   self.save_notes()  
               return True     
        return False
    
    # deletes a note by its code
    def delete_note(self, key):
        for note in self.notes:
            if (key == note.code):
               self.notes.remove(note)
               
               if self.autosave:
                   self.save_notes()   
               return True
        return False
    
    # returns a list of a patient's complete patient record, from last to first created note by code
    def list_notes(self):
        patient_record_list = []
        
        if (len(self.notes) == 0):
            return patient_record_list
       
        for note in self.notes:
            patient_record_list.append(note)
        
        sorted_patient_record_list = sorted(patient_record_list, key=lambda note: note.code, reverse=True)

        # return patient_record_list need to sort it by datetime or by "code?"
        return sorted_patient_record_list
