# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CODApivot_v0.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFrame, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(842, 722)
        MainWindow.setStyleSheet(u"QWidget { \n"
"	background-color: #323232;\n"
"}\n"
"\n"
"QMainWindow{\n"
"	background-color: #323232;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    background-color: transparent; /* Transparent background for each menu item */\n"
"    color: #ffffff; /* White font color for menu items */\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 10, 841, 701))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet(u"QWidget { \n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    background-color: #414141;\n"
"    color: #e6e6e6;\n"
"    border: 1px solid #2e2e2e; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}\n"
"\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #5a5a5a;\n"
"    border: 1px solid #2e2e2e; /* Border  */\n"
"    color: #e6e6e6;\n"
"	height: 23px;\n"
"	width: 150px;\n"
"}")
        self.tabWidget.setUsesScrollButtons(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.DefineFixedImageFrame = QFrame(self.tab)
        self.DefineFixedImageFrame.setObjectName(u"DefineFixedImageFrame")
        self.DefineFixedImageFrame.setGeometry(QRect(10, 10, 651, 141))
        self.DefineFixedImageFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineFixedImageFrame.setFrameShape(QFrame.StyledPanel)
        self.DefineFixedImageFrame.setFrameShadow(QFrame.Raised)
        self.FixedImageTableHeaderText = QTextEdit(self.DefineFixedImageFrame)
        self.FixedImageTableHeaderText.setObjectName(u"FixedImageTableHeaderText")
        self.FixedImageTableHeaderText.setGeometry(QRect(0, 0, 651, 24))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(True)
        self.FixedImageTableHeaderText.setFont(font1)
        self.FixedImageTableHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.FixedImageTableHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FixedImageTableHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FixedImageTableHeaderText.setReadOnly(True)
        self.chooseFixedImageButton = QPushButton(self.DefineFixedImageFrame)
        self.chooseFixedImageButton.setObjectName(u"chooseFixedImageButton")
        self.chooseFixedImageButton.setGeometry(QRect(534, 35, 41, 31))
        font2 = QFont()
        font2.setBold(True)
        self.chooseFixedImageButton.setFont(font2)
        self.chooseFixedImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #323232;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"	qproperty-icon: url(Folder.jpg); /* Default icon */\n"
"}\n"
" ")
        self.chooseFixedImageButton.setIconSize(QSize(35, 35))
        self.fixedImageTableWidget = QTableWidget(self.DefineFixedImageFrame)
        if (self.fixedImageTableWidget.columnCount() < 3):
            self.fixedImageTableWidget.setColumnCount(3)
        if (self.fixedImageTableWidget.rowCount() < 1):
            self.fixedImageTableWidget.setRowCount(1)
        self.fixedImageTableWidget.setObjectName(u"fixedImageTableWidget")
        self.fixedImageTableWidget.setGeometry(QRect(10, 35, 525, 91))
        self.fixedImageTableWidget.setFont(font1)
        self.fixedImageTableWidget.setStyleSheet(u"QTableView {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; \n"
"    font-weight: bold;\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    border: 0px solid #e6e6e6; /* Border  */\n"
"    gridline-color: #e6e6e6; /* Set the color of the gridlines */\n"
"    background-color: #646464;\n"
"    color: #e6e6e6; \n"
"    font-weight: bold;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QHeaderView {\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    background-color: #646464; /* Background for the entire header area */\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #646464; /* Match the header background */\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    border: 0px solid #e6e6e6; /* Border  */\n"
"    gridline-color: #e6e6e6; /* Set the color of the gridlines */\n"
"}\n"
"\n"
"QTableView::viewport {\n"
"    background-color: #646464; /* Background beneath the last row */\n"
"}\n"
"\n"
"Q"
                        "TableWidget::item:selected {\n"
"    background-color: #666f75; /* background for selected cells */\n"
"   color: #e6e6e6; /* Text color for selected cells */\n"
"}\n"
"\n"
"QTableWidget::item:selected:!active {\n"
"    background-color: #5a5a5a; /* background when table loses focus */\n"
"    color: #e6e6e6; /* Text color */\n"
"}\n"
"\n"
"QTableWidget QLineEdit {\n"
"    background-color: #666f75; /* Background when editing (light orange) */\n"
"    color: #e6e6e6; /* Text color while editing */\n"
"    border: 1px solid #e6e6e6; /* Border for the editor */\n"
"}")
        self.fixedImageTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.fixedImageTableWidget.setRowCount(1)
        self.fixedImageTableWidget.setColumnCount(3)
        self.fixedImageTableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.fixedImageTableWidget.horizontalHeader().setDefaultSectionSize(153)
        self.fixedImageTableWidget.verticalHeader().setVisible(False)
        self.fixedImageTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.fixedImageTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.deleteFixedImageButton = QPushButton(self.DefineFixedImageFrame)
        self.deleteFixedImageButton.setObjectName(u"deleteFixedImageButton")
        self.deleteFixedImageButton.setEnabled(True)
        self.deleteFixedImageButton.setGeometry(QRect(595, 95, 51, 30))
        self.deleteFixedImageButton.setFont(font1)
        self.deleteFixedImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.keepFixedImageButton = QPushButton(self.DefineFixedImageFrame)
        self.keepFixedImageButton.setObjectName(u"keepFixedImageButton")
        self.keepFixedImageButton.setEnabled(True)
        self.keepFixedImageButton.setGeometry(QRect(540, 95, 51, 30))
        self.keepFixedImageButton.setFont(font1)
        self.keepFixedImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.fixedImageTableWidget.raise_()
        self.FixedImageTableHeaderText.raise_()
        self.chooseFixedImageButton.raise_()
        self.deleteFixedImageButton.raise_()
        self.keepFixedImageButton.raise_()
        self.DefineMovingImageFrame = QFrame(self.tab)
        self.DefineMovingImageFrame.setObjectName(u"DefineMovingImageFrame")
        self.DefineMovingImageFrame.setGeometry(QRect(10, 160, 651, 351))
        self.DefineMovingImageFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineMovingImageFrame.setFrameShape(QFrame.StyledPanel)
        self.DefineMovingImageFrame.setFrameShadow(QFrame.Raised)
        self.MovingImageTableHeaderText = QTextEdit(self.DefineMovingImageFrame)
        self.MovingImageTableHeaderText.setObjectName(u"MovingImageTableHeaderText")
        self.MovingImageTableHeaderText.setGeometry(QRect(0, 0, 651, 24))
        self.MovingImageTableHeaderText.setFont(font1)
        self.MovingImageTableHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.MovingImageTableHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MovingImageTableHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MovingImageTableHeaderText.setReadOnly(True)
        self.movingImageTableWidget = QTableWidget(self.DefineMovingImageFrame)
        if (self.movingImageTableWidget.columnCount() < 3):
            self.movingImageTableWidget.setColumnCount(3)
        if (self.movingImageTableWidget.rowCount() < 1):
            self.movingImageTableWidget.setRowCount(1)
        self.movingImageTableWidget.setObjectName(u"movingImageTableWidget")
        self.movingImageTableWidget.setGeometry(QRect(10, 35, 525, 301))
        self.movingImageTableWidget.setFont(font2)
        self.movingImageTableWidget.setStyleSheet(u"QTableView {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; \n"
"    font-weight: bold;\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    border: 0px solid #e6e6e6; /* Border  */\n"
"    gridline-color: #e6e6e6; /* Set the color of the gridlines */\n"
"    background-color: #646464;\n"
"    color: #e6e6e6; \n"
"    font-weight: bold;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QHeaderView {\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    background-color: #646464; /* Background for the entire header area */\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #646464; /* Match the header background */\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    border: 0px solid #e6e6e6; /* Border  */\n"
"    gridline-color: #e6e6e6; /* Set the color of the gridlines */\n"
"}\n"
"\n"
"QTableView::viewport {\n"
"    background-color: #646464; /* Background beneath the last row */\n"
"}\n"
"\n"
"Q"
                        "TableWidget::item:selected {\n"
"    background-color: #666f75; /* background for selected cells */\n"
"   color: #e6e6e6; /* Text color for selected cells */\n"
"}\n"
"\n"
"QTableWidget::item:selected:!active {\n"
"    background-color: #5a5a5a; /* background when table loses focus */\n"
"    color: #e6e6e6; /* Text color */\n"
"}\n"
"\n"
"QTableWidget QLineEdit {\n"
"    background-color: #666f75; /* Background when editing (light orange) */\n"
"    color: #e6e6e6; /* Text color while editing */\n"
"    border: 1px solid #e6e6e6; /* Border for the editor */\n"
"}")
        self.movingImageTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.movingImageTableWidget.setRowCount(1)
        self.movingImageTableWidget.setColumnCount(3)
        self.movingImageTableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.movingImageTableWidget.horizontalHeader().setDefaultSectionSize(153)
        self.movingImageTableWidget.verticalHeader().setVisible(False)
        self.movingImageTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.movingImageTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.chooseMovingImageButton = QPushButton(self.DefineMovingImageFrame)
        self.chooseMovingImageButton.setObjectName(u"chooseMovingImageButton")
        self.chooseMovingImageButton.setGeometry(QRect(534, 35, 41, 31))
        self.chooseMovingImageButton.setFont(font2)
        self.chooseMovingImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #323232;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"	qproperty-icon: url(Folder.jpg); /* Default icon */\n"
"}\n"
" ")
        self.chooseMovingImageButton.setIconSize(QSize(35, 35))
        self.deleteMovingImageButton = QPushButton(self.DefineMovingImageFrame)
        self.deleteMovingImageButton.setObjectName(u"deleteMovingImageButton")
        self.deleteMovingImageButton.setGeometry(QRect(595, 305, 50, 30))
        self.deleteMovingImageButton.setFont(font1)
        self.deleteMovingImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.keepMovingImageButton = QPushButton(self.DefineMovingImageFrame)
        self.keepMovingImageButton.setObjectName(u"keepMovingImageButton")
        self.keepMovingImageButton.setEnabled(True)
        self.keepMovingImageButton.setGeometry(QRect(540, 305, 50, 30))
        self.keepMovingImageButton.setFont(font1)
        self.keepMovingImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.SetJobFolderFrame = QFrame(self.tab)
        self.SetJobFolderFrame.setObjectName(u"SetJobFolderFrame")
        self.SetJobFolderFrame.setGeometry(QRect(10, 520, 651, 131))
        self.SetJobFolderFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.SetJobFolderFrame.setFrameShape(QFrame.StyledPanel)
        self.SetJobFolderFrame.setFrameShadow(QFrame.Raised)
        self.JobFolderTableHeaderText = QTextEdit(self.SetJobFolderFrame)
        self.JobFolderTableHeaderText.setObjectName(u"JobFolderTableHeaderText")
        self.JobFolderTableHeaderText.setGeometry(QRect(0, 0, 651, 24))
        self.JobFolderTableHeaderText.setFont(font1)
        self.JobFolderTableHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.JobFolderTableHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.JobFolderTableHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.JobFolderTableHeaderText.setReadOnly(True)
        self.JobFolderCheckBox = QCheckBox(self.SetJobFolderFrame)
        self.JobFolderCheckBox.setObjectName(u"JobFolderCheckBox")
        self.JobFolderCheckBox.setGeometry(QRect(545, 80, 101, 41))
        font3 = QFont()
        font3.setPointSize(8)
        font3.setBold(True)
        self.JobFolderCheckBox.setFont(font3)
        self.JobFolderCheckBox.setStyleSheet(u"QCheckBox {\n"
"    background-color: #4b4b4b;\n"
"    color: #e6e6e6; /* Text color */\n"
"    padding: 2px; /* Optional: space around the text */\n"
"	width: 100px; /* Optional: Adjust width to allow for wrapping */\n"
"    word-wrap: break-word; /* Enable word wrap */\n"
"}\n"
"")
        self.setJobTableWidget = QTableWidget(self.SetJobFolderFrame)
        if (self.setJobTableWidget.columnCount() < 2):
            self.setJobTableWidget.setColumnCount(2)
        if (self.setJobTableWidget.rowCount() < 1):
            self.setJobTableWidget.setRowCount(1)
        self.setJobTableWidget.setObjectName(u"setJobTableWidget")
        self.setJobTableWidget.setGeometry(QRect(10, 35, 525, 81))
        self.setJobTableWidget.setStyleSheet(u"QTableView {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; \n"
"    font-weight: bold;\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    border: 0px solid #e6e6e6; /* Border  */\n"
"    gridline-color: #e6e6e6; /* Set the color of the gridlines */\n"
"    background-color: #646464;\n"
"    color: #e6e6e6; \n"
"    font-weight: bold;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QHeaderView {\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    background-color: #646464; /* Background for the entire header area */\n"
"}\n"
"\n"
"QTableCornerButton::section {\n"
"    background-color: #646464; /* Match the header background */\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    border: 0px solid #e6e6e6; /* Border  */\n"
"    gridline-color: #e6e6e6; /* Set the color of the gridlines */\n"
"}\n"
"\n"
"QTableView::viewport {\n"
"    background-color: #646464; /* Background beneath the last row */\n"
"}\n"
"\n"
"Q"
                        "TableWidget::item:selected {\n"
"    background-color: #666f75; /* background for selected cells */\n"
"   color: #e6e6e6; /* Text color for selected cells */\n"
"}\n"
"\n"
"QTableWidget::item:selected:!active {\n"
"    background-color: #5a5a5a; /* background when table loses focus */\n"
"    color: #e6e6e6; /* Text color */\n"
"}\n"
"\n"
"QTableWidget QLineEdit {\n"
"    background-color: #666f75; /* Background when editing (light orange) */\n"
"    color: #e6e6e6; /* Text color while editing */\n"
"    border: 1px solid #e6e6e6; /* Border for the editor */\n"
"}")
        self.setJobTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setJobTableWidget.setRowCount(1)
        self.setJobTableWidget.setColumnCount(2)
        self.setJobTableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.setJobTableWidget.horizontalHeader().setDefaultSectionSize(229)
        self.setJobTableWidget.verticalHeader().setVisible(False)
        self.setJobTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.setJobTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.chooseJobFolderButton = QPushButton(self.SetJobFolderFrame)
        self.chooseJobFolderButton.setObjectName(u"chooseJobFolderButton")
        self.chooseJobFolderButton.setGeometry(QRect(534, 35, 41, 31))
        self.chooseJobFolderButton.setFont(font2)
        self.chooseJobFolderButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #323232;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"	qproperty-icon: url(Folder.jpg); /* Default icon */\n"
