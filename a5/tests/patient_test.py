from unittest import TestCase
from clinic.patient import Patient

class PatientTest(TestCase):
    
    def test_str(self):
        patient1 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        patient2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")

        self.assertIsNotNone(repr(patient1))
         
        expected_repr1 = "Patient(PHN: 9790012000, Name: 'John Doe', Birth_date: '2000-10-10', Phone: '250 203 1010', Email: 'john.doe@gmail.com', Address: '300 Moss St, Victoria') "
        self.assertEqual(repr(patient1), expected_repr1, "john")
        expected_repr2 = "Patient(PHN: 9790014444, Name: 'Mary Doe', Birth_date: '1995-07-01', Phone: '250 203 2020', Email: 'mary.doe@gmail.com', Address: '300 Moss St, Victoria') "
        self.assertEqual(repr(patient2), expected_repr2, "mary")
        self.assertNotEqual(repr(patient1), repr(patient2), "different patients")
        
         
    def test_eq(self):
        patient1 = Patient(9790012000, "John Doe", "2000-10-10", "250 203 1010", "john.doe@gmail.com", "300 Moss St, Victoria")
        patient2 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")
        patient3 = Patient(9790014444, "Mary Doe", "1995-07-01", "250 203 2020", "mary.doe@gmail.com", "300 Moss St, Victoria")

        self.assertNotEqual(patient1, patient2, "different patients")
        self.assertEqual(patient2, patient3, "same patients")
       

if __name__ == '__main__':
	unittest.main()
