import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor

class ProgressBarWindow(QWidget):
    def __init__(self,Name):
        super().__init__()
        self.Name = Name

        self.app = QApplication(sys.argv)
        self.window = ProgressBarWindow(self.Name)
        self.window.show()
        self.window.start_loading()
        self.sys.exit(self.app.exec_())
        self.initUI()

    def initUI(self):
        # 设置窗口标题和初始大小
        self.setWindowTitle(self.Name)
        self.setGeometry(300, 300,600, 50)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建标签，用于显示进度文字
        #self.label = QLabel('加载进度: 0%', self)
        #self.label.setFont(QFont('Arial', 14))
        #self.label.setAlignment(Qt.AlignCenter)
        #layout.addWidget(self.label)

        # 创建进度条
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        # 创建按钮，用于开始加载
        #self.startButton = QPushButton('开始加载', self)
        #self.startButton.clicked.connect(self.start_loading)
        #layout.addWidget(self.startButton)

        # 设置布局
        self.setLayout(layout)

        # 创建一个定时器，用于模拟加载过程
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)

    def start_loading(self):
        # 启动定时器，模拟每100毫秒进度增加1
        self.timer.start(100)
        #self.startButton.setEnabled(False)

    def update_progress(self):
        # 更新进度条和标签的文字
        value = self.progressBar.value()
        if value < 100:
            value += 1
            self.progressBar.setValue(value)
            #self.label.setText(f'加载进度: {value}%')
        else:
            # 当进度达到100%时，停止定时器
            self.timer.stop()
            #self.label.setText('加载完成!')
            #self.startButton.setEnabled(True)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProgressBarWindow('加载进度')
    sys.exit(app.exec_())