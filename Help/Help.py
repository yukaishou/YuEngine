import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPlainTextEdit, QAction,
                             QFileDialog, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel)
from PyQt5.QtCore import Qt, QTimer

class TextViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        # 先初始化属性
        self.lines = []
        self.pages = []
        self.current_page = 0
        self.total_pages = 0
        self.lines_per_page = 1

        # 后初始化UI
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('文档与帮助')
        self.setGeometry(100, 100, 800, 600)

        # 创建菜单栏
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文档')
        open_action = QAction('打开', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 文本显示区域
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)
        layout.addWidget(self.text_edit)

        # 控制区域
        control_layout = QHBoxLayout()
        self.prev_btn = QPushButton('上一页 (←)')
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn = QPushButton('下一页 (→)')
        self.next_btn.clicked.connect(self.next_page)
        self.page_label = QLabel()

        # 设置快捷键
        self.prev_btn.setShortcut(Qt.Key_Left)
        self.next_btn.setShortcut(Qt.Key_Right)

        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.next_btn)
        control_layout.addWidget(self.page_label)
        layout.addLayout(control_layout)

        self.update_controls()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '打开文件')
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.lines = content.split('\n')
                QTimer.singleShot(0, self.calculate_pages)
            except Exception as e:
                self.text_edit.setPlainText(f"打开文件失败：{str(e)}")

    def calculate_pages(self, keep_position=True):
        if not self.lines:
            return

        # 计算新的分页参数
        line_height = self.text_edit.fontMetrics().lineSpacing()
        visible_height = self.text_edit.height()
        new_lines_per_page = visible_height // line_height or 1

        # 保存当前阅读位置
        if keep_position and self.pages:
            old_start_line = self.current_page * self.lines_per_page
            new_page = old_start_line // new_lines_per_page
        else:
            new_page = 0

        # 生成新分页
        self.lines_per_page = new_lines_per_page
        self.pages = [
            '\n'.join(self.lines[i:i + self.lines_per_page])
            for i in range(0, len(self.lines), self.lines_per_page)
        ]
        self.total_pages = len(self.pages)
        self.current_page = min(new_page, self.total_pages - 1) if self.total_pages else 0
        self.update_display()

    def update_display(self):
        if self.total_pages == 0:
            self.text_edit.clear()
            self.page_label.setText("无内容")
        else:
            self.text_edit.setPlainText(self.pages[self.current_page])
            self.page_label.setText(f"第 {self.current_page + 1} 页 / 共 {self.total_pages} 页")
        self.update_controls()

    def update_controls(self):
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(self.current_page < self.total_pages - 1)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_display()

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_display()

    def resizeEvent(self, event):
        if self.lines:
            QTimer.singleShot(0, lambda: self.calculate_pages(keep_position=True))
        super().resizeEvent(event)

    # 其他方法保持不变...
    # (保持后续的 open_file、calculate_pages、update_display 等方法不变)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = TextViewer()
    viewer.show()
    sys.exit(app.exec_())


