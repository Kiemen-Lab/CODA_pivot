"""
Author: Ashley Kiemen (Johns Hopkins)
Date: October 23, 2024
"""
import os
import cv2
import pickle
import numpy as np
import pandas as pd
from PIL import Image
from pandas.io.formats.info import frame_sub_kwargs
from scipy.stats import mode
from datetime import datetime
from PySide6 import QtWidgets
from scipy.spatial import KDTree
from PySide6.QtCore import Qt, QPointF, Signal, QObject, QEvent
from PySide6.QtWidgets import QStyledItemDelegate, QFileDialog, QLabel, QColorDialog, QHeaderView, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from PySide6.QtGui import QPixmap, QTransform, QImage, QPainter, QCursor, QColor, QPen, QMouseEvent

class CustomDelegateTable(QStyledItemDelegate):
    # Define a custom signal
    valueUpdatedTable = Signal(str, int, int)  # Emit new_value, row, and column

    def __init__(self, parent=None):
        super().__init__(parent)

    def setModelData(self, editor, model, index):
        """Capture the value when exiting edit mode."""
        # Retrieve the new value entered by the user
        new_value = editor.text()
        row = index.row()
        column = index.column()

        # Emit the signal with the new value and cell coordinates
        self.valueUpdatedTable.emit(new_value, row, column)
        # print(f"Emitted new fixed value: {new_value} from ({row}, {column})")

        # Call the base class method to set the data in the model
        super().setModelData(editor, model, index)

