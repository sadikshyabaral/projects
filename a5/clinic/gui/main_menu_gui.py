import sys

from PyQt6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QStatusBar,
    QPushButton, QMessageBox, QVBoxLayout, 
    QWidget, QLineEdit, QDialog, QTableView, QHeaderView
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize, QAbstractTableModel, QModelIndex

from clinic.controller import Controller
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.gui.appointment_gui import AppointmentGUI

# display patients in a table view
class PatientTableModel(QAbstractTableModel):
    def __init__(self, patients=None):
        super().__init__()
        
        if patients:
            self.patients = patients
        else:
            self.patients = []
            
        self.headers = ["PHN", "Name", "Birth Date", "Phone", "Email", "Address"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.patients)

    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    # format the data 
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        patient = self.patients[index.row()]
        column = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return patient.phn 
            elif column == 1:
                return patient.name
            elif column == 2:
                return patient.birth_date
            elif column == 3:
                return patient.phone
            elif column == 4:
                return patient.email
            elif column == 5:
                return patient.address
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section]
        return None
    
class MainMenuGUI(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller
        
        self.setWindowTitle('Medical Clinic System - Main Menu')
        
        self.resize(QSize(1000, 700))
        
        # create a toolbar
        toolbar = QToolBar("toolbar")
        self.addToolBar(toolbar)

        patient_action = QAction("Patient", self)
        patient_action.setStatusTip("Patient menu")
        patient_action.triggered.connect(self.onToolBarButtonClick)
        patient_action.setCheckable(True)
        toolbar.addAction(patient_action)
        
        toolbar.addSeparator()
        
        start_appointment_action = QAction("start appointment", self)
        start_appointment_action.setStatusTip("start appointment")
        start_appointment_action.triggered.connect(self.start_appointment)
        start_appointment_action.setCheckable(True)
        toolbar.addAction(start_appointment_action)
        
        toolbar.addSeparator()
        
        log_out_action = QAction("Log out", self)
        log_out_action.setStatusTip("log out")
        log_out_action.triggered.connect(self.logout)
        log_out_action.setCheckable(False) 
        toolbar.addAction(log_out_action)

        self.setStatusBar(QStatusBar(self))
        
        # Create layout for buttons
        layout = QVBoxLayout()

        add_patient_button = QPushButton("Add New Patient")
        add_patient_button.clicked.connect(self.create_patient)
        layout.addWidget(add_patient_button)

        search_patient_button = QPushButton("Search Patient by PHN")
        search_patient_button.clicked.connect(self.search_patient)
        layout.addWidget(search_patient_button)

        retrieve_patient_button = QPushButton("Retrieve Patients by Name")
        retrieve_patient_button.clicked.connect(self.retrieve_patients_by_name)
        layout.addWidget(retrieve_patient_button)

        update_patient_button = QPushButton("Update Patient Data")
        update_patient_button.clicked.connect(self.update_patient)
        layout.addWidget(update_patient_button)

        delete_patient_button = QPushButton("Remove Patient")
        delete_patient_button.clicked.connect(self.delete_patient)
        layout.addWidget(delete_patient_button)

        list_all_patients_button = QPushButton("List All Patients")
        list_all_patients_button.clicked.connect(self.list_all_patients)
        layout.addWidget(list_all_patients_button)

        self.setLayout(layout)
        
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Set the spacing and margins to make buttons closer together
        layout.setSpacing(10)  # Space between buttons
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around the layout
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
        
    def onToolBarButtonClick(self, s):
        print("click", s)

# functions to call respective windows once respective button has been pressed on main window

    def create_patient(self):
        self.create_patient_window = CreatePatientWindow(self.controller, self)
        self.create_patient_window.exec()

    def search_patient(self):
        self.search_patient_window = SearchPatientWindow(self.controller, self)
        self.search_patient_window.exec()

    def retrieve_patients_by_name(self):
        self.retrieve_patient_window = RetrievePatientsWindow(self.controller)
        self.retrieve_patient_window.exec()

    def update_patient(self):
        self.update_patient_window = UpdatePatientWindow(self.controller)
        self.update_patient_window.exec()

    def delete_patient(self):
        self.delete_patient_window = DeletePatientWindow(self.controller, self)
        self.delete_patient_window.exec()

    def list_all_patients(self):
        self.list_all_patients_window = ListAllPatientsWindow(self.controller, self)
        self.list_all_patients_window.exec()
        
    def start_appointment(self):
        self.start_appointment_window = StartAppointment(self.controller, self)
        self.start_appointment_window.exec()
    
    def logout(self, s):
        print("User logged out.")
        
        button = QMessageBox.critical(
            self,
            "Log out?",
            "Are you sure you want to log out?",
            buttons = QMessageBox.StandardButton.Yes,
            defaultButton=QMessageBox.StandardButton.No,
        )
        
        if button == QMessageBox.StandardButton.Yes:
            self.controller.logout()
            self.close()

# Windows for each action
class StartAppointment(QDialog):
      
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Search Patient")
        
        # Creating the widgets for searching PHN
        self.phn_search_label = QLabel("Enter PHN to search:")
        self.phn_search_entry = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.submit_search_patient)

        # Layout for search UI
        layout = QVBoxLayout()
        layout.addWidget(self.phn_search_label)
        layout.addWidget(self.phn_search_entry)
        layout.addWidget(self.search_button)

        # Set the layout for the dialog
        self.setLayout(layout)

    def submit_search_patient(self):
        phn = int(self.phn_search_entry.text())  
        patient = self.controller.search_patient(phn)

        if patient:
            # if patient is found, open the appointment menu GUI
            self.controller.set_current_patient(phn)
            self.close()
            self.parent().close()
    
            # open the appoitment menu GUI
            self.clinic_window = AppointmentGUI(self.controller, phn)
            self.clinic_window.show()
            
        else:
            self.show_message("Error", "No patient found with the given PHN.")

    def show_message(self, title, message):
        # Function to display a message box
        QMessageBox.information(self, title, message)

