import sys
import time
from pathlib import Path
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread, QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from editor import editor_NewAsset as new
from editor import editor_NewDIR as newdir
from editor.editor_NewAsset import NewDialog
import subprocess


# ==================== 文件监控模块 ====================
class FileMonitorWorker(QObject):
    file_changed = pyqtSignal(str, str)  # (event_type, path)

    def __init__(self, watch_path):
        super().__init__()
        self.watch_path = watch_path
        self.observer = Observer()
        self.event_handler = QtFileHandler(self.file_changed)

    def run_monitoring(self):
        self.observer.schedule(
            self.event_handler,
            str(self.watch_path),
            recursive=True
        )
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except Exception as e:
            print(f"Monitoring error: {e}")
        finally:
            self.observer.stop()
            self.observer.join()

class QtFileHandler(FileSystemEventHandler):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def on_any_event(self, event):
        if event.is_directory:
            return

        if event.event_type == 'created':
            self.signal.emit("created", event.src_path)
        elif event.event_type == 'modified':
            self.signal.emit("modified", event.src_path)
        elif event.event_type == 'deleted':
            self.signal.emit("deleted", event.src_path)

# ==================== 界面组件 ====================
class ProjectPanel(QDockWidget):
    def __init__(self):
        super().__init__("Project")
        self.init_ui()
        self.monitor_thread = None
        self.setup_file_monitor()

    def init_ui(self):
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setStyleSheet("""
            QTreeWidget { 
                background-color: #252526;
                color: #D4D4D4;
                border: none;
            }
        """)
        self.setWidget(self.tree)

        # 上下文菜单
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)

    def setup_file_monitor(self):
        default_path = Path.home() / "D:\YuEngine\prefabs\projects\prefab_project/assets"
        self.monitor_thread = QThread()
        self.worker = FileMonitorWorker(default_path)
        self.worker.moveToThread(self.monitor_thread)
        self.worker.file_changed.connect(self.update_project_tree)
        self.monitor_thread.started.connect(self.worker.run_monitoring)
        self.monitor_thread.start()
        self.build_project_tree(default_path)

    def build_project_tree(self, path):
        self.tree.clear()
        root_path = Path(path)
        root_item = QTreeWidgetItem([root_path.name])
        root_item.setData(0, Qt.UserRole, str(root_path))
        self.tree.addTopLevelItem(root_item)
        self.populate_tree_items(root_item, root_path)

    def populate_tree_items(self, parent_item, path):
        try:
            for child in sorted(path.iterdir(), key=lambda x: x.is_file()):
                item = QTreeWidgetItem([child.name])
                item.setData(0, Qt.UserRole, str(child))
                parent_item.addChild(item)
                if child.is_dir():
                    self.populate_tree_items(item, child)
        except PermissionError:
            pass

    def update_project_tree(self, event_type, path):
        target_path = Path(path)
        parent_path = target_path.parent
        parent_items = self.tree.findItems(parent_path.name, Qt.MatchRecursive)

        if event_type == "deleted":
            items = self.tree.findItems(target_path.name, Qt.MatchRecursive)
            for item in items:
                if Path(item.data(0, Qt.UserRole)) == target_path:
                    parent = item.parent()
                    if parent:
                        parent.removeChild(item)
                    else:
                        self.tree.takeTopLevelItem(
                            self.tree.indexOfTopLevelItem(item))
        else:
            if parent_items:
                parent_item = parent_items[0]
                if not any(Path(child.data(0, Qt.UserRole)) == target_path
                          for child in parent_item.takeChildren()):
                    new_item = QTreeWidgetItem([target_path.name])
                    new_item.setData(0, Qt.UserRole, str(target_path))
                    parent_item.addChild(new_item)

    def show_context_menu(self, pos):
        menu = QMenu()
        actions = {
            "New Folder": self.create_folder,
            "Show in Explorer": self.show_in_explorer,
            "Refresh": self.refresh_tree,
            "New Asset": self.create_asset
        }
        for text, callback in actions.items():
            action = menu.addAction(text)
            action.triggered.connect(callback)
        menu.exec_(self.tree.viewport().mapToGlobal(pos))

    def create_folder(self):
        # 创建文件夹对话框
        dialog = newdir.CreateFolderDialog()
        dialog.exec_()

    def create_asset(self):
        print("New Asset")
        # 创建资产对话框
        dialog = NewDialog()
        dialog.exec_()

    def rename_asset(self):
        print("Rename Asset")

    def show_in_explorer(self):
        item = self.tree.currentItem()
        if item:
            path = Path(item.data(0, Qt.UserRole))
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    def refresh_tree(self):
        current_root = Path(self.worker.watch_path)
        self.build_project_tree(current_root)

class UnityStyleEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.setWindowTitle("YuEngine editor")
        self.setGeometry(100, 100, 1280, 720)

        # 核心组件
        self.create_menu_bar()
        self.create_toolbar()
        self.create_central_area()
        self.create_dock_panels()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu("File")
        file_menu.addAction("New Project...")
        file_menu.addAction("Open Project...")
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        # 编辑菜单
        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addAction("Cut")

        # 视图菜单
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Reset Layout", self.reset_layout)

        # 引擎菜单
        engine_menu = menubar.addMenu("Engine")
        engine_menu.addAction("Run")
        engine_menu.addAction("Stop")
        engine_menu.addAction("Build")



    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # 工具按钮
        tools = [
            ("Resources/image/editor/Bar/Transfrom.png", "Move Tool"),
            ("Resources/image/editor/Bar/rotation.png", "Rotate Tool"),
            ("Resources/image/editor/Bar/Scall.png", "Scale Tool"),
            ("Resources/image/editor/Bar/Play.png", "Play Mode")
        ]
        for icon, tooltip in tools:
            btn = QAction(QIcon(icon), tooltip, self)
            toolbar.addAction(btn)

    def create_central_area(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 场景视图标签
        scene_view = QLabel("Scene View")
        scene_view.setAlignment(Qt.AlignCenter)
        scene_view.setStyleSheet("""
            QLabel {
                background-color: #2D2D2D;
                color: #AAAAAA;
                font-size: 24px;
                border: 2px solid #3F3F46;
            }
        """)
        layout.addWidget(scene_view)

    def create_dock_panels(self):
        # 层级面板
        hierarchy = QDockWidget("Wrold", self)
        hierarchy.setWidget(self.create_hierarchy_tree())
        self.addDockWidget(Qt.LeftDockWidgetArea, hierarchy)

        # 项目面板
        self.project_panel = ProjectPanel()
        self.addDockWidget(Qt.RightDockWidgetArea, self.project_panel)

        # 属性面板
        inspector = QDockWidget("Inspector", self)
        inspector.setWidget(self.create_inspector_form())
        self.addDockWidget(Qt.RightDockWidgetArea, inspector)

    def create_hierarchy_tree(self):
        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        tree.setStyleSheet("""
            QTreeWidget { 
                background-color: #252526;
                color: #D4D4D4;
                border: none;
            }
        """)
        for i in range(1, 6):
            item = QTreeWidgetItem([f"GameObject {i}"])
            tree.addTopLevelItem(item)
        return tree

    def create_inspector_form(self):
        form = QWidget()
        layout = QFormLayout(form)

        fields = [
            ("Name", QLineEdit("Main Camera")),
            ("Tag", QComboBox()),
            ("Position", QLineEdit("0, 0, 0")),
            ("Rotation", QLineEdit("0, 0, 0")),
            ("Scale", QLineEdit("1, 1, 1"))
        ]

        for label, widget in fields:
            widget.setStyleSheet("""
                QWidget {
                    background: #333333;
                    color: #FFFFFF;
                    border: 1px solid #3F3F46;
                    padding: 3px;
                }
            """)
            layout.addRow(label, widget)

        return form

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #383838;
            }
            QMenuBar {
                background-color: #2D2D2D;
                color: #D4D4D4;
            }
            QMenuBar::item:selected {
                background: #3F3F46;
            }
            QDockWidget::title {
                background: #252526;
                padding: 4px;
            }
            QToolBar {
                background: #333333;
                border: none;
                padding: 2px;
            }
            QToolButton {
                padding: 4px;
            }
        """)

    def reset_layout(self):
        # 重置布局逻辑
        pass

# ==================== 启动应用 ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 设置图标字体
    font = app.font()
    font.setPixelSize(12)
    app.setFont(font)

    window = UnityStyleEditor()
    window.show()
    sys.exit(app.exec_())







