import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CreateFolderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("新建文件夹")
        self.setMinimumSize(500, 400)

        # 设置字体
        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(10)

        # 主布局
        main_layout = QVBoxLayout(self)

        # 标题
        title_label = QLabel("New Folder")
        title_label.setFont(font)
        title_label.setStyleSheet("font-weight: bold;")

        # 路径显示
        self.path_label = QLabel("Location: /project/src")
        self.path_label.setFont(font)

        # 输入框
        self.name_edit = QLineEdit()
        self.name_edit.setFont(font)
        self.name_edit.setPlaceholderText("Name of the new folder")

        # 目录树结构
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setFont(font)

        # 模拟目录结构
        root = QTreeWidgetItem(self.tree, ["project"])
        src = QTreeWidgetItem(root, ["src"])
        QTreeWidgetItem(src, ["main"])
        QTreeWidgetItem(root, ["test"])

        # 按钮区域
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        self.ok_button = button_box.button(QDialogButtonBox.Ok)
        self.ok_button.setEnabled(False)

        # 添加组件到布局
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.path_label)
        main_layout.addWidget(self.name_edit)
        main_layout.addWidget(QLabel("Choose a directory:"))

        # 添加带边框的树控件
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame_layout = QVBoxLayout(frame)
        frame_layout.addWidget(self.tree)
        main_layout.addWidget(frame)

        main_layout.addWidget(button_box)

        # 信号连接
        self.name_edit.textChanged.connect(self.validate_input)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.setStyleSheet("background: #23252e;")

    def validate_input(self):
        text = self.name_edit.text()
        # 简单验证：非空且不含特殊字符
        is_valid = bool(text.strip()) and '/' not in text
        self.ok_button.setEnabled(is_valid)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = app.font()
    font.setPixelSize(12)
    app.setFont(font)
    dialog = CreateFolderDialog()
    if dialog.exec_() == QDialog.Accepted:
        print("New folder name:", dialog.name_edit.text())
    sys.exit(app.exec_())