class ClickableLabel(QLabel):
    doubleClicked = Signal()  # Custom signal for double-click

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleClicked.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Use super() to initialize the parent class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Ensure the main widget is managed in a layout
        layout = QVBoxLayout(self.ui.tabWidget)
        self.ui.centralWidget.setLayout(layout)
        self.setCentralWidget(self.ui.centralWidget)  # Set the central widget
        self.setWindowTitle("CODApivot")

        # app level variables
        self.import_project_tab = 0
        self.fiducials_tab = 1
        self.overlay_tab = 4
        self.apply_to_data_tab = 2
        self.job_status_tab = 3
        self.widget_dimensions = 0
        self.widgets_list = 0
        self.original_width = 0
        self.original_height = 0
        self.scaleCount = 0
        self.padnum = 30
        self.view_key = 0
        self.shift_key = 0
        self.updown_key = 0

        # fixed image variables
        self.ScaleFixed = ""
        self.pthFixed = ""
        self.nmFixed = ""
        # moving image variables
        self.nmMoving = ""
        self.pthMoving = ""
        self.scaleMoving = ""
        self.movingIMS = []
        self.movingIMSlist = []
        self.numMovingDelete = [[], []]
        # job variables
        self.ResultsName = ""
        self.jobFolder = ""
        self.editTableActive = 0

        # current frame variables
        self.current_index = self.import_project_tab
        self.panning = 0  # Flag to indicate if panning is in progress
        self.last_mouse_position = QPointF()  # Track the last position of the mouse
        self.flip_state = False
        self.rotation_angle = 0
        self.brightness = 0
        self.contrast = 1
        self.editWhichImage = 0
        self.editWhichFid = 0
        self.zoom_default = 1
        self.zoom_scale = self.zoom_default
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.rad = 10
        self.ptsColor = QColor(30, 255, 150)  # default color of fiducial points
        self.label = []
        self.border_left = []
        self.border_right = []
        self.text_left = []
        self.text_right = []
        self.frame_left = []
        self.frame_right = []
        self.ColorButton = []
        self.pts = []
        self.pts2 = []
        self.ImageWidth = 0
        self.ImageHeight = 0

        # Fiducials tab variables
        self.imFixed0 = []
        self.imMoving0 = []
        self.nmLoadedFixed = ""
        self.fixed_flip_state = False
        self.fixed_rotation_angle = 0
        self.moving_flip_state = False
        self.moving_rotation_angle = 0
        self.fixed_brightness = 0
        self.moving_brightness = 0
        self.fixed_contrast = 1
        self.moving_contrast = 1
        self.rad_tabF = self.rad  # default size of fiducial points
        self.ptsColor_tabF = self.ptsColor  # default color of fiducial points
        self.fixed_zoom_default = 1
        self.moving_zoom_default = 1
        self.fixed_zoom_scale = self.fixed_zoom_default  # Initialize zoom scale
        self.moving_zoom_scale = self.moving_zoom_default  # Initialize zoom scale
        self.fixed_pan_offset_x = 0
        self.fixed_pan_offset_y = 0
        self.moving_pan_offset_x = 0
        self.moving_pan_offset_y = 0

        # Fiducial point variables
        self.ptsFixed = np.array([[0, 0]], dtype=np.float64)
        self.ptsMoving = np.array([[0, 0]], dtype=np.float64)
        self.add_fiducial_active = False  # Flag to track fiducial selection mode
        self.delete_mode_active = False
        self.potential_deletion = -5

        # Overlay tab variables
        self.RMSE0 = 0
        self.RMSE = 0
        self.tform = 0
        self.flip_im = 0
        self.ptsMovingReg = np.array([[0, 0]], dtype=np.float64)
        self.imMovingReg = []

        # Overlay tab view settings variables
        self.imOverlay0 = []
        self.imOverlay = []
        self.rad_tabO = self.rad_tabF  # default size of fiducial points
        self.rad_tabOb = int(np.ceil(self.rad_tabF * 0.75))  # default size of fiducial points
        self.ptsColor_tabO = self.ptsColor_tabF  # default color of fiducial points
        self.ptsColor_tabOb = self.ptsColor_tabF # default complement color of fiducial points
        self.unregistered_flip_state = False
        self.unregistered_rotation_angle = 0
        self.registered_flip_state = False
        self.registered_rotation_angle = 0
        self.unregistered_brightness = 0
        self.registered_brightness = 0
        self.unregistered_contrast = 1
        self.registered_contrast = 1
        self.unregistered_zoom_default = 1
        self.registered_zoom_default = 1
        self.unregistered_zoom_scale = self.unregistered_zoom_default  # Initialize zoom scale
        self.registered_zoom_scale = self.registered_zoom_default  # Initialize zoom scale
        self.unregistered_pan_offset_x = 0
        self.unregistered_pan_offset_y = 0
        self.registered_pan_offset_x = 0
        self.registered_pan_offset_y = 0
        self.whichColor = 0

        # Apply to coordinates tab variables
        self.all_images_checked = 0
        self.max_points = "1000"
        self.xColumn = 1
        self.yColumn = 1
        self.first_row = 0
        self.pthCoords = ""
        self.nmCoords = ""
        self.pthMovingCoords = ""
        self.nmMovingCoords = ""
        self.nmLoadedMoving = ""
        self.nmCoordsLoaded = ""
        self.Coords = ""
        self.imMovingCoords = []
        self.imMovingCoordsReg = []
        self.imPlotHold = []
        self.numMovingCoords = [[0], [0]]
        self.ScaleCoords = ""
        self.ptsCoords = []
        self.ptsCoordsReg = []
        self.rad_tabC = self.rad_tabF  # default size of fiducial points
        self.ptsColor_tabC = self.ptsColor_tabF  # default color of fiducial points
        self.coords_flip_state = False
        self.coords_rotation_angle = 0
        self.coords_brightness = 0
        self.coords_contrast = 1
        self.coords_zoom_default = 1
        self.coords_zoom_scale = self.coords_zoom_default  # Initialize zoom scale
        self.coords_pan_offset_x = 0
        self.coords_pan_offset_y = 0
        self.tformCoords = []
        self.sampled_indices = []

        # Import project tab Set some initial settings
        self.ui.tabWidget.setCurrentIndex(self.import_project_tab)
        self.ui.fixedImageTableWidget.setHorizontalHeaderLabels(["Filename", "Scale", "Folder"])
        self.ui.movingImageTableWidget.setHorizontalHeaderLabels(["Filename", "Scale", "Folder"])
        self.ui.setJobTableWidget.setHorizontalHeaderLabels(["Results Name", "Folder"])
        self.ui.fixedImageTableWidget.setVerticalHeaderLabels([""])
        self.ui.movingImageTableWidget.setVerticalHeaderLabels(["1"])
        self.ui.setJobTableWidget.setVerticalHeaderLabels([""])
        self.default_model_name()
        self.ui.setJobTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(self.ResultsName))
        self.ui.deleteFixedImageButton.setVisible(False)
        self.ui.deleteMovingImageButton.setVisible(False)
        self.ui.keepFixedImageButton.setVisible(False)
        self.ui.keepMovingImageButton.setVisible(False)
        # Disable all tabs in the QTabWidget
        self.ui.tabWidget.tabBar().installEventFilter(self)
        self.initiate_import_project_tab()

        # initial populate of tables
        self.populate_fixed_table()
        self.populate_moving_table()
        self.populate_project_table()
        # Create and set the custom delegate, connect the delegate's signal to a slot in MainWindow
        self.delegate = CustomDelegateTable(self.ui.fixedImageTableWidget)
        self.ui.fixedImageTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedTable.connect(self.handle_value_update_fixed)

        self.delegate = CustomDelegateTable(self.ui.movingImageTableWidget)
        self.ui.movingImageTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedTable.connect(self.handle_value_update_moving)

        self.delegate = CustomDelegateTable(self.ui.setJobTableWidget)
        self.ui.setJobTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedTable.connect(self.handle_value_update_job)

        self.delegate = CustomDelegateTable(self.ui.RegisterCoordinatesTableWidget)
        self.ui.RegisterCoordinatesTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedTable.connect(self.handle_value_update_coordinates)

        # move some buttons
        self.ui.NavigationButton.setGeometry(745, 640, 75, 30)
        self.ui.NavigationButton_F.setGeometry(745, 640, 75, 30)
        self.ui.NavigationButton_O.setGeometry(745, 640, 75, 30)
        self.ui.NavigationButton_C.setGeometry(745, 640, 75, 30)
        self.ui.NavigationButton_J.setGeometry(745, 640, 75, 30)
        self.ui.SavingRegistrationResultsText.setGeometry(10, 480, 400, 24)
        self.ui.ChooseMovingImageFrame.setGeometry(10, 580, 480, 85)
        self.ui.MakingCoordOverlayText.setGeometry(10, 165, 400, 24)
        self.ui.FixedImageFrameHeaderText.setGeometry(self.ui.UnregisteredImageFrameHeaderText.geometry())
        self.ui.MovingImageFrameHeaderText.setGeometry(self.ui.RegisteredImageFrameHeaderText.geometry())
        self.ui.FixedImageDisplayFrame.setGeometry(self.ui.UnregisteredImageDisplayFrame.geometry())
        self.ui.MovingImageDisplayFrame.setGeometry(self.ui.RegisteredImageDisplayFrame.geometry())
        self.ui.FixedImageBorder.setGeometry(self.ui.UnregisteredImageBorder.geometry())
        self.ui.MovingImageBorder.setGeometry(self.ui.RegisteredImageBorder.geometry())

        # app navigation buttons
        self.ui.NavigationButton.clicked.connect(self.view_navigation_tab)
        self.ui.NavigationButton_F.clicked.connect(self.view_navigation_tab)
        self.ui.NavigationButton_O.clicked.connect(self.view_navigation_tab)
        self.ui.NavigationButton_C.clicked.connect(self.view_navigation_tab)
        self.ui.NavigationButton_J.clicked.connect(self.view_navigation_tab)

        self.ui.CloseNavigationButton.clicked.connect(self.close_navigation_tab)
        self.ui.CloseNavigationButton_F.clicked.connect(self.close_navigation_tab)
        self.ui.CloseNavigationButton_O.clicked.connect(self.close_navigation_tab)
        self.ui.CloseNavigationButton_C.clicked.connect(self.close_navigation_tab)
        self.ui.CloseNavigationButton_J.clicked.connect(self.close_navigation_tab)

        self.ui.GoToImportProjectTab.clicked.connect(self.initiate_import_project_tab)
        self.ui.GoToImportProjectTab_F.clicked.connect(self.initiate_import_project_tab)
        self.ui.GoToImportProjectTab_O.clicked.connect(self.initiate_import_project_tab)
        self.ui.GoToImportProjectTab_C.clicked.connect(self.initiate_import_project_tab)
        self.ui.GoToImportProjectTab_J.clicked.connect(self.initiate_import_project_tab)

        self.ui.GoToFiducialsTab.clicked.connect(self.initiate_fiducials_tab)
        self.ui.GoToFiducialsTab_F.clicked.connect(self.initiate_fiducials_tab)
        self.ui.GoToFiducialsTab_O.clicked.connect(self.initiate_fiducials_tab)
        self.ui.GoToFiducialsTab_C.clicked.connect(self.initiate_fiducials_tab)
        self.ui.GoToFiducialsTab_J.clicked.connect(self.initiate_fiducials_tab)

        self.ui.GoToCoordsTab.clicked.connect(self.initiate_apply_to_coords_tab)
        self.ui.GoToCoordsTab_F.clicked.connect(self.initiate_apply_to_coords_tab)
        self.ui.GoToCoordsTab_O.clicked.connect(self.initiate_apply_to_coords_tab)
        self.ui.GoToCoordsTab_C.clicked.connect(self.initiate_apply_to_coords_tab)
        self.ui.GoToCoordsTab_J.clicked.connect(self.initiate_apply_to_coords_tab)

        self.ui.GoToJobStatusTab.clicked.connect(self.initiate_job_status_tab)
        self.ui.GoToJobStatusTab_F.clicked.connect(self.initiate_job_status_tab)
        self.ui.GoToJobStatusTab_O.clicked.connect(self.initiate_job_status_tab)
        self.ui.GoToJobStatusTab_C.clicked.connect(self.initiate_job_status_tab)
        self.ui.GoToJobStatusTab_J.clicked.connect(self.initiate_job_status_tab)

        # Import project tab what functions to call when a button is clicked
        self.ui.loadTemplateButton.clicked.connect(self.browse_for_template)
        self.ui.chooseFixedImageButton.clicked.connect(self.browse_for_fixed_image)
        self.ui.chooseMovingImageButton.clicked.connect(self.browse_for_moving_image)
        self.ui.chooseJobFolderButton.clicked.connect(self.browse_for_job_folder)
        self.ui.deleteFixedImageButton.clicked.connect(self.delete_fixed_image)
        self.ui.keepFixedImageButton.clicked.connect(self.keep_fixed_image)
        self.ui.deleteMovingImageButton.clicked.connect(self.delete_moving_image)
        self.ui.keepMovingImageButton.clicked.connect(self.keep_moving_image)
        self.ui.fixedImageTableWidget.cellDoubleClicked.connect(self.doubleclick_fixed_table)
        self.ui.movingImageTableWidget.cellDoubleClicked.connect(self.doubleclick_moving_table)
        self.ui.setJobTableWidget.cellDoubleClicked.connect(self.doubleclick_job_table)
        self.ui.JobFolderCheckBox.stateChanged.connect(self.checkbox_changed)

        # Fiducials tab settings
        self.fixed_image_label = ClickableLabel(self.ui.FixedImageDisplayFrame)
        self.fixed_image_label.setScaledContents(True)  # Allow scaling to fit the frame
        self.moving_image_label = ClickableLabel(self.ui.MovingImageDisplayFrame)
        self.moving_image_label.setScaledContents(True)  # Allow scaling to fit the frame

        # Fiducials tab what functions to call when a button is clicked
        self.ui.MovingImagesComboBox.currentIndexChanged.connect(self.new_combobox_selection_changed)
        self.ui.OldMovingImagesComboBox.currentIndexChanged.connect(self.old_combobox_selection_changed)
        self.ui.LoadNewMovingImageButton.clicked.connect(self.load_new_moving_image)
        self.ui.LoadOldMovingImageButton.clicked.connect(self.load_old_moving_image)
        self.ui.PickNewMovingImageButton.clicked.connect(self.confirm_load_new_image)
        # fiducial point settings
        self.ui.AddFiducialButton.clicked.connect(self.toggle_add_fiducial_mode)
        self.ui.ColorFiducialButton.clicked.connect(self.change_fiducial_color)
        self.ui.ShrinkFiducialButton.clicked.connect(self.decrease_fiducial_size)
        self.ui.GrowFiducialButton.clicked.connect(self.increase_fiducial_size)
        self.ui.DeleteAllButton.clicked.connect(self.delete_fiducials)
        self.ui.AttemptICPRegistrationButton.clicked.connect(self.begin_calculate_icp_tabF)

        # Overlay tab settings
        self.ui.DisableFrame_O1.setGeometry(self.ui.ImageViewControlsFrame_O.geometry())
        self.ui.DisableFrame_O2.setGeometry(self.ui.SaveRegistrationControlFrame.geometry())
        self.overlay0_label = ClickableLabel(self.ui.UnregisteredImageDisplayFrame)
        self.overlay0_label.setScaledContents(True)  # Allow scaling to fit the frame
        self.overlay_label = ClickableLabel(self.ui.RegisteredImageDisplayFrame)
        self.overlay_label.setScaledContents(True)  # Allow scaling to fit the frame

        # Overlay tab what functions to call when a button is clicked
        self.ui.ReturnToFiducialsTab_O.clicked.connect(self.return_to_fiducials_tab)
        self.ui.SaveRegistrationResultsButton_O.clicked.connect(self.save_registration_results)


        # fiducial settings overlay tab
        self.ui.ColorFiducialButton_O.clicked.connect(self.call_change_fiducial_color0)
        self.ui.ColorFiducialButton2_O.clicked.connect(self.call_change_fiducial_color1)
        self.ui.ShrinkFiducialButton_O.clicked.connect(self.call_decrease_fiducial_size0)
        self.ui.ShrinkFiducialButton2_O.clicked.connect(self.call_decrease_fiducial_size1)
        self.ui.GrowFiducialButton_O.clicked.connect(self.call_increase_fiducial_size0)
        self.ui.GrowFiducialButton2_O.clicked.connect(self.call_increase_fiducial_size1)

        # Apply to coordinates tab settings
        self.coordinates_label = ClickableLabel(self.ui.RegisterCoordsDisplayFrame)
        self.coordinates_label.setScaledContents(True)  # Allow scaling to fit the frame

        # Apply to coordinates tab what functions to call when a button is clicked
        self.ui.chooseCoordinatesFileButton.clicked.connect(self.browse_for_coordinates_file)
        self.ui.CorrespondingImageComboBox.currentIndexChanged.connect(self.on_combo_box_changed)
        self.ui.RegisterCoordinatesTableWidget.cellDoubleClicked.connect(self.doubleclick_coordinates_table)
        self.ui.LoadCoordinatesButton.clicked.connect(self.load_coordinates_to_register)
        self.ui.SwapXYButton.clicked.connect(self.swap_xy)
        self.ui.EditTableButton.clicked.connect(self.return_to_edit_table)
        self.ui.ViewUnregisteredMovingButton.clicked.connect(self.define_image_unregistered)
        self.ui.ViewRegisteredMovingButton.clicked.connect(self.define_image_registered)
        self.ui.ViewFixedButton.clicked.connect(self.define_image_fixed)
        self.ui.SaveRegisteredCoordinatesButton.clicked.connect(self.save_registered_coordinates)
        self.ui.UnregisteredMovingCheckBox.stateChanged.connect(self.unregistered_coords_checkbox_changed)
        self.ui.RegisteredMovingCheckBox.stateChanged.connect(self.registered_coords_checkbox_changed)
        self.ui.FixedCheckBox.stateChanged.connect(self.fixed_coords_checkbox_changed)

        # fiducial point settings apply to coordinates tab
        self.ui.ColorFiducialButton_C.clicked.connect(self.change_fiducial_color)
        self.ui.ShrinkFiducialButton_C.clicked.connect(self.decrease_fiducial_size)
        self.ui.GrowFiducialButton_C.clicked.connect(self.increase_fiducial_size)

        # button styles
        self.activeButton = """
                        QPushButton {
                            background-color: #5a5a5a;
                            color: #e6e6e6; /* Text color */
                            border: 1px solid #e6e6e6; /* Border */
                            border-radius: 5px; /* Optional: Rounded corners */
                            padding: 5px; /* Optional: Padding around text */
                        }

                        QPushButton:hover {
                            background-color: #666f75; /* Grey-blue when hovered */
                        }

                        QPushButton:pressed {
                            background-color: #7b8e9c; /* More blue when pressed */
                        }
                    """
        self.inactiveButton = """ QPushButton {
                                        background-color: #5a5a5a;
                                        border: 1px solid #424242;
                                        color: #424242;
                                        border-radius: 5px; /* Optional: Rounded corners */
                                        padding: 5px; /* Optional: Padding around text */
                                    }
                                                """
        self.activeLabel = """ QLabel { 
                                        background-color: transparent;
                                        border: 5px solid #40ad40; /* Border  */
                                    }
                                            """

        self.inactiveLabel = """ QLabel { 
                                        background-color: transparent;
                                        border: 3px solid #e6e6e6; /* Border  */
                                    }
                                            """
        self.activeFrame = """ QFrame { 
                                    background-color: #3d4a3d;
                                }
                                            """

        self.inactiveFrame = """ QFrame { 
                                        background-color: #4b4b4b;
                                    }
                                            """
        self.activeTextLabel = """ QLabel { 
                                        background-color: transparent;
                                        color: #40ad40; /* Text color */
                                        border: 0px solid #e6e6e6; /* Border  */
                                        qproperty-alignment: 'AlignCenter';
                                    }
                                            """
        self.inactiveTextLabel = """ QLabel { 
                                            background-color: transparent;
                                            color: #e6e6e6; /* Text color */
                                            border: 0px solid #e6e6e6; /* Border  */
                                            qproperty-alignment: 'AlignCenter';
                                        }
                                                """
        self.style_QuestBox = """
                            QMessageBox {
                                background-color: #414141;  /* Dark background */
                                color: #e6e6e6;            /* Light text */
                                border: 1px solid #e6e6e6; /* Border */
                                border-radius: 5px; /* Optional: Rounded corners */
                            }
                            QMessageBox QLabel {
                                color: #e6e6e6;            /* Custom font color for the message text */
                            }
                            QPushButton {
                                background-color: #4b4b4b; /* Button background */
                                color: #e6e6e6;            /* Light text */
                                border: none;
                                padding: 5px;
                            }
                            QPushButton:hover {
                                background-color: #666f75; /* Grey-blue when hovered */
                            }

                            QPushButton:pressed {
                                background-color: #7b8e9c; /* More blue when pressed */
                            }
                        """

    def eventFilter(self, source, event):
        """
        Intercept events on the tab bar to block mouse clicks on the tab titles.
        """
        if source == self.ui.tabWidget.tabBar() and event.type() == QMouseEvent.MouseButtonPress:
            # Ignore mouse clicks on the tab bar to prevent tab switching
            return True  # Stops the event from propagating further
        return super().eventFilter(source, event)

    def view_navigation_tab(self):
        # button view settings
        self.ui.WhatNextControlFrame.setVisible(True)
        self.ui.WhatNextControlFrame_F.setVisible(True)
        self.ui.WhatNextControlFrame_O.setVisible(True)
        self.ui.WhatNextControlFrame_C.setVisible(True)
        self.ui.WhatNextControlFrame_J.setVisible(True)

        self.ui.NavigationButton.setVisible(False)
        self.ui.NavigationButton_F.setVisible(False)
        self.ui.NavigationButton_O.setVisible(False)
        self.ui.NavigationButton_C.setVisible(False)
        self.ui.NavigationButton_J.setVisible(False)

        if not self.ui.FiducialPointControlsFrame.isVisible():
            self.ui.ChooseMovingImageFrame.setVisible(False)

    def close_navigation_tab(self):
        # button view settings
        self.ui.WhatNextControlFrame.setVisible(False)
        self.ui.WhatNextControlFrame_F.setVisible(False)
        self.ui.WhatNextControlFrame_O.setVisible(False)
        self.ui.WhatNextControlFrame_C.setVisible(False)
        self.ui.WhatNextControlFrame_J.setVisible(False)

        self.ui.NavigationButton.setVisible(True)
        self.ui.NavigationButton_F.setVisible(True)
        self.ui.NavigationButton_O.setVisible(True)
        self.ui.NavigationButton_C.setVisible(True)
        self.ui.NavigationButton_J.setVisible(True)

        if not self.ui.FiducialPointControlsFrame.isVisible():
            self.ui.ChooseMovingImageFrame.setVisible(True)

    def define_edit_frame(self, whichImage=None):

        # current tab
        self.current_index = self.ui.tabWidget.currentIndex()

        if whichImage is None:
            whichImage = self.editWhichImage

        if self.current_index == self.fiducials_tab:
            # point view variables
            self.rad = self.rad_tabF
            self.ptsColor = self.ptsColor_tabF
            self.ColorButton = self.ui.ColorFiducialButton
            # frame variables
            self.border_left = self.ui.FixedImageBorder
            self.border_right = self.ui.MovingImageBorder
            self.text_left = self.ui.FixedImageFrameHeaderText
            self.text_right = self.ui.MovingImageFrameHeaderText
            self.frame_left = self.ui.FixedImageDisplayFrame
            self.frame_right = self.ui.MovingImageDisplayFrame
            if whichImage == 0:  # fixed image
                # image view variables
                self.flip_state = self.fixed_flip_state
                self.rotation_angle = self.fixed_rotation_angle
                self.brightness = self.fixed_brightness
                self.contrast = self.fixed_contrast
                self.zoom_default = self.fixed_zoom_default
                self.zoom_scale = self.fixed_zoom_scale
                self.pan_offset_x = self.fixed_pan_offset_x
                self.pan_offset_y = self.fixed_pan_offset_y
                self.label = self.fixed_image_label
                self.pts = self.ptsFixed
                self.pts2 = []
                try:
                    self.ImageHeight = self.imFixed0.height()
                    self.ImageWidth = self.imFixed0.width()
                except:
                    self.ImageHeight = 0
                    self.ImageWidth = 0
            else:  # moving image
                # image view variables
                self.flip_state = self.moving_flip_state
                self.rotation_angle = self.moving_rotation_angle
                self.brightness = self.moving_brightness
                self.contrast = self.moving_contrast
                self.zoom_default = self.moving_zoom_default
                self.zoom_scale = self.moving_zoom_scale
                self.pan_offset_x = self.moving_pan_offset_x
                self.pan_offset_y = self.moving_pan_offset_y
                self.label = self.moving_image_label
                self.pts = self.ptsMoving
                self.pts2 = []
                try:
                    self.ImageHeight = self.imMoving0.height()
                    self.ImageWidth = self.imMoving0.width()
                except:
                    self.ImageHeight = 0
                    self.ImageWidth = 0
        elif self.current_index == self.overlay_tab:
            # point view variables
            if self.whichColor == 0:
                self.ColorButton = self.ui.ColorFiducialButton_O
                self.ptsColor = self.ptsColor_tabO
                self.rad = self.rad_tabO
            else:
                self.ColorButton = self.ui.ColorFiducialButton2_O
                self.ptsColor = self.ptsColor_tabOb
                self.rad = self.rad_tabOb
            # frame variables
            self.border_left = self.ui.UnregisteredImageBorder
            self.border_right = self.ui.RegisteredImageBorder
            self.text_left = self.ui.UnregisteredImageFrameHeaderText
            self.text_right = self.ui.RegisteredImageFrameHeaderText
            self.frame_left = self.ui.UnregisteredImageDisplayFrame
            self.frame_right = self.ui.RegisteredImageDisplayFrame
            try:
                self.ImageHeight = max([self.imFixed0.height(), self.imMoving0.height()])
                self.ImageWidth = max([self.imFixed0.width(), self.imMoving0.width()])
            except:
                self.ImageHeight = 0
                self.ImageWidth = 0
            if whichImage == 0:  # unregistered image
                # image view variables
                self.flip_state = self.unregistered_flip_state
                self.rotation_angle = self.unregistered_rotation_angle
                self.brightness = 0
                self.contrast = 1
                self.zoom_default = self.unregistered_zoom_default
                self.zoom_scale = self.unregistered_zoom_scale
                self.pan_offset_x = self.unregistered_pan_offset_x
                self.pan_offset_y = self.unregistered_pan_offset_y
                self.label = self.overlay0_label
                self.pts = self.ptsFixed
                self.pts2 = self.ptsMoving
            else:  # registered image
                # image view variables
                self.flip_state = self.registered_flip_state
                self.rotation_angle = self.registered_rotation_angle
                self.brightness = 0
                self.contrast = 1
                self.zoom_default = self.registered_zoom_default
                self.zoom_scale = self.registered_zoom_scale
                self.pan_offset_x = self.registered_pan_offset_x
                self.pan_offset_y = self.registered_pan_offset_y
                self.label = self.overlay_label
                self.pts = self.ptsFixed
                self.pts2 = self.ptsMovingReg
        elif self.current_index == self.apply_to_data_tab: # apply to coordinates tab
            # point view variables
            self.rad = self.rad_tabC
            self.ptsColor = self.ptsColor_tabC
            self.ColorButton = self.ui.ColorFiducialButton_C
            # frame variables
            self.border_left = self.ui.RegisterCoordsImageBorder
            self.border_right = self.ui.RegisterCoordsImageBorder
            self.text_left = self.ui.RegisterCoordsFrameHeaderText
            self.text_right = self.ui.RegisterCoordsFrameHeaderText
            self.frame_left = self.ui.RegisterCoordsDisplayFrame
            self.frame_right = self.ui.RegisterCoordsDisplayFrame

            # image view variables
            self.flip_state = self.coords_flip_state
            self.rotation_angle = self.coords_rotation_angle
            self.brightness = self.coords_brightness
            self.contrast = self.coords_contrast
            self.zoom_default = self.coords_zoom_default
            self.zoom_scale = self.coords_zoom_scale
            self.pan_offset_x = self.coords_pan_offset_x
            self.pan_offset_y = self.coords_pan_offset_y
            self.label = self.coordinates_label
            if whichImage == 0:
                self.pts = self.ptsCoords
                try:
                    self.ImageHeight = self.imMovingCoords.height()
                    self.ImageWidth = self.imMovingCoords.width()
                except:
                    self.ImageHeight = 0
                    self.ImageWidth = 0
            elif whichImage == 1:
                self.pts = self.ptsCoordsReg
                try:
                    self.ImageHeight = self.imMovingCoordsReg.height()
                    self.ImageWidth = self.imMovingCoordsReg.width()
                except:
                    self.ImageHeight = 0
                    self.ImageWidth = 0
            else:
                self.pts = self.ptsCoordsReg
                try:
                    self.ImageHeight = self.imFixed0.height()
                    self.ImageWidth = self.imFixed0.width()
                except:
                    self.ImageHeight = 0
                    self.ImageWidth = 0
            self.pts2 = []
        else:
            return

    def return_edit_frame(self, whichImage=None):
        # current tab
        self.current_index = self.ui.tabWidget.currentIndex()

        if whichImage is None:
            whichImage = self.editWhichImage

        if self.current_index == self.fiducials_tab:
            # point view variables
            self.rad_tabF = self.rad
            self.ptsColor_tabF = self.ptsColor
            self.ui.ColorFiducialButton = self.ColorButton
            # frame variables
            self.ui.FixedImageBorder = self.border_left
            self.ui.MovingImageBorder = self.border_right
            self.ui.FixedImageFrameHeaderText = self.text_left
            self.ui.MovingImageFrameHeaderText = self.text_right
            self.ui.FixedImageDisplayFrame = self.frame_left
            self.ui.MovingImageDisplayFrame = self.frame_right

            if whichImage == 0:  # fixed image
                # image view variables
                self.fixed_flip_state = self.flip_state
                self.fixed_rotation_angle = self.rotation_angle
                self.fixed_brightness = self.brightness
                self.fixed_contrast = self.contrast
                self.fixed_zoom_default = self.zoom_default
                self.fixed_zoom_scale = self.zoom_scale
                self.fixed_pan_offset_x = self.pan_offset_x
                self.fixed_pan_offset_y = self.pan_offset_y
            else:  # moving image
                # image view variables
                self.moving_flip_state = self.flip_state
                self.moving_rotation_angle = self.rotation_angle
                self.moving_brightness = self.brightness
                self.moving_contrast = self.contrast
                self.moving_zoom_default = self.zoom_default
                self.moving_zoom_scale = self.zoom_scale
                self.moving_pan_offset_x = self.pan_offset_x
                self.moving_pan_offset_y = self.pan_offset_y

        elif self.current_index == self.overlay_tab:
            # point view variables
            if self.whichColor == 0:
                self.ptsColor_tabO = self.ptsColor
                self.ui.ColorFiducialButton_O = self.ColorButton
                self.rad_tabO = self.rad
            else:
                self.ptsColor_tabOb = self.ptsColor
                self.ui.ColorFiducialButton2_O = self.ColorButton
                self.rad_tabOb = self.rad
            # frame variables
            self.ui.UnregisteredImageBorder = self.border_left
            self.ui.RegisteredImageBorder = self.border_right
            self.ui.UnregisteredImageFrameHeaderText = self.text_left
            self.ui.RegisteredImageFrameHeaderText = self.text_right
            self.ui.UnregisteredImageDisplayFrame = self.frame_left
            self.ui.RegisteredImageDisplayFrame = self.frame_right

            if whichImage == 0:  # unregistered image
                # image view variables
                self.unregistered_flip_state = self.flip_state
                self.unregistered_rotation_angle = self.rotation_angle
                self.unregistered_zoom_default = self.zoom_default
                self.unregistered_zoom_scale = self.zoom_scale
                self.unregistered_pan_offset_x = self.pan_offset_x
                self.unregistered_pan_offset_y = self.pan_offset_y
            else:  # registered image
                # image view variables
                self.registered_flip_state = self.flip_state
                self.registered_rotation_angle = self.rotation_angle
                self.registered_zoom_default = self.zoom_default
                self.registered_zoom_scale = self.zoom_scale
                self.registered_pan_offset_x = self.pan_offset_x
                self.registered_pan_offset_y = self.pan_offset_y
        elif self.current_index == self.apply_to_data_tab:
            # point view variables
            self.rad_tabC = self.rad
            self.ptsColor_tabC = self.ptsColor
            self.ui.ColorFiducialButton_C = self.ColorButton
            # frame variables
            self.ui.RegisterCoordsImageBorder = self.border_left
            self.ui.RegisterCoordsFrameHeaderText = self.text_left
            self.ui.RegisterCoordsDisplayFrame = self.frame_left

            # image view variables
            self.coords_flip_state = self.flip_state
            self.coords_rotation_angle = self.rotation_angle
            self.coords_brightness = self.brightness
            self.coords_contrast = self.contrast
            self.coords_zoom_default = self.zoom_default
            self.coords_zoom_scale = self.zoom_scale
            self.coords_pan_offset_x = self.pan_offset_x
            self.coords_pan_offset_y = self.pan_offset_y
        else:
            return

    def delete_fiducials(self):

        # Exit fiducial and zoom / pan mode if necessary
        if self.add_fiducial_active:
            self.toggle_add_fiducial_mode()

        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("Delete fiducial pairs?")  # Set the window title
        msg_box.setText("Would you like to delete one point or all points?")  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        delete_one_button = msg_box.addButton("Delete One", QtWidgets.QMessageBox.ActionRole)
        delete_all_button = msg_box.addButton("Delete All", QtWidgets.QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QtWidgets.QMessageBox.Cancel)
        msg_box.setStyleSheet(self.style_QuestBox)

        # Show the message box and get the user's response
        response = msg_box.exec()

        # Handle the response
        if msg_box.clickedButton() == delete_one_button:
            self.delete_one_point()
        elif msg_box.clickedButton() == delete_all_button:
            self.delete_all_points()
        elif response == cancel_button:
            return

    def delete_one_point(self):
        # set labels to inactive
        self.ui.FixedImageBorder.setStyleSheet(self.inactiveLabel)
        self.ui.FixedImageFrameHeaderText.setStyleSheet(self.inactiveTextLabel)
        self.ui.FixedImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        tmp = self.ui.FixedImageDisplayFrame.geometry()
        self.ui.FixedImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
        self.ui.MovingImageBorder.setStyleSheet(self.inactiveLabel)
        self.ui.MovingImageFrameHeaderText.setStyleSheet(self.inactiveTextLabel)
        self.ui.MovingImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        tmp = self.ui.MovingImageDisplayFrame.geometry()
        self.ui.MovingImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)

        # set cursor to active
        self.delete_mode_active = True
        crosshair_cursor = self.create_large_crosshair_cursor()
        self.setCursor(crosshair_cursor)

    def delete_all_points(self):

        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("Confirm deletion")  # Set the window title
        msg_box.setText("Are you sure you want to delete ALL fiducial points?")  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons
        msg_box.setStyleSheet(self.style_QuestBox)

        # Show the message box and get the response
        response = msg_box.exec()
        if response == QtWidgets.QMessageBox.Cancel:
            return
        else:
            self.ptsFixed = np.array([[0, 0]], dtype=np.float64)
            self.ptsMoving = np.array([[0, 0]], dtype=np.float64)
            self.update_both_images()

    def call_change_fiducial_color0(self):
        self.whichColor = 0 # color 1
        self.change_fiducial_color()

    def call_change_fiducial_color1(self):
        self.whichColor = 1  # color 2
        self.change_fiducial_color()

    def change_fiducial_color(self):
        """Open a color picker dialog to change the fiducial color."""

        self.define_edit_frame()

        # Open the color dialog
        color_dialog = QColorDialog(self.ptsColor, self)

        # Set a stylesheet to change the font color to white
        color_dialog.setStyleSheet("""
                QWidget {
                    color: white;  /* Set font color to white */
                    background-color: #2E2E2E;  /* Optional: Set background color to dark gray for contrast */
                }
                QPushButton {
                    background-color: #4C4C4C;  /* Optional: Dark button background */
                    color: white;
                }
                QLabel {
                    color: white;
                }
            """)

        # Open the color dialog and check if a valid color is selected
        if color_dialog.exec():
            color = color_dialog.selectedColor()

            if color.isValid():
                if self.current_index == self.fiducials_tab: # fiducials tab
                    self.ptsColor_tabF = color
                elif self.current_index == self.overlay_tab: # image overlay tab
                    if self.whichColor == 0:
                        self.ptsColor_tabO = color
                    else:
                        self.ptsColor_tabOb = color
                elif self.current_index == self.apply_to_data_tab: # apply to coordinates tab
                    self.ptsColor_tabC = color
                self.update_button_color()

                # update image views
                self.update_both_images()

                # if currently in fiducial mode, update the cursor color
                if self.add_fiducial_active and self.current_index == self.fiducials_tab:
                    crosshair_cursor = self.create_large_crosshair_cursor()
                    self.setCursor(crosshair_cursor)

    def update_button_color(self):
        """Update the button background and font color to match the selected fiducial color."""

        # get the current frame info
        self.define_edit_frame()

        # Calculate the average of the RGB values
        avg_rgb = (self.ptsColor.red() + self.ptsColor.green() + self.ptsColor.blue()) / 3

        # Determine font color based on the average RGB value
        font_color = "white" if avg_rgb < 125 else "black"
        color_rgb = f"rgb({self.ptsColor.red()}, {self.ptsColor.green()}, {self.ptsColor.blue()})"
        tmp = f"background-color: {color_rgb}; color: {font_color};border: 1px solid  #e6e6e6;border-radius: 5px;padding: 5px;"
        self.ColorButton.setStyleSheet(tmp)
        self.whichColor = 0

    def update_zoom_default(self, whichImage=None):

        if whichImage is None:
            whichImage = self.editWhichImage

        self.define_edit_frame(whichImage)
        if self.ImageWidth == 0 or self.ImageHeight == 0:
            return

        if whichImage == 0:
            frame = self.frame_left
        else:
            frame = self.frame_right

        width_scale = frame.width() / self.ImageWidth
        height_scale = frame.height() / self.ImageHeight

        zoom_default0 = self.zoom_default
        zoom_scale0 = self.zoom_scale
        zz = zoom_scale0 / zoom_default0
        self.zoom_default = min(width_scale, height_scale)
        self.zoom_scale = zz * self.zoom_default
        self.return_edit_frame(whichImage)

    def handle_fiducial_click(self, x, y, event):

        if self.add_fiducial_active:
            self.editWhichImage = self.editWhichFid
            if self.editWhichImage == 0:  # Fixed image
                zz = self.fixed_zoom_scale / self.fixed_zoom_default
                image_W = self.imFixed0.width() # width of image in pixels
                image_H = self.imFixed0.height() # height of image in pixels
                frame_size_W = self.ui.FixedImageDisplayFrame.width() # round(image_W / scale)
                frame_size_H = self.ui.FixedImageDisplayFrame.height() #round(image_H / scale)
                flip = self.fixed_flip_state
                ang = self.fixed_rotation_angle
            else:  # Moving image
                zz = self.moving_zoom_scale / self.moving_zoom_default
                image_W = self.imMoving0.width() # width of image in pixels
                image_H = self.imMoving0.height() # height of image in pixels
                frame_size_W = self.ui.MovingImageDisplayFrame.width()  # round(image_W / scale)
                frame_size_H = self.ui.MovingImageDisplayFrame.height()  # round(image_H / scale)
                flip = self.moving_flip_state
                ang = self.moving_rotation_angle

            # remove the effect of zoom, then rescale x and y from label space to image space
            scale = max([image_H / frame_size_H, image_W / frame_size_W, frame_size_W / image_W, frame_size_H / image_H])
            image_x = round(x / zz * scale)
            image_y = round(y / zz * scale)

            # account for flipping and rotation
            if flip:
                if ang == 90 or ang == 270:
                    image_x = image_H - image_x
                else:
                    image_x = image_W - image_x
            if ang == 90:
                tmp = image_x
                image_x = image_y
                image_y = image_H - tmp
            elif ang == 180:
                image_x = image_W - image_x
                image_y = image_H - image_y
            elif ang == 270:
                tmp = image_x
                image_x = image_W - image_y
                image_y = tmp

            # Add coordinates to the appropriate list
            add_to_list = np.array([image_x, image_y])
            if self.editWhichImage == 0:  # Fixed image
                self.ptsFixed = np.vstack([self.ptsFixed, add_to_list])
            else:  # Moving image
                self.ptsMoving = np.vstack([self.ptsMoving, add_to_list])

            # plot
            self.update_image_view()

            # take the next step
            self.editWhichFid = not self.editWhichFid
            self.highlight_current_frame()

        elif self.delete_mode_active:
            # figure out which image to zoom in on
            frame_info_left = self.frame_left.geometry()
            frame_info_right = self.frame_right.geometry()
            y = y - self.padnum
            in_left_x = x > frame_info_left.x() and x < frame_info_left.x() + frame_info_left.width()
            in_left_y = y > frame_info_left.y() and y < frame_info_left.y() + frame_info_left.height()
            in_right_x = x > frame_info_right.x() and x < frame_info_right.x() + frame_info_right.width()
            in_right_y = y > frame_info_right.y() and y < frame_info_right.y() + frame_info_right.height()

            if in_left_x and in_left_y:
                if self.current_index != self.apply_to_data_tab:
                    self.editWhichImage = 0
            elif in_right_x and in_right_y:
                if self.current_index != self.apply_to_data_tab:
                    self.editWhichImage = 1
            else:
                return

            if in_left_x and in_left_y:
                image_type = 0 # fixed image
                zz = self.fixed_zoom_scale / self.fixed_zoom_default
                image_W = self.imFixed0.width()  # width of image in pixels
                image_H = self.imFixed0.height()  # height of image in pixels
                frame_size_W = self.ui.FixedImageDisplayFrame.width()  # round(image_W / scale)
                frame_size_H = self.ui.FixedImageDisplayFrame.height()  # round(image_H / scale)
                flip = self.fixed_flip_state
                ang = self.fixed_rotation_angle
                local_pos = self.fixed_image_label.mapFromGlobal(event.globalPosition().toPoint())
                x = local_pos.x()
                y = local_pos.y()
                pts = self.ptsFixed
            elif in_right_x and in_right_y:
                image_type = 1  # moving image
                zz = self.moving_zoom_scale / self.moving_zoom_default
                image_W = self.imMoving0.width()  # width of image in pixels
                image_H = self.imMoving0.height()  # height of image in pixels
                frame_size_W = self.ui.MovingImageDisplayFrame.width()  # round(image_W / scale)
                frame_size_H = self.ui.MovingImageDisplayFrame.height()  # round(image_H / scale)
                flip = self.moving_flip_state
                ang = self.moving_rotation_angle
                local_pos = self.moving_image_label.mapFromGlobal(event.globalPosition().toPoint())
                x = local_pos.x()
                y = local_pos.y()
                pts = self.ptsMoving
            else:
                print("not inside a frame")
                return

            # there are no points to delete
            pts = np.delete(pts, 0, axis=0)
            if pts.size == 0:
                self.potential_deletion = -5
                self.update_both_images()
                self.setCursor(Qt.ArrowCursor)
                self.delete_mode_active = False
                return

            # remove the effect of zoom, then rescale x and y from label space to image space
            scale = max([image_H / frame_size_H, image_W / frame_size_W, frame_size_W / image_W, frame_size_H / image_H])
            image_x = round(x / zz * scale)
            image_y = round(y / zz * scale)

            # account for flipping and rotation
            if flip:
                if ang == 90 or ang == 270:
                    image_x = image_H - image_x
                else:
                    image_x = image_W - image_x
            if ang == 90:
                tmp = image_x
                image_x = image_y
                image_y = image_H - tmp
            elif ang == 180:
                image_x = image_W - image_x
                image_y = image_H - image_y
            elif ang == 270:
                tmp = image_x
                image_x = image_W - image_y
                image_y = tmp

            # find the point closest to the clicked coordinate
            self.potential_deletion, closest_point = self.find_closest_row(pts, image_x, image_y)

            # update both images with the target point to delete
            self.update_both_images()

            # confirm deletion
            msg_box = QtWidgets.QMessageBox()  # Create a message box
            msg_box.setWindowTitle("Confirm deletion")  # Set the window title
            msg_box.setText("Are you sure you want to delete THIS fiducial point?")  # Set the message text
            msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons
            msg_box.setStyleSheet(self.style_QuestBox)

            # Show the message box and get the response
            response = msg_box.exec()
            if response == QtWidgets.QMessageBox.Yes:
                # remove the selected fiducial then return to normal mode
                self.ptsFixed = np.delete(self.ptsFixed, self.potential_deletion + 1, axis=0)
                self.ptsMoving = np.delete(self.ptsMoving, self.potential_deletion + 1, axis=0)

            # delete the point or keep it, then replot the images
            self.potential_deletion = -5
            self.update_both_images()
            self.setCursor(Qt.ArrowCursor)
            self.delete_mode_active = False

    def find_closest_row(self, pts, image_x, image_y):
        # Ensure pts is a NumPy array with float data type
        pts = np.asarray(pts, dtype=np.float64)

        # Calculate the Euclidean distance to (image_x, image_y) for all rows in pts
        distances = np.sqrt((pts[:, 0] - image_x) ** 2 + (pts[:, 1] - image_y) ** 2)
        closest_index = np.argmin(distances)  # Index of the row with the minimum distance
        return closest_index, pts[closest_index]

    def toggle_add_fiducial_mode(self):
        """Toggle fiducial selection mode."""

        if self.current_index != self.fiducials_tab:
            return

        self.add_fiducial_active = not self.add_fiducial_active

        if self.delete_mode_active:
            self.delete_mode_active = False

        if self.add_fiducial_active:
            self.ui.AddFiducialButton.setText("Quit")

            # start by selecting a point on the fixed image
            self.editWhichImage = 0
            self.editWhichFid = 0
            self.highlight_current_frame()
            crosshair_cursor = self.create_large_crosshair_cursor()
            self.setCursor(crosshair_cursor)
        else:
            # Reset the cursor to default
            self.ui.AddFiducialButton.setText("Add")
            self.setCursor(Qt.ArrowCursor)

            # remove point from fixed image list if necessary
            if self.editWhichFid == 1: # moving image
                self.ptsFixed = np.delete(self.ptsFixed, -1, axis=0)
                self.editWhichImage = 0
                self.highlight_current_frame()
                self.update_image_view()

    def closeEvent(self, event):
        # Reset the cursor to default before closing
        self.setCursor(Qt.ArrowCursor)
        super().closeEvent(event)

    def create_large_crosshair_cursor(self):
        # Create a larger pixmap for the crosshair
        pixmap_size = 512  # Increase the size of the pixmap
        pixmap = QPixmap(pixmap_size, pixmap_size)
        pixmap.fill(Qt.transparent)  # Transparent background

        # Extract RGB values from self.ptColor
        r, g, b = self.ptsColor_tabF.red(), self.ptsColor_tabF.green(), self.ptsColor_tabF.blue()
        ff = 0.6
        crosshair_color = QColor(int(r * ff), int(g * ff), int(b * ff))

        # Draw the extended crosshair
        painter = QPainter(pixmap)
        pen = QPen(crosshair_color) # set the color to match the fiducial points
        pen.setWidth(2)  # Set the thickness (e.g., 5px)
        painter.setPen(pen)

        # Vertical line
        painter.drawLine(pixmap_size // 2, 0, pixmap_size // 2, pixmap_size)
        # Horizontal line
        painter.drawLine(0, pixmap_size // 2, pixmap_size, pixmap_size // 2)
        painter.end()

        # Set the center of the crosshair to the hotspot
        return QCursor(pixmap, pixmap_size // 2, pixmap_size // 2)

    def reset_transformations(self, whichImage=None):
        """Reset all transformations to their defaults."""

        if whichImage is not None:
            self.editWhichImage = whichImage

        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index != self.fiducials_tab and self.current_index != self.overlay_tab and self.current_index != self.apply_to_data_tab:
            return

        self.flip_state = False
        self.rotation_angle = 0
        self.zoom_scale = self.zoom_default
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        self.brightness = 0
        self.contrast = 1
        self.return_edit_frame()
        self.update_image_view()

    def flip_image_y(self, whichImage=None):
        """Flip the image horizontally while ensuring it fits within bounds."""

        if whichImage is not None:
            self.editWhichImage = whichImage

        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index != self.fiducials_tab and self.current_index != self.overlay_tab and self.current_index != self.apply_to_data_tab:
            return

        # flip
        self.flip_state = not self.flip_state
        self.pan_offset_x = -self.pan_offset_x
        self.return_edit_frame()
        self.update_image_view()

    def rotate_label_ui(self, whichImage=None):
        """Rotate the image while ensuring pan offsets align with the rotation."""

        if whichImage is not None:
            self.editWhichImage = whichImage

        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index != self.fiducials_tab and self.current_index != self.overlay_tab and self.current_index != self.apply_to_data_tab:
            return

        # rotate
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.return_edit_frame()
        self.update_image_view()

    def increase_brightness(self, whichImage=None):

        if whichImage is not None:
            self.editWhichImage = whichImage

        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index != self.fiducials_tab and self.current_index != self.apply_to_data_tab:
            return

        self.brightness = self.brightness + 5
        self.return_edit_frame()
        self.update_image_view()

    def decrease_brightness(self, whichImage=None):

        if whichImage is not None:
            self.editWhichImage = whichImage

        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index != self.fiducials_tab and self.current_index != self.apply_to_data_tab:
            return

        self.brightness = self.brightness - 5
        self.return_edit_frame()
        self.update_image_view()

    def increase_contrast(self, whichImage=None):

        if whichImage is not None:
            self.editWhichImage = whichImage

        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index != self.fiducials_tab and self.current_index != self.apply_to_data_tab:
            return

        self.contrast = self.contrast + 0.05
        self.return_edit_frame()
        self.update_image_view()

    def decrease_contrast(self, whichImage=None):

        if whichImage is not None:
            self.editWhichImage = whichImage

        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index != self.fiducials_tab and self.current_index != self.apply_to_data_tab:
            return

        self.contrast = self.contrast - 0.05
        self.return_edit_frame()
        self.update_image_view()

    def call_increase_fiducial_size0(self):
        self.whichColor = 0  # color 1
        self.increase_fiducial_size()

    def call_increase_fiducial_size1(self):
        self.whichColor = 1  # color 1
        self.increase_fiducial_size()

    def call_decrease_fiducial_size0(self):
        self.whichColor = 0  # color 1
        self.decrease_fiducial_size()

    def call_decrease_fiducial_size1(self):
        self.whichColor = 1  # color 1
        self.decrease_fiducial_size()

    def increase_fiducial_size(self):

        self.define_edit_frame()
        self.rad = max([self.rad + 1, 1])
        self.return_edit_frame()
        self.whichColor = 0
        self.update_both_images()

    def decrease_fiducial_size(self):

        self.define_edit_frame()
        self.rad = max([self.rad - 1, 1])
        self.return_edit_frame()
        self.whichColor = 0
        self.update_both_images()

    def promote_text_to_clickable_label(self, text_widget, click_handler):
        # Save the existing properties of the original QLabel
        geometry = text_widget.geometry()
        parent = text_widget.parent()
        stylesheet = text_widget.styleSheet()
        font = text_widget.font()
        alignment = text_widget.alignment()
        text = text_widget.text()
        object_name = text_widget.objectName()
        palette = text_widget.palette()  # Save the palette for font color

        # Create a new ClickableLabel with the same properties
        clickable_label = ClickableLabel(parent)
        clickable_label.setObjectName(object_name)  # Retain the original object name
        clickable_label.setGeometry(geometry)  # Set the same geometry
        clickable_label.setText(text)  # Copy the text content
        clickable_label.setStyleSheet(stylesheet)  # Apply the stylesheet
        clickable_label.setFont(font)  # Set the font
        clickable_label.setAlignment(alignment)  # Set the text alignment
        clickable_label.setPalette(palette)  # Apply the palette to copy the font color
        clickable_label.setAutoFillBackground(True)  # Ensure background and font color render correctly
        clickable_label.show()  # Make it visible

        # Connect the doubleClicked signal to the desired handler
        clickable_label.doubleClicked.connect(click_handler)

        # Replace the original QLabel in the UI with the new ClickableLabel
        setattr(self.ui, object_name, clickable_label)

    def highlight_current_frame(self):

        # turn off both frames
        if not self.add_fiducial_active:
            self.define_edit_frame()
            self.border_left.setStyleSheet(self.inactiveLabel)
            self.text_left.setStyleSheet(self.inactiveTextLabel)
            self.frame_left.setStyleSheet(self.inactiveFrame)
            tmp = self.frame_left.geometry()
            self.border_left.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
            self.border_right.setStyleSheet(self.inactiveLabel)
            self.text_right.setStyleSheet(self.inactiveTextLabel)
            self.frame_right.setStyleSheet(self.inactiveFrame)
            tmp = self.frame_right.geometry()
            self.border_right.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
            return

        self.editWhichImage = self.editWhichFid
        self.define_edit_frame()
        if self.editWhichImage == 0:  # left image
            self.border_left.setStyleSheet(self.activeLabel)
            tmp = self.frame_left.geometry()
            self.border_left.setGeometry(tmp.x() - 5, tmp.y() - 5, tmp.width() + 10, tmp.height() + 10)
            self.text_left.setStyleSheet(self.activeTextLabel)
            self.frame_left.setStyleSheet(self.activeFrame)

            self.border_right.setStyleSheet(self.inactiveLabel)
            tmp = self.frame_right.geometry()
            self.border_right.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
            self.text_right.setStyleSheet(self.inactiveTextLabel)
            self.frame_right.setStyleSheet(self.inactiveFrame)
        else:  # right image
            self.border_left.setStyleSheet(self.inactiveLabel)
            tmp = self.frame_left.geometry()
            self.border_left.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
            self.text_left.setStyleSheet(self.inactiveTextLabel)
            self.frame_left.setStyleSheet(self.inactiveFrame)

            self.border_right.setStyleSheet(self.activeLabel)
            tmp = self.frame_right.geometry()
            self.border_right.setGeometry(tmp.x() - 5, tmp.y() - 5, tmp.width() + 10, tmp.height() + 10)
            self.text_right.setStyleSheet(self.activeTextLabel)
            self.frame_right.setStyleSheet(self.activeFrame)

    def begin_calculate_icp_tabF(self):

        # turn off active labels
        self.ui.FixedImageBorder.setStyleSheet(self.inactiveLabel)
        self.ui.FixedImageFrameHeaderText.setStyleSheet(self.inactiveTextLabel)
        self.ui.FixedImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        tmp = self.ui.FixedImageDisplayFrame.geometry()
        self.ui.FixedImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
        self.ui.MovingImageBorder.setStyleSheet(self.inactiveLabel)
        self.ui.MovingImageFrameHeaderText.setStyleSheet(self.inactiveTextLabel)
        self.ui.MovingImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        tmp = self.ui.MovingImageDisplayFrame.geometry()
        self.ui.MovingImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)

        if self.add_fiducial_active:
            self.toggle_add_fiducial_mode()

        # button view settings
        self.close_navigation_tab()
        self.ui.NavigationButton_F.setVisible(False)
        self.ui.FiducialPointControlsFrame.setVisible(False)
        self.ui.ChooseMovingImageFrame.setVisible(False)
        self.ui.PickNewMovingImageButton.setVisible(False)
        self.ui.AttemptICPRegistrationButton.setVisible(False)
        self.ui.FiducialTabUpdateText.setVisible(True)
        self.ui.FiducialTabUpdateText.setText(f"Calculating Point Cloud Registration. Please Wait...")
        QtWidgets.QApplication.processEvents()

        # save the fiducial points
        self.save_fiducial_state()

        pts_fixed = np.delete(self.ptsFixed, 0, axis=0)
        pts_moving = np.delete(self.ptsMoving, 0, axis=0)
        width = self.imMoving0.width()

        pts_moving_0 = pts_moving
        pts_out_0, tform_0, RMSE_0, RMSE0 = self.icp_registration(pts_fixed, pts_moving_0)

        pts_moving_f = np.column_stack([width - pts_moving[:, 0], pts_moving[:, 1]])
        pts_out_f, tform_f, RMSE_f, RMSE0 = self.icp_registration(pts_fixed, pts_moving_f)

        self.RMSE0 = RMSE0
        if RMSE_0 < RMSE_f:
            self.ptsMovingReg = pts_out_0
            self.RMSE = RMSE_0
            self.tform = tform_0
            self.flip_im = 0
        else:
            self.ptsMovingReg = pts_out_f
            self.RMSE = RMSE_f
            self.tform = tform_f
            self.flip_im = 1

        self.initiate_overlay_tab()

    def save_registered_images(self):

        # save registered moving image
        outputFolder = os.path.join(self.jobFolder, self.ResultsName, "Registered images")
        # Check if the folder exists, and create it if it doesn't
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        tmp = self.nmMoving[:self.nmMoving.rfind('.')] + ".jpg"
        outfile = os.path.join(outputFolder, tmp)
        #image = self.imMovingReg.toImage()
        #image = image.convertToFormat(QImage.Format_RGB888)
        self.imMovingReg.save(outfile, "JPG")

        # save the fixed image if it does not already exist
        tmp = self.nmFixed[:self.nmFixed.rfind('.')] + ".jpg"
        outfile = os.path.join(outputFolder, tmp)
        if not os.path.exists(outfile):
            #image = self.imFixed0.toImage()
            #image = image.convertToFormat(QImage.Format_RGB888)
            self.imFixed0.save(outfile, "JPG")

    def browse_for_coordinates_file(self):

        open_to = os.path.join(self.jobFolder, self.ResultsName)
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select .csv or .xlsx File containing coordinates",
            open_to,  # Specify the initial folder here
            "Data Files (*.csv *.xlsx);;All Files (*)")
        if file_path:
            self.pthCoords = os.path.dirname(file_path)  # Extract the folder
            self.nmCoords = os.path.basename(file_path)  # Extract the filename

        # add this information to the table
        self.xColumn = ""
        self.yColumn = ""
        self.populate_coordinates_table()

    def unregistered_coords_checkbox_changed(self, state):
        """Handle the checkbox state change."""
        if state > 0:
            self.all_images_checked += 1
        else:
            self.all_images_checked -= 1

        if self.all_images_checked == 3:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(True)
        else:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(False)

    def registered_coords_checkbox_changed(self, state):
        """Handle the checkbox state change."""
        if state > 0:
            self.all_images_checked += 1
        else:
            self.all_images_checked -= 1

        if self.all_images_checked == 3:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(True)
        else:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(False)

    def fixed_coords_checkbox_changed(self, state):
        """Handle the checkbox state change."""
        if state > 0:
            self.all_images_checked += 1
        else:
            self.all_images_checked -= 1

        if self.all_images_checked == 3:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(True)
        else:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(False)

    def populate_coordinates_combo_box(self):
        """
        Populate the QComboBox with strings from column 1 of self.movingIMS.
        """

        # Clear the current items in the combo box
        self.ui.CorrespondingImageComboBox.clear()

        # initialize the combo box list
        self.ui.CorrespondingImageComboBox.addItem("Select")
        self.numMovingCoords = [[], []]

        # Add items from column 1 of self.movingIMS
        for index, row in enumerate(self.movingIMS):
            if len(row) > 1:  # Ensure the row has at least two columns
                filename = row[0]  # Get the filename from column 1
                filename_out1 = filename[:filename.rfind('.')] + ".pkl"
                filename_out2 = filename[:filename.rfind('.')] + ".jpg"

                # check if fiducial points, a transform, and a registered image exists
                filepath1 = os.path.join(self.jobFolder, self.ResultsName, "Fiducial point selection", filename_out1) # os.path.join(self.jobFolder, self.ResultsName, "aligned_stack", filename_out)
                filepath2 = os.path.join(self.jobFolder, self.ResultsName, "Registration transforms", filename_out1)
                filepath3 = os.path.join(self.jobFolder, self.ResultsName, "Registered images", filename_out2)

                if os.path.isfile(filepath1) and os.path.isfile(filepath2) and os.path.isfile(filepath3):  # Check if the file exists
                    self.ui.CorrespondingImageComboBox.addItem(filename)  # Add to OldMovingImagesComboBox
                    self.numMovingCoords[0].append(index)
                else:
                    self.numMovingCoords[1].append(index)

    def doubleclick_coordinates_table(self, row, column):

        # if the table is populated and table edit mode is not already active
        if len(self.nmCoords) > 0 or len(self.nmMovingCoords) > 0:

            # if editing the scale
            if column in [2, 3, 4, 5]: # editing the scale, x, y, or # points
                self.ui.LoadCoordinatesButton.setVisible(False)
                # enable text input to the scale window
                item = self.ui.RegisterCoordinatesTableWidget.item(row, column)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Enable editing
                    self.ui.RegisterCoordinatesTableWidget.editItem(item)  # Put the cell into edit mode

    def handle_value_update_coordinates(self, new_value, row, column):
        """
        Handle the updated value in a cell after editing.
        """

        if column == 2: # scale
            try:
                float(new_value)
                self.ScaleCoords = new_value
            except:
                if new_value != "":
                    text = "The entered value is not a number. Please enter a number"
                    self.show_error_message(text)
        elif column == 3: # x column
            if self.get_column_number(new_value):
                self.xColumn = new_value
            else:
                text = "Enter fully numeric (e.g. '5') or alphabetical (e.g. 'AB') text"
                self.show_error_message(text)
        elif column == 4: # y column
            if self.get_column_number(new_value):
                self.yColumn = new_value
            else:
                text = "Enter fully numeric (e.g. '5') or alphabetical (e.g. 'AB') text"
                self.show_error_message(text)
        elif column == 5:
            try:
                float(new_value)
                self.max_points = new_value
            except:
                if new_value != "":
                    text = "The entered value is not a number. Please enter a number"
                    self.show_error_message(text)
        else:
            self.ui.LoadCoordinatesButton.setVisible(True)
            return
        self.ui.LoadCoordinatesButton.setVisible(True)
        self.populate_coordinates_table()

    def on_combo_box_changed(self):

        # get the current filename and index from the droplist
        current_index_in_table = self.ui.CorrespondingImageComboBox.currentIndex()
        if current_index_in_table == 0:
            self.nmMovingCoords = ""
            self.ScaleCoords = ""
            self.pthMovingCoords = ""
        else:
            row_number = self.numMovingCoords[0]
            row_number = row_number[current_index_in_table - 1]
            self.nmMovingCoords = self.movingIMS[row_number][0]
            self.ScaleCoords = self.movingIMS[row_number][1]
            self.pthMovingCoords = self.movingIMS[row_number][2]

        # update the table
        self.populate_coordinates_table()

    def populate_coordinates_table(self):

        # Populate the first row with the variables' values
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{self.nmCoords}  "))
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{self.nmMovingCoords}  "))  # Convert scale to string if necessary
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(self.ScaleCoords))
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(self.xColumn))
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(self.yColumn))
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 5, QtWidgets.QTableWidgetItem(str(self.max_points)))
        self.ui.RegisterCoordinatesTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_table_is_complete_coords_tab()

    def check_if_table_is_complete_coords_tab(self):
        coordsFrameDone = (len(self.nmCoords) > 0 and len(self.nmMovingCoords) > 0 and len(self.ScaleCoords) > 0
                           and len(self.xColumn) > 0 and len(self.yColumn) > 0  and len(self.max_points) > 0)

        # make fixed frame green if completed
        if coordsFrameDone:
            self.ui.RegisterCoordinatesFrame.setStyleSheet("background-color: #3d4a3d;")
            self.ui.LoadCoordinatesButton.setVisible(True)
        else:
            self.ui.RegisterCoordinatesFrame.setStyleSheet("background-color: #4b4b4b;")
            self.ui.LoadCoordinatesButton.setVisible(False)

    def initiate_apply_to_coords_tab(self):

        # save the current fiducial points and view settings if the user is in the fiducials tab
        self.close_navigation_tab()
        self.save_fiducial_state()

        # move to apply to coordinates tab
        self.ui.tabWidget.setCurrentIndex(self.apply_to_data_tab)

        # initial view settings
        self.ui.MakingCoordOverlayText.setVisible(False)
        self.ui.ImageViewControlsFrame_C.setVisible(False)
        self.ui.RegisterCoordsDisplayFrame.setVisible(False)
        self.ui.RegisterCoordsImageBorder.setVisible(False)
        self.ui.RegisterCoordsFrameHeaderText.setVisible(False)
        self.ui.CoordinatesOverlayControlsFrame.setVisible(False)
        self.ui.LoadCoordinatesButton.setVisible(False)
        self.ui.BrowseForCoordinatesFileText.setEnabled(False)
        self.ui.CorrespondingImageText.setEnabled(False)
        self.ui.DisableFrame_C.setGeometry(self.ui.RegisterCoordinatesFrame.geometry())
        self.ui.DisableFrame_C.setVisible(False)
        self.ui.DisableFrame_C_2.setGeometry(self.ui.CoordinatesOverlayControlsFrame.geometry())
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setGeometry(self.ui.ImageViewControlsFrame_C.geometry())
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.SaveRegisteredCoordinatesButton.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.PlottingImageText.setText("Replotting the Image. Please Wait...")

        # uncheck the check boxes
        self.ui.UnregisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.FixedCheckBox.setCheckState(Qt.Unchecked)
        self.all_images_checked = 0

        # clear large variables to save memory
        self.imMoving0 = []
        self.imMovingReg = []
        self.nmMoving = []

        # initiate coordinates variables
        self.pthCoords = ""
        self.nmCoords = ""
        self.pthMovingCoords = ""
        self.nmMovingCoords = ""
        self.nmLoadedMoving = ""
        self.nmCoordsLoaded = ""
        self.Coords = ""
        self.imMovingCoords = []
        self.imMovingCoordsReg = []
        self.imPlotHold = []
        self.ScaleCoords = ""
        self.xColumn = ""
        self.yColumn = ""
        self.max_points = "1000"
        self.all_images_checked = 0
        self.tformCoords = []
        self.sampled_indices = []
        self.rad_tabC = np.ceil(float(self.rad_tabF) / 2)

        # populate dropdown list
        self.populate_coordinates_combo_box()
        self.update_button_color()

        # populate the blank table
        self.ui.RegisterCoordinatesTableWidget.setHorizontalHeaderLabels(
            ["Data Filename", "Moving Image Filename", "Scale", "X Column", "Y Column", "# Points to Plot", " "])
        if self.nmMovingCoords or self.nmCoords:
            self.ui.RegisterCoordinatesTableWidget.setVerticalHeaderLabels([""])
        self.populate_coordinates_table()

    def return_to_edit_table(self):

        # change some view settings
        self.ui.ImageViewControlsFrame_C.setVisible(False)
        self.ui.CoordinatesOverlayControlsFrame.setVisible(False)
        self.ui.RegisterCoordsDisplayFrame.setVisible(False)
        self.ui.RegisterCoordsImageBorder.setVisible(False)
        self.ui.RegisterCoordsFrameHeaderText.setVisible(False)
        self.ui.DisableFrame_C.setVisible(False)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)

    def define_image_unregistered(self):
        self.editWhichImage = 0
        self.close_navigation_tab()
        self.imPlotHold = []
        self.ui.NavigationButton_C.setVisible(False)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        self.reset_transformations(self.editWhichImage)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.NavigationButton_C.setVisible(True)

    def define_image_registered(self):
        self.editWhichImage = 1
        self.close_navigation_tab()
        self.ui.NavigationButton_C.setVisible(False)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        self.reset_transformations(self.editWhichImage)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.NavigationButton_C.setVisible(True)

    def define_image_fixed(self):
        self.editWhichImage = 2
        self.close_navigation_tab()
        self.imPlotHold = []
        self.ui.NavigationButton_C.setVisible(False)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        self.reset_transformations(self.editWhichImage)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.NavigationButton_C.setVisible(True)

    def load_coordinates_to_register(self):

        # change some view settings while the data loads
        self.ui.MakingCoordOverlayText.setVisible(True)
        self.ui.DisableFrame_C.setVisible(True)
        QtWidgets.QApplication.processEvents()

        # load the fixed image and the unregistered and registered moving images
        image_path_fixed = os.path.join(self.pthFixed, self.nmFixed)
        image_path_moving = os.path.join(self.pthMovingCoords, self.nmMovingCoords)
        image_path_reg = self.nmMovingCoords[:self.nmMovingCoords.rfind('.')] + ".jpg"
        image_path_reg = os.path.join(self.jobFolder, self.ResultsName, "Registered images", image_path_reg)
        # print(f"moving image: {self.nmMovingCoords}, loaded image: {self.nmLoadedMoving}")
        if self.nmMovingCoords != self.nmLoadedMoving:
            try:
                self.imFixed0 = self.load_image(image_path_fixed)         # load the fixed image
                self.imMovingCoords = self.load_image(image_path_moving)  # load the moving image
                self.imMovingCoordsReg = self.load_image(image_path_reg)  # load the registered moving image
                self.nmLoadedMoving = self.nmMovingCoords
            except:
                text = "One or more images could not be loaded."
                self.show_error_message(text)

        # define the first settings
        self.editWhichImage = 0 # unregistered moving image
        self.coords_flip_state = 0
        self.coords_rotation_angle = 0
        self.coords_brightness = 0
        self.coords_contrast = 1
        self.coords_pan_offset_x = 0
        self.coords_pan_offset_y = 0

        # set the zoom default
        width_scale = self.ui.RegisterCoordsDisplayFrame.width() / self.imMovingCoords.width()
        height_scale = self.ui.RegisterCoordsDisplayFrame.height() / self.imMovingCoords.height()
        self.coords_zoom_default = min(width_scale, height_scale)
        self.coords_zoom_scale = self.coords_zoom_default

        # uncheck the check boxes
        self.ui.UnregisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.FixedCheckBox.setCheckState(Qt.Unchecked)
        self.all_images_checked = 0

        # load and subsample the coordinates
        self.get_coordinates_from_file()

        downsample_num = min([self.ptsCoords.shape[0], int(self.max_points)])
        self.max_points = str(downsample_num)
        self.populate_coordinates_table()
        self.sampled_indices = np.random.choice(self.ptsCoords.shape[0], size=downsample_num, replace=False)

        # display the image
        self.update_image_view()

        # change some view settings
        self.ui.MakingCoordOverlayText.setVisible(False)
        self.ui.ImageViewControlsFrame_C.setVisible(True)
        self.ui.CoordinatesOverlayControlsFrame.setVisible(True)
        self.ui.RegisterCoordsDisplayFrame.setVisible(True)
        self.ui.RegisterCoordsImageBorder.setVisible(True)
        self.ui.RegisterCoordsFrameHeaderText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)

    def save_registered_coordinates(self):

        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.PlottingImageText.setText("Saving the Coordinates. Please Wait...")
        QtWidgets.QApplication.processEvents()

        # load the coordinates again
        xCol = self.get_column_number(self.xColumn)
        yCol = self.get_column_number(self.yColumn)

        # Substitute the registered coordinates into the X matrix
        X = self.Coords
        X[self.first_row:, [xCol, yCol]] = self.ptsCoordsReg

        # Save the updated matrix to a new file in a specified folder
        output_folder = os.path.join(self.jobFolder, self.ResultsName, "Registered coordinate data")
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
        image_name, _ = os.path.splitext(self.nmFixed)
        output_file = os.path.join(output_folder, f"Registered_{self.nmCoords}")

        # Save the updated X matrix as a CSV file
        pd.DataFrame(X).to_csv(output_file, header=None, index=False)

    def get_coordinates_from_file(self):

        # load the coordinates
        xCol = self.get_column_number(self.xColumn)
        yCol = self.get_column_number(self.yColumn)
        file_path = os.path.join(self.pthCoords, self.nmCoords)
        file_ext = os.path.splitext(file_path)[1]
        if self.nmCoords != self.nmCoordsLoaded:
            if file_ext == ".csv":
                self.Coords = pd.read_csv(file_path, header=None).values
            elif file_ext in [".xlsx", ".xls"]:
                self.Coords = pd.read_excel(file_path, header=None).values
            self.nmCoordsLoaded = self.nmCoords

        # Check if the first row contains text labels
        try:
            # Try converting the first row to float
            float(self.Coords[0, xCol])
            float(self.Coords[0, yCol])
            self.first_row = 0
        except ValueError:
            # If conversion fails, exclude the first row
            self.first_row = 1
        self.ptsCoords = self.Coords[self.first_row:, [xCol, yCol]].astype(float)
        self.ptsCoords = np.round(self.ptsCoords)
        self.ptsCoords = self.ptsCoords * float(self.ScaleCoords)

        # Load the transformation data and register the coordinates
        tmp = self.nmMovingCoords[:self.nmMovingCoords.rfind('.')] + ".pkl"
        outputFolder = os.path.join(self.jobFolder, self.ResultsName, "Registration transforms")
        outfile = os.path.join(outputFolder, tmp)
        with open(outfile, 'rb') as file:
            data = pickle.load(file)

        self.tformCoords = data.get('tform')
        self.ptsCoordsReg = (self.tformCoords[:2, :2] @ self.ptsCoords.T).T + self.tformCoords[:2, 2]

    def get_column_number(self, xD):
        if xD.isdigit():  # Check if the input is fully numeric
            return int(xD)
        elif xD.isalpha():  # Check if the input is fully alphabetic
            xD = xD[::-1]  # Reverse the string
            xnum = 0
            for b, xb in enumerate(xD):
                asc = ord(xb.upper()) - ord('A') + 1  # Convert character to 1-based index
                xnum += asc * (26 ** b) # Multiply by 26^(position-1)
            xnum = xnum - 1  # because python
            return xnum
        else:
            # Raise an error for mixed inputs
            return

    def swap_xy(self):
        tmp = self.xColumn
        self.xColumn = self.yColumn
        self.yColumn = tmp

        # update the table
        self.populate_coordinates_table()

        # change some visibility settings
        self.ui.NavigationButton_C.setVisible(False)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        # load and subsample the coordinates
        self.get_coordinates_from_file()

        # replot the image
        self.update_image_view()

        # make buttons clickable again
        self.ui.NavigationButton_C.setVisible(True)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)

        # uncheck the check boxes
        self.ui.UnregisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.FixedCheckBox.setCheckState(Qt.Unchecked)
        self.all_images_checked = 0

    def transform_image(self, szz=None):

        # pad the image
        width = max([self.imFixed0.width(), self.imMoving0.width()])
        height = max([self.imFixed0.height(), self.imMoving0.height()])

        pixmap = self.imMoving0
        if self.flip_im:
            transform = QTransform().scale(-1, 1)  # Horizontal flip
            pixmap = pixmap.transformed(transform, mode=Qt.SmoothTransformation)

        # Prepare the image array
        border = 1
        fv, array, arrayg = self.pad_images(pixmap, width, height, border)

        # Determine the output shape
        if szz is None:
            szz = (width, height)  # (width, height)

        # Apply the adjusted transformation
        fv=int(fv)
        transformed_array = cv2.warpAffine(array, self.tform[:2, :], szz, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=[fv, fv, fv])
        # Crop the image to the size of the fixed image if necessary
        if transformed_array.shape[1] > self.imFixed0.height() or transformed_array.shape[0] > self.imFixed0.width():
            transformed_array = transformed_array[:self.imFixed0.height(), :self.imFixed0.width()]
        transformed_array = np.ascontiguousarray(transformed_array)

        # Convert back to pixmap
        height = transformed_array.shape[1]
        width = transformed_array.shape[0]
        ss = transformed_array.strides[0]
        adjusted_image = QImage(transformed_array.data, height, width, ss, QImage.Format_RGB888)
        self.imMovingReg = QPixmap.fromImage(adjusted_image)

    def icp_registration(self, pts_fixed, pts_moving):
        """
        Perform a simple ICP registration of self.ptsMoving into self.ptsFixed space.
        Returns:
            registered_pts (np.ndarray): The registered points in the self.ptsFixed space.
            tform (np.ndarray): The 3x3 transformation matrix combining rotation and translation.
            RMSE_unregistered (float): RMSE of the points before registration.
            RMSE_registered (float): RMSE of the points after registration.
        """
        pts_moving0 = pts_moving

        # Compute the initial RMSE (unregistered points)
        kdtree = KDTree(pts_fixed)
        distances, _ = kdtree.query(pts_moving0)
        RMSE0 = np.sqrt(np.mean(distances ** 2))

        # scale is the ratio of the mean distance from the centroid
        centroid_fixed = np.mean(pts_fixed, axis=0)
        centroid_moving = np.mean(pts_moving0, axis=0)
        dist_fixed = np.sqrt(np.sum((pts_fixed - centroid_fixed) ** 2, axis=1))
        dist_moving = np.sqrt(np.sum((pts_moving0 - centroid_moving) ** 2, axis=1))
        scale_val = np.mean(dist_fixed) / np.mean(dist_moving)

        # ICP calculation for known point pairs
        pts_moving = pts_moving0 * scale_val
        centroid_moving = np.mean(pts_moving, axis=0)
        centered_moving = pts_moving - np.mean(pts_moving, axis=0)
        centered_fixed = pts_fixed - np.mean(pts_fixed, axis=0)
        H = centered_moving.T @ centered_fixed

        # Compute the Singular Value Decomposition (SVD), rotation, and translation
        U, _, Vt = np.linalg.svd(H)
        R = Vt.T @ U.T
        if np.linalg.det(R) < 0:  # Handle reflection case
            Vt[-1, :] *= -1
            R = Vt.T @ U.T
        t = centroid_fixed - R @ centroid_moving

        # Construct the final transformation matrix
        R_scale = R * scale_val
        tform = np.eye(3)
        tform[:2, :2] = R_scale
        tform[:2, 2] = t

        # apply the transform to the points
        registered_pts = (tform[:2, :2] @ pts_moving0.T).T + tform[:2, 2]

        # Compute the RMSE of the registered points
        distances, _ = kdtree.query(registered_pts)
        RMSE = np.sqrt(np.mean(distances ** 2))

        return registered_pts, tform, RMSE, RMSE0

    def initiate_overlay_tab(self):

        # close navigation button
        self.close_navigation_tab()

        # initial button settings
        self.ui.DisableFrame_O1.setVisible(False)
        self.ui.DisableFrame_O2.setVisible(False)
        self.ui.SavingRegistrationResultsText.setVisible(False)
        self.ui.SaveRegistrationControlFrame.setEnabled(True)
        self.ui.ImageViewControlsFrame_O.setEnabled(True)

        self.add_fiducial_active = False
        self.delete_mode_active = False

        # fill in text
        self.ui.UnregisteredImageFrameHeaderText.setText(f"Pre-Registration Overlay (RMSE: {round(self.RMSE0)} pixels).")
        self.ui.RegisteredImageFrameHeaderText.setText(f"Post-Registration-Overlay (RMSE: {round(self.RMSE)} pixels).")
        # go to overlay tab
        self.ui.tabWidget.setCurrentIndex(self.overlay_tab)

        # create and display the overlay image
        self.ptsColor_tabO = self.ptsColor_tabF
        self.ptsColor_tabOb = QColor(255 - self.ptsColor_tabO.red(), 255 - self.ptsColor_tabO.green(), 255 - self.ptsColor_tabO.blue())
        self.update_button_color()
        self.whichColor = 1
        self.update_button_color()
        self.imOverlay0, self.unregistered_zoom_default = self.make_overlay_image(self.imFixed0, self.imMoving0)
        self.registered_zoom_scale = self.unregistered_zoom_default

        # plot registered overlay
        self.transform_image()
        self.imOverlay, self.registered_zoom_default = self.make_overlay_image(self.imFixed0, self.imMovingReg)
        self.editWhichImage = 0
        self.reset_transformations(self.editWhichImage)
        self.editWhichImage = 1
        self.reset_transformations(self.editWhichImage)

    def make_overlay_image(self, imFixed, imMoving):

        # pad images to be the same size
        height = max([imFixed.height(), imMoving.height()])
        width = max([imFixed.width(), imMoving.width()])

        brightness = 0
        contrast = 1.1
        imFixed = self.adjust_brightness_contrast(imFixed, contrast, brightness)
        imMoving = self.adjust_brightness_contrast(imMoving, contrast, brightness)

        # pad the fixed image
        fillval_F, imFixed_pad, imFixed_pad_G = self.pad_images(imFixed, width, height)

        # pad the moving image
        fillval_M, imMoving_pad, imMoving_pad_G = self.pad_images(imMoving, width, height)

        # make the combined overlay image
        combined_array = np.stack((imMoving_pad_G, imFixed_pad_G, imMoving_pad_G), axis=-1)  # (H, W, 3)
        imOverlay = QImage(combined_array.data, width, height, 3 * width, QImage.Format_RGB888)
        imOverlay = QPixmap.fromImage(imOverlay)

        # Calculate zoom_default
        width_scale = self.ui.UnregisteredImageDisplayFrame.width() / width
        height_scale = self.ui.UnregisteredImageDisplayFrame.height() / height
        zoom_default = min(width_scale, height_scale)

        return imOverlay, zoom_default

    def pad_images(self, pixmap, width, height, border=None):

        # Convert pixmap to image
        image = pixmap.toImage()
        width0 = image.width()
        height0 = image.height()
        bytes_per_line = image.bytesPerLine()
        ptr = image.bits()
        channels = int(np.size(ptr) / width0 / height0)

        ptr = np.array(ptr).reshape((height0, bytes_per_line))  # Convert memoryview to NumPy array
        array = np.frombuffer(ptr, dtype=np.uint8).reshape((height0, width0, channels))

        if border is not None:
            # add a white border
            array[:15, :, :] = 255  # Top border
            array[-15:, :, :] = 255  # Bottom border
            array[:, :15, :] = 255  # Left border
            array[:, -15:, :] = 255  # Right border

        r = mode(array[..., 0].flatten(), axis=None).mode
        g = mode(array[..., 1].flatten(), axis=None).mode
        b = mode(array[..., 2].flatten(), axis=None).mode

        # Pad each channel to the desired width and height
        pad_width = ((0, height - height0), (0, width - width0))  # Padding for height and width
        r_pad = np.pad(array[..., 0], pad_width, mode='constant', constant_values=r)
        g_pad = np.pad(array[..., 1], pad_width, mode='constant', constant_values=g)
        b_pad = np.pad(array[..., 2], pad_width, mode='constant', constant_values=b)

        # Combine the padded channels into a single RGB array and a grayscale array
        array_pad = np.stack((b_pad, g_pad, r_pad), axis=-1)

        # Flatten the image and calculate the mode
        flattened_image = array[..., 0:3].flatten()  # Combine channels 1, 2, and 3 into a single array
        mode_val = mode(flattened_image, axis=None).mode
        array_pad_gray = np.mean(array_pad, axis=-1).astype(np.uint8)
        if mode_val > 25: # complement if the image is brightfield
            array_pad_gray = 255 - array_pad_gray

        return mode_val, array_pad, array_pad_gray

    def return_to_fiducials_tab(self):
        # initial button settings
        self.close_navigation_tab()
        self.ui.FiducialTabUpdateText.setVisible(False)
        self.ui.LoadNewMovingImageButton.setEnabled(False)
        self.ui.LoadOldMovingImageButton.setEnabled(False)
        self.ui.AttemptICPRegistrationButton.setVisible(False)
        self.ui.FiducialPointControlsFrame.setVisible(True)
        self.ui.ChooseMovingImageFrame.setVisible(False)
        self.ui.PickNewMovingImageButton.setVisible(True)
        QtWidgets.QApplication.processEvents()

        # go to fiducials tab and update the images
        self.ui.tabWidget.setCurrentIndex(self.fiducials_tab)
        self.populate_moving_images_combo_box()
        self.update_button_color()
        self.update_both_images()

    def save_registration_results(self):

        # turn off active labels
        self.ui.UnregisteredImageBorder.setStyleSheet(self.inactiveLabel)
        self.ui.UnregisteredImageFrameHeaderText.setStyleSheet(self.inactiveTextLabel)
        self.ui.UnregisteredImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        tmp = self.ui.UnregisteredImageDisplayFrame.geometry()
        self.ui.UnregisteredImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
        self.ui.RegisteredImageBorder.setStyleSheet(self.inactiveLabel)
        self.ui.RegisteredImageFrameHeaderText.setStyleSheet(self.inactiveTextLabel)
        self.ui.RegisteredImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        tmp = self.ui.RegisteredImageDisplayFrame.geometry()
        self.ui.RegisteredImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
        QtWidgets.QApplication.processEvents()

        # save registration info info
        tmp = self.nmMoving[:self.nmMoving.rfind('.')] + ".pkl"
        outputFolder = os.path.join(self.jobFolder, self.ResultsName, "Registration transforms")
        outfile = os.path.join(outputFolder, tmp)

        # Check if the folder exists, and create it if it doesn't
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        tform = self.tform
        RMSE0 = self.RMSE0
        RMSE = self.RMSE
        # Save variables to the pkl file
        with open(outfile, 'wb') as file:
            pickle.dump({'tform': tform,'RMSE': RMSE, 'RMSE0': RMSE0,
                         }, file)

        # save the images
        self.save_registered_images()

        # what to do next
        self.ui.SaveRegistrationControlFrame.setEnabled(False)
        self.ui.ImageViewControlsFrame_O.setEnabled(False)
        self.ui.DisableFrame_O1.setVisible(True)
        self.ui.DisableFrame_O2.setVisible(True)

    def initiate_import_project_tab(self):

        # save the current fiducial points and view settings if the user is in the fiducials tab
        self.close_navigation_tab()
        self.save_fiducial_state()

        # go to import project tab
        self.ui.tabWidget.setCurrentIndex(self.import_project_tab)
        # check status of tables
        self.check_if_tables_are_complete_import_project_tab()

    def initiate_job_status_tab(self):

        # save the current fiducial points and view settings if the user is in the fiducials tab
        self.close_navigation_tab()
        self.save_fiducial_state()

        # set up the table
        self.ui.JobStatusTableWidget.setHorizontalHeaderLabels(["Image Name", "# Fiducial Pairs", "Registration Calculated", "Images Registered"," "])

        num_rows = self.movingIMS.shape[0] + 1
        self.ui.JobStatusTableWidget.setRowCount(num_rows)

        # populate the rows of the table with the info in movingIMS
        self.ui.JobStatusTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"Fixed image: {self.nmFixed}  "))
        self.ui.JobStatusTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(" - "))
        self.ui.JobStatusTableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(" - "))
        self.ui.JobStatusTableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(" - "))

        row_count = 1
        for row in self.movingIMS:
            self.ui.JobStatusTableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(f"Moving image {row_count}:  {row[0]}  "))
            row_count += 1

        # check if corresponding files exist
        check_file_status = np.zeros((self.movingIMS.shape[0], 3), dtype=int)
        folder_1 = os.path.join(self.jobFolder, self.ResultsName, "Fiducial point selection")
        folder_2 = os.path.join(self.jobFolder, self.ResultsName, "Registration transforms")
        folder_3 = os.path.join(self.jobFolder, self.ResultsName, "Registered images")
        for i, row in enumerate(self.movingIMS):
            image_file = row[0]
            image_name, _ = os.path.splitext(image_file)

            # Construct the expected .pkl filenames
            outfile = os.path.join(folder_1, f"{image_name}.pkl")
            if os.path.exists(outfile):
                with open(outfile, 'rb') as file:
                    data = pickle.load(file)
                pts = data.get('pts_F')
                if pts.shape[0] >= 10:
                    check_file_status[i, 0] = pts.shape[0]
            outfile = os.path.join(folder_2, f"{image_name}.pkl")
            if os.path.exists(outfile):
                with open(outfile, 'rb') as file:
                    data = pickle.load(file)
                RMSE = data.get('RMSE')
                check_file_status[i, 1] = RMSE
            else:
                check_file_status[i, 1] = 0
            if os.path.exists(os.path.join(folder_3, f"{image_name}.jpg")):
                check_file_status[i, 2] = 1

        row_count = 1
        for row in check_file_status:
            # fiducial point setting
            self.ui.JobStatusTableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(f"{row[0]} pairs"))
            #cell_item = QtWidgets.QTableWidgetItem(f"{row[0]} pairs")
            #if row[0] >= 10:
            #    cell_item.setBackground(QBrush(QColor("#40ad40")))
            #else:
            #    cell_item.setBackground(QBrush(QColor("#40ad40")))
            #self.ui.JobStatusTableWidget.setItem(row_count, 1, cell_item)
            if row[1]:
                self.ui.JobStatusTableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(f"RMSE: {str(row[1])} pixels"))
            else:
                self.ui.JobStatusTableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(""))

            if row[2] == 1:
                self.ui.JobStatusTableWidget.setItem(row_count, 3, QtWidgets.QTableWidgetItem("done"))
            else:
                self.ui.JobStatusTableWidget.setItem(row_count, 3, QtWidgets.QTableWidgetItem(""))
            row_count += 1

        # go to job status tab
        self.ui.tabWidget.setCurrentIndex(self.job_status_tab)
        self.ui.JobStatusTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def initiate_fiducials_tab(self):

        # save the current fiducial points and view settings if the user is in the fiducials tab
        self.close_navigation_tab()
        self.save_fiducial_state()

        # save job settings in a template file
        self.save_template_file()

        # initial button settings
        self.ui.ChooseMovingImageFrame.setVisible(True)
        self.ui.LoadNewMovingImageButton.setEnabled(False)
        self.ui.LoadOldMovingImageButton.setEnabled(False)
        self.ui.FiducialPointControlsFrame.setVisible(False)
        self.ui.PickNewMovingImageButton.setVisible(False)
        self.ui.AttemptICPRegistrationButton.setVisible(False)
        self.ui.FiducialTabUpdateText.setVisible(False)
        QtWidgets.QApplication.processEvents()

        # populate dropdown lists
        self.populate_moving_images_combo_box()
        self.ui.LoadNewMovingImageButton.setStyleSheet(self.inactiveButton)
        self.ui.LoadOldMovingImageButton.setStyleSheet(self.inactiveButton)

        # load and display fixed image
        image_path = os.path.join(self.pthFixed, self.nmFixed)
        if self.nmFixed != self.nmLoadedFixed:
            self.imFixed0 = self.load_image(image_path)  # store the original pixmap
            self.nmLoadedFixed = self.nmFixed

        # Calculate zoom_default
        width_scale = self.ui.FixedImageDisplayFrame.width() / self.imFixed0.width()
        height_scale = self.ui.FixedImageDisplayFrame.height() / self.imFixed0.height()
        self.fixed_zoom_default = min(width_scale, height_scale)

        # go to fiducials tab
        self.ui.tabWidget.setCurrentIndex(self.fiducials_tab)
        self.update_button_color()

        # set fiducial point count
        self.ptsFixed = np.array([[0, 0]], dtype=np.float64)
        self.ptsMoving = np.array([[0, 0]], dtype=np.float64)
        self.editWhichImage = 0
        self.add_fiducial_active = 0
        self.highlight_current_frame()

        # display image
        self.imMoving0 = []
        self.moving_zoom_default = 1
        self.editWhichImage = 0
        self.reset_transformations(self.editWhichImage)
        self.editWhichImage = 1
        self.reset_transformations(self.editWhichImage)

    def update_both_images(self):

        self.define_edit_frame()
        if self.current_index == self.fiducials_tab or self.current_index == self.overlay_tab: # fiducials tab
            self.editWhichImage = not self.editWhichImage
            self.update_image_view()
            self.editWhichImage = not self.editWhichImage
            self.update_image_view()
        elif self.current_index == self.apply_to_data_tab: # apply to coordinates tab
            self.update_image_view()

    def update_image_view(self):
        """Update the image view with all transformations (flip, rotate, zoom, and pan) preserved."""

        # define the current frame variables and pixmap
        self.update_zoom_default(self.editWhichImage)
        self.define_edit_frame(self.editWhichImage)
        if self.current_index == self.fiducials_tab:
            if self.editWhichImage == 0:  # fiducials tab fixed image
                pixmap = self.imFixed0
            else: # fiducials tab moving image
                pixmap = self.imMoving0
            self.pts = np.delete(self.pts, 0, axis=0)  # remove the first point
        elif self.current_index == self.overlay_tab:
            if self.editWhichImage == 0: # overlay tab unregistered images
                pixmap = self.imOverlay0
            else:  # overlay tab registered images
                pixmap = self.imOverlay #self.imMovingReg
            self.pts = np.delete(self.pts, 0, axis=0)  # remove the first point
        elif self.current_index == self.apply_to_data_tab:
            if self.editWhichImage == 0: # register coordinates tab unregistered moving image
                pixmap = self.imMovingCoords
            elif self.editWhichImage == 1: # register coordinates tab registered moving image
                pixmap = self.imMovingCoordsReg
            else: # Apply to coordinates tab fixed image
                pixmap = self.imFixed0
            # randomly subsample the coordinate points
            self.pts = self.pts[self.sampled_indices]
        else:
            return

        zz = self.zoom_scale / self.zoom_default
        if pixmap is not None:
            if pixmap == []:
                self.label.clear()
                return

            if self.brightness != 0 or self.contrast != 1:
                pixmap = self.adjust_brightness_contrast(pixmap, self.contrast, self.brightness)

            size_pt = max([int(np.ceil(max([pixmap.width(), pixmap.height()]) / 1000 / zz * self.rad)), 1])
            #if self.current_index == self.apply_to_data_tab and self.editWhichImage > 0 and zz < 2.5:
            #    size_pt = max([int(np.ceil(max([pixmap.width(), pixmap.height()]) / 1000 / 2.5 * self.rad)), 1])
            pixmap = self.add_points_to_image(pixmap, self.pts, size_pt, self.ptsColor)

            #if self.current_index == self.apply_to_data_tab:
            #    self.imPlotHold = pixmap

            if self.current_index == self.fiducials_tab : # if in fiducials tab, overlay the potential deletion point if required
                # update fiducial point count
                count = self.ptsMoving.shape[0] - 1
                self.ui.FiducialFrameHeaderText.setText(f"Fiducial Point View (# Pairs : {count})")
                if count > 9:
                    self.ui.AttemptICPRegistrationButton.setVisible(True)
                else:
                    self.ui.AttemptICPRegistrationButton.setVisible(False)

                if self.delete_mode_active and self.potential_deletion != -5:
                    size_pt = size_pt * 2
                    color = QColor(round(self.ptsColor.red() * 0.5), round(self.ptsColor.green() * 0.5), round(self.ptsColor.blue() * 0.5))
                    pixmap = self.add_points_to_image(pixmap, [self.pts[self.potential_deletion]], size_pt, color)
            elif self.current_index == self.overlay_tab: # if in overlay tab, also overlay the fiducial points of the moving image
                self.rad = self.rad_tabOb
                size_pt = max([int(np.ceil(max([pixmap.width(), pixmap.height()]) / 1000 / zz * self.rad)), 1])
                if self.editWhichImage == 0:
                    self.pts2 = np.delete(self.pts2, 0, axis=0)

                color = self.ptsColor_tabOb
                pixmap = self.add_points_to_image(pixmap, self.pts2, size_pt, color)

            # Create a transformation matrix,apply flip, rotation, and zoom
            transform = QTransform()
            if self.flip_state:
                transform.scale(-1, 1)
            transform.rotate(self.rotation_angle)
            transform.scale(self.zoom_scale, self.zoom_scale)
            transformed_pixmap = pixmap.transformed(transform, mode=Qt.SmoothTransformation)
            self.label.setPixmap(transformed_pixmap)
            self.label.resize(transformed_pixmap.size())

            # Apply pan offsets
            offset_x, offset_y = self._apply_flip_and_rotation()
            parent_rect = self.label.parent().rect()
            new_x = offset_x + (parent_rect.width() - self.label.width()) // 2
            new_y = offset_y + (parent_rect.height() - self.label.height()) // 2
            self.label.move(int(new_x), int(new_y))

    def add_points_to_image(self, pixmap, pts, size_pt, color):

        pts = np.round(pts).astype(int)

        # overlay the fiducial points
        image = pixmap.toImage()
        width = image.width()
        height = image.height()
        bytes_per_line = image.bytesPerLine()

        # Convert QImage to NumPy array
        ptr = image.bits()
        channels = int(np.size(ptr) / width / height)
        ptr = np.array(ptr).reshape((height, bytes_per_line))  # Convert memoryview to NumPy array
        array = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width, channels))

        # Define the square region bounds
        x_start = np.maximum(pts[:, 0] - size_pt, 0)  # Ensure within image bounds
        x_end = np.minimum(pts[:, 0] + size_pt + 1, width)  # Ensure within image bounds
        y_start = np.maximum(pts[:, 1] - size_pt, 0)  # Ensure within image bounds
        y_end = np.minimum(pts[:, 1] + size_pt + 1, height)  # Ensure within image bounds
        mask = np.zeros(array.shape[:2], dtype=bool)
        for x_s, x_e, y_s, y_e in zip(x_start, x_end, y_start, y_end):
            mask[y_s:y_e, x_s:x_e] = True

        # Apply changes to all pixels in the mask
        array[mask, 0] = color.blue()  # Blue channel
        array[mask, 1] = color.green()  # Green channel
        array[mask, 2] = color.red()  # Red channel

        # Convert the modified array back to QImage
        new_image = QImage(array.data, width, height, QImage.Format_ARGB32 if channels == 4 else QImage.Format_RGB888)
        image_pts = QPixmap.fromImage(new_image)

        return image_pts

    def _apply_flip_and_rotation(self):

        # account for the effect of rotation
        self.define_edit_frame()
        if self.rotation_angle == 90:
            if self.flip_state:
                return self.pan_offset_y, -self.pan_offset_x
            else:
                return -self.pan_offset_y, self.pan_offset_x
        elif self.rotation_angle == 180:
            return -self.pan_offset_x, -self.pan_offset_y
        elif self.rotation_angle == 270:
            if self.flip_state:
                return -self.pan_offset_y, self.pan_offset_x
            else:
                return self.pan_offset_y, -self.pan_offset_x
        else:  # 0 degrees
            return self.pan_offset_x, self.pan_offset_y

    def adjust_brightness_contrast(self, pixmap, contrast, brightness):
        # Convert QPixmap to QImage
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format_RGB888)

        # Get width, height, and bytes per line
        width = image.width()
        height = image.height()
        bytes_per_line = image.bytesPerLine()

        # Create a NumPy array from the image bits
        ptr = image.bits()
        array = np.frombuffer(ptr, dtype=np.uint8).reshape((height, bytes_per_line))  # Full buffer with padding

        # Crop to actual image width (remove padding bytes at the end of each row)
        array = array[:, :width * 3].reshape((height, width, 3))  # Reshape into RGB format

        # Extract RGB channels
        r, g, b = array[:, :, 0], array[:, :, 1], array[:, :, 2]

        # Apply brightness and contrast adjustments
        def adjust_channel(channel, brightness, contrast):
            channel = channel.astype(np.float32)
            channel = channel * contrast + brightness
            channel = np.clip(channel, 0, 255)
            return channel.astype(np.uint8)

        r = adjust_channel(r, brightness, contrast)
        g = adjust_channel(g, brightness, contrast)
        b = adjust_channel(b, brightness, contrast)

        # Combine channels back into the QImage
        adjusted_array = np.stack((r, g, b), axis=-1)
        adjusted_image = QImage(adjusted_array.data, width, height, adjusted_array.strides[0], QImage.Format_RGB888)

        # Convert back to QPixmap
        pixmap = QPixmap.fromImage(adjusted_image)
        return pixmap

    def mousePressEvent(self, event):
        """Handle mouse press events."""

        # skip if the current tab does not contain an image
        if self.current_index != self.fiducials_tab and self.current_index != self.overlay_tab and self.current_index != self.apply_to_data_tab:
            return

        if self.add_fiducial_active:
            self.editWhichImage = self.editWhichFid
        self.define_edit_frame()

        # figure out which image
        frame_info_left = self.frame_left.geometry()
        frame_info_right = self.frame_right.geometry()
        cursor_pos = self.mapFromGlobal(event.globalPosition().toPoint())
        y = cursor_pos.y() - self.padnum
        in_left_x = cursor_pos.x() > frame_info_left.x() and cursor_pos.x() < frame_info_left.x() + frame_info_left.width()
        in_left_y = y > frame_info_left.y() and y < frame_info_left.y() + frame_info_left.height()
        in_right_x = cursor_pos.x() > frame_info_right.x() and cursor_pos.x() < frame_info_right.x() + frame_info_right.width()
        in_right_y = y > frame_info_right.y() and y < frame_info_right.y() + frame_info_right.height()

        # left click to pan
        if event.button() == Qt.LeftButton:
            if in_left_x and in_left_y:
                if self.current_index != self.apply_to_data_tab:
                    self.editWhichImage = 0
            elif in_right_x and in_right_y:
                if self.current_index != self.apply_to_data_tab:
                    self.editWhichImage = 1
            else:
                return

            # Get the mouse position relative to the target label
            self.define_edit_frame(self.editWhichImage)
            self.panning = 1
            self.last_mouse_position = event.globalPosition()  # Store the initial mouse position

    def mouseMoveEvent(self, event):
        """Handle mouse move events for panning."""

        # if panning
        if self.panning != 0:
            self.panning += self.panning # the mouse was clicked and now moved
            delta = event.globalPosition() - self.last_mouse_position
            self.last_mouse_position = event.globalPosition()

            # remove the effect of rotation and flipping
            if self.rotation_angle == 90:
                if self.flip_state:
                    offset_x = -delta.y()
                    offset_y = delta.x()
                else:
                    offset_x = delta.y()
                    offset_y = -delta.x()
            elif self.rotation_angle == 180:
                offset_x = -delta.x()
                offset_y = -delta.y()
            elif self.rotation_angle == 270:
                if self.flip_state:
                    offset_x = delta.y()
                    offset_y = -delta.x()
                else:
                    offset_x = -delta.y()
                    offset_y = delta.x()
            else:
                offset_x = delta.x()
                offset_y = delta.y()

            # Update pan offsets
            self.pan_offset_x += offset_x
            self.pan_offset_y += offset_y
            self.return_edit_frame(self.editWhichImage)

            # Reapply transformations
            self.update_image_view()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""

        if event.button() == Qt.LeftButton:
            if self.panning < 3 and self.current_index == self.fiducials_tab and (self.add_fiducial_active or self.delete_mode_active):

                if self.add_fiducial_active:
                    self.editWhichImage = self.editWhichFid
                self.define_edit_frame()

                # figure out which image
                frame_info_left = self.frame_left.geometry()
                frame_info_right = self.frame_right.geometry()
                cursor_pos = self.mapFromGlobal(event.globalPosition().toPoint())
                y = cursor_pos.y() - self.padnum
                in_left_x = cursor_pos.x() > frame_info_left.x() and cursor_pos.x() < frame_info_left.x() + frame_info_left.width()
                in_left_y = y > frame_info_left.y() and y < frame_info_left.y() + frame_info_left.height()
                in_right_x = cursor_pos.x() > frame_info_right.x() and cursor_pos.x() < frame_info_right.x() + frame_info_right.width()
                in_right_y = y > frame_info_right.y() and y < frame_info_right.y() + frame_info_right.height()

                # right-click to add or delete fiducials
                local_pos = self.label.mapFromGlobal(event.globalPosition().toPoint())
                if self.add_fiducial_active: # add a fiducial
                    if in_left_x and in_left_y and self.editWhichFid == 0:
                        self.handle_fiducial_click(local_pos.x(), local_pos.y(), event)
                    elif in_right_x and in_right_y and self.editWhichFid == 1:
                        self.handle_fiducial_click(local_pos.x(), local_pos.y(), event)
                elif self.delete_mode_active and self.current_index == self.fiducials_tab:
                    cursor_pos = self.mapFromGlobal(event.globalPosition().toPoint())
                    self.handle_fiducial_click(cursor_pos.x(), cursor_pos.y(), event)
                else:
                    return
        self.panning = 0

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming."""

        self.define_edit_frame()
        if self.current_index != self.fiducials_tab and self.current_index != self.overlay_tab and self.current_index != self.apply_to_data_tab:
            return

        # figure out which image to zoom
        frame_info_left = self.frame_left.geometry()
        frame_info_right = self.frame_right.geometry()
        cursor_pos = self.mapFromGlobal(event.globalPosition().toPoint())
        y = cursor_pos.y() - self.padnum
        in_left_x = cursor_pos.x() > frame_info_left.x() and cursor_pos.x() < frame_info_left.x() + frame_info_left.width()
        in_left_y = y > frame_info_left.y() and y < frame_info_left.y() + frame_info_left.height()
        in_right_x = cursor_pos.x() > frame_info_right.x() and cursor_pos.x() < frame_info_right.x() + frame_info_right.width()
        in_right_y = y > frame_info_right.y() and y < frame_info_right.y() + frame_info_right.height()

        if in_left_x and in_left_y:
            if self.current_index != self.apply_to_data_tab:
                self.editWhichImage = 0
        elif in_right_x and in_right_y:
            if self.current_index != self.apply_to_data_tab:
                self.editWhichImage = 1
        else:
            return

        # Get the mouse position relative to the target label
        self.define_edit_frame(self.editWhichImage)
        cursor_pos = self.label.mapFromGlobal(event.globalPosition().toPoint())

        # remove the effect of rotation and flipping
        if self.rotation_angle == 90:
            if self.flip_state:
                zoom_focus_x = -(cursor_pos.y() - self.label.height() / 2)
                zoom_focus_y = (cursor_pos.x() - self.label.width() / 2)
            else:
                zoom_focus_x = (cursor_pos.y() - self.label.height() / 2)
                zoom_focus_y = -(cursor_pos.x() - self.label.width() / 2)
        elif self.rotation_angle == 180:
            zoom_focus_x = -(cursor_pos.x() - self.label.width() / 2)
            zoom_focus_y = -(cursor_pos.y() - self.label.height() / 2)
        elif self.rotation_angle == 270:
            if self.flip_state:
                zoom_focus_x = (cursor_pos.y() - self.label.height() / 2)
                zoom_focus_y = -(cursor_pos.x() - self.label.width() / 2)
            else:
                zoom_focus_x = -(cursor_pos.y() - self.label.height() / 2)
                zoom_focus_y = (cursor_pos.x() - self.label.width() / 2)
        else:
            zoom_focus_x = (cursor_pos.x() - self.label.width() / 2)
            zoom_focus_y = (cursor_pos.y() - self.label.height() / 2)

        # Adjust zoom scale based on scroll direction
        delta = event.angleDelta().y()
        scale_factor = 1.1 if delta > 0 else 0.9
        new_zoom_scale = self.zoom_scale * scale_factor
        new_zoom_scale = max(0.1, min(new_zoom_scale, 10.0))  # Clamp between 0.1 and 10.0

        # Calculate scaling factor and adjust pan offsets
        scale_change = new_zoom_scale / self.zoom_scale
        self.pan_offset_x += zoom_focus_x * (1 - scale_change)
        self.pan_offset_y += zoom_focus_y * (1 - scale_change)
        self.zoom_scale = new_zoom_scale

        # Update the zoom scale and pan offsets
        self.return_edit_frame(self.editWhichImage)

        # Reapply transformations
        self.update_image_view()

    def populate_moving_images_combo_box(self):
        """
        Populate the QComboBox with strings from column 1 of self.movingIMS.
        """

        # Clear the current items in the combo box
        self.ui.MovingImagesComboBox.clear()
        self.ui.OldMovingImagesComboBox.clear()

        # initialize the combo box list
        self.ui.MovingImagesComboBox.addItem("Select")
        self.ui.OldMovingImagesComboBox.addItem("Select")
        self.numMovingDelete = [[], []]

        # Add items from column 1 of self.movingIMS
        for index, row in enumerate(self.movingIMS):
            if len(row) > 1:  # Ensure the row has at least two columns
                filename = row[0]  # Get the filename from column 1
                filename_out = filename[:filename.rfind('.')] + ".pkl" # dot_index = filename.find(".") filename_out = "moving_image_" + filename[:dot_index] + ".png"
                filepath = os.path.join(self.jobFolder, self.ResultsName, "Registration transforms", filename_out) # os.path.join(self.jobFolder, self.ResultsName, "aligned_stack", filename_out)

                if os.path.isfile(filepath):  # Check if the file exists
                    self.ui.OldMovingImagesComboBox.addItem(filename)  # Add to OldMovingImagesComboBox
                    self.numMovingDelete[0].append(index)
                else:
                    self.ui.MovingImagesComboBox.addItem(filename)  # Add to MovingImagesComboBox
                    self.numMovingDelete[1].append(index)

    def new_combobox_selection_changed(self, index):
        # This code will execute when the selected item in the combo box changes
        selected_item = self.ui.MovingImagesComboBox.currentText()

        if selected_item == "Select":
            self.ui.LoadNewMovingImageButton.setEnabled(False)
            self.ui.LoadNewMovingImageButton.setStyleSheet(self.inactiveButton)
        else:
            self.ui.OldMovingImagesComboBox.setCurrentIndex(0)
            self.ui.LoadOldMovingImageButton.setEnabled(False)
            self.ui.LoadOldMovingImageButton.setStyleSheet(self.inactiveButton)

            self.ui.LoadNewMovingImageButton.setEnabled(True)
            self.ui.LoadNewMovingImageButton.setStyleSheet(self.activeButton)

    def old_combobox_selection_changed(self, index):
        # This code will execute when the selected item in the combo box changes
        selected_item = self.ui.OldMovingImagesComboBox.currentText()

        if selected_item == "Select":
            self.ui.LoadOldMovingImageButton.setEnabled(False)
            self.ui.LoadOldMovingImageButton.setStyleSheet(self.inactiveButton)
        else:
            self.ui.MovingImagesComboBox.setCurrentIndex(0)
            self.ui.LoadNewMovingImageButton.setStyleSheet(self.inactiveButton)

            self.ui.LoadOldMovingImageButton.setEnabled(True)
            self.ui.LoadOldMovingImageButton.setStyleSheet(self.activeButton)

    def load_new_moving_image(self):

        # get the current filename and index from the droplist
        current_index_in_table = self.ui.MovingImagesComboBox.currentIndex()
        row_number = self.numMovingDelete[1]
        row_number = row_number[current_index_in_table - 1]
        self.import_moving_image(row_number)

    def load_old_moving_image(self):
        # get the current filename and index from the droplist
        current_index_in_table = self.ui.OldMovingImagesComboBox.currentIndex()
        row_number = self.numMovingDelete[0]
        row_number = row_number[current_index_in_table - 1]
        self.import_moving_image(row_number)

    def save_fiducial_state(self):
        self.define_edit_frame()
        if self.current_index == self.fiducials_tab and self.ptsFixed.shape[0] > 1:
            # save fiducial info
            tmp = self.nmMoving[:self.nmMoving.rfind('.')] + ".pkl"
            outputFolder = os.path.join(self.jobFolder, self.ResultsName, "Fiducial point selection")
            outfile = os.path.join(outputFolder, tmp)

            # Check if the folder exists, and create it if it doesn't
            if not os.path.exists(outputFolder):
                os.makedirs(outputFolder)
            panx_F = self.fixed_pan_offset_x
            pany_F = self.fixed_pan_offset_y
            rot_F = self.fixed_rotation_angle
            flip_F = self.fixed_flip_state
            zoom_F = self.fixed_zoom_scale
            zoom0_F = self.fixed_zoom_default
            con_F = self.fixed_contrast
            bri_F = self.fixed_brightness
            pts_F = self.ptsFixed

            panx_M = self.moving_pan_offset_x
            pany_M = self.moving_pan_offset_y
            rot_M = self.moving_rotation_angle
            flip_M = self.moving_flip_state
            zoom_M = self.moving_zoom_scale
            zoom0_M = self.moving_zoom_default
            con_M = self.moving_contrast
            bri_M = self.moving_brightness
            pts_M = self.ptsMoving

            pts_size = self.rad_tabF
            pts_color = self.ptsColor_tabF

            # Save variables to the pkl file
            with open(outfile, 'wb') as file:
                pickle.dump({'panx_F': panx_F, 'pany_F': pany_F, 'rot_F': rot_F, 'flip_F': flip_F,
                             'zoom_F': zoom_F, 'zoom0_F': zoom0_F, 'con_F': con_F, 'bri_F': bri_F,
                             'panx_M': panx_M, 'pany_M': pany_M, 'rot_M': rot_M, 'flip_M': flip_M,
                             'zoom_M': zoom_M, 'zoom0_M': zoom0_M, 'con_M': con_M, 'bri_M': bri_M,
                             'pts_F': pts_F, 'pts_M': pts_M, 'pts_size': pts_size, 'pts_color': pts_color,
                             }, file)

    def import_moving_image(self, row_number):

        self.nmMoving = self.movingIMS[row_number][0]
        self.scaleMoving = self.movingIMS[row_number][1]
        self.pthMoving = self.movingIMS[row_number][2]

        # load the image
        image_path = os.path.join(self.pthMoving, self.nmMoving)
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return
        self.imMoving0 = self.load_image(image_path)  # store the original pixmap

        # check if saved fiducial points exist
        tmp = self.nmMoving[:self.nmMoving.rfind('.')] + ".pkl"
        outputFolder = os.path.join(self.jobFolder, self.ResultsName, "Fiducial point selection")
        outfile = os.path.join(outputFolder, tmp)
        if os.path.exists(outfile):
            self.load_previous_settings(outfile)
            self.update_both_images()
        else:
            # Calculate zoom_default
            width_scale = self.ui.MovingImageDisplayFrame.width() / self.imMoving0.width()
            height_scale = self.ui.MovingImageDisplayFrame.height() / self.imMoving0.height()
            self.moving_zoom_default = min(width_scale, height_scale)

            self.editWhichImage = 0
            self.reset_transformations(self.editWhichImage)
            self.editWhichImage = 1
            self.reset_transformations(self.editWhichImage)

        # display image
        self.update_button_color()

        # change some view settings
        self.ui.ChooseMovingImageFrame.setVisible(False)
        self.ui.FiducialPointControlsFrame.setVisible(True)
        self.ui.PickNewMovingImageButton.setVisible(True)

    def load_previous_settings(self, outfile):
        with open(outfile, 'rb') as file:
            data = pickle.load(file)

        # Check if the folder exists, and create it if it doesn't
        self.fixed_pan_offset_x = data.get('panx_F')
        self.fixed_pan_offset_y = data.get('pany_F')
        self.fixed_rotation_angle = data.get('rot_F')
        self.fixed_flip_state = data.get('flip_F')
        self.fixed_zoom_scale = data.get('zoom_F')
        self.fixed_zoom_default = data.get('zoom0_F')
        self.fixed_contrast = data.get('con_F')
        self.fixed_brightness = data.get('bri_F')

        self.moving_pan_offset_x = data.get('panx_M')
        self.moving_pan_offset_y = data.get('pany_M')
        self.moving_rotation_angle = data.get('rot_M')
        self.moving_flip_state = data.get('flip_M')
        self.moving_zoom_scale = data.get('zoom_M')
        self.moving_zoom_default = data.get('zoom0_M')
        self.moving_contrast = data.get('con_M')
        self.moving_brightness = data.get('bri_M')

        self.ptsFixed = data.get('pts_F')
        self.ptsMoving = data.get('pts_M')
        self.rad_tabF  = data.get('pts_size')
        self.ptsColor_tabF = data.get('pts_color')

    def confirm_load_new_image(self):
        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("Load a new moving image?")  # Set the window title
        msg_box.setText("Are you sure you want to load a new image? (the current fiducials will be saved)")  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        msg_box.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons

        # Apply custom stylesheet for background and font color
        msg_box.setStyleSheet(self.style_QuestBox)

        # Show the message box and get the response
        response = msg_box.exec()
        if response == QtWidgets.QMessageBox.Cancel:
            return

        # save the fiducial points
        self.save_fiducial_state()
        self.initiate_fiducials_tab()

    def handle_value_update_fixed(self, new_value, row, column):
        """Handle the new value emitted by the delegate."""

        # Optionally update other variables or UI elements
        if column == 1:  # For example, update ScaleFixed if editing the Scale column
            # Check if the string is a number
            try:
                float(new_value)
                self.ScaleFixed = new_value
            except:
                text = "The entered value is not a number. Please enter a number"
                self.show_error_message(text)
            self.populate_fixed_table()

    def handle_value_update_moving(self, new_value, row, column):
        """Handle the new value emitted by the delegate."""

        # Optionally update other variables or UI elements
        if column == 1:  # For example, update ScaleFixed if editing the Scale column
            # Check if the string is a number
            try:
                float(new_value)
                self.movingIMS[row][column] = new_value
            except:
                text = "The entered value is not a number. Please enter a number"
                self.show_error_message(text)
            self.populate_moving_table()

    def handle_value_update_job(self, new_value, row, column):
        """Handle the new value emitted by the delegate."""

        # Optionally update other variables or UI elements
        if column == 0:  # For example, update ScaleFixed if editing the Scale column
            # Check if the string is a number

            max_folder_length = 255
            invalid_chars = '<>:\"/\\|?*'
            reserved_names = [
                "CON", "PRN", "AUX", "NUL",
                "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
                "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"]

            t1 = len(new_value) > max_folder_length
            t2 = new_value.upper() in reserved_names
            t3 = any(char in new_value for char in invalid_chars)
            t4 = new_value == ""
            if t1 or t2 or t3 or t4:
                text = f"The entered value {new_value} is not a valid folder name. Please try again."
                self.show_error_message(text)
            else:
                self.ResultsName = new_value
            self.populate_project_table()

    def doubleclick_moving_table(self, row, column):

        # if the table is populated and table edit mode is not already active
        if len(self.movingIMS) > 0 and self.editTableActive == 0:

            # if editing the scale
            if column == 1:
                # enable text input to the scale window
                item = self.ui.movingImageTableWidget.item(row, column)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Enable editing
                    self.ui.movingImageTableWidget.editItem(item)  # Put the cell into edit mode
            elif column == 0 or column == 2:
                # turn on edit table mode
                self.editTableActive = 2  # moving image
                self.enter_edit_table()
                self.numMovingDelete = row

                # make delete visible
                self.ui.keepMovingImageButton.setVisible(True)
                self.ui.deleteMovingImageButton.setVisible(True)

    def doubleclick_fixed_table(self, row, column):

        # if the table is populated and table edit mode is not already active
        if len(self.nmFixed) > 0 and self.editTableActive == 0:

            # if editing the scale
            if column == 1:
                # enable text input to the results name window
                item = self.ui.fixedImageTableWidget.item(row, column)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Enable editing
                    self.ui.fixedImageTableWidget.editItem(item)  # Put the cell into edit mode
            elif column == 0 or column == 2:
                # turn on edit table mode
                self.editTableActive = 1  # fixed image
                self.enter_edit_table()

                # make delete visible
                self.ui.keepFixedImageButton.setVisible(True)
                self.ui.deleteFixedImageButton.setVisible(True)

    def doubleclick_job_table(self, row, column):

        # if table edit mode is not already active
        if self.editTableActive == 0:

            # if editing the job name
            if column == 0:
                item = self.ui.setJobTableWidget.item(row, column)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Enable editing
                    self.ui.setJobTableWidget.editItem(item)  # Put the cell into edit mode

    def enter_edit_table(self):

        # disable other buttons
        self.ui.setJobTableWidget.setEnabled(False)
        self.ui.chooseFixedImageButton.setEnabled(False)
        self.ui.chooseMovingImageButton.setEnabled(False)
        self.ui.loadTemplateButton.setEnabled(False)
        self.close_navigation_tab()
        self.ui.NavigationButton.setVisible(False)

        if self.editTableActive == 1:
            self.ui.DefineMovingImageFrame.setEnabled(False)
        elif self.editTableActive == 2:
            self.ui.DefineFixedImageFrame.setEnabled(False)

    def exit_edit_table(self):
        # turn off edit table active
        self.editTableActive = 0

        # disable other buttons
        self.ui.DefineFixedImageFrame.setEnabled(True)
        self.ui.DefineMovingImageFrame.setEnabled(True)
        self.ui.setJobTableWidget.setEnabled(True)
        self.ui.chooseFixedImageButton.setEnabled(True)
        self.ui.chooseMovingImageButton.setEnabled(True)
        self.ui.loadTemplateButton.setEnabled(True)
        self.ui.NavigationButton.setVisible(True)

        # make delete invisible
        self.ui.keepFixedImageButton.setVisible(False)
        self.ui.deleteFixedImageButton.setVisible(False)
        self.ui.keepMovingImageButton.setVisible(False)
        self.ui.deleteMovingImageButton.setVisible(False)

    def keep_fixed_image(self):
        self.exit_edit_table()

    def delete_fixed_image(self):
        # delete the body of the table
        self.nmFixed = ""
        self.pthFixed = ""
        self.ScaleFixed = ""
        self.populate_fixed_table()
        if self.ui.JobFolderCheckBox.isChecked():
            self.ui.JobFolderCheckBox.setChecked(False)
            self.jobFolder = ""
            self.populate_project_table()
        self.exit_edit_table()

    def keep_moving_image(self):
        self.exit_edit_table()

    def delete_moving_image(self):
        # remove the selected image from the table
        self.movingIMS = np.delete(self.movingIMS, self.numMovingDelete, axis=0)

        self.populate_moving_table()
        self.exit_edit_table()

    def checkbox_changed(self, state):
        """Handle the checkbox state change."""
        if state > 0:
            self.jobFolder = self.pthFixed
        else:
            self.jobFolder = ""
        self.populate_project_table()

    def show_error_message(self, text):
        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("ERROR MESSAGE")  # Set the window title
        msg_box.setText(text)  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        msg_box.setStandardButtons(
            QtWidgets.QMessageBox.Ok)  # Add Yes and Cancel buttons

        # Apply custom stylesheet for background and font color
        msg_box.setStyleSheet(self.style_QuestBox)

        # Show the message box and get the response
        response = msg_box.exec()

    def browse_for_job_folder(self):

        if self.jobFolder:
            msg_box = QtWidgets.QMessageBox()  # Create a message box
            msg_box.setWindowTitle("Job Folder Already Defined")  # Set the window title
            msg_box.setText("Would you like to Replace the Current Job Folder?")  # Set the message text
            msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
            msg_box.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons

            # Apply custom stylesheet for background and font color
            msg_box.setStyleSheet(self.style_QuestBox)

            # Show the message box and get the response
            response = msg_box.exec()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        folder = QFileDialog.getExistingDirectory(self, "Select Job Folder", "")
        if folder:  # If a file is selected
            self.jobFolder = folder
            self.populate_project_table()

    def browse_for_moving_image(self):

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Moving Image File", "")
        if filename:  # If a file is selected
            self.pthMoving, self.nmMoving = os.path.split(filename)
            self.scaleMoving = ""
            if self.is_image_file(self.pthMoving, self.nmMoving):

                if len(self.movingIMS) == 0:
                    self.movingIMS = np.array([[self.nmMoving, self.scaleMoving, self.pthMoving]], dtype=object)
                else:
                    add_to_list = np.array([self.nmMoving, self.scaleMoving, self.pthMoving])
                    self.movingIMS = np.vstack([self.movingIMS, add_to_list])
                self.populate_moving_table()

    def browse_for_fixed_image(self):

        if self.nmFixed:
            msg_box = QtWidgets.QMessageBox()  # Create a message box
            msg_box.setWindowTitle("Fixed Image Already Defined")  # Set the window title
            msg_box.setText("Would you like to Replace the Current Fixed Image?")  # Set the message text
            msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
            msg_box.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons

            # Apply custom stylesheet for background and font color
            msg_box.setStyleSheet(self.style_QuestBox)

            # Show the message box and get the response
            response = msg_box.exec()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Fixed Image File", "")
        if filename:  # If a file is selected
            self.pthFixed, self.nmFixed = os.path.split(filename)
            if self.is_image_file(self.pthFixed, self.nmFixed):
                self.populate_fixed_table()

    def is_image_file(self, file_folder, file_name):
        try:
            with Image.open(os.path.join(file_folder, file_name)) as img:
                img.verify()  # Verify that it is an image
            return True
        except (IOError, SyntaxError):
            return False

    def populate_moving_table(self):

        if len(self.movingIMS) == 0:
            self.ui.movingImageTableWidget.setRowCount(0)
            return

        # Set the number of rows in the table
        num_rows = self.movingIMS.size / 3
        self.ui.movingImageTableWidget.setRowCount(num_rows)

        # populate the rows of the table with the info in movingIMS
        row_count = 0
        for row in self.movingIMS:
            self.ui.movingImageTableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(f"{row[0]}  "))
            self.ui.movingImageTableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(f"{row[1]}  "))
            self.ui.movingImageTableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(f"{row[2]}  "))
            row_count += 1

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_tables_are_complete_import_project_tab()
        if self.movingIMS.shape[0] > 0:
            self.ui.movingImageTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def populate_fixed_table(self):

        # Populate the first row with the variables' values
        self.ui.fixedImageTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{self.nmFixed}  "))
        self.ui.fixedImageTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{self.ScaleFixed}  "))  # Convert scale to string if necessary
        self.ui.fixedImageTableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{self.pthFixed}  "))

        if len(self.pthFixed) > 0:
            self.ui.JobFolderCheckBox.setVisible(True)
        else:
            self.ui.JobFolderCheckBox.setVisible(False)

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_tables_are_complete_import_project_tab()
        if self.nmFixed:
            self.ui.fixedImageTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def populate_project_table(self):
        self.ui.setJobTableWidget.setRowCount(1)
        self.ui.setJobTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{self.ResultsName}  "))
        self.ui.setJobTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{self.jobFolder}  "))

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_tables_are_complete_import_project_tab()
        if self.ResultsName:
            self.ui.setJobTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def check_if_tables_are_complete_import_project_tab(self):
        fixedFrameDone = len(self.nmFixed) > 0 and len(self.ScaleFixed) > 0 and len(self.pthFixed) > 0
        jobFrameDone = len(self.jobFolder) > 0 and len(self.ResultsName) > 0
        movingFrameDone = True
        if len(self.movingIMS) == 0:
            movingFrameDone = False
        else:
            for row in self.movingIMS:
                for cell in row:
                    if not isinstance(cell, str) or not cell.strip():
                        movingFrameDone = False

        # make fixed frame green if completed
        if fixedFrameDone:
            self.ui.DefineFixedImageFrame.setStyleSheet("background-color: #3d4a3d;")
        else:
            self.ui.DefineFixedImageFrame.setStyleSheet("background-color: #4b4b4b;")

        # make moving frame green if completed
        if movingFrameDone:
            self.ui.DefineMovingImageFrame.setStyleSheet("background-color: #3d4a3d;")
        else:
            self.ui.DefineMovingImageFrame.setStyleSheet("background-color: #4b4b4b;")

        # make project frame green if completed
        if jobFrameDone:
            self.ui.SetJobFolderFrame.setStyleSheet("background-color: #3d4a3d;")
            self.ui.JobFolderCheckBox.setStyleSheet("background-color: #3d4a3d;")
            self.ui.JobFolderCheckBox.setStyleSheet("color: #e6e6e6;")
        else:
            self.ui.SetJobFolderFrame.setStyleSheet("background-color: #4b4b4b;")
            self.ui.JobFolderCheckBox.setStyleSheet("background-color: #4b4b4b;")
            self.ui.JobFolderCheckBox.setStyleSheet("color: #e6e6e6;")

        # enable continue buttons if all frames are completed
        if fixedFrameDone and jobFrameDone and movingFrameDone:
            self.close_navigation_tab()
        else:
            self.close_navigation_tab()
            self.ui.NavigationButton.setVisible(False)

    def browse_for_template(self):
        """Choose a template file to load."""

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Template .csv File", "",
                                                             "Data Files (*.csv)")
        if file_path:
            self.load_template_info(file_path)

    def save_template_file(self):
        line1 = ['', 'filename', 'scale factor', 'path']
        line2 = ['Fixed image', '', '', '']
        line3 = ['', self.nmFixed, self.ScaleFixed, self.pthFixed]
        line4 = ['Output folder', '', '', '']
        line5 = ['', self.ResultsName, '', self.jobFolder]
        line6 = ['Moving images', '', '', '']
        Xout = np.row_stack([line1, line2, line3, line4, line5, line6])
        for b in range(0, self.movingIMS.shape[0]):
            tmp = ['',self.movingIMS[b, 0], self.movingIMS[b, 1], self.movingIMS[b, 2]]
            Xout = np.row_stack([Xout, tmp])

        outputFolder = os.path.join(self.jobFolder, self.ResultsName)
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        outfile = os.path.join(outputFolder, "template.csv")
        np.savetxt(outfile, Xout, delimiter=",", fmt="%s")

    def load_template_info(self, file_path):
        # Read the CSV file
        X = pd.read_csv(file_path, header=None).values

        # Get location and name of fixed image
        self.nmFixed = X[2, 1]
        self.ScaleFixed = X[2, 2]
        self.pthFixed = X[2, 3]

        # Get location of output folder
        self.ResultsName = X[4, 1]
        self.jobFolder = X[4, 3]
        if not os.path.isdir(self.jobFolder):
            os.makedirs(self.jobFolder)

        # Get a list of all moving images
        mvims = np.array([["", "", ""]], dtype=object)
        for b in range(6, len(X)):  # Adjusting for 0-based indexing in Python
            add_to_list = np.array([X[b, 1], X[b, 2], X[b, 3]])
            mvims = np.vstack([mvims, add_to_list])
        mvims = np.delete(mvims, 0, axis=0)
        self.movingIMS = mvims

        self.populate_fixed_table()
        self.populate_moving_table()
        self.populate_project_table()

    def default_model_name(self):
        # """Set the initial text of the model_name text box to today's date."""
        today = datetime.now()
        self.ResultsName = "Registration_results_" + today.strftime("%m_%d_%Y")

    def keyReleaseEvent(self, event):
        # Update key states on release
        if event.key() == 16777248:
            self.shift_key = 0
        elif event.key() == 82 or event.key() == 70 or event.key() == 68 or event.key() == 66 or event.key() == 67:
            self.view_key = 0
        elif event.key == 44 or event.key() == 46:
            self.updown_key = 0

    def keyPressEvent(self, event):
        """Handle key press events."""
        print(event.key())
        # Check if the Esc key is pressed
        if event.key() == Qt.Key_Escape:
            if self.add_fiducial_active:
                self.toggle_add_fiducial_mode()
        elif event.key() == 16777248:
            self.shift_key = 1 # right
        elif event.key() == 82: # r
            self.view_key = 1 # rotate
        elif event.key() == 70: # f
            self.view_key = 2 # flip
        elif event.key() == 68: # d
            self.view_key = 3 # return view
        elif event.key() == 66: #b
            self.view_key = 4 # brightness
        elif event.key == 67: # c
            self.view_key = 5 # contrast
        elif event.key == 44: # <
            self.updown_key = 1 # down
        elif event.key == 46: # >
            self.updown_key = 2 # up
        else:
            # Pass the event to the base class for default handling
            super().keyPressEvent(event)

        if self.shift_key == 0:
            whichImage = 0 # left
            if self.view_key == 1:
                print("left rotate")
                self.rotate_label_ui(whichImage)
            elif self.view_key == 2:
                print("left flip")
                self.flip_image_y(whichImage)
            elif self.view_key == 3:
                print("left return")
                self.reset_transformations(whichImage)
            elif self.view_key == 4 and self.updown_key == 1:
                print("left brightness")
                self.decrease_brightness(whichImage)
            elif self.view_key == 4 and self.updown_key == 2:
                print("right brightness")
                self.increase_brightness(whichImage)
            elif self.view_key == 5 and self.updown_key == 1:
                print("left contrast")
                self.decrease_contrast(whichImage)
            elif self.view_key == 5 and self.updown_key == 2:
                print("right contrast")
                self.increase_contrast(whichImage)
        elif self.shift_key == 1:
            whichImage = 1 # right
            if self.view_key == 1:
                print("right rotate")
                self.rotate_label_ui(whichImage)
            elif self.view_key == 2:
                print("right flip")
                self.flip_image_y(whichImage)
            elif self.view_key == 3:
                print("right return")
                self.reset_transformations(whichImage)
            elif self.view_key == 4 and self.updown_key == 1:
                print("left brightness")
                self.decrease_brightness(whichImage)
            elif self.view_key == 4 and self.updown_key == 2:
                print("right brightness")
                self.increase_brightness(whichImage)
            elif self.view_key == 5 and self.updown_key == 1:
                print("left contrast")
                self.decrease_contrast(whichImage)
            elif self.view_key == 5 and self.updown_key == 2:
                print("right contrast")
                self.increase_contrast(whichImage)

    def load_image(self, image_path):

        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if len(image.shape) == 2:
            # Grayscale image: Convert to RGB
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            # RGBA image: Convert to RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        elif image.shape[2] == 3:
            # Convert BGR to RGB (OpenCV loads images in BGR format)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if image.dtype != np.uint8:
            # Only normalize if the image is not already 8-bit
            image = image.astype(np.float32)
            image = (image / np.iinfo(image.dtype).max * 255).astype(np.uint8)

        height, width, channels = image.shape
        bytes_per_line = channels * width
        qimage = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        return pixmap

    def resizeEvent(self, event):
        # Get the new size of the main window
        new_size = event.size()

        # Calculate scaling factors based on the new size of tabWidget
        if self.scaleCount == 0:
            num_children = len(self.ui.tabWidget.findChildren(QWidget))
            self.widget_dimensions = np.zeros((4, num_children + 1))
            self.widget_dimensions[0, 0] = self.width()
            self.widget_dimensions[1, 0] = self.height()
            self.original_width = new_size.width()
            self.original_height = new_size.height()

        scale_width = new_size.width() / self.original_width
        scale_height = new_size.height() / self.original_height

        self.padnum = self.padnum * scale_height

        # Scale the main window proportionally
        self.resize(self.widget_dimensions[0, 0] * scale_width, self.widget_dimensions[1, 0] * scale_height)

        if self.scaleCount == 0:
            self.widgets_list = [
                self.ui.centralWidget,
                self.ui.tabWidget]
            # Append children of self.ui.tabWidget with "Text" or "Button" in their name
            for child in self.ui.tabWidget.findChildren(QWidget):
                if "Widget" in child.objectName() or "Tab" in child.objectName() or "Frame" in child.objectName() or "Text" in child.objectName() or "Button" in child.objectName() or "CheckBox" in child.objectName() or "ComboBox" in child.objectName() or "Image" in child.objectName():
                    if not "Name" in child.objectName():
                        self.widgets_list.append(child)

        # Iterate over the selected child widgets of tabWidget and scale them
        for idx, child in enumerate(self.widgets_list):

            # Document widget dimensions on the first scale event
            if self.scaleCount == 0:
                self.widget_dimensions[0, idx + 1] = child.width()  # Store width in row 0
                self.widget_dimensions[1, idx + 1] = child.height()  # Store height in row 1
                self.widget_dimensions[2, idx + 1] = child.x() # top left x position
                self.widget_dimensions[3, idx + 1] = child.y() # top left y position

            child_width = self.widget_dimensions[0, idx + 1] * scale_width
            child_height = self.widget_dimensions[1, idx + 1] * scale_height
            child.resize(int(child_width), int(child_height))

            # Optionally, reposition the child widgets proportionally
            child_x = self.widget_dimensions[2, idx + 1] * scale_width
            child_y = self.widget_dimensions[3, idx + 1] * scale_height
            child.move(int(child_x), int(child_y))

        self.ui.DisableFrame_O1.setGeometry(self.ui.ImageViewControlsFrame_O.geometry())
        self.ui.DisableFrame_O2.setGeometry(self.ui.SaveRegistrationControlFrame.geometry())
        self.ui.DisableFrame_C.setGeometry(self.ui.RegisterCoordinatesFrame.geometry())
        self.ui.DisableFrame_C_2.setGeometry(self.ui.CoordinatesOverlayControlsFrame.geometry())
        self.ui.DisableFrame_C_3.setGeometry(self.ui.ImageViewControlsFrame_C.geometry())

        self.scaleCount = self.scaleCount + 1
        self.update_both_images()
        super().resizeEvent(event)  # Call the base class's resizeEvent

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    from CODApivot_v0 import Ui_MainWindow  # Replace with your actual UI import

    window = MainWindow()
    window.show()
    sys.exit(app.exec())