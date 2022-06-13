import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from python_scp_gui import Ui_mainWindow
from pathlib import Path

HOME = str(Path.home())


class MainWidget(Ui_mainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.copyButton.clicked.connect(self.copy)
        self.saveDefaultButton.clicked.connect(self.save_default_conf)
        self.chooseLocalButton.clicked.connect(self.open_local)

    def open_template(self):
        fname = QFileDialog.getOpenFileName(ex, 'Open template file', HOME, filter='Word files (*.docx)')
        self.lineEdit_getTemplate.setText(fname[0])
        self.template = self.lineEdit_getTemplate.text()

    def open_data(self):
        fname = QFileDialog.getOpenFileName(ex, 'Open data file', HOME, filter='Excel files (*.xlsx)')
        self.lineEdit_getData.setText(fname[0])
        self.data_file = self.lineEdit_getData.text()

    def open_dir(self):
        dir_name = QFileDialog.getExistingDirectory(ex, 'Choose folder', HOME)
        self.lineEdit_chooseDir.setText(dir_name)
        self.letters_dir = self.lineEdit_chooseDir.text()

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
