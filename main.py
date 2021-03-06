import sys  # We need sys so that we can pass argv to QApplication
from os.path import expanduser
# from PyQt5 import QtGui  # Import the PyQt5 module we'll need
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
# from PyQt5.QtGui import QIcon

import mainwindow  # this holds our MainWindow and all design related things
import conversion  # this performs the merge


class MainWin(QMainWindow, mainwindow.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the mainwindow.py file
        super(self.__class__, self).__init__()

        self.setupUi(self)  # This is defined in design.py file automatically
        # It sets up layout and widgets that are defined

        # On mac, menubars are displayed on the system by default. Disable
        self.menuBar.setNativeMenuBar(False)

        # Add trigger to menubar items
        self.actionQuit.triggered.connect(self.close)
        self.actionInfo.triggered.connect(show_info)

        # Set current date
        self.dateEdit.setDate(QtCore.QDate.currentDate())

        # Connect button press to functions
        self.log1Button.clicked.connect(self.select_file1)
        self.log2Button.clicked.connect(self.select_file2)

        self.listButton.clicked.connect(self.parse_indices)

        self.outFolderButton.clicked.connect(self.select_output)

        self.mergeButton.clicked.connect(self.process_all)

    def select_file1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Selecting log file 1", "",
            "Log Files (*.log);;All Files (*)", options=options
            )
        if fileName:
            self.log1_line.insert(fileName)

    def select_file2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Selecting log file 2", "",
            "Log Files (*.log);;All Files (*)", options=options
            )
        if fileName:
            self.log2_line.insert(fileName)

    def parse_indices(self):
        ind_1, ind_2 = conversion.parse_indices(
            logfile_1=self.log1_line.text(),
            logfile_2=self.log2_line.text()
            )
        for i1 in ind_1:
            self.listWidget_1.addItem(i1)
        for i2 in ind_2:
            self.listWidget_2.addItem(i2)

    def select_output(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        dirName = QFileDialog.getExistingDirectory(
            self,
            "Select folder for output file",
            expanduser('~'),
            options=options
            )
        if dirName:
            self.outfolder_line.insert(dirName)

    def process_all(self):
        outcome = conversion.merge(
            logfile_1=self.log1_line.text(),
            logfile_2=self.log2_line.text(),
            MSNumber=self.MS_line.text() + '.csv',
            InvestigatorName=self.inv_line.text(),
            ExperimentName=self.exp_line.text(),
            Date=self.dateEdit.date().toString('MM/dd/yyyy'),
            Description=self.desc_line.text(),
            Reads=self.cycles_line.text()
            )

        self.statusBar.showMessage('File %s written' % outcome)


def show_info():
    msgbox = QMessageBox()
    msgbox.setText('A program by IMV')
    msgbox.exec_()


def main():
    app = QApplication(sys.argv)  # A new instance of QApplication
    mainwin = MainWin()  # We set the form to be our ExampleApp (design)
    mainwin.show()  # Show the form
    sys.exit(app.exec_())  # and execute the app


if __name__ == '__main__':
    main()
