import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer

class LoadProjectUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_progress = 0

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('YuEngine -- project manager')
        self.setGeometry(300, 300, 800, 600)

        # 核心组件
        self.create_top_panel()   # 顶部加载控制
        self.create_center_form() # 加载参数配置
        self.create_log_output()  # 日志输出
        self.create_menu()        # 菜单栏

    def create_top_panel(self):
        """加载进度控制面板"""
        top_widget = QWidget()
        layout = QHBoxLayout()

        # 加载进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar, 80)

        # 取消按钮
        btn_cancel = QPushButton("取消加载")
        btn_cancel.clicked.connect(self.cancel_load)
        layout.addWidget(btn_cancel, 20)

        top_widget.setLayout(layout)
        dock = QDockWidget("加载进度", self)
        dock.setWidget(top_widget)
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

    def create_center_form(self):
        """加载参数表单"""
        form_widget = QWidget()
        form_layout = QFormLayout()

        # 项目选择
        self.project_combo = QComboBox()
        self.project_combo.addItems(['项目1', '项目2', '项目3', '项目4'])
        form_layout.addRow("选择项目:", self.project_combo)

        # 开始加载按钮
        btn_load = QPushButton("开始加载")
        btn_load.clicked.connect(self.start_load)
        form_layout.addRow(btn_load)

        form_widget.setLayout(form_layout)
        self.setCentralWidget(form_widget)

    def create_log_output(self):
        """日志输出控制台"""
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        dock = QDockWidget("加载日志", self)
        dock.setWidget(self.log_area)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def create_menu(self):
        """菜单栏"""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('文件')

        act_new = QAction('新建项目', self)
        act_open = QAction('打开项目...', self)
        file_menu.addActions([act_new, act_open])

    # 功能逻辑部分
    def start_load(self):
        """模拟加载过程"""
        self.load_progress = 0
        self.progress_bar.setValue(0)
        self.log_area.append(">>> 开始加载项目...")

        # 模拟进度更新
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(200)  # 200ms更新一次

    def update_progress(self):
        self.load_progress += 1
        self.progress_bar.setValue(self.load_progress)

        # 输出日志模拟
        if self.load_progress % 10 == 0:
            self.log_area.append(f"正在处理阶段 {self.load_progress}%...")

        # 完成时停止
        if self.load_progress >= 100:
            self.timer.stop()
            self.log_area.append("加载完成！")
            QMessageBox.information(self, "成功", "项目加载成功！")

    def cancel_load(self):
        self.timer.stop()
        self.log_area.append("加载已取消")
        self.progress_bar.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LoadProjectUI()
    ex.show()
    sys.exit(app.exec_())


