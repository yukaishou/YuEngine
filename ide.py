import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs

class PythonIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.process = None
        self.current_file = None
        self.auto_save_timer = QTimer()
        self.init_connections()

    def initUI(self):
        self.setWindowTitle('PyIDE Pro')
        self.setGeometry(300, 300, 1200, 800)
        self.setup_editor()
        self.setup_console()
        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_statusbar()
        self.setup_dock_widgets()

    def setup_editor(self):
        # 使用QScintilla编辑器
        self.editor = QsciScintilla()
        self.editor.setUtf8(True)

        # 设置Python语法高亮
        lexer = QsciLexerPython()
        lexer.setDefaultFont(QFont("Consolas", 12))
        self.editor.setLexer(lexer)

        # 代码补全
        self.api = QsciAPIs(lexer)
        for kw in dir(__builtins__):
            self.api.add(kw)
        self.api.prepare()

        # 编辑器设置
        self.editor.setAutoIndent(True)
        self.editor.setIndentationWidth(4)
        self.editor.setTabWidth(4)
        self.editor.setMarginLineNumbers(0, True)
        self.editor.setMarginWidth(0, "0000")
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor(240, 240, 240))

        # 自动补全
        self.editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.editor.setAutoCompletionThreshold(1)
        self.editor.setAutoCompletionCaseSensitivity(False)

        self.setCentralWidget(self.editor)

    def setup_console(self):
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 10))
        self.console_dock = QDockWidget("Console", self)
        self.console_dock.setWidget(self.console)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console_dock)

    def create_actions(self):
        # 文件操作
        self.new_action = QAction(QIcon.fromTheme("document-new"), "&New", self)
        self.open_action = QAction(QIcon.fromTheme("document-open"), "&Open...", self)
        self.save_action = QAction(QIcon.fromTheme("document-save"), "&Save", self)
        self.save_as_action = QAction(QIcon.fromTheme("document-save-as"), "Save &As...", self)
        self.exit_action = QAction("E&xit", self)

        # 编辑操作
        self.run_action = QAction(QIcon.fromTheme("system-run"), "&Run", self)
        self.stop_action = QAction(QIcon.fromTheme("process-stop"), "S&top", self)

        # 绑定信号
        self.new_action.triggered.connect(self.new_file)
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_as_file)
        self.exit_action.triggered.connect(self.close)
        self.run_action.triggered.connect(self.run_code)
        self.stop_action.triggered.connect(self.stop_process)

    def create_menus(self):
        # 文件菜单
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # 运行菜单
        run_menu = self.menuBar().addMenu("&Run")
        run_menu.addAction(self.run_action)
        run_menu.addAction(self.stop_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.run_action)
        toolbar.addAction(self.stop_action)

    def create_statusbar(self):
        self.status = self.statusBar()
        self.cursor_label = QLabel("Line: 1 | Column: 1")
        self.status.addPermanentWidget(self.cursor_label)
        self.editor.cursorPositionChanged.connect(self.update_cursor_position)

    def setup_dock_widgets(self):
        # 文件树
        self.file_tree = QTreeWidget()
        self.file_tree_dock = QDockWidget("Project", self)
        self.file_tree_dock.setWidget(self.file_tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.file_tree_dock)

    def init_connections(self):
        self.auto_save_timer.timeout.connect(self.auto_save)
        self.auto_save_timer.start(30000)  # 30秒自动保存

    def auto_save(self):
        if self.editor.text():
            with open("autosave.py", "w") as f:
                f.write(self.editor.text())

    def update_cursor_position(self, line, index):
        self.cursor_label.setText(f"Line: {line+1} | Column: {index+1}")

    def run_code(self):
        if self.process and self.process.state() == QProcess.Running:
            return

        self.console.clear()
        code = self.editor.text()

        if not code.strip():
            return

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)
        self.process.finished.connect(self.process_finished)

        if self.current_file:
            self.process.start(sys.executable, [self.current_file])
        else:
            with open("temp_runner.py", "w") as f:
                f.write(code)
            self.process.start(sys.executable, ["temp_runner.py"])

    def stop_process(self):
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.console.appendPlainText("\n[Process stopped by user]")

    def read_output(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.console.appendPlainText(data)

    def read_error(self):
        error = self.process.readAllStandardError().data().decode()
        self.console.appendPlainText(f"\n[Error]\n{error}")

    def process_finished(self):
        self.console.appendPlainText(f"\n[Process exited with code {self.process.exitCode()}]")
        if os.path.exists("temp_runner.py"):
            os.remove("temp_runner.py")

    def new_file(self):
        self.editor.clear()
        self.current_file = None

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Python File", "", "Python Files (*.py)")
        if path:
            with open(path, "r") as f:
                self.editor.setText(f.read())
            self.current_file = path
            self.update_title()

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as f:
                f.write(self.editor.text())
        else:
            self.save_as_file()

    def save_as_file(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py)")
        if path:
            with open(path, "w") as f:
                f.write(self.editor.text())
            self.current_file = path
            self.update_title()

    def update_title(self):
        name = os.path.basename(self.current_file) if self.current_file else "Untitled"
        self.setWindowTitle(f"{name} - PyIDE Pro")

    def closeEvent(self, event):
        if self.process and self.process.state() == QProcess.Running:
            self.stop_process()
            event.ignore()
        else:
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 设置暗色主题
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)

    ide = PythonIDE()
    ide.show()
    sys.exit(app.exec_())



