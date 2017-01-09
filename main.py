from PyQt5 import QtGui  # Import the PyQt5 module we'll need
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog

import sys  # We need sys so that we can pass argv to QApplication
import mainwindow  # This file holds our MainWindow and all design related things

# it also keeps events etc that we defined in Qt Designer
import os  # For listing directory methods

class ExampleApp(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()

        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        # When the button is pressed, execute select_file function
        self.log1Button.clicked.connect(self.select_file1)


    def select_file1(self):
        self.log1_line.clear() # In case there are any existing elements in the list
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Log Files (*.log)", options=options)
        if fileName:
            print(fileName)
            self.log1_line.insert(fileName)


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()  # We set the form to be our ExampleApp (design)
    form.show()  # Show the form
    app.exec_()  # and execute the app


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
