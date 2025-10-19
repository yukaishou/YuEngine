import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

class ProjectItemWidget(QWidget):
    """ 自定义项目列表项 """
    def __init__(self, name, path, last_modified):
        super().__init__()
        self.setFixedHeight(70)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        # 项目图标
        icon_label = QLabel()
        icon_label.setPixmap(QIcon("Resource/image/Logo.png").pixmap(32, 32))

        # 文字信息
        text_layout = QVBoxLayout()
        title = QLabel(name)
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        path_label = QLabel(path)
        path_label.setStyleSheet("color: #666;")
        modified_label = QLabel(f"Last modified: {last_modified}")
        modified_label.setStyleSheet("color: #999; font-size: 12px;")

        text_layout.addWidget(title)
        text_layout.addWidget(path_label)
        text_layout.addWidget(modified_label)

        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        self.setLayout(layout)

class ProjectSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_projects()

    def initUI(self):
        self.setWindowTitle('YuEngine')
        self.resize(800, 500)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 顶部欢迎栏
        header = QLabel("Welcome to YuEngine")
        header.setStyleSheet("""
            background: #3d3d3d;
            color: white;
            font-size: 20px;
            padding: 15px;
        """)
        header.setFixedHeight(60)

        # 主体区域
        body_layout = QHBoxLayout()

        # 左侧面板
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_layout = QVBoxLayout()

        # 搜索框
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search project...")
        self.search_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin: 10px;
            }
        """)

        # 项目列表
        self.project_list = QListWidget()
        self.project_list.setStyleSheet("""
            QListWidget {
                border: none;
                background: #f5f5f5;
            }
            QListWidget::item:hover {
                background: #e0e0e0;
            }
            QListWidget::item:selected {
                background: #d0d0d0;
                border: none;
            }
        """)

        left_layout.addWidget(self.search_box)
        left_layout.addWidget(self.project_list)
        left_panel.setLayout(left_layout)

        # 右侧面板
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)

        # 项目详情
        self.detail_label = QLabel("Select a project to view details")
        self.detail_label.setStyleSheet("font-size: 16px; color: #333;")
        self.detail_label.setWordWrap(True)

        # 按钮组
        button_layout = QHBoxLayout()
        self.open_btn = QPushButton("Open")
        self.new_btn = QPushButton("New Project")
        self.import_btn = QPushButton("Get from VCS")

        for btn in [self.open_btn, self.new_btn, self.import_btn]:
            btn.setFixedSize(120, 30)
            btn.setStyleSheet("""
                QPushButton {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #45a049;
                }
            """)

        button_layout.addWidget(self.open_btn)
        button_layout.addWidget(self.new_btn)
        button_layout.addWidget(self.import_btn)

        right_layout.addWidget(self.detail_label)
        right_layout.addLayout(button_layout)
        right_panel.setLayout(right_layout)

        body_layout.addWidget(left_panel)
        body_layout.addWidget(right_panel)

        main_layout.addWidget(header)
        main_layout.addLayout(body_layout)
        self.setLayout(main_layout)

        # 连接信号
        self.project_list.itemClicked.connect(self.show_details)
        self.search_box.textChanged.connect(self.filter_projects)

    def load_projects(self):
        # 示例项目数据
        projects = [
            {"name": "MyProject", "path": "/path/to/project1", "modified": "2023-10-20"},
            {"name": "WebApp", "path": "/code/webapp", "modified": "2023-10-19"},
            {"name": "DataAnalysis", "path": "~/projects/data", "modified": "2023-10-18"},
            {"name": "DataAnalysis", "path": "~/projects/data", "modified": "2023-10-18"},
            {"name": "DataAnalysis", "path": "~/projects/data", "modified": "2023-10-18"},
            {"name": "DataAnalysis", "path": "~/projects/data", "modified": "2023-10-18"}
        ]

        for p in projects:
            item = QListWidgetItem()
            widget = ProjectItemWidget(p["name"], p["path"], p["modified"])
            self.project_list.addItem(item)
            self.project_list.setItemWidget(item, widget)
            item.setSizeHint(widget.sizeHint())

    def show_details(self, item):
        widget = self.project_list.itemWidget(item)
        details = f"""
            <b>Project Name:</b> {widget.findChild(QLabel).text()}<br>
            <b>Location:</b> {widget.findChildren(QLabel)[1].text()}<br>
            <b>Last Modified:</b> {widget.findChildren(QLabel)[2].text()}
        """
        self.detail_label.setText(details)

    def filter_projects(self, text):
        for i in range(self.project_list.count()):
            item = self.project_list.item(i)
            widget = self.project_list.itemWidget(item)
            name = widget.findChild(QLabel).text().lower()
            item.setHidden(text.lower() not in name)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProjectSelector()
    window.show()
    sys.exit(app.exec_())
