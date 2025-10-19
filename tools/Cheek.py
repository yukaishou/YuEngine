import sys


def check_compilation_status():
    """检查编译状态"""
    status = {
        'is_frozen': getattr(sys, 'frozen', False),
        'is_compiled': hasattr(sys, '_MEIPASS'),  # PyInstaller
        'has_compiled_attr': hasattr(sys, '__compiled__'),
    }

    # 检查常见打包工具的特征
    if hasattr(sys, 'frozen'):
        status['packager'] = 'PyInstaller/cx_Freeze/py2exe'
    if hasattr(sys, '_MEIPASS'):
        status['packager'] = 'PyInstaller'
    if hasattr(sys, 'frozen') and not hasattr(sys, '_MEIPASS'):
        status['packager'] = 'cx_Freeze or py2exe'

    return status
