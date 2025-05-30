import sys
from PySide6 import QtWidgets
from base.CODApivot_bend import MainWindow
from base.CODApivot_v0 import Ui_MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()