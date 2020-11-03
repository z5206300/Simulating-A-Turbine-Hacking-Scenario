  
import PyQt5
from PyQt5 import QtWidgets, uic, QtCore
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import sqlite3
import sys
import hashlib

attempts = 0


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('TurbineLogin.ui', self)

        self.button = self.findChild(QtWidgets.QPushButton, 'loginButton')
        self.button.clicked.connect(self.loginProcess)

        self.password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.button = self.findChild(QtWidgets.QPushButton, 'exitButton')
        self.button.clicked.connect(self.exitProcess)

        self.show()

    def loginProcess(self):

        username = str(self.username.text())
        password = str(self.password.text())

        # You can create a new database by changing the name within the quotes
        conn = sqlite3.connect('login.db')

        # The database will be saved in the location where your 'py' file is saved
        c = conn.cursor()

        hashP = hashlib.md5(password.encode('utf-8')).hexdigest()
        c.execute("SELECT * FROM LOGIN WHERE username='" + username + "' and password='" + hashP + "'")

        global attempts
        attempts = attempts + 1

        if c.fetchone():
            self.successfulLogin()

        if attempts > 2:
            self.destroy()

        else:
            self.hide()
            otherview = SecondForm(self)
            otherview.show()

    def successfulLogin(self):
        self.close()

    def exitProcess(self):
        sys.exit()


class SecondForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(SecondForm, self).__init__(parent)
        uic.loadUi('Incorrect.ui', self)
        self.button = self.findChild(QtWidgets.QPushButton, 'continueb')
        self.button.clicked.connect(self.back)

    def back(self):
        self.parent().show()
        self.close()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
