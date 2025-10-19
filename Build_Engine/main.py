import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QCheckBox

from pubilc.ui import Progress
from tkinter import messagebox
import os
import shutil
from tools import File
import json
class BuildSettingsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('编译引擎')
        self.setGeometry(100, 100, 400, 300)
        #设置图标
        self.setWindowIcon(QIcon('../Resource/image/Logo.png'))

        layout = QVBoxLayout()

        # 平台选择
        platform_label = QLabel('目标平台:')
        self.platform_combo = QComboBox()
        self.platform_combo.addItem('Windows')
        layout.addWidget(platform_label)
        layout.addWidget(self.platform_combo)

        # 构建模式选择
        mode_label = QLabel('编译模式:')
        self.mode_combo = QComboBox()
        self.mode_combo.addItem('Development')
        self.mode_combo.addItem('Release')
        layout.addWidget(mode_label)
        layout.addWidget(self.mode_combo)

        # 版本号输入
        version_label = QLabel('版本号:')
        self.version_input = QLineEdit()
        self.version_input.setPlaceholderText('例如: 1.0.0')
        layout.addWidget(version_label)
        layout.addWidget(self.version_input)

        # 精简构建
        self.slim_build_checkbox = QCheckBox('精简构建')
        layout.addWidget(self.slim_build_checkbox)

        # 构建按钮
        self.build_button = QPushButton('开始构建')
        self.build_button.clicked.connect(self.build)
        layout.addWidget(self.build_button)

        self.setLayout(layout)

    def build(self):
        platform = self.platform_combo.currentText()
        mode = self.mode_combo.currentText()
        version = self.version_input.text()
        slim_build = self.slim_build_checkbox.isChecked()
        print(f'开始构建: 平台={platform}, 模式={mode}, 版本号={version}, 精简构建={slim_build}')
        self.build_button.setEnabled(False)
        #提示框
        messagebox.showinfo('提示', '开始构建')
        #构建核心程序
        print("开始构建核心程序")
        os.system("pyinstaller ../YuEngine/YuEngine.py --onefile --noconsole")
        os.system("pyinstaller ../YuEngine/Loading_Ainmtion.py --onefile --noconsole")
        os.system("pyinstaller ../YuEngine/Main_UI.py --onefile --noconsole")
        os.system("pyinstaller ../YuEngine/editor/editor.py --onefile --noconsole")
        os.system("pyinstaller ../YuEngine/Login.py --onefile --noconsole")
        #把../YuEngine/Resourse拷贝到dist目录下
        print("开始拷贝资源文件")
        shutil.copytree('../YuEngine/Resource', '../YuEngine/dist/Resource')
        print("构建配置文件")
        with open('../YuEngine/dist/version.txt', 'w', encoding='utf-8') as f:
            f.write(version)
        shutil.copytree('../YuEngine/dist', '../YuEngine/Release/Engine/YuEngine ' + version)
        #shutil.copytree("../YuEngine/editor/resources","../YuEngine/dist/resources")
        File.clear_folder("../YuEngine/dist")
        print("构建完成")
        #提示框
        messagebox.showinfo('提示', '构建完成')
        self.build_button.setEnabled(True)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BuildSettingsUI()
    ex.show()
    sys.exit(app.exec_())
