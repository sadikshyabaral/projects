import sys
from clinic.controller import Controller
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.gui.main_menu_gui import MainMenuGUI

from PyQt6.QtWidgets import (
    QApplication, QLabel, 
    QPushButton, QLineEdit, 
    QGridLayout, QWidget, QMessageBox
)

from PyQt6.QtCore import QSize

class ClinicGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = Controller(autosave=True)

        layout = QGridLayout()
        self.setLayout(layout)

        self.setWindowTitle("My Clinic")
        
        username = QLabel("username:")
        layout.addWidget(username, 1, 0)
        password = QLabel("password:")
        layout.addWidget(password, 2, 0)

        self.u_input = QLineEdit()
        layout.addWidget(self.u_input, 1, 1)
        self.p_input = QLineEdit()
        self.p_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.p_input, 2, 1)
        
        button = QPushButton("Log In")
        layout.addWidget(button, 3,1)
        button.setCheckable(True)
        button.clicked.connect(self.login)
        button.setFixedSize(QSize(100,50))

    def login(self):
       
       try:
            self.controller.login(self.u_input.text(), self.p_input.text())
       except InvalidLoginException:
            self.show_message("Error", "Invalid login, please try again.")
            return
       self.controller.logged_in = True
       self.open_clinic_gui()
        
            
    def open_clinic_gui(self):
      # close the login window
      self.close()
      
      # open the main menu GUI
      self.clinic_window = MainMenuGUI(self.controller)
      self.clinic_window.show()
    
    def show_message(self, title, message):
        # Display a message box with the given title and message
        QMessageBox.information(self, title, message)

def main():
   app = QApplication(sys.argv)
   window = ClinicGUI()
   window.show()
   app.exec()

if __name__ == '__main__':
   main()
 