import unittest

from clinic.patient_record import *
from clinic.note import *
from clinic.patient import *

class PatientRecordTest(unittest.TestCase):
    def test_create_note(self):
        expected_note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        expected_note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")

        patient = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        # creating first note
        self.assertTrue(patient.record.create_note("Patient comes with headache and high blood pressure."))
        self.assertEqual("Note code: 1, text: Patient comes with headache and high blood pressure., timestamp: %r" % patient.record.notes[0].time_stamp,
                          str(expected_note_1), "initial note for headache patient")
        
        #creating follow up note
        self.assertTrue(patient.record.create_note("Patient complains of a strong headache on the back of neck."))
        self.assertEqual("Note code: 2, text: Patient complains of a strong headache on the back of neck., timestamp: %r" % patient.record.notes[1].time_stamp,
                          str(expected_note_2), "follow up note for headache patient")
        
    def test_search_note(self):
        patient = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # searching for a note when there are no notes
        self.assertFalse(patient.record.search_note(1), "cannot search if no notes")

        note1 = Note(1,"Patient comes with headache and high blood pressure.")
        patient.record.notes.append(note1)

        # searching when only one note
        self.assertTrue(patient.record.search_note(1), "searching for note found in a notes list with only that note")
        self.assertFalse(patient.record.search_note(2), "searching for a note that does not exist")

        note2 = Note(2,"Patient complains of a strong headache on the back of neck.")
        patient.record.notes.append(note2)
        note3 = Note(3,"Patient is taking medicines to control blood pressure.")
        patient.record.notes.append(note3)

        # searching in a list of notes
        self.assertTrue(patient.record.search_note(3), "searching for a note in a list that contains multiple notes")
        
        # searching after a note has been removed (mocking delete_note)
        patient.record.notes.remove(note2)
        self.assertFalse(patient.record.search_note(2), "searching for a note that has been removed (a.k.a deleted)")
        self.assertTrue(patient.record.search_note(3), "searching for a valid note in a list that has been removed from")
    
    def test_delete_note(self):
        patient = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        # deleting when no notes have been created
        self.assertFalse(patient.record.delete_note(1), "cannot delete if no notes")

        note1 = Note(1,"Patient comes with headache and high blood pressure.")
        patient.record.notes.append(note1)
        note2 = Note(2,"Patient complains of a strong headache on the back of neck.")
        patient.record.notes.append(note2)
        note3 = Note(3,"Patient is taking medicines to control blood pressure.")
        patient.record.notes.append(note3)
        self.assertTrue(len(patient.record.notes) == 3)
        
        # deleting a note in the middle of two with remaining notes in patient record notes
        self.assertTrue(patient.record.delete_note(2), "removing a note from the 'middle' of patient notes")
        self.assertTrue(len(patient.record.notes) == 2)

        # *** do I need to check if I can no longer find the note in notes? (assertNotIn) or is checking length enough ***
        self.assertTrue(patient.record.delete_note(3), "removing note from back of patient notes (most recent)")
        self.assertTrue(len(patient.record.notes) ==1)

        self.assertFalse(patient.record.delete_note(3), "trying to delete a note that has already been deleted")

        # deleting "final" note in patient record notes
        self.assertTrue(patient.record.delete_note(1), "removing the only note in patient notes")
        self.assertTrue(len(patient.record.notes) == 0)

    def test_update_note(self):
        patient = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        # update when no notes have been created
        self.assertFalse(patient.record.update_note(1, "Patient comes with migraine and high blood pressure"), "cannot update if no notes")

        note1 = Note(1,"Patient comes with headache and high blood pressure.")
        patient.record.notes.append(note1)
        # use below if you change the time_stamp to include the creation hour/minute/second/millisecond
        # old_time_stamp = patient.record.notes[0].time_stamp
        note2 = Note(2,"Patient complains of a strong headache on the back of neck.")
        patient.record.notes.append(note2)
        note3 = Note(3,"Patient is taking medicines to control blood pressure.")
        patient.record.notes.append(note3)
        self.assertTrue(len(patient.record.notes) == 3)

        self.assertTrue(patient.record.update_note(1, "Patient comes with migraine and high blood pressure"), "updating properly")
        # following is only true if more information than just year-month-day are saved in note's timestamp
        # self.assertNotEqual(patient.record.notes[0].time_stamp, old_time_stamp)

        self.assertFalse(patient.record.update_note(4, "Patient is no longer with the clinic"), "cannot update a note that doesn't exist")

    def test_retrieve_notes(self):
        patient = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")
        
        # retrieving from empty notes list
        self.assertIsNone(patient.record.retrieve_notes("headache"), "cannot retrieve notes if no notes")

        note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
        note_4 = Note(4, "Patient feels general improvement and no more headaches.")
        note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

        # retrieve one note
        patient.record.notes.append(note_1)
        retrieved_list = patient.record.retrieve_notes("headache")
        self.assertEqual(len(retrieved_list), 1, "retrieved list of notes has size 1")
        actual_note = retrieved_list[0]
        self.assertEqual(actual_note, note_1, "retrieved note in the list is note 1")

        # retrieve no notes
        retrieved_list = patient.record.retrieve_notes("lungs")
        self.assertEqual(len(retrieved_list), 0)

        # retrieve three notes where searched text is a part of a word
        patient.record.notes.append(note_2)
        patient.record.notes.append(note_3)
        patient.record.notes.append(note_4)
        patient.record.notes.append(note_5)
        retrieved_list = patient.record.retrieve_notes("head")
        self.assertEqual(len(retrieved_list), 3, "retrieved list of 'head' notes from Joe Hancock has size 3")
        self.assertEqual(retrieved_list[0], note_1, "first retrieved note in the list is note 1")
        self.assertEqual(retrieved_list[1], note_2, "second retrieved note in the list is note 2")
        self.assertEqual(retrieved_list[2], note_4, "third retrieved note in the list is note 4")

    def test_list_notes(self):
        patient = Patient(9792225555, "Joe Hancock", "1990-01-15", "278 456 7890", "john.hancock@outlook.com", "5000 Douglas St, Saanich")

        # listing notes when there are no notes
        notes_list = patient.record.list_notes()
        self.assertEqual(len(notes_list), 0, "list of notes for patient has size 0")

        note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        note_2 = Note(2, "Patient complains of a strong headache on the back of neck.")
        note_3 = Note(3, "Patient is taking medicines to control blood pressure.")
        note_4 = Note(4, "Patient feels general improvement and no more headaches.")
        note_5 = Note(5, "Patient says high BP is controlled, 120x80 in general.")

        # listing notes when there is only one note
        patient.record.notes.append(note_1)
        notes_list = patient.record.list_notes()
        self.assertEqual(len(notes_list), 1, "list of notes for patient has size 1")
        self.assertEqual(notes_list[0], note_1, "Patient comes with headache and high blood pressure.")

        #listing notes in larger list
        patient.record.notes.append(note_2)
        patient.record.notes.append(note_3)
        patient.record.notes.append(note_4)
        patient.record.notes.append(note_5)

        notes_list = patient.record.list_notes()
        self.assertEqual(len(notes_list), 5, "list of notes has size 5")
        self.assertEqual(notes_list[0], note_5, "note 5 is the first in the list of patients")
        self.assertEqual(notes_list[1], note_4, "note 4 is the second in the list of patients")
        self.assertEqual(notes_list[2], note_3, "note 3 is the third in the list of patients")
        self.assertEqual(notes_list[3], note_2, "note 2 is the fourth in the list of patients")
        self.assertEqual(notes_list[4], note_1, "note 1 is the fifth in the list of patients")

        # listing notes from a deleted-from list
        patient.record.notes.remove(patient.record.notes[0]) # removing note_1
        patient.record.notes.remove(patient.record.notes[1]) # removing note_3
        patient.record.notes.remove(patient.record.notes[2]) # removing note_5

        notes_list = patient.record.list_notes()
        self.assertEqual(len(notes_list), 2, "list of notes has size 2")
        self.assertEqual(notes_list[0], note_4, "note 4 is the first in the list of notes")
        self.assertEqual(notes_list[1], note_2, "note 2 is the second in the list of notes")
        

if __name__ == '__main__':
	unittest.main()
