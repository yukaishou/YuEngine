import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout,
                             QMessageBox)
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, Qt, QThread


class APIWorker(QObject):
    finished = pyqtSignal(dict)

    def __init__(self, url, data):
        super().__init__()
        self.url = url
        self.data = data

    def process_request(self):
        manager = QNetworkAccessManager()
        request = QNetworkRequest(QUrl(self.url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")

        reply = manager.post(request, json.dumps(self.data).encode())
        while not reply.isFinished():
            QApplication.processEvents()

        response = json.loads(reply.readAll().data().decode())
        self.finished.emit(response)


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.manager = QNetworkAccessManager()

    def initUI(self):
        self.setWindowTitle('用户登录')
        self.setFixedSize(600, 300)

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel('用户名:'))
        layout.addWidget(self.username)
        layout.addWidget(QLabel('密码:'))
        layout.addWidget(self.password)

        btn_login = QPushButton('登录')
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login)

        btn_register = QPushButton('注册')
        btn_register.clicked.connect(self.show_register)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def handle_login(self):
        self.send_request('http://localhost:5000/login')

    def show_register(self):
        self.register_win = RegisterWindow()
        self.register_win.show()

    def send_request(self, url):
        data = {
            'username': self.username.text(),
            'password': self.password.text()
        }

        self.worker = APIWorker(url, data)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.process_request)
        self.worker.finished.connect(self.handle_response)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker_thread.start()

    def handle_response(self, response):
        if response['success']:
            QMessageBox.information(self, '成功', response['message'])
            save_acc(self.username.text(), self.password.text())
            # 关闭应用
            QApplication.quit()
        else:
            QMessageBox.warning(self, '错误', response['message'])


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowModality(Qt.ApplicationModal)

    def initUI(self):
        self.setWindowTitle('用户注册')
        self.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel('用户名:'))
        layout.addWidget(self.username)
        layout.addWidget(QLabel('密码:'))
        layout.addWidget(self.password)

        btn_register = QPushButton('注册')
        btn_register.clicked.connect(self.handle_register)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def handle_register(self):
        self.send_request('http://localhost:5000/register')

    def send_request(self, url):
        data = {
            'username': self.username.text(),
            'password': self.password.text()
        }

        self.worker = APIWorker(url, data)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.process_request)
        self.worker.finished.connect(self.handle_response)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker_thread.start()

    def handle_response(self, response):
        if response['success']:
            QMessageBox.information(self, '成功', response['message'])
            # 注册成功后保存账号密码
            save_acc(self.username.text(), self.password.text())
            self.close()

        else:
            QMessageBox.warning(self, '错误', response['message'])

def save_acc (username, password):
    with open('save/acc/acc.txt', 'w') as f:
        f.write(username + '\n')
        f.write(password + '\n')
# 类似登录窗口的网络请求处理
# 可以复用APIWorker类

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
