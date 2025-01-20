import unittest

from clinic.patient_record import *
from clinic.note import *

class NoteTest(unittest.TestCase):
    
    def test_str(self):
        note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        note_2 = Note(2, "Patient is taking medicines to control blood pressure.")

        self.assertIsNotNone(str(note_1))
        self.assertEqual("Note code: 1, text: Patient comes with headache and high blood pressure., timestamp: %r" % note_1.time_stamp,
                          str(note_1), "headache patient")
        self.assertIsNotNone(str(note_2))
        self.assertEqual("Note code: 2, text: Patient is taking medicines to control blood pressure., timestamp: %r" % note_2.time_stamp,
                          str(note_2), "blood pressure patient")
        self.assertNotEqual(str(note_1), str(note_2), "different notes, different strings")
         
    def test_eq(self):
        note_1 = Note(1, "Patient comes with headache and high blood pressure.")
        note_1a = Note(1, "Patient comes with headache and high blood pressure.")
        note_2 = Note(3, "Patient is taking medicines to control blood pressure.")
        
        self.assertEqual(note_1, note_1a, "same notes, same text strings, different timestamps")
        self.assertNotEqual(note_1, note_2, "different notes, different text strings")

if __name__ == '__main__':
	unittest.main()
