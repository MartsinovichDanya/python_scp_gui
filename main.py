import sys
import json
from os.path import exists
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from python_scp_gui import Ui_mainWindow
from pathlib import Path
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient


class MainWidget(Ui_mainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.copyButton.clicked.connect(self.copy)
        self.saveDefaultButton.clicked.connect(self.save_default_conf)
        self.chooseLocalButton.clicked.connect(self.open_local)

        self.portEdit.setValue(22)

        if exists('default_creds.json'):
            with open('default_creds.json', 'r') as f:
                ssh_creds = json.loads(f.read())
            self.hostEdit.setText(ssh_creds['hostname'])
            self.portEdit.setValue(ssh_creds['port'])
            self.usernameEdit.setText(ssh_creds['username'])
            self.passEdit.setText(ssh_creds['password'])

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
        ssh_creds = {
            'hostname': self.hostEdit.text(),
            'username': self.usernameEdit.text(),
            'password': self.passEdit.text(),
            'port': self.portEdit.value()
        }

        paths = {
            'local': self.localPathEdit.text(),
            'remote': self.remotePathEdit.text()
        }

        if '' in ssh_creds.values() or '' in paths.values():
            self.message('warning', 'All fields must be filled!')
            return None

        try:
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(**ssh_creds)

            scp = SCPClient(ssh.get_transport())

            if self.isDirButton.isChecked():
                scp.put(paths['local'], remote_path=paths['remote'], recursive=True)
            else:
                scp.put(paths['local'], remote_path=paths['remote'])

            ssh.close()

            self.message('info', 'Done!')
        except Exception as e:
            self.message('error', str(e))

    def save_default_conf(self):
        ssh_creds = {
            'hostname': self.hostEdit.text(),
            'username': self.usernameEdit.text(),
            'password': self.passEdit.text(),
            'port': self.portEdit.value()
        }

        with open('default_creds.json', 'w') as f:
            f.write(json.dumps(ssh_creds))

        self.message('info', 'Saved!')

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
