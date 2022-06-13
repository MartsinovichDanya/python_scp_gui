import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from python_scp_gui import Ui_mainWindow
from pathlib import Path


class MainWidget(Ui_mainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.copyButton.clicked.connect(self.copy)
        self.saveDefaultButton.clicked.connect(self.save_default_conf)
        self.chooseLocalButton.clicked.connect(self.open_local)

        self.portEdit.setValue(22)

    def open_local(self):
        if self.isDirButton.isChecked():
            path = self.open_local_dir()
        else:
            path = self.open_local_file()

        self.localPathEdit.setText(path)

    @staticmethod
    def open_local_file():
        fname = QFileDialog.getOpenFileName(ex, 'Choose local file', str(Path.home()))
        return fname[0]

    @staticmethod
    def open_local_dir():
        dir_name = QFileDialog.getExistingDirectory(ex, 'Choose local dir', str(Path.home()))
        return dir_name

    def copy(self):
        pass

    def save_default_conf(self):
        pass

    def run(self):
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        if self.template and self.data_file and self.letters_dir:
            try:
                for step in do_things(self.template, self.data_file, self.letters_dir):
                    if step == 'convert':
                        self.message('info', 'Идет конвертация файлов в pdf.\nПожалуйста, подождите.')
                        self.progressBar.hide()
                    else:
                        self.progressBar.setMaximum(step[1])
                        self.progressBar.setValue(step[0])
            except Exception as e:
                self.message('error', str(e))
            else:
                self.message('info', 'Письма сгенерированы успешно!')
        else:
            self.message('warning', 'Вы заполнили не все поля.')

    @staticmethod
    def message(status, text):
        msg = QMessageBox()
        msg.setWindowTitle(status)
        msg.setText(text)
        if status == 'warning':
            msg.setIcon(QMessageBox.Warning)
        elif status == 'info':
            msg.setIcon(QMessageBox.Information)
        elif status == 'error':
            msg.setIcon(QMessageBox.Critical)

        msg.exec_()


app = QApplication(sys.argv)
ex = MainWidget()
ex.show()
sys.exit(app.exec_())