"}\n"
" ")
        self.chooseJobFolderButton.setIconSize(QSize(35, 35))
        self.JobFolderCheckBox.raise_()
        self.JobFolderTableHeaderText.raise_()
        self.setJobTableWidget.raise_()
        self.chooseJobFolderButton.raise_()
        self.loadTemplateButton = QPushButton(self.tab)
        self.loadTemplateButton.setObjectName(u"loadTemplateButton")
        self.loadTemplateButton.setGeometry(QRect(670, 10, 161, 30))
        self.loadTemplateButton.setFont(font1)
        self.loadTemplateButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.goToApplyRegistrationTabButton = QPushButton(self.tab)
        self.goToApplyRegistrationTabButton.setObjectName(u"goToApplyRegistrationTabButton")
        self.goToApplyRegistrationTabButton.setGeometry(QRect(670, 80, 161, 30))
        self.goToApplyRegistrationTabButton.setFont(font1)
        self.goToApplyRegistrationTabButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.goToFiducialPointTabButton = QPushButton(self.tab)
        self.goToFiducialPointTabButton.setObjectName(u"goToFiducialPointTabButton")
        self.goToFiducialPointTabButton.setGeometry(QRect(670, 45, 161, 30))
        self.goToFiducialPointTabButton.setFont(font1)
        self.goToFiducialPointTabButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.ChooseMovingImageFrame = QFrame(self.tab_3)
        self.ChooseMovingImageFrame.setObjectName(u"ChooseMovingImageFrame")
        self.ChooseMovingImageFrame.setGeometry(QRect(290, 10, 521, 84))
        self.ChooseMovingImageFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ChooseMovingImageFrame.setFrameShape(QFrame.StyledPanel)
        self.ChooseMovingImageFrame.setFrameShadow(QFrame.Raised)
        self.LoadNewMovingImageButton = QPushButton(self.ChooseMovingImageFrame)
        self.LoadNewMovingImageButton.setObjectName(u"LoadNewMovingImageButton")
        self.LoadNewMovingImageButton.setGeometry(QRect(420, 10, 91, 30))
        self.LoadNewMovingImageButton.setFont(font1)
        self.LoadNewMovingImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.LoadOldMovingImageButton = QPushButton(self.ChooseMovingImageFrame)
        self.LoadOldMovingImageButton.setObjectName(u"LoadOldMovingImageButton")
        self.LoadOldMovingImageButton.setGeometry(QRect(420, 46, 91, 30))
        self.LoadOldMovingImageButton.setFont(font1)
        self.LoadOldMovingImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.MovingImagesComboBox = QComboBox(self.ChooseMovingImageFrame)
        self.MovingImagesComboBox.setObjectName(u"MovingImagesComboBox")
        self.MovingImagesComboBox.setGeometry(QRect(250, 12, 151, 25))
        font4 = QFont()
        font4.setPointSize(10)
        self.MovingImagesComboBox.setFont(font4)
        self.MovingImagesComboBox.setStyleSheet(u"QComboBox {\n"
"    background-color: #707070; /* Light gray background color */\n"
"    color: #e6e6e6; /* Dark gray font color */\n"
"    padding: 5px; /* Optional: adds padding inside the combobox */\n"
"    border: 1px solid #555555; /* Optional: border color */\n"
"    border-radius: 5px; /* Optional: rounded corners */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView { /* Styles for dropdown list */\n"
"    background-color: #707070; /* Dropdown background color */\n"
"    color: #e6e6e6; /* Dropdown font color */\n"
"    selection-background-color: #cce5ff; /* Background color when an item is selected */\n"
"    selection-color: #e6e6e6; /* Font color of selected item */\n"
"}\n"
"\n"
"")
        self.textEdit_5 = QTextEdit(self.ChooseMovingImageFrame)
        self.textEdit_5.setObjectName(u"textEdit_5")
        self.textEdit_5.setGeometry(QRect(70, 13, 171, 27))
        font5 = QFont()
        font5.setPointSize(9)
        self.textEdit_5.setFont(font5)
        self.textEdit_5.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.textEdit_5.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_5.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_5.setReadOnly(True)
        self.textEdit_6 = QTextEdit(self.ChooseMovingImageFrame)
        self.textEdit_6.setObjectName(u"textEdit_6")
        self.textEdit_6.setGeometry(QRect(4, 49, 241, 27))
        self.textEdit_6.setFont(font5)
        self.textEdit_6.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.textEdit_6.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_6.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_6.setReadOnly(True)
        self.OldMovingImagesComboBox = QComboBox(self.ChooseMovingImageFrame)
        self.OldMovingImagesComboBox.setObjectName(u"OldMovingImagesComboBox")
        self.OldMovingImagesComboBox.setGeometry(QRect(250, 48, 151, 25))
        self.OldMovingImagesComboBox.setFont(font4)
        self.OldMovingImagesComboBox.setStyleSheet(u"QComboBox {\n"
"    background-color: #707070; /* Light gray background color */\n"
"    color: #e6e6e6; /* Dark gray font color */\n"
"    padding: 5px; /* Optional: adds padding inside the combobox */\n"
"    border: 1px solid #555555; /* Optional: border color */\n"
"    border-radius: 5px; /* Optional: rounded corners */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView { /* Styles for dropdown list */\n"
"    background-color: #707070; /* Dropdown background color */\n"
"    color: #e6e6e6; /* Dropdown font color */\n"
"    selection-background-color: #cce5ff; /* Background color when an item is selected */\n"
"    selection-color: #e6e6e6; /* Font color of selected item */\n"
"}\n"
"\n"
"")
        self.PickNewMovingImageButton = QPushButton(self.ChooseMovingImageFrame)
        self.PickNewMovingImageButton.setObjectName(u"PickNewMovingImageButton")
        self.PickNewMovingImageButton.setGeometry(QRect(350, 0, 171, 30))
        self.PickNewMovingImageButton.setFont(font1)
        self.PickNewMovingImageButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.FiducialPointControlsFrame = QFrame(self.tab_3)
        self.FiducialPointControlsFrame.setObjectName(u"FiducialPointControlsFrame")
        self.FiducialPointControlsFrame.setGeometry(QRect(422, 500, 401, 111))
        self.FiducialPointControlsFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.FiducialPointControlsFrame.setFrameShape(QFrame.StyledPanel)
        self.FiducialPointControlsFrame.setFrameShadow(QFrame.Raised)
        self.FiducialFrameHeaderText = QTextEdit(self.FiducialPointControlsFrame)
        self.FiducialFrameHeaderText.setObjectName(u"FiducialFrameHeaderText")
        self.FiducialFrameHeaderText.setGeometry(QRect(0, 0, 401, 24))
        self.FiducialFrameHeaderText.setFont(font)
        self.FiducialFrameHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.FiducialFrameHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FiducialFrameHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FiducialFrameHeaderText.setReadOnly(True)
        self.AddFiducialButton = QPushButton(self.FiducialPointControlsFrame)
        self.AddFiducialButton.setObjectName(u"AddFiducialButton")
        self.AddFiducialButton.setGeometry(QRect(10, 35, 85, 30))
        self.AddFiducialButton.setFont(font1)
        self.AddFiducialButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.ColorFiducialButton = QPushButton(self.FiducialPointControlsFrame)
        self.ColorFiducialButton.setObjectName(u"ColorFiducialButton")
        self.ColorFiducialButton.setGeometry(QRect(10, 70, 85, 30))
        self.ColorFiducialButton.setFont(font1)
        self.ColorFiducialButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.ShrinkFiducialButton = QPushButton(self.FiducialPointControlsFrame)
        self.ShrinkFiducialButton.setObjectName(u"ShrinkFiducialButton")
        self.ShrinkFiducialButton.setGeometry(QRect(135, 73, 30, 25))
        font6 = QFont()
        font6.setPointSize(12)
        font6.setBold(True)
        self.ShrinkFiducialButton.setFont(font6)
        self.ShrinkFiducialButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.GrowFiducialButton = QPushButton(self.FiducialPointControlsFrame)
        self.GrowFiducialButton.setObjectName(u"GrowFiducialButton")
        self.GrowFiducialButton.setGeometry(QRect(170, 73, 30, 25))
        self.GrowFiducialButton.setFont(font6)
        self.GrowFiducialButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.FiducialSizeText = QTextEdit(self.FiducialPointControlsFrame)
        self.FiducialSizeText.setObjectName(u"FiducialSizeText")
        self.FiducialSizeText.setGeometry(QRect(93, 73, 41, 24))
        self.FiducialSizeText.setFont(font4)
        self.FiducialSizeText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.FiducialSizeText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FiducialSizeText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FiducialSizeText.setReadOnly(True)
        self.DeleteFromFixedButton = QPushButton(self.FiducialPointControlsFrame)
        self.DeleteFromFixedButton.setObjectName(u"DeleteFromFixedButton")
        self.DeleteFromFixedButton.setGeometry(QRect(305, 35, 85, 30))
        self.DeleteFromFixedButton.setFont(font1)
        self.DeleteFromFixedButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.DeleteAllButton = QPushButton(self.FiducialPointControlsFrame)
        self.DeleteAllButton.setObjectName(u"DeleteAllButton")
        self.DeleteAllButton.setGeometry(QRect(305, 70, 85, 30))
        self.DeleteAllButton.setFont(font1)
        self.DeleteAllButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.FiducialFrameHeaderText.raise_()
        self.AddFiducialButton.raise_()
        self.GrowFiducialButton.raise_()
        self.FiducialSizeText.raise_()
        self.ShrinkFiducialButton.raise_()
        self.DeleteFromFixedButton.raise_()
        self.DeleteAllButton.raise_()
        self.ColorFiducialButton.raise_()
        self.FixedImageDisplayFrame = QFrame(self.tab_3)
        self.FixedImageDisplayFrame.setObjectName(u"FixedImageDisplayFrame")
        self.FixedImageDisplayFrame.setGeometry(QRect(10, 125, 400, 350))
        self.FixedImageDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.FixedImageDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.FixedImageDisplayFrame.setFrameShadow(QFrame.Raised)
        self.MovingImageDisplayFrame = QFrame(self.tab_3)
        self.MovingImageDisplayFrame.setObjectName(u"MovingImageDisplayFrame")
        self.MovingImageDisplayFrame.setGeometry(QRect(422, 125, 400, 350))
        self.MovingImageDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.MovingImageDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.MovingImageDisplayFrame.setFrameShadow(QFrame.Raised)
        self.ImageViewControlsFrame = QFrame(self.tab_3)
        self.ImageViewControlsFrame.setObjectName(u"ImageViewControlsFrame")
        self.ImageViewControlsFrame.setGeometry(QRect(10, 500, 401, 111))
        self.ImageViewControlsFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ImageViewControlsFrame.setFrameShape(QFrame.StyledPanel)
        self.ImageViewControlsFrame.setFrameShadow(QFrame.Raised)
        self.ImageViewFrameHeaderText = QTextEdit(self.ImageViewControlsFrame)
        self.ImageViewFrameHeaderText.setObjectName(u"ImageViewFrameHeaderText")
        self.ImageViewFrameHeaderText.setGeometry(QRect(0, 0, 401, 24))
        self.ImageViewFrameHeaderText.setFont(font)
        self.ImageViewFrameHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ImageViewFrameHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ImageViewFrameHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ImageViewFrameHeaderText.setReadOnly(True)
        self.ZoomPanButton = QPushButton(self.ImageViewControlsFrame)
        self.ZoomPanButton.setObjectName(u"ZoomPanButton")
        self.ZoomPanButton.setGeometry(QRect(10, 35, 85, 30))
        self.ZoomPanButton.setFont(font1)
        self.ZoomPanButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.RotateButton = QPushButton(self.ImageViewControlsFrame)
        self.RotateButton.setObjectName(u"RotateButton")
        self.RotateButton.setGeometry(QRect(100, 35, 85, 30))
        self.RotateButton.setFont(font1)
        self.RotateButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.RevertButton = QPushButton(self.ImageViewControlsFrame)
        self.RevertButton.setObjectName(u"RevertButton")
        self.RevertButton.setGeometry(QRect(100, 70, 85, 30))
        self.RevertButton.setFont(font1)
        self.RevertButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.FlipButton = QPushButton(self.ImageViewControlsFrame)
        self.FlipButton.setObjectName(u"FlipButton")
        self.FlipButton.setGeometry(QRect(10, 70, 85, 30))
        self.FlipButton.setFont(font1)
        self.FlipButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.brightnessDownButton = QPushButton(self.ImageViewControlsFrame)
        self.brightnessDownButton.setObjectName(u"brightnessDownButton")
        self.brightnessDownButton.setGeometry(QRect(348, 34, 21, 25))
        self.brightnessDownButton.setFont(font1)
        self.brightnessDownButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.brightnessUpButton = QPushButton(self.ImageViewControlsFrame)
        self.brightnessUpButton.setObjectName(u"brightnessUpButton")
        self.brightnessUpButton.setGeometry(QRect(373, 34, 21, 25))
        self.brightnessUpButton.setFont(font1)
        self.brightnessUpButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.contrastDownButton = QPushButton(self.ImageViewControlsFrame)
        self.contrastDownButton.setObjectName(u"contrastDownButton")
        self.contrastDownButton.setGeometry(QRect(348, 74, 21, 25))
        self.contrastDownButton.setFont(font1)
        self.contrastDownButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.contrastUpButton = QPushButton(self.ImageViewControlsFrame)
        self.contrastUpButton.setObjectName(u"contrastUpButton")
        self.contrastUpButton.setGeometry(QRect(373, 74, 21, 25))
        self.contrastUpButton.setFont(font1)
        self.contrastUpButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.ContrastImage = QPushButton(self.ImageViewControlsFrame)
        self.ContrastImage.setObjectName(u"ContrastImage")
        self.ContrastImage.setGeometry(QRect(310, 70, 35, 35))
        self.ContrastImage.setFont(font2)
        self.ContrastImage.setStyleSheet(u"QPushButton {\n"
"    background-color: #4b4b4b;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        icon = QIcon()
        icon.addFile(u"Contrast.jpg", QSize(), QIcon.Normal, QIcon.Off)
        self.ContrastImage.setIcon(icon)
        self.ContrastImage.setIconSize(QSize(35, 35))
        self.BrightnessImage = QPushButton(self.ImageViewControlsFrame)
        self.BrightnessImage.setObjectName(u"BrightnessImage")
        self.BrightnessImage.setGeometry(QRect(310, 30, 35, 35))
        self.BrightnessImage.setFont(font2)
        self.BrightnessImage.setStyleSheet(u"QPushButton {\n"
"    background-color: #4b4b4b;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u"Brightness.jpg", QSize(), QIcon.Normal, QIcon.Off)
        self.BrightnessImage.setIcon(icon1)
        self.BrightnessImage.setIconSize(QSize(33, 33))
        self.CalculatingICPText = QTextEdit(self.tab_3)
        self.CalculatingICPText.setObjectName(u"CalculatingICPText")
        self.CalculatingICPText.setGeometry(QRect(10, 640, 341, 24))
        self.CalculatingICPText.setFont(font5)
        self.CalculatingICPText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.CalculatingICPText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CalculatingICPText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.moving_image_border = QLabel(self.tab_3)
        self.moving_image_border.setObjectName(u"moving_image_border")
        self.moving_image_border.setGeometry(QRect(420, 123, 404, 354))
        self.moving_image_border.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 3px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.FixedImageFrameHeaderText = QLabel(self.tab_3)
        self.FixedImageFrameHeaderText.setObjectName(u"FixedImageFrameHeaderText")
        self.FixedImageFrameHeaderText.setGeometry(QRect(10, 97, 400, 24))
        font7 = QFont()
        font7.setPointSize(11)
        font7.setBold(True)
        self.FixedImageFrameHeaderText.setFont(font7)
        self.FixedImageFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.MovingImageFrameHeaderText = QLabel(self.tab_3)
        self.MovingImageFrameHeaderText.setObjectName(u"MovingImageFrameHeaderText")
        self.MovingImageFrameHeaderText.setGeometry(QRect(422, 97, 400, 24))
        self.MovingImageFrameHeaderText.setFont(font7)
        self.MovingImageFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.fixed_image_border = QLabel(self.tab_3)
        self.fixed_image_border.setObjectName(u"fixed_image_border")
        self.fixed_image_border.setGeometry(QRect(8, 123, 404, 354))
        self.fixed_image_border.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 3px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.tabWidget.addTab(self.tab_3, "")
        self.fixed_image_border.raise_()
        self.moving_image_border.raise_()
        self.ChooseMovingImageFrame.raise_()
        self.FiducialPointControlsFrame.raise_()
        self.FixedImageDisplayFrame.raise_()
        self.MovingImageDisplayFrame.raise_()
        self.ImageViewControlsFrame.raise_()
        self.CalculatingICPText.raise_()
        self.FixedImageFrameHeaderText.raise_()
        self.MovingImageFrameHeaderText.raise_()
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.DefineFixedImageFrame_10 = QFrame(self.tab_2)
        self.DefineFixedImageFrame_10.setObjectName(u"DefineFixedImageFrame_10")
        self.DefineFixedImageFrame_10.setGeometry(QRect(10, 420, 371, 151))
        self.DefineFixedImageFrame_10.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineFixedImageFrame_10.setFrameShape(QFrame.StyledPanel)
        self.DefineFixedImageFrame_10.setFrameShadow(QFrame.Raised)
        self.textEdit_17 = QTextEdit(self.DefineFixedImageFrame_10)
        self.textEdit_17.setObjectName(u"textEdit_17")
        self.textEdit_17.setGeometry(QRect(0, 0, 371, 24))
        self.textEdit_17.setFont(font1)
        self.textEdit_17.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.textEdit_17.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_17.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_17.setReadOnly(True)
        self.pushButton_22 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_22.setObjectName(u"pushButton_22")
        self.pushButton_22.setGeometry(QRect(10, 70, 71, 30))
        self.pushButton_22.setFont(font2)
        self.pushButton_22.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_27 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_27.setObjectName(u"pushButton_27")
        self.pushButton_27.setGeometry(QRect(85, 70, 71, 30))
        self.pushButton_27.setFont(font2)
        self.pushButton_27.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_28 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_28.setObjectName(u"pushButton_28")
        self.pushButton_28.setGeometry(QRect(160, 70, 71, 30))
        self.pushButton_28.setFont(font2)
        self.pushButton_28.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_30 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_30.setObjectName(u"pushButton_30")
        self.pushButton_30.setGeometry(QRect(85, 105, 71, 30))
        self.pushButton_30.setFont(font2)
        self.pushButton_30.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_31 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_31.setObjectName(u"pushButton_31")
        self.pushButton_31.setGeometry(QRect(160, 105, 71, 30))
        self.pushButton_31.setFont(font2)
        self.pushButton_31.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_32 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_32.setObjectName(u"pushButton_32")
        self.pushButton_32.setGeometry(QRect(10, 105, 71, 30))
        self.pushButton_32.setFont(font2)
        self.pushButton_32.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_33 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_33.setObjectName(u"pushButton_33")
        self.pushButton_33.setGeometry(QRect(305, 70, 21, 25))
        self.pushButton_33.setFont(font2)
        self.pushButton_33.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_34 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_34.setObjectName(u"pushButton_34")
        self.pushButton_34.setGeometry(QRect(330, 70, 21, 25))
        self.pushButton_34.setFont(font2)
        self.pushButton_34.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_35 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_35.setObjectName(u"pushButton_35")
        self.pushButton_35.setGeometry(QRect(305, 110, 21, 25))
        self.pushButton_35.setFont(font2)
        self.pushButton_35.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_36 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_36.setObjectName(u"pushButton_36")
        self.pushButton_36.setGeometry(QRect(330, 110, 21, 25))
        self.pushButton_36.setFont(font2)
        self.pushButton_36.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_14 = QPushButton(self.DefineFixedImageFrame_10)
        self.pushButton_14.setObjectName(u"pushButton_14")
        self.pushButton_14.setGeometry(QRect(260, 63, 40, 40))
        self.pushButton_14.setFont(font2)
        self.pushButton_14.setStyleSheet(u"QPushButton {\n"
"    background-color: #4b4b4b;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u"../../../../.designer/backup/Brightness.jpg", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_14.setIcon(icon2)
        self.pushButton_14.setIconSize(QSize(40, 40))
        self.DefineFixedImageFrame_11 = QFrame(self.tab_2)
        self.DefineFixedImageFrame_11.setObjectName(u"DefineFixedImageFrame_11")
        self.DefineFixedImageFrame_11.setGeometry(QRect(390, 100, 371, 311))
        self.DefineFixedImageFrame_11.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineFixedImageFrame_11.setFrameShape(QFrame.StyledPanel)
        self.DefineFixedImageFrame_11.setFrameShadow(QFrame.Raised)
        self.textEdit_21 = QTextEdit(self.DefineFixedImageFrame_11)
        self.textEdit_21.setObjectName(u"textEdit_21")
        self.textEdit_21.setGeometry(QRect(0, 0, 371, 24))
        self.textEdit_21.setFont(font1)
        self.textEdit_21.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.textEdit_21.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_21.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.DefineFixedImageFrame_12 = QFrame(self.tab_2)
        self.DefineFixedImageFrame_12.setObjectName(u"DefineFixedImageFrame_12")
        self.DefineFixedImageFrame_12.setGeometry(QRect(390, 420, 371, 71))
        self.DefineFixedImageFrame_12.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineFixedImageFrame_12.setFrameShape(QFrame.StyledPanel)
        self.DefineFixedImageFrame_12.setFrameShadow(QFrame.Raised)
        self.textEdit_22 = QTextEdit(self.DefineFixedImageFrame_12)
        self.textEdit_22.setObjectName(u"textEdit_22")
        self.textEdit_22.setGeometry(QRect(0, 0, 371, 24))
        self.textEdit_22.setFont(font1)
        self.textEdit_22.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.textEdit_22.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_22.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_22.setReadOnly(True)
        self.pushButton_37 = QPushButton(self.DefineFixedImageFrame_12)
        self.pushButton_37.setObjectName(u"pushButton_37")
        self.pushButton_37.setGeometry(QRect(10, 33, 141, 30))
        self.pushButton_37.setFont(font2)
        self.pushButton_37.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_38 = QPushButton(self.DefineFixedImageFrame_12)
        self.pushButton_38.setObjectName(u"pushButton_38")
        self.pushButton_38.setGeometry(QRect(155, 33, 141, 30))
        self.pushButton_38.setFont(font2)
        self.pushButton_38.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.DefineFixedImageFrame_13 = QFrame(self.tab_2)
        self.DefineFixedImageFrame_13.setObjectName(u"DefineFixedImageFrame_13")
        self.DefineFixedImageFrame_13.setGeometry(QRect(390, 500, 371, 71))
        self.DefineFixedImageFrame_13.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineFixedImageFrame_13.setFrameShape(QFrame.StyledPanel)
        self.DefineFixedImageFrame_13.setFrameShadow(QFrame.Raised)
        self.textEdit_24 = QTextEdit(self.DefineFixedImageFrame_13)
        self.textEdit_24.setObjectName(u"textEdit_24")
        self.textEdit_24.setGeometry(QRect(0, 0, 371, 24))
        self.textEdit_24.setFont(font1)
        self.textEdit_24.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.textEdit_24.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_24.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_24.setReadOnly(True)
        self.pushButton_42 = QPushButton(self.DefineFixedImageFrame_13)
        self.pushButton_42.setObjectName(u"pushButton_42")
        self.pushButton_42.setGeometry(QRect(10, 33, 111, 30))
        self.pushButton_42.setFont(font2)
        self.pushButton_42.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_43 = QPushButton(self.DefineFixedImageFrame_13)
        self.pushButton_43.setObjectName(u"pushButton_43")
        self.pushButton_43.setGeometry(QRect(125, 33, 111, 30))
        self.pushButton_43.setFont(font2)
        self.pushButton_43.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.pushButton_44 = QPushButton(self.DefineFixedImageFrame_13)
        self.pushButton_44.setObjectName(u"pushButton_44")
        self.pushButton_44.setGeometry(QRect(240, 33, 111, 30))
        self.pushButton_44.setFont(font2)
        self.pushButton_44.setStyleSheet(u"QPushButton {\n"
"    background-color: #5a5a5a;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #666f75; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #7b8e9c; /* More blue when pressed */\n"
"}")
        self.DefineFixedImageFrame_14 = QFrame(self.tab_2)
        self.DefineFixedImageFrame_14.setObjectName(u"DefineFixedImageFrame_14")
        self.DefineFixedImageFrame_14.setGeometry(QRect(10, 100, 371, 311))
        self.DefineFixedImageFrame_14.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineFixedImageFrame_14.setFrameShape(QFrame.StyledPanel)
        self.DefineFixedImageFrame_14.setFrameShadow(QFrame.Raised)
        self.textEdit_26 = QTextEdit(self.DefineFixedImageFrame_14)
        self.textEdit_26.setObjectName(u"textEdit_26")
        self.textEdit_26.setGeometry(QRect(0, 0, 371, 24))
        self.textEdit_26.setFont(font1)
        self.textEdit_26.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.textEdit_26.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_26.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.DefineFixedImageFrame_16 = QFrame(self.tab_2)
        self.DefineFixedImageFrame_16.setObjectName(u"DefineFixedImageFrame_16")
        self.DefineFixedImageFrame_16.setGeometry(QRect(10, 10, 231, 81))
        self.DefineFixedImageFrame_16.setStyleSheet(u"QFrame { \n"
"	background-color: #323232;\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.DefineFixedImageFrame_16.setFrameShape(QFrame.StyledPanel)
        self.DefineFixedImageFrame_16.setFrameShadow(QFrame.Raised)
        self.textEdit_29 = QTextEdit(self.DefineFixedImageFrame_16)
        self.textEdit_29.setObjectName(u"textEdit_29")
        self.textEdit_29.setGeometry(QRect(2, 5, 201, 24))
        self.textEdit_29.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.textEdit_29.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_29.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_29.setReadOnly(True)
        self.textEdit_30 = QTextEdit(self.DefineFixedImageFrame_16)
        self.textEdit_30.setObjectName(u"textEdit_30")
        self.textEdit_30.setGeometry(QRect(2, 28, 201, 24))
        self.textEdit_30.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.textEdit_30.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_30.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_30.setReadOnly(True)
        self.textEdit_31 = QTextEdit(self.DefineFixedImageFrame_16)
        self.textEdit_31.setObjectName(u"textEdit_31")
        self.textEdit_31.setGeometry(QRect(2, 51, 201, 24))
        self.textEdit_31.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.textEdit_31.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_31.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_31.setReadOnly(True)
        self.textEdit_32 = QTextEdit(self.tab_2)
        self.textEdit_32.setObjectName(u"textEdit_32")
        self.textEdit_32.setGeometry(QRect(10, 575, 321, 24))
        self.textEdit_32.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.textEdit_32.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_32.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit_32.setReadOnly(True)
        self.tabWidget.addTab(self.tab_2, "")
        self.DefineFixedImageFrame_16.raise_()
        self.DefineFixedImageFrame_10.raise_()
        self.DefineFixedImageFrame_11.raise_()
        self.DefineFixedImageFrame_12.raise_()
        self.DefineFixedImageFrame_13.raise_()
        self.DefineFixedImageFrame_14.raise_()
        self.textEdit_32.raise_()
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.FixedImageTableHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Define Fixed Image</span></p></body></html>", None))
        self.chooseFixedImageButton.setText("")
        self.deleteFixedImageButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.keepFixedImageButton.setText(QCoreApplication.translate("MainWindow", u"Keep", None))
        self.MovingImageTableHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Define Moving Image(s)</p></body></html>", None))
        self.chooseMovingImageButton.setText("")
        self.deleteMovingImageButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.keepMovingImageButton.setText(QCoreApplication.translate("MainWindow", u"Keep", None))
        self.JobFolderTableHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Set Job Folder (where to save results)</p></body></html>", None))
        self.JobFolderCheckBox.setText(QCoreApplication.translate("MainWindow", u"Use Fixed \n"
"Image Folder", None))
        self.chooseJobFolderButton.setText("")
        self.loadTemplateButton.setText(QCoreApplication.translate("MainWindow", u"Load Template", None))
        self.goToApplyRegistrationTabButton.setText(QCoreApplication.translate("MainWindow", u"Apply Registration", None))
        self.goToFiducialPointTabButton.setText(QCoreApplication.translate("MainWindow", u"Fiducial Point Selection", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Import Project", None))
        self.LoadNewMovingImageButton.setText(QCoreApplication.translate("MainWindow", u"Load Image", None))
        self.LoadOldMovingImageButton.setText(QCoreApplication.translate("MainWindow", u"Load Image", None))
        self.textEdit_5.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt; font-weight:600;\">Register Moving Image</span></p></body></html>", None))
        self.textEdit_6.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt; font-weight:600;\">Re-register Completed Moving Image</span></p></body></html>", None))
        self.PickNewMovingImageButton.setText(QCoreApplication.translate("MainWindow", u"Load New Moving Image", None))
        self.FiducialFrameHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Fiducial Point Controls</span></p></body></html>", None))
        self.AddFiducialButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.ColorFiducialButton.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.ShrinkFiducialButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.GrowFiducialButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.FiducialSizeText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt; font-weight:600;\">Size</span></p></body></html>", None))
        self.DeleteFromFixedButton.setText(QCoreApplication.translate("MainWindow", u"Delete One", None))
        self.DeleteAllButton.setText(QCoreApplication.translate("MainWindow", u"Delete all", None))
        self.ImageViewFrameHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Image View Controls</span></p></body></html>", None))
        self.ZoomPanButton.setText(QCoreApplication.translate("MainWindow", u"Zoom/Pan", None))
        self.RotateButton.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
        self.RevertButton.setText(QCoreApplication.translate("MainWindow", u"Revert", None))
        self.FlipButton.setText(QCoreApplication.translate("MainWindow", u"Flip", None))
        self.brightnessDownButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.brightnessUpButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.contrastDownButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.contrastUpButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ContrastImage.setText("")
        self.BrightnessImage.setText("")
        self.CalculatingICPText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Calculating Point Cloud Registration. Please Wait...</span></p></body></html>", None))
        self.moving_image_border.setText("")
        self.FixedImageFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u" Fixed Image", None))
        self.MovingImageFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u" Moving Image", None))
        self.fixed_image_border.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Select Point Cloud", None))
        self.textEdit_17.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Image View Controls</p></body></html>", None))
        self.pushButton_22.setText(QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.pushButton_27.setText(QCoreApplication.translate("MainWindow", u"Pan", None))
        self.pushButton_28.setText(QCoreApplication.translate("MainWindow", u"Crop", None))
        self.pushButton_30.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
        self.pushButton_31.setText(QCoreApplication.translate("MainWindow", u"Revert", None))
        self.pushButton_32.setText(QCoreApplication.translate("MainWindow", u"Flip", None))
        self.pushButton_33.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_34.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_35.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_36.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pushButton_14.setText("")
        self.textEdit_21.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Moving Image</p></body></html>", None))
        self.textEdit_22.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Is the registration acceptable?</p></body></html>", None))
        self.pushButton_37.setText(QCoreApplication.translate("MainWindow", u"Yes, Save the Results", None))
        self.pushButton_38.setText(QCoreApplication.translate("MainWindow", u"No, Return to Fiducials", None))
        self.textEdit_24.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">What Do You Want to Do Next?</p></body></html>", None))
        self.pushButton_42.setText(QCoreApplication.translate("MainWindow", u"Register Images", None))
        self.pushButton_43.setText(QCoreApplication.translate("MainWindow", u"Apply to Data", None))
        self.pushButton_44.setText(QCoreApplication.translate("MainWindow", u"Apply to Images", None))
        self.textEdit_26.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Fixed Image</p></body></html>", None))
        self.textEdit_29.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Fixed Image Size: </span></p></body></html>", None))
        self.textEdit_30.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Unregistered RMSE: </span></p></body></html>", None))
        self.textEdit_31.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Registered RMSE: </span></p></body></html>", None))
        self.textEdit_32.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Saving Registration Results. Please Wait...</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"View Overlay", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Apply to Coordinates", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Apply to Images", None))
    # retranslateUi

