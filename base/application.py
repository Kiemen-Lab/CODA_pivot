import sys
from PySide6 import QtWidgets
from base.CODApivot_bend import MainWindow

def CODApivot():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())