class CreatePatientWindow(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Add New Patient")

        # Form fields for patient data
        self.phn_label = QLabel("Personal Health Number (PHN):")
        self.phn_entry = QLineEdit()

        self.name_label = QLabel("Full Name:")
        self.name_entry = QLineEdit()

        self.birth_date_label = QLabel("Birth Date (YYYY-MM-DD):")
        self.birth_date_entry = QLineEdit()

        self.phone_label = QLabel("Phone Number:")
        self.phone_entry = QLineEdit()

        self.email_label = QLabel("Email:")
        self.email_entry = QLineEdit()

        self.address_label = QLabel("Address:")
        self.address_entry = QLineEdit()

        self.submit_button = QPushButton("Add Patient")
        self.submit_button.clicked.connect(self.submit_create_patient)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.phn_label)
        layout.addWidget(self.phn_entry)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_entry)
        layout.addWidget(self.birth_date_label)
        layout.addWidget(self.birth_date_entry)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_entry)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_entry)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_entry)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_create_patient(self):
        try:
            phn = self.phn_entry.text()
            name = self.name_entry.text()
            birth_date = self.birth_date_entry.text()
            phone = self.phone_entry.text()
            email = self.email_entry.text()
            address = self.address_entry.text()
            
            if not phn or not name or not birth_date or not phone or not email or not address:
                self.parent().show_message("Error", "All fields must be filled out.")
                return
            
            try:
                phn_int = int(phn)
            except ValueError:
                self.parent().show_message("Error", "PHN must be a valid integer.")
                return
            
            self.controller.create_patient(int(phn), name, birth_date, phone, email, address)
            self.accept()
            self.parent().show_message("Success", "Patient added successfully.")
            
        except IllegalAccessException:
            self.parent().show_message("Error", "Must log in first.")
        except IllegalOperationException:
            self.parent().show_message("Error", f"Patient with PHN {phn} already exists.")

class SearchPatientWindow(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Search Patient")

        self.phn_search_label = QLabel("Enter PHN to search:")
        self.phn_search_entry = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.submit_search_patient)

        layout = QVBoxLayout()
        layout.addWidget(self.phn_search_label)
        layout.addWidget(self.phn_search_entry)
        layout.addWidget(self.search_button)

        self.setLayout(layout)

    def submit_search_patient(self):
        try:            
            
            try:
                int(self.phn_search_entry.text())
            except ValueError:
                self.parent().show_message("Error", "PHN must be a valid integer.")
                return
            
            phn = int(self.phn_search_entry.text())
            patient = self.controller.search_patient(phn)
            
            if patient:
                patient_info = f"PHN: {patient.phn}\nName: {patient.name}\nBirth Date: {patient.birth_date}\nPhone: {patient.phone}\nEmail: {patient.email}\nAddress: {patient.address}"
                self.parent().show_message("Patient Found", patient_info)
            else:
                self.parent().show_message("Error", "Patient not found.")
            self.accept()
        except IllegalAccessException:
            self.parent().show_message("Error", "Must log in first.")

class RetrievePatientsWindow(QDialog):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Retrieve Patients by Name")
        
        self.resize(QSize(700, 400))

        # Input for search criteria
        self.name_label = QLabel("Search for:")
        self.name_entry = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.submit_search_by_name)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_entry)
        layout.addWidget(self.search_button)

        # Create and add QTableView to display patients
        self.patient_table = QTableView()
        layout.addWidget(self.patient_table)

        self.setLayout(layout)

    def submit_search_by_name(self):
        search_string = self.name_entry.text()
        try:
            # Retrieve the list of patients matching the search string
            found_patients = self.controller.retrieve_patients(search_string)
            if found_patients:
                self.display_patients(found_patients)
            else:
                self.show_message("No Patients Found", f"No patients found with name: {search_string}")
        except IllegalAccessException:
            self.show_message("Error", "Must log in first.")

    def display_patients(self, patients):
        # Populate the table with retrieved patients
        model = PatientTableModel(patients)
        self.patient_table.setModel(model)

        # Resize columns to fit content
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)

