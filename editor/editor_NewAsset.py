import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial

class CreationCard(QWidget):
    clicked = pyqtSignal(str)  # 修改信号定义

    def __init__(self, title, desc, icon_path=None):
        super().__init__()
        self.setFixedSize(180, 180)
        self.setCursor(Qt.PointingHandCursor)

        # 样式设置
        self.setStyleSheet("""
            QWidget {
                background: #2d2f3b;
                border-radius: 5px;
                border: 1px solid #3c3f51;
            }
            QWidget:hover {
                background: #363847;
                border: 1px solid #4b4e61;
            }
        """)

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)

        # 图标处理
        icon_label = QLabel()
        try:
            if icon_path:
                # 修复路径转义问题
                safe_path = icon_path.replace("\\", "/")
                pixmap = QPixmap(safe_path)
                if pixmap.isNull():
                    raise ValueError("Invalid image file")
                pixmap = pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(pixmap)
            else:
                # 默认图标
                icon_label.setText("ICON")
                icon_label.setStyleSheet("color: white;")
        except Exception as e:
            print(f"Error loading icon: {str(e)}")
            icon_label.setText("ERR")
            icon_label.setStyleSheet("color: red;")

        layout.addWidget(icon_label, 0, Qt.AlignLeft)

        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px;
            color: #e4e6f2;
            padding: 5px 0;
        """)
        layout.addWidget(title_label)

        # 描述
        desc_label = QLabel(desc)
        desc_label.setStyleSheet("color: #7a7f8f;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.clicked.emit(self.title())  # 发射信号时携带标题

class NewDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Asset")
        self.setFixedSize(600, 600)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 15, 20, 20)

        # 标题
        title = QLabel("New Asset")
        title.setStyleSheet("font-size: 24px; color: white;")
        main_layout.addWidget(title)

        # 说明文字
        desc = QLabel("Choose the type of asset you want to create：")
        desc.setStyleSheet("color: #7a7f8f; padding: 10px 0;")
        main_layout.addWidget(desc)

        # 卡片容器
        grid = QGridLayout()
        grid.setSpacing(20)

        # 创建卡片（修复路径转义问题）
        cards = [
            ("Scene", "Scene DIR", r"D:\YuEngine\Resource\image\editor\Asset\Scene.png"),
            ("Animation", "FPS Animation", r"D:\YuEngine\Resource\image\editor\Asset\Animation.png"),
            ("Script", "Python Script", r"D:\YuEngine\Resource\image\editor\Asset\Script.png"),
            ("Shader", "Comshader", r"D:\YuEngine\Resource\image\editor\Asset\Shader.png"),
        ]

        # 使用partial解决闭包变量捕获问题
        for i, (title, desc, icon) in enumerate(cards):
            card = CreationCard(title, desc, icon)
            card.clicked.connect(partial(self.on_card_clicked, title))
            grid.addWidget(card, i // 2, i % 2)  # 改为2列布局

        main_layout.addLayout(grid)
        main_layout.addStretch()

        # 底部按钮
        btn_box = QDialogButtonBox(QDialogButtonBox.Cancel)
        btn_box.rejected.connect(self.reject)
        main_layout.addWidget(btn_box)

        self.setLayout(main_layout)
        self.setStyleSheet("background: #23252e;")

    def on_card_clicked(self, type_name):
        print(f"Creating: {type_name}")
        self.accept()

if __name__ == "__main__":
        try:
            app = QApplication(sys.argv)
            window = NewDialog()
            window.show()
            sys.exit(app.exec_())
        except Exception as e:
            print(f"Fatal error: {str(e)}")
            sys.exit(1)



