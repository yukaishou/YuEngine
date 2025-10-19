import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QCheckBox

class BuildSettingsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('构建设置')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # 平台选择
        platform_label = QLabel('目标平台:')
        self.platform_combo = QComboBox()
        self.platform_combo.addItem('Windows')
        layout.addWidget(platform_label)
        layout.addWidget(self.platform_combo)

        # 构建模式选择
        mode_label = QLabel('构建模式:')
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
        build_button = QPushButton('开始构建')
        build_button.clicked.connect(self.build)
        layout.addWidget(build_button)

        self.setLayout(layout)

    def build(self):
        platform = self.platform_combo.currentText()
        mode = self.mode_combo.currentText()
        version = self.version_input.text()
        slim_build = self.slim_build_checkbox.isChecked()
        print(f'开始构建: 平台={platform}, 模式={mode}, 版本号={version}, 精简构建={slim_build}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BuildSettingsUI()
    ex.show()
    sys.exit(app.exec_())
