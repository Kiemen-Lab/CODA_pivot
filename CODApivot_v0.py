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
        MainWindow.resize(852, 745)
        icon = QIcon()
        icon.addFile(u"logo square large.jpg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.tabWidget = QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 841, 711))
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
"	width: 120px;\n"
"}\n"
"")
        self.tabWidget.setUsesScrollButtons(False)
        self.ImportProjectTabName = QWidget()
        self.ImportProjectTabName.setObjectName(u"ImportProjectTabName")
        self.DefineFixedImageFrame = QFrame(self.ImportProjectTabName)
        self.DefineFixedImageFrame.setObjectName(u"DefineFixedImageFrame")
        self.DefineFixedImageFrame.setGeometry(QRect(10, 10, 815, 120))
        self.DefineFixedImageFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineFixedImageFrame.setFrameShape(QFrame.StyledPanel)
        self.DefineFixedImageFrame.setFrameShadow(QFrame.Raised)
        self.FixedImageTableHeaderText = QTextEdit(self.DefineFixedImageFrame)
        self.FixedImageTableHeaderText.setObjectName(u"FixedImageTableHeaderText")
        self.FixedImageTableHeaderText.setGeometry(QRect(0, 0, 815, 25))
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
        self.chooseFixedImageButton.setGeometry(QRect(694, 35, 41, 31))
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
        self.fixedImageTableWidget.setGeometry(QRect(10, 35, 685, 75))
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
"	text-align: center;\n"
"}\n"
"\n"
"QTableView::viewport {\n"
"    background-color: #646464; /* Background beneath the las"
                        "t row */\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
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
        self.fixedImageTableWidget.horizontalHeader().setMinimumSectionSize(75)
        self.fixedImageTableWidget.horizontalHeader().setDefaultSectionSize(227)
        self.fixedImageTableWidget.horizontalHeader().setStretchLastSection(True)
        self.fixedImageTableWidget.verticalHeader().setVisible(False)
        self.fixedImageTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.fixedImageTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.deleteFixedImageButton = QPushButton(self.DefineFixedImageFrame)
        self.deleteFixedImageButton.setObjectName(u"deleteFixedImageButton")
        self.deleteFixedImageButton.setEnabled(True)
        self.deleteFixedImageButton.setGeometry(QRect(755, 79, 50, 30))
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
        self.keepFixedImageButton.setGeometry(QRect(700, 79, 50, 30))
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
        self.DefineMovingImageFrame = QFrame(self.ImportProjectTabName)
        self.DefineMovingImageFrame.setObjectName(u"DefineMovingImageFrame")
        self.DefineMovingImageFrame.setGeometry(QRect(10, 140, 815, 275))
        self.DefineMovingImageFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DefineMovingImageFrame.setFrameShape(QFrame.StyledPanel)
        self.DefineMovingImageFrame.setFrameShadow(QFrame.Raised)
        self.MovingImageTableHeaderText = QTextEdit(self.DefineMovingImageFrame)
        self.MovingImageTableHeaderText.setObjectName(u"MovingImageTableHeaderText")
        self.MovingImageTableHeaderText.setGeometry(QRect(0, 0, 815, 25))
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
        self.movingImageTableWidget.setGeometry(QRect(10, 35, 685, 230))
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
"	text-align: center;\n"
"}\n"
"\n"
"QTableView::viewport {\n"
"    background-color: #646464; /* Background beneath the las"
                        "t row */\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
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
        self.movingImageTableWidget.horizontalHeader().setMinimumSectionSize(75)
        self.movingImageTableWidget.horizontalHeader().setDefaultSectionSize(227)
        self.movingImageTableWidget.horizontalHeader().setStretchLastSection(True)
        self.movingImageTableWidget.verticalHeader().setVisible(False)
        self.movingImageTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.movingImageTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.chooseMovingImageButton = QPushButton(self.DefineMovingImageFrame)
        self.chooseMovingImageButton.setObjectName(u"chooseMovingImageButton")
        self.chooseMovingImageButton.setGeometry(QRect(694, 35, 41, 31))
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
        self.deleteMovingImageButton.setGeometry(QRect(755, 79, 50, 30))
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
        self.keepMovingImageButton.setGeometry(QRect(700, 79, 50, 30))
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
        self.SetJobFolderFrame = QFrame(self.ImportProjectTabName)
        self.SetJobFolderFrame.setObjectName(u"SetJobFolderFrame")
        self.SetJobFolderFrame.setGeometry(QRect(10, 425, 815, 120))
        self.SetJobFolderFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.SetJobFolderFrame.setFrameShape(QFrame.StyledPanel)
        self.SetJobFolderFrame.setFrameShadow(QFrame.Raised)
        self.JobFolderTableHeaderText = QTextEdit(self.SetJobFolderFrame)
        self.JobFolderTableHeaderText.setObjectName(u"JobFolderTableHeaderText")
        self.JobFolderTableHeaderText.setGeometry(QRect(0, 0, 815, 25))
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
        self.JobFolderCheckBox.setGeometry(QRect(700, 74, 101, 41))
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
        self.setJobTableWidget.setGeometry(QRect(10, 35, 685, 75))
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
"	text-align: center;\n"
"}\n"
"\n"
"QTableView::viewport {\n"
"    background-color: #646464; /* Background beneath the las"
                        "t row */\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
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
        self.setJobTableWidget.horizontalHeader().setMinimumSectionSize(75)
        self.setJobTableWidget.horizontalHeader().setDefaultSectionSize(340)
        self.setJobTableWidget.horizontalHeader().setStretchLastSection(True)
        self.setJobTableWidget.verticalHeader().setVisible(False)
        self.setJobTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.setJobTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.chooseJobFolderButton = QPushButton(self.SetJobFolderFrame)
        self.chooseJobFolderButton.setObjectName(u"chooseJobFolderButton")
        self.chooseJobFolderButton.setGeometry(QRect(694, 35, 41, 31))
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
        self.loadTemplateButton = QPushButton(self.ImportProjectTabName)
        self.loadTemplateButton.setObjectName(u"loadTemplateButton")
        self.loadTemplateButton.setGeometry(QRect(20, 555, 110, 30))
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
        self.NavigationButton = QPushButton(self.ImportProjectTabName)
        self.NavigationButton.setObjectName(u"NavigationButton")
        self.NavigationButton.setGeometry(QRect(755, 550, 65, 30))
        self.NavigationButton.setFont(font1)
        self.NavigationButton.setStyleSheet(u"QPushButton {\n"
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
        self.WhatNextControlFrame = QFrame(self.ImportProjectTabName)
        self.WhatNextControlFrame.setObjectName(u"WhatNextControlFrame")
        self.WhatNextControlFrame.setGeometry(QRect(425, 605, 405, 75))
        self.WhatNextControlFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextControlFrame.setFrameShape(QFrame.StyledPanel)
        self.WhatNextControlFrame.setFrameShadow(QFrame.Raised)
        self.WhatNextText = QTextEdit(self.WhatNextControlFrame)
        self.WhatNextText.setObjectName(u"WhatNextText")
        self.WhatNextText.setGeometry(QRect(0, 0, 405, 25))
        self.WhatNextText.setFont(font1)
        self.WhatNextText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText.setReadOnly(True)
        self.GoToImportProjectTab = QPushButton(self.WhatNextControlFrame)
        self.GoToImportProjectTab.setObjectName(u"GoToImportProjectTab")
        self.GoToImportProjectTab.setGeometry(QRect(10, 35, 80, 30))
        self.GoToImportProjectTab.setFont(font1)
        self.GoToImportProjectTab.setStyleSheet(u"QPushButton {\n"
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
        self.GoToFiducialsTab = QPushButton(self.WhatNextControlFrame)
        self.GoToFiducialsTab.setObjectName(u"GoToFiducialsTab")
        self.GoToFiducialsTab.setGeometry(QRect(95, 35, 90, 30))
        self.GoToFiducialsTab.setFont(font1)
        self.GoToFiducialsTab.setStyleSheet(u"QPushButton {\n"
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
        self.GoToJobStatusTab = QPushButton(self.WhatNextControlFrame)
        self.GoToJobStatusTab.setObjectName(u"GoToJobStatusTab")
        self.GoToJobStatusTab.setGeometry(QRect(275, 35, 57, 30))
        self.GoToJobStatusTab.setFont(font1)
        self.GoToJobStatusTab.setStyleSheet(u"QPushButton {\n"
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
        self.GoToCoordsTab = QPushButton(self.WhatNextControlFrame)
        self.GoToCoordsTab.setObjectName(u"GoToCoordsTab")
        self.GoToCoordsTab.setGeometry(QRect(190, 35, 80, 30))
        self.GoToCoordsTab.setFont(font1)
        self.GoToCoordsTab.setStyleSheet(u"QPushButton {\n"
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
        self.CloseNavigationButton = QPushButton(self.WhatNextControlFrame)
        self.CloseNavigationButton.setObjectName(u"CloseNavigationButton")
        self.CloseNavigationButton.setGeometry(QRect(337, 35, 58, 30))
        self.CloseNavigationButton.setFont(font1)
        self.CloseNavigationButton.setStyleSheet(u"QPushButton {\n"
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
        self.tabWidget.addTab(self.ImportProjectTabName, "")
        self.AddFiducialsTabName = QWidget()
        self.AddFiducialsTabName.setObjectName(u"AddFiducialsTabName")
        self.ChooseMovingImageFrame = QFrame(self.AddFiducialsTabName)
        self.ChooseMovingImageFrame.setObjectName(u"ChooseMovingImageFrame")
        self.ChooseMovingImageFrame.setGeometry(QRect(350, 10, 480, 85))
        self.ChooseMovingImageFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ChooseMovingImageFrame.setFrameShape(QFrame.StyledPanel)
        self.ChooseMovingImageFrame.setFrameShadow(QFrame.Raised)
        self.LoadNewMovingImageButton = QPushButton(self.ChooseMovingImageFrame)
        self.LoadNewMovingImageButton.setObjectName(u"LoadNewMovingImageButton")
        self.LoadNewMovingImageButton.setGeometry(QRect(380, 10, 91, 30))
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
        self.LoadOldMovingImageButton.setGeometry(QRect(380, 46, 91, 30))
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
        self.MovingImagesComboBox.setGeometry(QRect(170, 12, 201, 25))
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
        self.MovingImagesText = QTextEdit(self.ChooseMovingImageFrame)
        self.MovingImagesText.setObjectName(u"MovingImagesText")
        self.MovingImagesText.setGeometry(QRect(5, 13, 160, 27))
        font5 = QFont()
        font5.setPointSize(9)
        self.MovingImagesText.setFont(font5)
        self.MovingImagesText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.MovingImagesText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MovingImagesText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MovingImagesText.setReadOnly(True)
        self.OldMovingImagesText = QTextEdit(self.ChooseMovingImageFrame)
        self.OldMovingImagesText.setObjectName(u"OldMovingImagesText")
        self.OldMovingImagesText.setGeometry(QRect(5, 49, 160, 27))
        self.OldMovingImagesText.setFont(font5)
        self.OldMovingImagesText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.OldMovingImagesText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.OldMovingImagesText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.OldMovingImagesText.setReadOnly(True)
        self.OldMovingImagesComboBox = QComboBox(self.ChooseMovingImageFrame)
        self.OldMovingImagesComboBox.setObjectName(u"OldMovingImagesComboBox")
        self.OldMovingImagesComboBox.setGeometry(QRect(170, 48, 201, 25))
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
        self.FiducialPointControlsFrame = QFrame(self.AddFiducialsTabName)
        self.FiducialPointControlsFrame.setObjectName(u"FiducialPointControlsFrame")
        self.FiducialPointControlsFrame.setGeometry(QRect(10, 605, 250, 75))
        self.FiducialPointControlsFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.FiducialPointControlsFrame.setFrameShape(QFrame.StyledPanel)
        self.FiducialPointControlsFrame.setFrameShadow(QFrame.Raised)
        self.FiducialFrameHeaderText = QTextEdit(self.FiducialPointControlsFrame)
        self.FiducialFrameHeaderText.setObjectName(u"FiducialFrameHeaderText")
        self.FiducialFrameHeaderText.setGeometry(QRect(0, 0, 250, 25))
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
        self.AddFiducialButton.setGeometry(QRect(10, 35, 55, 30))
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
        self.ColorFiducialButton.setGeometry(QRect(135, 35, 45, 30))
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
        self.ShrinkFiducialButton.setGeometry(QRect(185, 38, 25, 25))
        self.ShrinkFiducialButton.setFont(font1)
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
        self.GrowFiducialButton.setGeometry(QRect(215, 38, 25, 25))
        self.GrowFiducialButton.setFont(font1)
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
        self.DeleteAllButton = QPushButton(self.FiducialPointControlsFrame)
        self.DeleteAllButton.setObjectName(u"DeleteAllButton")
        self.DeleteAllButton.setGeometry(QRect(70, 35, 55, 30))
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
        self.DeleteAllButton.raise_()
        self.FiducialFrameHeaderText.raise_()
        self.AddFiducialButton.raise_()
        self.GrowFiducialButton.raise_()
        self.ColorFiducialButton.raise_()
        self.ShrinkFiducialButton.raise_()
        self.FixedImageDisplayFrame = QFrame(self.AddFiducialsTabName)
        self.FixedImageDisplayFrame.setObjectName(u"FixedImageDisplayFrame")
        self.FixedImageDisplayFrame.setGeometry(QRect(10, 125, 400, 350))
        self.FixedImageDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.FixedImageDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.FixedImageDisplayFrame.setFrameShadow(QFrame.Raised)
        self.MovingImageDisplayFrame = QFrame(self.AddFiducialsTabName)
        self.MovingImageDisplayFrame.setObjectName(u"MovingImageDisplayFrame")
        self.MovingImageDisplayFrame.setGeometry(QRect(425, 125, 400, 350))
        self.MovingImageDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.MovingImageDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.MovingImageDisplayFrame.setFrameShadow(QFrame.Raised)
        self.FiducialTabUpdateText = QTextEdit(self.AddFiducialsTabName)
        self.FiducialTabUpdateText.setObjectName(u"FiducialTabUpdateText")
        self.FiducialTabUpdateText.setGeometry(QRect(10, 530, 341, 24))
        self.FiducialTabUpdateText.setFont(font5)
        self.FiducialTabUpdateText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.FiducialTabUpdateText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.FiducialTabUpdateText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MovingImageBorder = QLabel(self.AddFiducialsTabName)
        self.MovingImageBorder.setObjectName(u"MovingImageBorder")
        self.MovingImageBorder.setGeometry(QRect(422, 122, 406, 356))
        self.MovingImageBorder.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 5px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.FixedImageFrameHeaderText = QLabel(self.AddFiducialsTabName)
        self.FixedImageFrameHeaderText.setObjectName(u"FixedImageFrameHeaderText")
        self.FixedImageFrameHeaderText.setGeometry(QRect(10, 96, 400, 24))
        font6 = QFont()
        font6.setPointSize(11)
        font6.setBold(True)
        self.FixedImageFrameHeaderText.setFont(font6)
        self.FixedImageFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.MovingImageFrameHeaderText = QLabel(self.AddFiducialsTabName)
        self.MovingImageFrameHeaderText.setObjectName(u"MovingImageFrameHeaderText")
        self.MovingImageFrameHeaderText.setGeometry(QRect(422, 96, 400, 24))
        self.MovingImageFrameHeaderText.setFont(font6)
        self.MovingImageFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.FixedImageBorder = QLabel(self.AddFiducialsTabName)
        self.FixedImageBorder.setObjectName(u"FixedImageBorder")
        self.FixedImageBorder.setGeometry(QRect(7, 122, 406, 356))
        self.FixedImageBorder.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 5px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.PickNewMovingImageButton = QPushButton(self.AddFiducialsTabName)
        self.PickNewMovingImageButton.setObjectName(u"PickNewMovingImageButton")
        self.PickNewMovingImageButton.setGeometry(QRect(270, 610, 125, 30))
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
        self.AttemptICPRegistrationButton = QPushButton(self.AddFiducialsTabName)
        self.AttemptICPRegistrationButton.setObjectName(u"AttemptICPRegistrationButton")
        self.AttemptICPRegistrationButton.setGeometry(QRect(270, 650, 125, 30))
        self.AttemptICPRegistrationButton.setFont(font1)
        self.AttemptICPRegistrationButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #447544;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #488a48; /* Grey-blue when hovered */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #49a349; /* More blue when pressed */\n"
"}")
        self.NavigationButton_F = QPushButton(self.AddFiducialsTabName)
        self.NavigationButton_F.setObjectName(u"NavigationButton_F")
        self.NavigationButton_F.setGeometry(QRect(755, 550, 65, 30))
        self.NavigationButton_F.setFont(font1)
        self.NavigationButton_F.setStyleSheet(u"QPushButton {\n"
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
        self.WhatNextControlFrame_F = QFrame(self.AddFiducialsTabName)
        self.WhatNextControlFrame_F.setObjectName(u"WhatNextControlFrame_F")
        self.WhatNextControlFrame_F.setGeometry(QRect(425, 605, 405, 75))
        self.WhatNextControlFrame_F.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextControlFrame_F.setFrameShape(QFrame.StyledPanel)
        self.WhatNextControlFrame_F.setFrameShadow(QFrame.Raised)
        self.WhatNextText_F = QTextEdit(self.WhatNextControlFrame_F)
        self.WhatNextText_F.setObjectName(u"WhatNextText_F")
        self.WhatNextText_F.setGeometry(QRect(0, 0, 405, 25))
        self.WhatNextText_F.setFont(font1)
        self.WhatNextText_F.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextText_F.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_F.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_F.setReadOnly(True)
        self.GoToImportProjectTab_F = QPushButton(self.WhatNextControlFrame_F)
        self.GoToImportProjectTab_F.setObjectName(u"GoToImportProjectTab_F")
        self.GoToImportProjectTab_F.setGeometry(QRect(10, 35, 80, 30))
        self.GoToImportProjectTab_F.setFont(font1)
        self.GoToImportProjectTab_F.setStyleSheet(u"QPushButton {\n"
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
        self.GoToFiducialsTab_F = QPushButton(self.WhatNextControlFrame_F)
        self.GoToFiducialsTab_F.setObjectName(u"GoToFiducialsTab_F")
        self.GoToFiducialsTab_F.setGeometry(QRect(95, 35, 90, 30))
        self.GoToFiducialsTab_F.setFont(font1)
        self.GoToFiducialsTab_F.setStyleSheet(u"QPushButton {\n"
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
        self.GoToJobStatusTab_F = QPushButton(self.WhatNextControlFrame_F)
        self.GoToJobStatusTab_F.setObjectName(u"GoToJobStatusTab_F")
        self.GoToJobStatusTab_F.setGeometry(QRect(275, 35, 57, 30))
        self.GoToJobStatusTab_F.setFont(font1)
        self.GoToJobStatusTab_F.setStyleSheet(u"QPushButton {\n"
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
        self.GoToCoordsTab_F = QPushButton(self.WhatNextControlFrame_F)
        self.GoToCoordsTab_F.setObjectName(u"GoToCoordsTab_F")
        self.GoToCoordsTab_F.setGeometry(QRect(190, 35, 80, 30))
        self.GoToCoordsTab_F.setFont(font1)
        self.GoToCoordsTab_F.setStyleSheet(u"QPushButton {\n"
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
        self.CloseNavigationButton_F = QPushButton(self.WhatNextControlFrame_F)
        self.CloseNavigationButton_F.setObjectName(u"CloseNavigationButton_F")
        self.CloseNavigationButton_F.setGeometry(QRect(337, 35, 58, 30))
        self.CloseNavigationButton_F.setFont(font1)
        self.CloseNavigationButton_F.setStyleSheet(u"QPushButton {\n"
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
        self.tabWidget.addTab(self.AddFiducialsTabName, "")
        self.ChooseMovingImageFrame.raise_()
        self.FixedImageBorder.raise_()
        self.MovingImageBorder.raise_()
        self.FiducialPointControlsFrame.raise_()
        self.FixedImageDisplayFrame.raise_()
        self.MovingImageDisplayFrame.raise_()
        self.FiducialTabUpdateText.raise_()
        self.FixedImageFrameHeaderText.raise_()
        self.MovingImageFrameHeaderText.raise_()
        self.PickNewMovingImageButton.raise_()
        self.AttemptICPRegistrationButton.raise_()
        self.NavigationButton_F.raise_()
        self.WhatNextControlFrame_F.raise_()
        self.ApplyToCoordsTabName = QWidget()
        self.ApplyToCoordsTabName.setObjectName(u"ApplyToCoordsTabName")
        self.RegisterCoordsFrameHeaderText = QLabel(self.ApplyToCoordsTabName)
        self.RegisterCoordsFrameHeaderText.setObjectName(u"RegisterCoordsFrameHeaderText")
        self.RegisterCoordsFrameHeaderText.setGeometry(QRect(10, 166, 510, 24))
        self.RegisterCoordsFrameHeaderText.setFont(font6)
        self.RegisterCoordsFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.RegisterCoordsDisplayFrame = QFrame(self.ApplyToCoordsTabName)
        self.RegisterCoordsDisplayFrame.setObjectName(u"RegisterCoordsDisplayFrame")
        self.RegisterCoordsDisplayFrame.setGeometry(QRect(10, 195, 530, 385))
        self.RegisterCoordsDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.RegisterCoordsDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.RegisterCoordsDisplayFrame.setFrameShadow(QFrame.Raised)
        self.RegisterCoordsImageBorder = QLabel(self.ApplyToCoordsTabName)
        self.RegisterCoordsImageBorder.setObjectName(u"RegisterCoordsImageBorder")
        self.RegisterCoordsImageBorder.setGeometry(QRect(7, 192, 536, 391))
        self.RegisterCoordsImageBorder.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 5px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.ImageViewControlsFrame_C = QFrame(self.ApplyToCoordsTabName)
        self.ImageViewControlsFrame_C.setObjectName(u"ImageViewControlsFrame_C")
        self.ImageViewControlsFrame_C.setGeometry(QRect(10, 605, 125, 75))
        self.ImageViewControlsFrame_C.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ImageViewControlsFrame_C.setFrameShape(QFrame.StyledPanel)
        self.ImageViewControlsFrame_C.setFrameShadow(QFrame.Raised)
        self.ImageViewFrameHeaderText_C = QTextEdit(self.ImageViewControlsFrame_C)
        self.ImageViewFrameHeaderText_C.setObjectName(u"ImageViewFrameHeaderText_C")
        self.ImageViewFrameHeaderText_C.setGeometry(QRect(0, 0, 125, 25))
        self.ImageViewFrameHeaderText_C.setFont(font)
        self.ImageViewFrameHeaderText_C.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ImageViewFrameHeaderText_C.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ImageViewFrameHeaderText_C.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ImageViewFrameHeaderText_C.setReadOnly(True)
        self.ColorFiducialButton_C = QPushButton(self.ImageViewControlsFrame_C)
        self.ColorFiducialButton_C.setObjectName(u"ColorFiducialButton_C")
        self.ColorFiducialButton_C.setGeometry(QRect(10, 35, 45, 30))
        self.ColorFiducialButton_C.setFont(font1)
        self.ColorFiducialButton_C.setStyleSheet(u"QPushButton {\n"
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
        self.GrowFiducialButton_C = QPushButton(self.ImageViewControlsFrame_C)
        self.GrowFiducialButton_C.setObjectName(u"GrowFiducialButton_C")
        self.GrowFiducialButton_C.setGeometry(QRect(90, 38, 25, 25))
        self.GrowFiducialButton_C.setFont(font1)
        self.GrowFiducialButton_C.setStyleSheet(u"QPushButton {\n"
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
        self.ShrinkFiducialButton_C = QPushButton(self.ImageViewControlsFrame_C)
        self.ShrinkFiducialButton_C.setObjectName(u"ShrinkFiducialButton_C")
        self.ShrinkFiducialButton_C.setGeometry(QRect(60, 38, 25, 25))
        self.ShrinkFiducialButton_C.setFont(font1)
        self.ShrinkFiducialButton_C.setStyleSheet(u"QPushButton {\n"
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
        self.RegisterCoordinatesFrame = QFrame(self.ApplyToCoordsTabName)
        self.RegisterCoordinatesFrame.setObjectName(u"RegisterCoordinatesFrame")
        self.RegisterCoordinatesFrame.setGeometry(QRect(10, 10, 810, 150))
        self.RegisterCoordinatesFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.RegisterCoordinatesFrame.setFrameShape(QFrame.StyledPanel)
        self.RegisterCoordinatesFrame.setFrameShadow(QFrame.Raised)
        self.RegisterCoordinatesTableHeaderText = QTextEdit(self.RegisterCoordinatesFrame)
        self.RegisterCoordinatesTableHeaderText.setObjectName(u"RegisterCoordinatesTableHeaderText")
        self.RegisterCoordinatesTableHeaderText.setGeometry(QRect(0, 0, 810, 25))
        self.RegisterCoordinatesTableHeaderText.setFont(font1)
        self.RegisterCoordinatesTableHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.RegisterCoordinatesTableHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.RegisterCoordinatesTableHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.RegisterCoordinatesTableHeaderText.setReadOnly(True)
        self.chooseCoordinatesFileButton = QPushButton(self.RegisterCoordinatesFrame)
        self.chooseCoordinatesFileButton.setObjectName(u"chooseCoordinatesFileButton")
        self.chooseCoordinatesFileButton.setGeometry(QRect(10, 35, 41, 31))
        self.chooseCoordinatesFileButton.setFont(font2)
        self.chooseCoordinatesFileButton.setStyleSheet(u"QPushButton {\n"
"    background-color: #323232;\n"
"    color: #e6e6e6; /* Text color */\n"
"    border: 1px solid #e6e6e6; /* Border  */\n"
"    border-radius: 0px; /* Optional: Rounded corners */\n"
"    padding: 5px; /* Optional: Padding around text */\n"
"	qproperty-icon: url(Folder.jpg); /* Default icon */\n"
"}\n"
" ")
        self.chooseCoordinatesFileButton.setIconSize(QSize(35, 35))
        self.RegisterCoordinatesTableWidget = QTableWidget(self.RegisterCoordinatesFrame)
        if (self.RegisterCoordinatesTableWidget.columnCount() < 7):
            self.RegisterCoordinatesTableWidget.setColumnCount(7)
        if (self.RegisterCoordinatesTableWidget.rowCount() < 1):
            self.RegisterCoordinatesTableWidget.setRowCount(1)
        self.RegisterCoordinatesTableWidget.setObjectName(u"RegisterCoordinatesTableWidget")
        self.RegisterCoordinatesTableWidget.setGeometry(QRect(10, 65, 791, 75))
        self.RegisterCoordinatesTableWidget.setFont(font1)
        self.RegisterCoordinatesTableWidget.setStyleSheet(u"QTableView {\n"
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
"	text-align: center;\n"
"}\n"
"\n"
"QTableView::viewport {\n"
"    background-color: #646464; /* Background beneath the las"
                        "t row */\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
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
        self.RegisterCoordinatesTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.RegisterCoordinatesTableWidget.setRowCount(1)
        self.RegisterCoordinatesTableWidget.setColumnCount(7)
        self.RegisterCoordinatesTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.RegisterCoordinatesTableWidget.horizontalHeader().setMinimumSectionSize(75)
        self.RegisterCoordinatesTableWidget.horizontalHeader().setDefaultSectionSize(109)
        self.RegisterCoordinatesTableWidget.horizontalHeader().setStretchLastSection(True)
        self.RegisterCoordinatesTableWidget.verticalHeader().setVisible(False)
        self.RegisterCoordinatesTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.RegisterCoordinatesTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.BrowseForCoordinatesFileText = QTextEdit(self.RegisterCoordinatesFrame)
        self.BrowseForCoordinatesFileText.setObjectName(u"BrowseForCoordinatesFileText")
        self.BrowseForCoordinatesFileText.setGeometry(QRect(51, 38, 201, 24))
        self.BrowseForCoordinatesFileText.setFont(font1)
        self.BrowseForCoordinatesFileText.setStyleSheet(u"QTextEdit { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.BrowseForCoordinatesFileText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.BrowseForCoordinatesFileText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.BrowseForCoordinatesFileText.setReadOnly(True)
        self.CorrespondingImageComboBox = QComboBox(self.RegisterCoordinatesFrame)
        self.CorrespondingImageComboBox.setObjectName(u"CorrespondingImageComboBox")
        self.CorrespondingImageComboBox.setGeometry(QRect(260, 36, 201, 25))
        self.CorrespondingImageComboBox.setFont(font4)
        self.CorrespondingImageComboBox.setStyleSheet(u"QComboBox {\n"
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
        self.CorrespondingImageText = QTextEdit(self.RegisterCoordinatesFrame)
        self.CorrespondingImageText.setObjectName(u"CorrespondingImageText")
        self.CorrespondingImageText.setGeometry(QRect(460, 37, 191, 24))
        self.CorrespondingImageText.setFont(font1)
        self.CorrespondingImageText.setStyleSheet(u"QTextEdit { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.CorrespondingImageText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CorrespondingImageText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CorrespondingImageText.setReadOnly(True)
        self.LoadCoordinatesButton = QPushButton(self.RegisterCoordinatesFrame)
        self.LoadCoordinatesButton.setObjectName(u"LoadCoordinatesButton")
        self.LoadCoordinatesButton.setGeometry(QRect(740, 30, 61, 30))
        self.LoadCoordinatesButton.setFont(font1)
        self.LoadCoordinatesButton.setStyleSheet(u"QPushButton {\n"
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
        self.RegisterCoordinatesTableHeaderText.raise_()
        self.BrowseForCoordinatesFileText.raise_()
        self.CorrespondingImageComboBox.raise_()
        self.CorrespondingImageText.raise_()
        self.chooseCoordinatesFileButton.raise_()
        self.RegisterCoordinatesTableWidget.raise_()
        self.LoadCoordinatesButton.raise_()
        self.CoordinatesOverlayControlsFrame = QFrame(self.ApplyToCoordsTabName)
        self.CoordinatesOverlayControlsFrame.setObjectName(u"CoordinatesOverlayControlsFrame")
        self.CoordinatesOverlayControlsFrame.setGeometry(QRect(550, 195, 270, 223))
        self.CoordinatesOverlayControlsFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.CoordinatesOverlayControlsFrame.setFrameShape(QFrame.StyledPanel)
        self.CoordinatesOverlayControlsFrame.setFrameShadow(QFrame.Raised)
        self.CoordinatesOverlayHeaderText = QTextEdit(self.CoordinatesOverlayControlsFrame)
        self.CoordinatesOverlayHeaderText.setObjectName(u"CoordinatesOverlayHeaderText")
        self.CoordinatesOverlayHeaderText.setGeometry(QRect(0, 0, 270, 25))
        self.CoordinatesOverlayHeaderText.setFont(font)
        self.CoordinatesOverlayHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.CoordinatesOverlayHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CoordinatesOverlayHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CoordinatesOverlayHeaderText.setReadOnly(True)
        self.SwapXYButton = QPushButton(self.CoordinatesOverlayControlsFrame)
        self.SwapXYButton.setObjectName(u"SwapXYButton")
        self.SwapXYButton.setGeometry(QRect(10, 35, 85, 30))
        self.SwapXYButton.setFont(font1)
        self.SwapXYButton.setStyleSheet(u"QPushButton {\n"
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
        self.EditTableButton = QPushButton(self.CoordinatesOverlayControlsFrame)
        self.EditTableButton.setObjectName(u"EditTableButton")
        self.EditTableButton.setGeometry(QRect(100, 35, 85, 30))
        self.EditTableButton.setFont(font1)
        self.EditTableButton.setStyleSheet(u"QPushButton {\n"
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
        self.UnregisteredMovingCheckBox = QCheckBox(self.CoordinatesOverlayControlsFrame)
        self.UnregisteredMovingCheckBox.setObjectName(u"UnregisteredMovingCheckBox")
        self.UnregisteredMovingCheckBox.setGeometry(QRect(165, 67, 101, 41))
        self.UnregisteredMovingCheckBox.setFont(font3)
        self.UnregisteredMovingCheckBox.setStyleSheet(u"QCheckBox {\n"
"    background-color: #4b4b4b;\n"
"    color: #e6e6e6; /* Text color */\n"
"    padding: 2px; /* Optional: space around the text */\n"
"	width: 100px; /* Optional: Adjust width to allow for wrapping */\n"
"    word-wrap: break-word; /* Enable word wrap */\n"
"}\n"
"")
        self.ViewFixedButton = QPushButton(self.CoordinatesOverlayControlsFrame)
        self.ViewFixedButton.setObjectName(u"ViewFixedButton")
        self.ViewFixedButton.setGeometry(QRect(10, 146, 145, 30))
        self.ViewFixedButton.setFont(font1)
        self.ViewFixedButton.setStyleSheet(u"QPushButton {\n"
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
        self.RegisteredMovingCheckBox = QCheckBox(self.CoordinatesOverlayControlsFrame)
        self.RegisteredMovingCheckBox.setObjectName(u"RegisteredMovingCheckBox")
        self.RegisteredMovingCheckBox.setGeometry(QRect(165, 104, 101, 41))
        self.RegisteredMovingCheckBox.setFont(font3)
        self.RegisteredMovingCheckBox.setStyleSheet(u"QCheckBox {\n"
"    background-color: #4b4b4b;\n"
"    color: #e6e6e6; /* Text color */\n"
"    padding: 2px; /* Optional: space around the text */\n"
"	width: 100px; /* Optional: Adjust width to allow for wrapping */\n"
"    word-wrap: break-word; /* Enable word wrap */\n"
"}\n"
"")
        self.ViewUnregisteredMovingButton = QPushButton(self.CoordinatesOverlayControlsFrame)
        self.ViewUnregisteredMovingButton.setObjectName(u"ViewUnregisteredMovingButton")
        self.ViewUnregisteredMovingButton.setGeometry(QRect(10, 72, 145, 30))
        self.ViewUnregisteredMovingButton.setFont(font1)
        self.ViewUnregisteredMovingButton.setStyleSheet(u"QPushButton {\n"
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
        self.FixedCheckBox = QCheckBox(self.CoordinatesOverlayControlsFrame)
        self.FixedCheckBox.setObjectName(u"FixedCheckBox")
        self.FixedCheckBox.setGeometry(QRect(165, 142, 101, 41))
        self.FixedCheckBox.setFont(font3)
        self.FixedCheckBox.setStyleSheet(u"QCheckBox {\n"
"    background-color: #4b4b4b;\n"
"    color: #e6e6e6; /* Text color */\n"
"    padding: 2px; /* Optional: space around the text */\n"
"	width: 100px; /* Optional: Adjust width to allow for wrapping */\n"
"    word-wrap: break-word; /* Enable word wrap */\n"
"}\n"
"")
        self.ViewRegisteredMovingButton = QPushButton(self.CoordinatesOverlayControlsFrame)
        self.ViewRegisteredMovingButton.setObjectName(u"ViewRegisteredMovingButton")
        self.ViewRegisteredMovingButton.setGeometry(QRect(10, 109, 145, 30))
        self.ViewRegisteredMovingButton.setFont(font1)
        self.ViewRegisteredMovingButton.setStyleSheet(u"QPushButton {\n"
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
        self.SaveRegisteredCoordinatesButton = QPushButton(self.CoordinatesOverlayControlsFrame)
        self.SaveRegisteredCoordinatesButton.setObjectName(u"SaveRegisteredCoordinatesButton")
        self.SaveRegisteredCoordinatesButton.setGeometry(QRect(10, 183, 145, 30))
        self.SaveRegisteredCoordinatesButton.setFont(font1)
        self.SaveRegisteredCoordinatesButton.setStyleSheet(u"QPushButton {\n"
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
        self.DisableFrame_C = QFrame(self.ApplyToCoordsTabName)
        self.DisableFrame_C.setObjectName(u"DisableFrame_C")
        self.DisableFrame_C.setGeometry(QRect(550, 510, 31, 31))
        self.DisableFrame_C.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_C.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_C.setFrameShadow(QFrame.Raised)
        self.NavigationButton_C = QPushButton(self.ApplyToCoordsTabName)
        self.NavigationButton_C.setObjectName(u"NavigationButton_C")
        self.NavigationButton_C.setGeometry(QRect(755, 550, 65, 30))
        self.NavigationButton_C.setFont(font1)
        self.NavigationButton_C.setStyleSheet(u"QPushButton {\n"
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
        self.PlottingImageText = QTextEdit(self.ApplyToCoordsTabName)
        self.PlottingImageText.setObjectName(u"PlottingImageText")
        self.PlottingImageText.setGeometry(QRect(550, 420, 271, 24))
        self.PlottingImageText.setFont(font5)
        self.PlottingImageText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.PlottingImageText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.PlottingImageText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.DisableFrame_C_2 = QFrame(self.ApplyToCoordsTabName)
        self.DisableFrame_C_2.setObjectName(u"DisableFrame_C_2")
        self.DisableFrame_C_2.setGeometry(QRect(590, 510, 31, 31))
        self.DisableFrame_C_2.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_C_2.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_C_2.setFrameShadow(QFrame.Raised)
        self.DisableFrame_C_3 = QFrame(self.ApplyToCoordsTabName)
        self.DisableFrame_C_3.setObjectName(u"DisableFrame_C_3")
        self.DisableFrame_C_3.setGeometry(QRect(630, 510, 31, 31))
        self.DisableFrame_C_3.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_C_3.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_C_3.setFrameShadow(QFrame.Raised)
        self.MakingCoordOverlayText = QTextEdit(self.ApplyToCoordsTabName)
        self.MakingCoordOverlayText.setObjectName(u"MakingCoordOverlayText")
        self.MakingCoordOverlayText.setGeometry(QRect(419, 165, 400, 24))
        self.MakingCoordOverlayText.setFont(font5)
        self.MakingCoordOverlayText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.MakingCoordOverlayText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.MakingCoordOverlayText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextControlFrame_C = QFrame(self.ApplyToCoordsTabName)
        self.WhatNextControlFrame_C.setObjectName(u"WhatNextControlFrame_C")
        self.WhatNextControlFrame_C.setGeometry(QRect(425, 605, 405, 75))
        self.WhatNextControlFrame_C.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextControlFrame_C.setFrameShape(QFrame.StyledPanel)
        self.WhatNextControlFrame_C.setFrameShadow(QFrame.Raised)
        self.WhatNextText_C = QTextEdit(self.WhatNextControlFrame_C)
        self.WhatNextText_C.setObjectName(u"WhatNextText_C")
        self.WhatNextText_C.setGeometry(QRect(0, 0, 405, 25))
        self.WhatNextText_C.setFont(font1)
        self.WhatNextText_C.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextText_C.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_C.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_C.setReadOnly(True)
        self.GoToImportProjectTab_C = QPushButton(self.WhatNextControlFrame_C)
        self.GoToImportProjectTab_C.setObjectName(u"GoToImportProjectTab_C")
        self.GoToImportProjectTab_C.setGeometry(QRect(10, 35, 80, 30))
        self.GoToImportProjectTab_C.setFont(font1)
        self.GoToImportProjectTab_C.setStyleSheet(u"QPushButton {\n"
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
        self.GoToFiducialsTab_C = QPushButton(self.WhatNextControlFrame_C)
        self.GoToFiducialsTab_C.setObjectName(u"GoToFiducialsTab_C")
        self.GoToFiducialsTab_C.setGeometry(QRect(95, 35, 90, 30))
        self.GoToFiducialsTab_C.setFont(font1)
        self.GoToFiducialsTab_C.setStyleSheet(u"QPushButton {\n"
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
        self.GoToJobStatusTab_C = QPushButton(self.WhatNextControlFrame_C)
        self.GoToJobStatusTab_C.setObjectName(u"GoToJobStatusTab_C")
        self.GoToJobStatusTab_C.setGeometry(QRect(275, 35, 57, 30))
        self.GoToJobStatusTab_C.setFont(font1)
        self.GoToJobStatusTab_C.setStyleSheet(u"QPushButton {\n"
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
        self.GoToCoordsTab_C = QPushButton(self.WhatNextControlFrame_C)
        self.GoToCoordsTab_C.setObjectName(u"GoToCoordsTab_C")
        self.GoToCoordsTab_C.setGeometry(QRect(190, 35, 80, 30))
        self.GoToCoordsTab_C.setFont(font1)
        self.GoToCoordsTab_C.setStyleSheet(u"QPushButton {\n"
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
        self.CloseNavigationButton_C = QPushButton(self.WhatNextControlFrame_C)
        self.CloseNavigationButton_C.setObjectName(u"CloseNavigationButton_C")
        self.CloseNavigationButton_C.setGeometry(QRect(337, 35, 58, 30))
        self.CloseNavigationButton_C.setFont(font1)
        self.CloseNavigationButton_C.setStyleSheet(u"QPushButton {\n"
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
        self.tabWidget.addTab(self.ApplyToCoordsTabName, "")
        self.RegisterCoordinatesFrame.raise_()
        self.RegisterCoordsImageBorder.raise_()
        self.RegisterCoordsFrameHeaderText.raise_()
        self.RegisterCoordsDisplayFrame.raise_()
        self.ImageViewControlsFrame_C.raise_()
        self.CoordinatesOverlayControlsFrame.raise_()
        self.DisableFrame_C.raise_()
        self.NavigationButton_C.raise_()
        self.PlottingImageText.raise_()
        self.DisableFrame_C_2.raise_()
        self.DisableFrame_C_3.raise_()
        self.MakingCoordOverlayText.raise_()
        self.WhatNextControlFrame_C.raise_()
        self.JobStatusTabName = QWidget()
        self.JobStatusTabName.setObjectName(u"JobStatusTabName")
        self.JobStatusFrame = QFrame(self.JobStatusTabName)
        self.JobStatusFrame.setObjectName(u"JobStatusFrame")
        self.JobStatusFrame.setGeometry(QRect(10, 10, 811, 451))
        self.JobStatusFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.JobStatusFrame.setFrameShape(QFrame.StyledPanel)
        self.JobStatusFrame.setFrameShadow(QFrame.Raised)
        self.JobStatusHeaderText = QTextEdit(self.JobStatusFrame)
        self.JobStatusHeaderText.setObjectName(u"JobStatusHeaderText")
        self.JobStatusHeaderText.setGeometry(QRect(0, 0, 811, 25))
        self.JobStatusHeaderText.setFont(font1)
        self.JobStatusHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.JobStatusHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.JobStatusHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.JobStatusHeaderText.setReadOnly(True)
        self.JobStatusTableWidget = QTableWidget(self.JobStatusFrame)
        if (self.JobStatusTableWidget.columnCount() < 5):
            self.JobStatusTableWidget.setColumnCount(5)
        if (self.JobStatusTableWidget.rowCount() < 1):
            self.JobStatusTableWidget.setRowCount(1)
        self.JobStatusTableWidget.setObjectName(u"JobStatusTableWidget")
        self.JobStatusTableWidget.setGeometry(QRect(10, 35, 791, 401))
        self.JobStatusTableWidget.setFont(font2)
        self.JobStatusTableWidget.setStyleSheet(u"QTableView {\n"
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
        self.JobStatusTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.JobStatusTableWidget.setRowCount(1)
        self.JobStatusTableWidget.setColumnCount(5)
        self.JobStatusTableWidget.horizontalHeader().setMinimumSectionSize(75)
        self.JobStatusTableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.JobStatusTableWidget.horizontalHeader().setStretchLastSection(True)
        self.JobStatusTableWidget.verticalHeader().setVisible(False)
        self.JobStatusTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.JobStatusTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.NavigationButton_J = QPushButton(self.JobStatusTabName)
        self.NavigationButton_J.setObjectName(u"NavigationButton_J")
        self.NavigationButton_J.setGeometry(QRect(755, 550, 65, 30))
        self.NavigationButton_J.setFont(font1)
        self.NavigationButton_J.setStyleSheet(u"QPushButton {\n"
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
        self.WhatNextControlFrame_J = QFrame(self.JobStatusTabName)
        self.WhatNextControlFrame_J.setObjectName(u"WhatNextControlFrame_J")
        self.WhatNextControlFrame_J.setGeometry(QRect(425, 605, 405, 75))
        self.WhatNextControlFrame_J.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextControlFrame_J.setFrameShape(QFrame.StyledPanel)
        self.WhatNextControlFrame_J.setFrameShadow(QFrame.Raised)
        self.WhatNextText_J = QTextEdit(self.WhatNextControlFrame_J)
        self.WhatNextText_J.setObjectName(u"WhatNextText_J")
        self.WhatNextText_J.setGeometry(QRect(0, 0, 405, 25))
        self.WhatNextText_J.setFont(font1)
        self.WhatNextText_J.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextText_J.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_J.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_J.setReadOnly(True)
        self.GoToImportProjectTab_J = QPushButton(self.WhatNextControlFrame_J)
        self.GoToImportProjectTab_J.setObjectName(u"GoToImportProjectTab_J")
        self.GoToImportProjectTab_J.setGeometry(QRect(10, 35, 80, 30))
        self.GoToImportProjectTab_J.setFont(font1)
        self.GoToImportProjectTab_J.setStyleSheet(u"QPushButton {\n"
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
        self.GoToFiducialsTab_J = QPushButton(self.WhatNextControlFrame_J)
        self.GoToFiducialsTab_J.setObjectName(u"GoToFiducialsTab_J")
        self.GoToFiducialsTab_J.setGeometry(QRect(95, 35, 90, 30))
        self.GoToFiducialsTab_J.setFont(font1)
        self.GoToFiducialsTab_J.setStyleSheet(u"QPushButton {\n"
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
        self.GoToJobStatusTab_J = QPushButton(self.WhatNextControlFrame_J)
        self.GoToJobStatusTab_J.setObjectName(u"GoToJobStatusTab_J")
        self.GoToJobStatusTab_J.setGeometry(QRect(275, 35, 57, 30))
        self.GoToJobStatusTab_J.setFont(font1)
        self.GoToJobStatusTab_J.setStyleSheet(u"QPushButton {\n"
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
        self.GoToCoordsTab_J = QPushButton(self.WhatNextControlFrame_J)
        self.GoToCoordsTab_J.setObjectName(u"GoToCoordsTab_J")
        self.GoToCoordsTab_J.setGeometry(QRect(190, 35, 80, 30))
        self.GoToCoordsTab_J.setFont(font1)
        self.GoToCoordsTab_J.setStyleSheet(u"QPushButton {\n"
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
        self.CloseNavigationButton_J = QPushButton(self.WhatNextControlFrame_J)
        self.CloseNavigationButton_J.setObjectName(u"CloseNavigationButton_J")
        self.CloseNavigationButton_J.setGeometry(QRect(337, 35, 58, 30))
        self.CloseNavigationButton_J.setFont(font1)
        self.CloseNavigationButton_J.setStyleSheet(u"QPushButton {\n"
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
        self.tabWidget.addTab(self.JobStatusTabName, "")
        self.ViewOverlaysTabName = QWidget()
        self.ViewOverlaysTabName.setObjectName(u"ViewOverlaysTabName")
        self.SavingRegistrationResultsText = QTextEdit(self.ViewOverlaysTabName)
        self.SavingRegistrationResultsText.setObjectName(u"SavingRegistrationResultsText")
        self.SavingRegistrationResultsText.setGeometry(QRect(500, 510, 320, 24))
        self.SavingRegistrationResultsText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.SavingRegistrationResultsText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SavingRegistrationResultsText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SavingRegistrationResultsText.setReadOnly(True)
        self.ImageViewControlsFrame_O = QFrame(self.ViewOverlaysTabName)
        self.ImageViewControlsFrame_O.setObjectName(u"ImageViewControlsFrame_O")
        self.ImageViewControlsFrame_O.setGeometry(QRect(10, 605, 235, 75))
        self.ImageViewControlsFrame_O.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ImageViewControlsFrame_O.setFrameShape(QFrame.StyledPanel)
        self.ImageViewControlsFrame_O.setFrameShadow(QFrame.Raised)
        self.ImageViewFrameHeaderText_O = QTextEdit(self.ImageViewControlsFrame_O)
        self.ImageViewFrameHeaderText_O.setObjectName(u"ImageViewFrameHeaderText_O")
        self.ImageViewFrameHeaderText_O.setGeometry(QRect(0, 0, 235, 25))
        self.ImageViewFrameHeaderText_O.setFont(font)
        self.ImageViewFrameHeaderText_O.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ImageViewFrameHeaderText_O.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ImageViewFrameHeaderText_O.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ImageViewFrameHeaderText_O.setReadOnly(True)
        self.GrowFiducialButton2_O = QPushButton(self.ImageViewControlsFrame_O)
        self.GrowFiducialButton2_O.setObjectName(u"GrowFiducialButton2_O")
        self.GrowFiducialButton2_O.setGeometry(QRect(200, 38, 25, 25))
        self.GrowFiducialButton2_O.setFont(font1)
        self.GrowFiducialButton2_O.setStyleSheet(u"QPushButton {\n"
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
        self.ColorFiducialButton_O = QPushButton(self.ImageViewControlsFrame_O)
        self.ColorFiducialButton_O.setObjectName(u"ColorFiducialButton_O")
        self.ColorFiducialButton_O.setGeometry(QRect(10, 35, 45, 30))
        self.ColorFiducialButton_O.setFont(font1)
        self.ColorFiducialButton_O.setStyleSheet(u"QPushButton {\n"
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
        self.ShrinkFiducialButton2_O = QPushButton(self.ImageViewControlsFrame_O)
        self.ShrinkFiducialButton2_O.setObjectName(u"ShrinkFiducialButton2_O")
        self.ShrinkFiducialButton2_O.setGeometry(QRect(170, 38, 25, 25))
        self.ShrinkFiducialButton2_O.setFont(font1)
        self.ShrinkFiducialButton2_O.setStyleSheet(u"QPushButton {\n"
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
        self.ColorFiducialButton2_O = QPushButton(self.ImageViewControlsFrame_O)
        self.ColorFiducialButton2_O.setObjectName(u"ColorFiducialButton2_O")
        self.ColorFiducialButton2_O.setGeometry(QRect(120, 35, 45, 30))
        self.ColorFiducialButton2_O.setFont(font1)
        self.ColorFiducialButton2_O.setStyleSheet(u"QPushButton {\n"
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
        self.GrowFiducialButton_O = QPushButton(self.ImageViewControlsFrame_O)
        self.GrowFiducialButton_O.setObjectName(u"GrowFiducialButton_O")
        self.GrowFiducialButton_O.setGeometry(QRect(90, 38, 25, 25))
        self.GrowFiducialButton_O.setFont(font1)
        self.GrowFiducialButton_O.setStyleSheet(u"QPushButton {\n"
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
        self.ShrinkFiducialButton_O = QPushButton(self.ImageViewControlsFrame_O)
        self.ShrinkFiducialButton_O.setObjectName(u"ShrinkFiducialButton_O")
        self.ShrinkFiducialButton_O.setGeometry(QRect(60, 38, 25, 25))
        self.ShrinkFiducialButton_O.setFont(font1)
        self.ShrinkFiducialButton_O.setStyleSheet(u"QPushButton {\n"
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
        self.UnregisteredImageFrameHeaderText = QLabel(self.ViewOverlaysTabName)
        self.UnregisteredImageFrameHeaderText.setObjectName(u"UnregisteredImageFrameHeaderText")
        self.UnregisteredImageFrameHeaderText.setGeometry(QRect(10, 20, 400, 24))
        self.UnregisteredImageFrameHeaderText.setFont(font6)
        self.UnregisteredImageFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.RegisteredImageFrameHeaderText = QLabel(self.ViewOverlaysTabName)
        self.RegisteredImageFrameHeaderText.setObjectName(u"RegisteredImageFrameHeaderText")
        self.RegisteredImageFrameHeaderText.setGeometry(QRect(422, 20, 400, 24))
        self.RegisteredImageFrameHeaderText.setFont(font6)
        self.RegisteredImageFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.UnregisteredImageDisplayFrame = QFrame(self.ViewOverlaysTabName)
        self.UnregisteredImageDisplayFrame.setObjectName(u"UnregisteredImageDisplayFrame")
        self.UnregisteredImageDisplayFrame.setGeometry(QRect(10, 50, 400, 451))
        self.UnregisteredImageDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.UnregisteredImageDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.UnregisteredImageDisplayFrame.setFrameShadow(QFrame.Raised)
        self.RegisteredImageBorder = QLabel(self.ViewOverlaysTabName)
        self.RegisteredImageBorder.setObjectName(u"RegisteredImageBorder")
        self.RegisteredImageBorder.setGeometry(QRect(422, 47, 406, 457))
        self.RegisteredImageBorder.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 5px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.RegisteredImageDisplayFrame = QFrame(self.ViewOverlaysTabName)
        self.RegisteredImageDisplayFrame.setObjectName(u"RegisteredImageDisplayFrame")
        self.RegisteredImageDisplayFrame.setGeometry(QRect(425, 50, 400, 451))
        self.RegisteredImageDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.RegisteredImageDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.RegisteredImageDisplayFrame.setFrameShadow(QFrame.Raised)
        self.UnregisteredImageBorder = QLabel(self.ViewOverlaysTabName)
        self.UnregisteredImageBorder.setObjectName(u"UnregisteredImageBorder")
        self.UnregisteredImageBorder.setGeometry(QRect(7, 47, 406, 457))
        self.UnregisteredImageBorder.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 5px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.SaveRegistrationControlFrame = QFrame(self.ViewOverlaysTabName)
        self.SaveRegistrationControlFrame.setObjectName(u"SaveRegistrationControlFrame")
        self.SaveRegistrationControlFrame.setGeometry(QRect(255, 605, 100, 75))
        self.SaveRegistrationControlFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.SaveRegistrationControlFrame.setFrameShape(QFrame.StyledPanel)
        self.SaveRegistrationControlFrame.setFrameShadow(QFrame.Raised)
        self.SaveRegistrationHeaderText = QTextEdit(self.SaveRegistrationControlFrame)
        self.SaveRegistrationHeaderText.setObjectName(u"SaveRegistrationHeaderText")
        self.SaveRegistrationHeaderText.setGeometry(QRect(0, 0, 100, 25))
        self.SaveRegistrationHeaderText.setFont(font)
        self.SaveRegistrationHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.SaveRegistrationHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SaveRegistrationHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SaveRegistrationHeaderText.setReadOnly(True)
        self.SaveRegistrationResultsButton_O = QPushButton(self.SaveRegistrationControlFrame)
        self.SaveRegistrationResultsButton_O.setObjectName(u"SaveRegistrationResultsButton_O")
        self.SaveRegistrationResultsButton_O.setGeometry(QRect(10, 35, 35, 30))
        self.SaveRegistrationResultsButton_O.setFont(font1)
        self.SaveRegistrationResultsButton_O.setStyleSheet(u"QPushButton {\n"
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
        self.ReturnToFiducialsTab_O = QPushButton(self.SaveRegistrationControlFrame)
        self.ReturnToFiducialsTab_O.setObjectName(u"ReturnToFiducialsTab_O")
        self.ReturnToFiducialsTab_O.setGeometry(QRect(50, 35, 35, 30))
        self.ReturnToFiducialsTab_O.setFont(font1)
        self.ReturnToFiducialsTab_O.setStyleSheet(u"QPushButton {\n"
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
        self.DisableFrame_O1 = QFrame(self.ViewOverlaysTabName)
        self.DisableFrame_O1.setObjectName(u"DisableFrame_O1")
        self.DisableFrame_O1.setGeometry(QRect(380, 10, 31, 31))
        self.DisableFrame_O1.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_O1.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_O1.setFrameShadow(QFrame.Raised)
        self.DisableFrame_O2 = QFrame(self.ViewOverlaysTabName)
        self.DisableFrame_O2.setObjectName(u"DisableFrame_O2")
        self.DisableFrame_O2.setGeometry(QRect(420, 10, 31, 31))
        self.DisableFrame_O2.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_O2.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_O2.setFrameShadow(QFrame.Raised)
        self.NavigationButton_O = QPushButton(self.ViewOverlaysTabName)
        self.NavigationButton_O.setObjectName(u"NavigationButton_O")
        self.NavigationButton_O.setGeometry(QRect(370, 560, 75, 30))
        self.NavigationButton_O.setFont(font1)
        self.NavigationButton_O.setStyleSheet(u"QPushButton {\n"
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
        self.TryElasticRegButton = QPushButton(self.ViewOverlaysTabName)
        self.TryElasticRegButton.setObjectName(u"TryElasticRegButton")
        self.TryElasticRegButton.setGeometry(QRect(670, 560, 161, 30))
        self.TryElasticRegButton.setFont(font1)
        self.TryElasticRegButton.setStyleSheet(u"QPushButton {\n"
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
        self.DisableFrame_O3 = QFrame(self.ViewOverlaysTabName)
        self.DisableFrame_O3.setObjectName(u"DisableFrame_O3")
        self.DisableFrame_O3.setGeometry(QRect(460, 10, 31, 31))
        self.DisableFrame_O3.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_O3.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_O3.setFrameShadow(QFrame.Raised)
        self.WhatNextControlFrame_O = QFrame(self.ViewOverlaysTabName)
        self.WhatNextControlFrame_O.setObjectName(u"WhatNextControlFrame_O")
        self.WhatNextControlFrame_O.setGeometry(QRect(425, 605, 405, 75))
        self.WhatNextControlFrame_O.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextControlFrame_O.setFrameShape(QFrame.StyledPanel)
        self.WhatNextControlFrame_O.setFrameShadow(QFrame.Raised)
        self.WhatNextText_O = QTextEdit(self.WhatNextControlFrame_O)
        self.WhatNextText_O.setObjectName(u"WhatNextText_O")
        self.WhatNextText_O.setGeometry(QRect(0, 0, 405, 25))
        self.WhatNextText_O.setFont(font1)
        self.WhatNextText_O.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextText_O.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_O.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_O.setReadOnly(True)
        self.GoToImportProjectTab_O = QPushButton(self.WhatNextControlFrame_O)
        self.GoToImportProjectTab_O.setObjectName(u"GoToImportProjectTab_O")
        self.GoToImportProjectTab_O.setGeometry(QRect(10, 35, 80, 30))
        self.GoToImportProjectTab_O.setFont(font1)
        self.GoToImportProjectTab_O.setStyleSheet(u"QPushButton {\n"
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
        self.GoToFiducialsTab_O = QPushButton(self.WhatNextControlFrame_O)
        self.GoToFiducialsTab_O.setObjectName(u"GoToFiducialsTab_O")
        self.GoToFiducialsTab_O.setGeometry(QRect(95, 35, 90, 30))
        self.GoToFiducialsTab_O.setFont(font1)
        self.GoToFiducialsTab_O.setStyleSheet(u"QPushButton {\n"
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
        self.GoToJobStatusTab_O = QPushButton(self.WhatNextControlFrame_O)
        self.GoToJobStatusTab_O.setObjectName(u"GoToJobStatusTab_O")
        self.GoToJobStatusTab_O.setGeometry(QRect(275, 35, 57, 30))
        self.GoToJobStatusTab_O.setFont(font1)
        self.GoToJobStatusTab_O.setStyleSheet(u"QPushButton {\n"
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
        self.GoToCoordsTab_O = QPushButton(self.WhatNextControlFrame_O)
        self.GoToCoordsTab_O.setObjectName(u"GoToCoordsTab_O")
        self.GoToCoordsTab_O.setGeometry(QRect(190, 35, 80, 30))
        self.GoToCoordsTab_O.setFont(font1)
        self.GoToCoordsTab_O.setStyleSheet(u"QPushButton {\n"
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
        self.CloseNavigationButton_O = QPushButton(self.WhatNextControlFrame_O)
        self.CloseNavigationButton_O.setObjectName(u"CloseNavigationButton_O")
        self.CloseNavigationButton_O.setGeometry(QRect(337, 35, 58, 30))
        self.CloseNavigationButton_O.setFont(font1)
        self.CloseNavigationButton_O.setStyleSheet(u"QPushButton {\n"
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
        self.tabWidget.addTab(self.ViewOverlaysTabName, "")
        self.UnregisteredImageBorder.raise_()
        self.ImageViewControlsFrame_O.raise_()
        self.UnregisteredImageFrameHeaderText.raise_()
        self.RegisteredImageFrameHeaderText.raise_()
        self.UnregisteredImageDisplayFrame.raise_()
        self.RegisteredImageBorder.raise_()
        self.SaveRegistrationControlFrame.raise_()
        self.DisableFrame_O1.raise_()
        self.DisableFrame_O2.raise_()
        self.RegisteredImageDisplayFrame.raise_()
        self.NavigationButton_O.raise_()
        self.SavingRegistrationResultsText.raise_()
        self.TryElasticRegButton.raise_()
        self.DisableFrame_O3.raise_()
        self.WhatNextControlFrame_O.raise_()
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.FiducialRegisteredImageDisplayFrame = QFrame(self.tab)
        self.FiducialRegisteredImageDisplayFrame.setObjectName(u"FiducialRegisteredImageDisplayFrame")
        self.FiducialRegisteredImageDisplayFrame.setGeometry(QRect(10, 50, 400, 451))
        self.FiducialRegisteredImageDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.FiducialRegisteredImageDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.FiducialRegisteredImageDisplayFrame.setFrameShadow(QFrame.Raised)
        self.FiducialRegisteredImageFrameHeaderText = QLabel(self.tab)
        self.FiducialRegisteredImageFrameHeaderText.setObjectName(u"FiducialRegisteredImageFrameHeaderText")
        self.FiducialRegisteredImageFrameHeaderText.setGeometry(QRect(10, 20, 400, 24))
        self.FiducialRegisteredImageFrameHeaderText.setFont(font6)
        self.FiducialRegisteredImageFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.ElasticRegisteredImageBorder = QLabel(self.tab)
        self.ElasticRegisteredImageBorder.setObjectName(u"ElasticRegisteredImageBorder")
        self.ElasticRegisteredImageBorder.setGeometry(QRect(422, 47, 406, 457))
        self.ElasticRegisteredImageBorder.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 5px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.FiducialRegisteredImageBorder = QLabel(self.tab)
        self.FiducialRegisteredImageBorder.setObjectName(u"FiducialRegisteredImageBorder")
        self.FiducialRegisteredImageBorder.setGeometry(QRect(7, 47, 406, 457))
        self.FiducialRegisteredImageBorder.setStyleSheet(u"QLabel {\n"
"        background-color: transparent; /* Transparent fill */\n"
"        border: 5px solid #e6e6e6;       /* Green border */\n"
"    }\n"
"")
        self.WhatNextControlFrame_E = QFrame(self.tab)
        self.WhatNextControlFrame_E.setObjectName(u"WhatNextControlFrame_E")
        self.WhatNextControlFrame_E.setGeometry(QRect(425, 605, 405, 75))
        self.WhatNextControlFrame_E.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextControlFrame_E.setFrameShape(QFrame.StyledPanel)
        self.WhatNextControlFrame_E.setFrameShadow(QFrame.Raised)
        self.WhatNextText_E = QTextEdit(self.WhatNextControlFrame_E)
        self.WhatNextText_E.setObjectName(u"WhatNextText_E")
        self.WhatNextText_E.setGeometry(QRect(0, 0, 405, 25))
        self.WhatNextText_E.setFont(font1)
        self.WhatNextText_E.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.WhatNextText_E.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_E.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.WhatNextText_E.setReadOnly(True)
        self.GoToImportProjectTab_E = QPushButton(self.WhatNextControlFrame_E)
        self.GoToImportProjectTab_E.setObjectName(u"GoToImportProjectTab_E")
        self.GoToImportProjectTab_E.setGeometry(QRect(10, 35, 80, 30))
        self.GoToImportProjectTab_E.setFont(font1)
        self.GoToImportProjectTab_E.setStyleSheet(u"QPushButton {\n"
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
        self.GoToFiducialsTab_E = QPushButton(self.WhatNextControlFrame_E)
        self.GoToFiducialsTab_E.setObjectName(u"GoToFiducialsTab_E")
        self.GoToFiducialsTab_E.setGeometry(QRect(95, 35, 90, 30))
        self.GoToFiducialsTab_E.setFont(font1)
        self.GoToFiducialsTab_E.setStyleSheet(u"QPushButton {\n"
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
        self.GoToJobStatusTab_E = QPushButton(self.WhatNextControlFrame_E)
        self.GoToJobStatusTab_E.setObjectName(u"GoToJobStatusTab_E")
        self.GoToJobStatusTab_E.setGeometry(QRect(275, 35, 57, 30))
        self.GoToJobStatusTab_E.setFont(font1)
        self.GoToJobStatusTab_E.setStyleSheet(u"QPushButton {\n"
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
        self.GoToCoordsTab_E = QPushButton(self.WhatNextControlFrame_E)
        self.GoToCoordsTab_E.setObjectName(u"GoToCoordsTab_E")
        self.GoToCoordsTab_E.setGeometry(QRect(190, 35, 80, 30))
        self.GoToCoordsTab_E.setFont(font1)
        self.GoToCoordsTab_E.setStyleSheet(u"QPushButton {\n"
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
        self.CloseNavigationButton_E = QPushButton(self.WhatNextControlFrame_E)
        self.CloseNavigationButton_E.setObjectName(u"CloseNavigationButton_E")
        self.CloseNavigationButton_E.setGeometry(QRect(337, 35, 58, 30))
        self.CloseNavigationButton_E.setFont(font1)
        self.CloseNavigationButton_E.setStyleSheet(u"QPushButton {\n"
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
        self.ElasticRegisteredImageDisplayFrame = QFrame(self.tab)
        self.ElasticRegisteredImageDisplayFrame.setObjectName(u"ElasticRegisteredImageDisplayFrame")
        self.ElasticRegisteredImageDisplayFrame.setGeometry(QRect(425, 50, 400, 451))
        self.ElasticRegisteredImageDisplayFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"}")
        self.ElasticRegisteredImageDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.ElasticRegisteredImageDisplayFrame.setFrameShadow(QFrame.Raised)
        self.ElasticRegisteredImageFrameHeaderText = QLabel(self.tab)
        self.ElasticRegisteredImageFrameHeaderText.setObjectName(u"ElasticRegisteredImageFrameHeaderText")
        self.ElasticRegisteredImageFrameHeaderText.setGeometry(QRect(422, 20, 400, 24))
        self.ElasticRegisteredImageFrameHeaderText.setFont(font6)
        self.ElasticRegisteredImageFrameHeaderText.setStyleSheet(u"QLabel { \n"
"	background-color: transparent;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 0px solid #e6e6e6; /* Border  */\n"
"    qproperty-alignment: 'AlignCenter';\n"
"}")
        self.QuitElasticRegistrationButton = QPushButton(self.tab)
        self.QuitElasticRegistrationButton.setObjectName(u"QuitElasticRegistrationButton")
        self.QuitElasticRegistrationButton.setGeometry(QRect(670, 560, 161, 30))
        self.QuitElasticRegistrationButton.setFont(font1)
        self.QuitElasticRegistrationButton.setStyleSheet(u"QPushButton {\n"
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
        self.NavigationButton_E = QPushButton(self.tab)
        self.NavigationButton_E.setObjectName(u"NavigationButton_E")
        self.NavigationButton_E.setGeometry(QRect(370, 560, 75, 30))
        self.NavigationButton_E.setFont(font1)
        self.NavigationButton_E.setStyleSheet(u"QPushButton {\n"
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
        self.ElasticRegistrationControlsFrame = QFrame(self.tab)
        self.ElasticRegistrationControlsFrame.setObjectName(u"ElasticRegistrationControlsFrame")
        self.ElasticRegistrationControlsFrame.setGeometry(QRect(10, 570, 345, 110))
        self.ElasticRegistrationControlsFrame.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ElasticRegistrationControlsFrame.setFrameShape(QFrame.StyledPanel)
        self.ElasticRegistrationControlsFrame.setFrameShadow(QFrame.Raised)
        self.ElasticRegistrationHeaderText = QTextEdit(self.ElasticRegistrationControlsFrame)
        self.ElasticRegistrationHeaderText.setObjectName(u"ElasticRegistrationHeaderText")
        self.ElasticRegistrationHeaderText.setGeometry(QRect(0, 0, 345, 25))
        self.ElasticRegistrationHeaderText.setFont(font)
        self.ElasticRegistrationHeaderText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ElasticRegistrationHeaderText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ElasticRegistrationHeaderText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ElasticRegistrationHeaderText.setReadOnly(True)
        self.GrowTileSpacingButton = QPushButton(self.ElasticRegistrationControlsFrame)
        self.GrowTileSpacingButton.setObjectName(u"GrowTileSpacingButton")
        self.GrowTileSpacingButton.setGeometry(QRect(120, 76, 25, 25))
        self.GrowTileSpacingButton.setFont(font1)
        self.GrowTileSpacingButton.setStyleSheet(u"QPushButton {\n"
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
        self.ShrinkTileSpacingButton = QPushButton(self.ElasticRegistrationControlsFrame)
        self.ShrinkTileSpacingButton.setObjectName(u"ShrinkTileSpacingButton")
        self.ShrinkTileSpacingButton.setGeometry(QRect(90, 76, 25, 25))
        self.ShrinkTileSpacingButton.setFont(font1)
        self.ShrinkTileSpacingButton.setStyleSheet(u"QPushButton {\n"
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
        self.GrowTileSizeButton = QPushButton(self.ElasticRegistrationControlsFrame)
        self.GrowTileSizeButton.setObjectName(u"GrowTileSizeButton")
        self.GrowTileSizeButton.setGeometry(QRect(120, 37, 25, 25))
        self.GrowTileSizeButton.setFont(font1)
        self.GrowTileSizeButton.setStyleSheet(u"QPushButton {\n"
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
        self.ShrinkTileSizeButton = QPushButton(self.ElasticRegistrationControlsFrame)
        self.ShrinkTileSizeButton.setObjectName(u"ShrinkTileSizeButton")
        self.ShrinkTileSizeButton.setGeometry(QRect(90, 37, 25, 25))
        self.ShrinkTileSizeButton.setFont(font1)
        self.ShrinkTileSizeButton.setStyleSheet(u"QPushButton {\n"
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
        self.CalculateElasticRegistrationButton = QPushButton(self.ElasticRegistrationControlsFrame)
        self.CalculateElasticRegistrationButton.setObjectName(u"CalculateElasticRegistrationButton")
        self.CalculateElasticRegistrationButton.setGeometry(QRect(160, 73, 70, 30))
        self.CalculateElasticRegistrationButton.setFont(font1)
        self.CalculateElasticRegistrationButton.setStyleSheet(u"QPushButton {\n"
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
        self.TileSizeText = QTextEdit(self.ElasticRegistrationControlsFrame)
        self.TileSizeText.setObjectName(u"TileSizeText")
        self.TileSizeText.setGeometry(QRect(25, 30, 60, 40))
        self.TileSizeText.setFont(font5)
        self.TileSizeText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.TileSizeText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.TileSizeText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.TileSizeText.setReadOnly(True)
        self.TileSpacingText = QTextEdit(self.ElasticRegistrationControlsFrame)
        self.TileSpacingText.setObjectName(u"TileSpacingText")
        self.TileSpacingText.setGeometry(QRect(5, 70, 80, 38))
        self.TileSpacingText.setFont(font5)
        self.TileSpacingText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #4b4b4b; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.TileSpacingText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.TileSpacingText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.TileSpacingText.setReadOnly(True)
        self.ColorSquaresButton = QPushButton(self.ElasticRegistrationControlsFrame)
        self.ColorSquaresButton.setObjectName(u"ColorSquaresButton")
        self.ColorSquaresButton.setGeometry(QRect(160, 34, 45, 30))
        self.ColorSquaresButton.setFont(font1)
        self.ColorSquaresButton.setStyleSheet(u"QPushButton {\n"
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
        self.GrowSquareLineButton = QPushButton(self.ElasticRegistrationControlsFrame)
        self.GrowSquareLineButton.setObjectName(u"GrowSquareLineButton")
        self.GrowSquareLineButton.setGeometry(QRect(240, 37, 25, 25))
        self.GrowSquareLineButton.setFont(font1)
        self.GrowSquareLineButton.setStyleSheet(u"QPushButton {\n"
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
        self.ShrinkSquareLineButton = QPushButton(self.ElasticRegistrationControlsFrame)
        self.ShrinkSquareLineButton.setObjectName(u"ShrinkSquareLineButton")
        self.ShrinkSquareLineButton.setGeometry(QRect(210, 37, 25, 25))
        self.ShrinkSquareLineButton.setFont(font1)
        self.ShrinkSquareLineButton.setStyleSheet(u"QPushButton {\n"
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
        self.ViewElasticCheckBox = QCheckBox(self.ElasticRegistrationControlsFrame)
        self.ViewElasticCheckBox.setObjectName(u"ViewElasticCheckBox")
        self.ViewElasticCheckBox.setGeometry(QRect(240, 70, 75, 30))
        self.ViewElasticCheckBox.setFont(font3)
        self.ViewElasticCheckBox.setStyleSheet(u"QCheckBox {\n"
"    background-color: #4b4b4b;\n"
"    color: #e6e6e6; /* Text color */\n"
"    padding: 2px; /* Optional: space around the text */\n"
"	width: 100px; /* Optional: Adjust width to allow for wrapping */\n"
"    word-wrap: break-word; /* Enable word wrap */\n"
"}\n"
"")
        self.TileSizeText.raise_()
        self.TileSpacingText.raise_()
        self.ElasticRegistrationHeaderText.raise_()
        self.GrowTileSpacingButton.raise_()
        self.ShrinkTileSpacingButton.raise_()
        self.GrowTileSizeButton.raise_()
        self.ShrinkTileSizeButton.raise_()
        self.CalculateElasticRegistrationButton.raise_()
        self.ColorSquaresButton.raise_()
        self.GrowSquareLineButton.raise_()
        self.ShrinkSquareLineButton.raise_()
        self.ViewElasticCheckBox.raise_()
        self.SaveRegistrationControlFrame_E = QFrame(self.tab)
        self.SaveRegistrationControlFrame_E.setObjectName(u"SaveRegistrationControlFrame_E")
        self.SaveRegistrationControlFrame_E.setGeometry(QRect(255, 510, 100, 75))
        self.SaveRegistrationControlFrame_E.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.SaveRegistrationControlFrame_E.setFrameShape(QFrame.StyledPanel)
        self.SaveRegistrationControlFrame_E.setFrameShadow(QFrame.Raised)
        self.SaveRegistrationHeaderText_E = QTextEdit(self.SaveRegistrationControlFrame_E)
        self.SaveRegistrationHeaderText_E.setObjectName(u"SaveRegistrationHeaderText_E")
        self.SaveRegistrationHeaderText_E.setGeometry(QRect(0, 0, 100, 25))
        self.SaveRegistrationHeaderText_E.setFont(font)
        self.SaveRegistrationHeaderText_E.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.SaveRegistrationHeaderText_E.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SaveRegistrationHeaderText_E.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.SaveRegistrationHeaderText_E.setReadOnly(True)
        self.SaveRegistrationResultsButton_E = QPushButton(self.SaveRegistrationControlFrame_E)
        self.SaveRegistrationResultsButton_E.setObjectName(u"SaveRegistrationResultsButton_E")
        self.SaveRegistrationResultsButton_E.setGeometry(QRect(10, 35, 35, 30))
        self.SaveRegistrationResultsButton_E.setFont(font1)
        self.SaveRegistrationResultsButton_E.setStyleSheet(u"QPushButton {\n"
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
        self.ReturnToFiducialsTab_E = QPushButton(self.SaveRegistrationControlFrame_E)
        self.ReturnToFiducialsTab_E.setObjectName(u"ReturnToFiducialsTab_E")
        self.ReturnToFiducialsTab_E.setGeometry(QRect(50, 35, 35, 30))
        self.ReturnToFiducialsTab_E.setFont(font1)
        self.ReturnToFiducialsTab_E.setStyleSheet(u"QPushButton {\n"
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
        self.ImageViewControlsFrame_E = QFrame(self.tab)
        self.ImageViewControlsFrame_E.setObjectName(u"ImageViewControlsFrame_E")
        self.ImageViewControlsFrame_E.setGeometry(QRect(10, 510, 235, 75))
        self.ImageViewControlsFrame_E.setStyleSheet(u"QFrame { \n"
"	background-color: #4b4b4b;\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ImageViewControlsFrame_E.setFrameShape(QFrame.StyledPanel)
        self.ImageViewControlsFrame_E.setFrameShadow(QFrame.Raised)
        self.ImageViewFrameHeaderText_E = QTextEdit(self.ImageViewControlsFrame_E)
        self.ImageViewFrameHeaderText_E.setObjectName(u"ImageViewFrameHeaderText_E")
        self.ImageViewFrameHeaderText_E.setGeometry(QRect(0, 0, 235, 25))
        self.ImageViewFrameHeaderText_E.setFont(font)
        self.ImageViewFrameHeaderText_E.setStyleSheet(u"QTextEdit { \n"
"	background-color: #4b4b4b;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ImageViewFrameHeaderText_E.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ImageViewFrameHeaderText_E.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ImageViewFrameHeaderText_E.setReadOnly(True)
        self.GrowFiducialButton2_E = QPushButton(self.ImageViewControlsFrame_E)
        self.GrowFiducialButton2_E.setObjectName(u"GrowFiducialButton2_E")
        self.GrowFiducialButton2_E.setGeometry(QRect(200, 38, 25, 25))
        self.GrowFiducialButton2_E.setFont(font1)
        self.GrowFiducialButton2_E.setStyleSheet(u"QPushButton {\n"
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
        self.ColorFiducialButton_E = QPushButton(self.ImageViewControlsFrame_E)
        self.ColorFiducialButton_E.setObjectName(u"ColorFiducialButton_E")
        self.ColorFiducialButton_E.setGeometry(QRect(10, 35, 45, 30))
        self.ColorFiducialButton_E.setFont(font1)
        self.ColorFiducialButton_E.setStyleSheet(u"QPushButton {\n"
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
        self.ShrinkFiducialButton2_E = QPushButton(self.ImageViewControlsFrame_E)
        self.ShrinkFiducialButton2_E.setObjectName(u"ShrinkFiducialButton2_E")
        self.ShrinkFiducialButton2_E.setGeometry(QRect(170, 38, 25, 25))
        self.ShrinkFiducialButton2_E.setFont(font1)
        self.ShrinkFiducialButton2_E.setStyleSheet(u"QPushButton {\n"
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
        self.ColorFiducialButton2_E = QPushButton(self.ImageViewControlsFrame_E)
        self.ColorFiducialButton2_E.setObjectName(u"ColorFiducialButton2_E")
        self.ColorFiducialButton2_E.setGeometry(QRect(120, 35, 45, 30))
        self.ColorFiducialButton2_E.setFont(font1)
        self.ColorFiducialButton2_E.setStyleSheet(u"QPushButton {\n"
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
        self.GrowFiducialButton_E = QPushButton(self.ImageViewControlsFrame_E)
        self.GrowFiducialButton_E.setObjectName(u"GrowFiducialButton_E")
        self.GrowFiducialButton_E.setGeometry(QRect(90, 38, 25, 25))
        self.GrowFiducialButton_E.setFont(font1)
        self.GrowFiducialButton_E.setStyleSheet(u"QPushButton {\n"
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
        self.ShrinkFiducialButton_E = QPushButton(self.ImageViewControlsFrame_E)
        self.ShrinkFiducialButton_E.setObjectName(u"ShrinkFiducialButton_E")
        self.ShrinkFiducialButton_E.setGeometry(QRect(60, 38, 25, 25))
        self.ShrinkFiducialButton_E.setFont(font1)
        self.ShrinkFiducialButton_E.setStyleSheet(u"QPushButton {\n"
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
        self.DisableFrame_E1 = QFrame(self.tab)
        self.DisableFrame_E1.setObjectName(u"DisableFrame_E1")
        self.DisableFrame_E1.setGeometry(QRect(460, 540, 31, 31))
        self.DisableFrame_E1.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_2 = QFrame(self.DisableFrame_E1)
        self.DisableFrame_E1_2.setObjectName(u"DisableFrame_E1_2")
        self.DisableFrame_E1_2.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_2.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_2.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_2.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E = QFrame(self.tab)
        self.ClockFrame_E.setObjectName(u"ClockFrame_E")
        self.ClockFrame_E.setGeometry(QRect(620, 540, 20, 15))
        self.ClockFrame_E.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_8 = QFrame(self.ClockFrame_E)
        self.DisableFrame_E1_8.setObjectName(u"DisableFrame_E1_8")
        self.DisableFrame_E1_8.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_8.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_8.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_8.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_2 = QFrame(self.ClockFrame_E)
        self.ClockFrame_E1_2.setObjectName(u"ClockFrame_E1_2")
        self.ClockFrame_E1_2.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_2.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_2.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_2.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_10 = QFrame(self.ClockFrame_E1_2)
        self.DisableFrame_E1_10.setObjectName(u"DisableFrame_E1_10")
        self.DisableFrame_E1_10.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_10.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_10.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_10.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_3 = QFrame(self.ClockFrame_E1_2)
        self.ClockFrame_E1_3.setObjectName(u"ClockFrame_E1_3")
        self.ClockFrame_E1_3.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_3.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_3.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_3.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_11 = QFrame(self.ClockFrame_E1_3)
        self.DisableFrame_E1_11.setObjectName(u"DisableFrame_E1_11")
        self.DisableFrame_E1_11.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_11.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_11.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_11.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_4 = QFrame(self.ClockFrame_E1_3)
        self.ClockFrame_E1_4.setObjectName(u"ClockFrame_E1_4")
        self.ClockFrame_E1_4.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_4.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_4.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_4.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_12 = QFrame(self.ClockFrame_E1_4)
        self.DisableFrame_E1_12.setObjectName(u"DisableFrame_E1_12")
        self.DisableFrame_E1_12.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_12.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_12.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_12.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_5 = QFrame(self.ClockFrame_E1_4)
        self.ClockFrame_E1_5.setObjectName(u"ClockFrame_E1_5")
        self.ClockFrame_E1_5.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_5.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_5.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_5.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_13 = QFrame(self.ClockFrame_E1_5)
        self.DisableFrame_E1_13.setObjectName(u"DisableFrame_E1_13")
        self.DisableFrame_E1_13.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_13.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_13.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_13.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_6 = QFrame(self.ClockFrame_E1_5)
        self.ClockFrame_E1_6.setObjectName(u"ClockFrame_E1_6")
        self.ClockFrame_E1_6.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_6.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_6.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_6.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_14 = QFrame(self.ClockFrame_E1_6)
        self.DisableFrame_E1_14.setObjectName(u"DisableFrame_E1_14")
        self.DisableFrame_E1_14.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_14.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_14.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_14.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_7 = QFrame(self.ClockFrame_E1_6)
        self.ClockFrame_E1_7.setObjectName(u"ClockFrame_E1_7")
        self.ClockFrame_E1_7.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_7.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_7.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_7.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_15 = QFrame(self.ClockFrame_E1_7)
        self.DisableFrame_E1_15.setObjectName(u"DisableFrame_E1_15")
        self.DisableFrame_E1_15.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_15.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_15.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_15.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_8 = QFrame(self.ClockFrame_E1_7)
        self.ClockFrame_E1_8.setObjectName(u"ClockFrame_E1_8")
        self.ClockFrame_E1_8.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_8.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_8.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_8.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_16 = QFrame(self.ClockFrame_E1_8)
        self.DisableFrame_E1_16.setObjectName(u"DisableFrame_E1_16")
        self.DisableFrame_E1_16.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_16.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_16.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_16.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_9 = QFrame(self.ClockFrame_E1_8)
        self.ClockFrame_E1_9.setObjectName(u"ClockFrame_E1_9")
        self.ClockFrame_E1_9.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_9.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_9.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_9.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_17 = QFrame(self.ClockFrame_E1_9)
        self.DisableFrame_E1_17.setObjectName(u"DisableFrame_E1_17")
        self.DisableFrame_E1_17.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_17.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_17.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_17.setFrameShadow(QFrame.Raised)
        self.ClockFrame_E1_10 = QFrame(self.ClockFrame_E1_9)
        self.ClockFrame_E1_10.setObjectName(u"ClockFrame_E1_10")
        self.ClockFrame_E1_10.setGeometry(QRect(0, 20, 20, 15))
        self.ClockFrame_E1_10.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.ClockFrame_E1_10.setFrameShape(QFrame.StyledPanel)
        self.ClockFrame_E1_10.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_18 = QFrame(self.ClockFrame_E1_10)
        self.DisableFrame_E1_18.setObjectName(u"DisableFrame_E1_18")
        self.DisableFrame_E1_18.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_18.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_18.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_18.setFrameShadow(QFrame.Raised)
        self.CalculatingElasticRegistrationText = QTextEdit(self.tab)
        self.CalculatingElasticRegistrationText.setObjectName(u"CalculatingElasticRegistrationText")
        self.CalculatingElasticRegistrationText.setGeometry(QRect(510, 510, 320, 24))
        self.CalculatingElasticRegistrationText.setStyleSheet(u"QTextEdit { \n"
"	background-color: #323232;\n"
"	color: #e6e6e6; /* Text color */\n"
"	border: 1px solid #323232; /* Border  */\n"
"    border-radius: 5px; /* Optional: Rounded corners */\n"
"}")
        self.CalculatingElasticRegistrationText.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CalculatingElasticRegistrationText.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.CalculatingElasticRegistrationText.setReadOnly(True)
        self.DisableFrame_E2 = QFrame(self.tab)
        self.DisableFrame_E2.setObjectName(u"DisableFrame_E2")
        self.DisableFrame_E2.setGeometry(QRect(500, 540, 31, 31))
        self.DisableFrame_E2.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E2.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E2.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_5 = QFrame(self.DisableFrame_E2)
        self.DisableFrame_E1_5.setObjectName(u"DisableFrame_E1_5")
        self.DisableFrame_E1_5.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_5.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_5.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_5.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E3 = QFrame(self.tab)
        self.DisableFrame_E3.setObjectName(u"DisableFrame_E3")
        self.DisableFrame_E3.setGeometry(QRect(540, 540, 31, 31))
        self.DisableFrame_E3.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E3.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E3.setFrameShadow(QFrame.Raised)
        self.DisableFrame_E1_9 = QFrame(self.DisableFrame_E3)
        self.DisableFrame_E1_9.setObjectName(u"DisableFrame_E1_9")
        self.DisableFrame_E1_9.setGeometry(QRect(-190, 30, 31, 31))
        self.DisableFrame_E1_9.setStyleSheet(u"QFrame { \n"
"	background-color: rgba(255, 255, 255, 0.4);\n"
"	border: 1px solid #e6e6e6; /* Border  */\n"
"}")
        self.DisableFrame_E1_9.setFrameShape(QFrame.StyledPanel)
        self.DisableFrame_E1_9.setFrameShadow(QFrame.Raised)
        self.tabWidget.addTab(self.tab, "")
        self.CalculatingElasticRegistrationText.raise_()
        self.ImageViewControlsFrame_E.raise_()
        self.SaveRegistrationControlFrame_E.raise_()
        self.FiducialRegisteredImageBorder.raise_()
        self.FiducialRegisteredImageDisplayFrame.raise_()
        self.FiducialRegisteredImageFrameHeaderText.raise_()
        self.ElasticRegisteredImageBorder.raise_()
        self.WhatNextControlFrame_E.raise_()
        self.ElasticRegisteredImageDisplayFrame.raise_()
        self.ElasticRegisteredImageFrameHeaderText.raise_()
        self.QuitElasticRegistrationButton.raise_()
        self.NavigationButton_E.raise_()
        self.ElasticRegistrationControlsFrame.raise_()
        self.ClockFrame_E.raise_()
        self.DisableFrame_E1.raise_()
        self.DisableFrame_E2.raise_()
        self.DisableFrame_E3.raise_()
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(5)


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
        self.NavigationButton.setText(QCoreApplication.translate("MainWindow", u"Navigate", None))
        self.WhatNextText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">App Navigation</p></body></html>", None))
        self.GoToImportProjectTab.setText(QCoreApplication.translate("MainWindow", u"Define Job", None))
        self.GoToFiducialsTab.setText(QCoreApplication.translate("MainWindow", u"Pick Fiducials", None))
        self.GoToJobStatusTab.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.GoToCoordsTab.setText(QCoreApplication.translate("MainWindow", u"Align Data", None))
        self.CloseNavigationButton.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ImportProjectTabName), QCoreApplication.translate("MainWindow", u"Define Job", None))
        self.LoadNewMovingImageButton.setText(QCoreApplication.translate("MainWindow", u"Load Image", None))
        self.LoadOldMovingImageButton.setText(QCoreApplication.translate("MainWindow", u"Load Image", None))
        self.MovingImagesText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt; font-weight:600;\">Register Moving Image</span></p></body></html>", None))
        self.OldMovingImagesText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt; font-weight:600;\">Re-register Moving Image</span></p></body></html>", None))
        self.FiducialFrameHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Fiducial Point View</span></p></body></html>", None))
        self.AddFiducialButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.ColorFiducialButton.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.ShrinkFiducialButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.GrowFiducialButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.DeleteAllButton.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.FiducialTabUpdateText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Calculating Point Cloud Registration. Please Wait...</span></p></body></html>", None))
        self.MovingImageBorder.setText("")
        self.FixedImageFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u" Fixed Image", None))
        self.MovingImageFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u" Moving Image", None))
        self.FixedImageBorder.setText("")
        self.PickNewMovingImageButton.setText(QCoreApplication.translate("MainWindow", u"View New Image", None))
        self.AttemptICPRegistrationButton.setText(QCoreApplication.translate("MainWindow", u"Register Points", None))
        self.NavigationButton_F.setText(QCoreApplication.translate("MainWindow", u"Navigate", None))
        self.WhatNextText_F.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">App Navigation</p></body></html>", None))
        self.GoToImportProjectTab_F.setText(QCoreApplication.translate("MainWindow", u"Define Job", None))
        self.GoToFiducialsTab_F.setText(QCoreApplication.translate("MainWindow", u"Pick Fiducials", None))
        self.GoToJobStatusTab_F.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.GoToCoordsTab_F.setText(QCoreApplication.translate("MainWindow", u"Align Data", None))
        self.CloseNavigationButton_F.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AddFiducialsTabName), QCoreApplication.translate("MainWindow", u"Pick Fiducials", None))
        self.RegisterCoordsFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u"Unregistered Moving Image", None))
        self.RegisterCoordsImageBorder.setText("")
        self.ImageViewFrameHeaderText_C.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Fiducial Point View</span></p></body></html>", None))
        self.ColorFiducialButton_C.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.GrowFiducialButton_C.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ShrinkFiducialButton_C.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.RegisterCoordinatesTableHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Define Coordinates to Register</span></p></body></html>", None))
        self.chooseCoordinatesFileButton.setText("")
        self.BrowseForCoordinatesFileText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Browse for Coordinates File</p></body></html>", None))
        self.CorrespondingImageText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Corresponding Image</p></body></html>", None))
        self.LoadCoordinatesButton.setText(QCoreApplication.translate("MainWindow", u"Load ", None))
        self.CoordinatesOverlayHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Confirm Coordinates Overlay</span></p></body></html>", None))
        self.SwapXYButton.setText(QCoreApplication.translate("MainWindow", u"Swap XY", None))
        self.EditTableButton.setText(QCoreApplication.translate("MainWindow", u"Edit Table", None))
        self.UnregisteredMovingCheckBox.setText(QCoreApplication.translate("MainWindow", u"Looks Good?", None))
        self.ViewFixedButton.setText(QCoreApplication.translate("MainWindow", u"Fixed", None))
        self.RegisteredMovingCheckBox.setText(QCoreApplication.translate("MainWindow", u"Looks Good?", None))
        self.ViewUnregisteredMovingButton.setText(QCoreApplication.translate("MainWindow", u"Unregistered Moving", None))
        self.FixedCheckBox.setText(QCoreApplication.translate("MainWindow", u"Looks Good?", None))
        self.ViewRegisteredMovingButton.setText(QCoreApplication.translate("MainWindow", u"Registered Moving", None))
        self.SaveRegisteredCoordinatesButton.setText(QCoreApplication.translate("MainWindow", u"Save Registered Data", None))
        self.NavigationButton_C.setText(QCoreApplication.translate("MainWindow", u"Navigate", None))
        self.PlottingImageText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Plotting Image. Please Wait...</span></p></body></html>", None))
        self.MakingCoordOverlayText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Making the Coordinate Overlay Image. Please Wait...</span></p></body></html>", None))
        self.WhatNextText_C.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">App Navigation</p></body></html>", None))
        self.GoToImportProjectTab_C.setText(QCoreApplication.translate("MainWindow", u"Define Job", None))
        self.GoToFiducialsTab_C.setText(QCoreApplication.translate("MainWindow", u"Pick Fiducials", None))
        self.GoToJobStatusTab_C.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.GoToCoordsTab_C.setText(QCoreApplication.translate("MainWindow", u"Align Data", None))
        self.CloseNavigationButton_C.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ApplyToCoordsTabName), QCoreApplication.translate("MainWindow", u"Align Data", None))
        self.JobStatusHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Job Status for each Moving Image</p></body></html>", None))
        self.NavigationButton_J.setText(QCoreApplication.translate("MainWindow", u"Navigate", None))
        self.WhatNextText_J.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">App Navigation</p></body></html>", None))
        self.GoToImportProjectTab_J.setText(QCoreApplication.translate("MainWindow", u"Define Job", None))
        self.GoToFiducialsTab_J.setText(QCoreApplication.translate("MainWindow", u"Pick Fiducials", None))
        self.GoToJobStatusTab_J.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.GoToCoordsTab_J.setText(QCoreApplication.translate("MainWindow", u"Align Data", None))
        self.CloseNavigationButton_J.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.JobStatusTabName), QCoreApplication.translate("MainWindow", u"Job Status", None))
        self.SavingRegistrationResultsText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:4.125pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Saving Registration Results. Please Wait...</span></p></body></html>", None))
        self.ImageViewFrameHeaderText_O.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Fiducial Point View</span></p></body></html>", None))
        self.GrowFiducialButton2_O.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ColorFiducialButton_O.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.ShrinkFiducialButton2_O.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.ColorFiducialButton2_O.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.GrowFiducialButton_O.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ShrinkFiducialButton_O.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.UnregisteredImageFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u"Pre-Registration Overlay", None))
        self.RegisteredImageFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u"Post-Registration-Overlay", None))
        self.RegisteredImageBorder.setText("")
        self.UnregisteredImageBorder.setText("")
        self.SaveRegistrationHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Save Results?</span></p></body></html>", None))
        self.SaveRegistrationResultsButton_O.setText(QCoreApplication.translate("MainWindow", u"Yes", None))
        self.ReturnToFiducialsTab_O.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.NavigationButton_O.setText(QCoreApplication.translate("MainWindow", u"Navigate", None))
        self.TryElasticRegButton.setText(QCoreApplication.translate("MainWindow", u"Try Elastic Registration", None))
        self.WhatNextText_O.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">App Navigation</p></body></html>", None))
        self.GoToImportProjectTab_O.setText(QCoreApplication.translate("MainWindow", u"Define Job", None))
        self.GoToFiducialsTab_O.setText(QCoreApplication.translate("MainWindow", u"Pick Fiducials", None))
        self.GoToJobStatusTab_O.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.GoToCoordsTab_O.setText(QCoreApplication.translate("MainWindow", u"Align Data", None))
        self.CloseNavigationButton_O.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ViewOverlaysTabName), QCoreApplication.translate("MainWindow", u"View Overlay", None))
        self.FiducialRegisteredImageFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u"Fiducial Registration Overlay", None))
        self.ElasticRegisteredImageBorder.setText("")
        self.FiducialRegisteredImageBorder.setText("")
        self.WhatNextText_E.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">App Navigation</p></body></html>", None))
        self.GoToImportProjectTab_E.setText(QCoreApplication.translate("MainWindow", u"Define Job", None))
        self.GoToFiducialsTab_E.setText(QCoreApplication.translate("MainWindow", u"Pick Fiducials", None))
        self.GoToJobStatusTab_E.setText(QCoreApplication.translate("MainWindow", u"Status", None))
        self.GoToCoordsTab_E.setText(QCoreApplication.translate("MainWindow", u"Align Data", None))
        self.CloseNavigationButton_E.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.ElasticRegisteredImageFrameHeaderText.setText(QCoreApplication.translate("MainWindow", u"Fiducial + Elastic Registration Overlay", None))
        self.QuitElasticRegistrationButton.setText(QCoreApplication.translate("MainWindow", u"Quit Elastic Registration", None))
        self.NavigationButton_E.setText(QCoreApplication.translate("MainWindow", u"Navigate", None))
        self.ElasticRegistrationHeaderText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Elastic Registration Settings</span></p></body></html>", None))
        self.GrowTileSpacingButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ShrinkTileSpacingButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.GrowTileSizeButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ShrinkTileSizeButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.CalculateElasticRegistrationButton.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
        self.TileSizeText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt; font-weight:600;\">Tile Size: 250</span></p></body></html>", None))
        self.TileSpacingText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"right\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8.25pt; font-weight:600;\">Tile Spacing: 100</span></p></body></html>", None))
        self.ColorSquaresButton.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.GrowSquareLineButton.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ShrinkSquareLineButton.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.ViewElasticCheckBox.setText(QCoreApplication.translate("MainWindow", u"Visible", None))
        self.SaveRegistrationHeaderText_E.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Save Results?</span></p></body></html>", None))
        self.SaveRegistrationResultsButton_E.setText(QCoreApplication.translate("MainWindow", u"Yes", None))
        self.ReturnToFiducialsTab_E.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.ImageViewFrameHeaderText_E.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt;\">Fiducial Point View</span></p></body></html>", None))
        self.GrowFiducialButton2_E.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ColorFiducialButton_E.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.ShrinkFiducialButton2_E.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.ColorFiducialButton2_E.setText(QCoreApplication.translate("MainWindow", u"Color", None))
        self.GrowFiducialButton_E.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.ShrinkFiducialButton_E.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.CalculatingElasticRegistrationText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:4.125pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Calculating Elastic Registration. Please Wait...</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Align Elastic", None))
    # retranslateUi

