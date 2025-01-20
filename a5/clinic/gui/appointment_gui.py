import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QGridLayout, QMessageBox, QPlainTextEdit

class AppointmentGUI(QMainWindow):
    def __init__(self, controller, current_patient_phn):
        super().__init__()
        self.controller = controller
        self.current_patient_phn = current_patient_phn

        self.setWindowTitle("Appointment for current patient")
        layout = QGridLayout()
        self.setLayout(layout)
        
        # Create central widget and set layout
        central_widget = QWidget()
        layout = QGridLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
        # creating a new note
        create_note_button = QPushButton("Create new note")
        layout.addWidget(create_note_button, 1, 0)
        create_note_button.setCheckable(True)
        create_note_button.clicked.connect(self.create_note)

        # retrieve existing notes
        self.note_search = QLineEdit(self)
        self.note_search.setPlaceholderText("enter keyword/phrase")
        layout.addWidget(self.note_search, 2, 0)
        
        note_search_button = QPushButton("Search")
        layout.addWidget(note_search_button, 2, 1)
        note_search_button.setCheckable(True)
        note_search_button.clicked.connect(lambda: self.retrieve_notes(self.note_search))

        # update existing note
        self.update_note_id = QLineEdit(self)
        self.update_note_id.setPlaceholderText("enter note ID #")
        layout.addWidget(self.update_note_id, 3, 0)
        
        update_note_button = QPushButton("Search")
        layout.addWidget(update_note_button, 3, 1)
        update_note_button.setCheckable(True)
        update_note_button.clicked.connect(lambda: self.update_note(self.update_note_id))

        # delete existing note
        self.delete_note_id = QLineEdit(self)
        self.delete_note_id.setPlaceholderText("enter note ID #")
        layout.addWidget(self.delete_note_id, 4, 0)
        
        delete_note_button = QPushButton("Delete")
        layout.addWidget(delete_note_button, 4, 1)
        update_note_button.setCheckable(True)
        delete_note_button.clicked.connect(lambda: self.delete_note(self.delete_note_id))
        
        # list full patient record
        list_patient_record_button = QPushButton("List Full Patient Record")
        layout.addWidget(list_patient_record_button, 5, 0, 1, 2)
        list_patient_record_button.setCheckable(True)
        list_patient_record_button.clicked.connect(lambda: self.list_full_patient_record)

# functions to call respective windows once respective button has been pressed on main window

    def create_note(self):
        self.new_note_window = NewNoteWindow(self.controller)
        self.new_note_window.show()
            
    def retrieve_notes(self, note_phn):
        self.show_notes_window = ShowNotesWindow(self.controller, note_phn)
        self.show_notes_window.show()

    def update_note(self, update_note_phn):
        self.show_update_note_window = UpdateNoteWindow(self.controller, update_note_phn)
        self.show_update_note_window.show()

    def delete_note(self, delete_note_phn):
        self.show_delete_note_window = DeleteNoteWindow(self.controller, delete_note_phn)
        self.show_delete_note_window.show()

    def list_full_patient_record(self):
        self.show_notes_window = ListPatientRecordWindow(self.controller)
        self.show_notes_window.show()
        

# Windows for each action

class NewNoteWindow(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        layout = QVBoxLayout()
        self.label = QLabel("New Note")
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.note_input = QLineEdit()
        self.note_input.setPlaceholderText("Type your note here...")
        layout.addWidget(self.note_input)

        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.save_note)
        layout.addWidget(self.create_button)
    
    def save_note(self):
        self.controller.create_note(self.note_input)

class ShowNotesWindow(QWidget):
    def __init__(self, controller, note_phn):
        super().__init__()
        self.controller = controller
        
        layout = QVBoxLayout()
        self.label = QLabel("Retrieved Notes")
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.note_display = QPlainTextEdit()
        self.note_display.setReadOnly(True)
        layout.addWidget(self.note_display)

        self.note_display.clear()

        found_notes = self.controller.retrieve_notes(note_phn)
        if found_notes:
            for note in found_notes:
                formatted_note = f"Note #: {note.code}, from: {note.time_stamp}. \n {note.text}"
                self.note_display.appendPlainText(formatted_note)
        else:
            err = QMessageBox(self)
            err.setWindowTitle("ERROR")
            err.setText("No notes found for that phrase.")
            exit_button = err.exec()
            if exit_button == QMessageBox.StandardButton.Ok:
                return
        
class UpdateNoteWindow(QWidget):
    def __init__(self, controller, update_note_id):
        super().__init__()
        self.controller = controller
        
        layout = QVBoxLayout()
        self.label = QLabel("Update Note")
        layout.addWidget(self.label)

        note = self.controller.search_note(update_note_id)
        self.update_note_id = update_note_id

        if note:
            self.update_note_content = QLineEdit()
            self.update_note_content.setPlaceholderText("Type new text for note:")
            layout.addWidget(self.update_note_content)

            self.update_button = QPushButton("Update")
            self.open_button.clicked.connect(self.update_note)
            layout.addWidget(self.open_button)
        else:
            err = QMessageBox(self)
            err.setWindowTitle("ERROR")
            err.setText("No note found for that ID.")
            exit_button = err.exec()
            if exit_button == QMessageBox.StandardButton.Ok:
                return

    def update_note(self):
        self.controller.update_note(self.update_note_id, self.update_note_content)

class DeleteNoteWindow(QWidget):
    def __init__(self, controller, delete_note_id):
        super().__init__()
        self.controller = controller
        
        layout = QVBoxLayout()
        self.label = QLabel("Delete Note")
        layout.addWidget(self.label)

        note = self.controller.search_note(delete_note_id)
        self.delete_note_id = delete_note_id

        if note:
            warn = QMessageBox(self)
            warn.setWindowTitle("WARN")
            warn.setText("Are you sure you want to delete this note?")
            exit_button = warn.exec()
            if exit_button == QMessageBox.StandardButton.Yes:
                self.delete_note
            if exit_button == QMessageBox.StandardButton.No:
                return
            
        else:
            err = QMessageBox(self)
            err.setWindowTitle("ERROR")
            err.setText("No note found for that ID.")
            exit_button = err.exec()
            if exit_button == QMessageBox.StandardButton.Ok:
                return

    def delete_note(self):
        self.controller.delete_note(self.delete_note_id)

class ListPatientRecordWindow(QWidget):
    def __init___(self, controller):
        super().__init__()
        self.controller = controller
        
        layout = QVBoxLayout()
        self.label = QLabel("List Patient Record")
        layout.addWidget(self.label)


        self.note_display = QPlainTextEdit()
        self.note_display.setReadOnly(True)
        layout.addWidget(self.note_display)

        self.note_display.clear()

        notes = self.controller.list_notes()
        if notes:
            for note in notes:
                formatted_note = f"Note #: {note.code}, from: {note.time_stamp}. \n {note.text}"
                self.note_display.appendPlainText(formatted_note)
        else:
            empty_text = "Patient record is empty"
            self.note_display.appendPlainText(empty_text)


def main():
    app = QApplication(sys.argv)
    window = AppointmentGUI()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()