class UpdatePatientWindow(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Update Patient")

        # Form fields for patient data
        self.phn_search_label = QLabel("Enter the PHN:")
        self.phn_search_entry = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.submit_search_patient)

        # Form fields for updating patient data (initially empty)
        self.phn_label = QLabel("Personal Health Number (PHN):")
        self.phn_entry = QLineEdit()
        self.phn_entry.setReadOnly(True)  # PHN should not be editable.

        self.name_label = QLabel("Full Name:")
        self.name_entry = QLineEdit()

        self.birth_date_label = QLabel("Birth Date (YYYY-MM-DD):")
        self.birth_date_entry = QLineEdit()

        self.phone_label = QLabel("Phone Number:")
        self.phone_entry = QLineEdit()

        self.email_label = QLabel("Email:")
        self.email_entry = QLineEdit()

        self.address_label = QLabel("Address:")
        self.address_entry = QLineEdit()

        self.submit_button = QPushButton("Update Patient")
        self.submit_button.clicked.connect(self.submit_update_patient)

        # Layout to hold all widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.phn_search_label)
        self.layout.addWidget(self.phn_search_entry)
        self.layout.addWidget(self.search_button)
        
        # These widgets will be hidden until a patient is found
        self.layout.addWidget(self.phn_label)
        self.layout.addWidget(self.phn_entry)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_entry)
        self.layout.addWidget(self.birth_date_label)
        self.layout.addWidget(self.birth_date_entry)
        self.layout.addWidget(self.phone_label)
        self.layout.addWidget(self.phone_entry)
        self.layout.addWidget(self.email_label)
        self.layout.addWidget(self.email_entry)
        self.layout.addWidget(self.address_label)
        self.layout.addWidget(self.address_entry)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit_search_patient(self):
        """Search for the patient by PHN and pre-fill the form if found."""
        self.search_phn = int(self.phn_search_entry.text())
        
        patient = self.controller.search_patient(self.search_phn)
        
        if patient:
            # Pre-fill the form fields with the patient's existing data
            self.phn_entry.setText(str(patient.phn))  # Ensure it's a string
            self.name_entry.setText(patient.name)
            self.birth_date_entry.setText(patient.birth_date)
            self.phone_entry.setText(patient.phone)
            self.email_entry.setText(patient.email)
            self.address_entry.setText(patient.address)
            self.submit_button.setEnabled(True)  # Enable the submit button once data is found
        else:
            self.show_message("Error", "Patient not found")

    def submit_update_patient(self):
        
        try:
            # Get updated data from the form
            phn = int(self.phn_entry.text()) 
            name = self.name_entry.text()
            birth_date = int(self.birth_date_entry.text())
            phone = int(self.phone_entry.text())
            email = self.email_entry.text()
            address = self.address_entry.text()

            # Update the patient data using the controller
            self.controller.update_patient(self.search_phn, phn, name, birth_date, phone, email, address)

            self.accept() 
            self.show_message("Success", "Patient updated successfully.")
        except IllegalAccessException:
            self.show_message("Error", "Must log in first.")
        except Exception as e:
            self.show_message("Error", f"An error occurred: {str(e)}")

    def show_message(self, title, message):
        """Display a message to the user."""
        QMessageBox.information(self, title, message)
        
class DeletePatientWindow(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Remove Patient")

        self.phn_search_label = QLabel("Enter the PHN:")
        self.phn_search_entry = QLineEdit()
        self.remove_button = QPushButton("Remove")
        self.remove_button.clicked.connect(self.submit_delete_patient)

        layout = QVBoxLayout()
        layout.addWidget(self.phn_search_label)
        layout.addWidget(self.phn_search_entry)
        layout.addWidget(self.remove_button)

        self.setLayout(layout)

    def submit_delete_patient(self):
        try:
            phn = int(self.phn_search_entry.text())
            patient = self.controller.search_patient(phn)

            if patient:
                
                reply = QMessageBox.question(
                    self,
                    "Confirm Deletion",
                    f"Are you sure you want to remove patient {patient.name} (PHN: {phn})?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    self.controller.delete_patient(phn)
                    self.parent().show_message("Success", "Patient Removed")
                else:
                    self.parent().show_message("Cancelled", "Patient removal cancelled.")
            else:
                self.parent().show_message("Error", "Patient not found")
            
            self.accept()
        except IllegalAccessException:
            self.parent().show_message("Error", "Must log in first.")

class ListAllPatientsWindow(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("List Patients")
        
        self.resize(QSize(700, 400))

        layout = QVBoxLayout()
        
        # Create and add QTableView to display patients
        self.patient_table = QTableView()
        layout.addWidget(self.patient_table)

        self.setLayout(layout)
        patients = self.controller.list_patients()
        self.display_patients(patients)

    def display_patients(self, patients):
        # Populate the table with patients
        model = PatientTableModel(patients)
        self.patient_table.setModel(model)

        # Resize columns to fit content
        self.patient_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

def main():
    app = QApplication(sys.argv)
    window = MainMenuGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()