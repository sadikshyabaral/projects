from .note import Note
from datetime import date, datetime
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord: 
      def __init__(self, phn, autosave):
         self.note_dao = NoteDAOPickle(phn, autosave)
      
      def create_note(self, text):
        return self.note_dao.create_note(text)
        
      def delete_note(self, key):
         return self.note_dao.delete_note(key)
      
      def update_note(self, key, text):
         return self.note_dao.update_note(key, text)
         
      def retrieve_notes(self, text):
         return self.note_dao.retrieve_notes(text)
     
      def search_note(self, code):
         return self.note_dao.search_note(code);

      def list_notes(self):
         return self.note_dao.list_notes();