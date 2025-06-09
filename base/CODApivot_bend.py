"""
Author: Ashley Kiemen (Johns Hopkins)
Date: October 23, 2024
"""

import os
import cv2
import json
import time
import scipy
import random
import pickle
import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import mode
from datetime import datetime
import matplotlib.pyplot as plt
from typing import Optional, Tuple
from skimage.transform import resize
from scipy.interpolate import griddata
from scipy.interpolate import LinearNDInterpolator
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QPointF, Signal, QEvent
from PySide6.QtGui import QPixmap, QTransform, QImage, QPainter, QCursor, QColor, QPen, QIcon
from PySide6.QtWidgets import QDialog, QStyledItemDelegate, QFileDialog, QLabel, QColorDialog, QHeaderView, QMainWindow, QVBoxLayout, QWidget
from base.CODApivot_v0 import Ui_MainWindow

# disable the decompression bomb protection entirely:
Image.MAX_IMAGE_PIXELS = None

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

class CenteredItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

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

        # define the tab number for each functional tab
        self.import_project_tab = 0 # first tab
        self.fiducials_tab = 1 # second tab
        self.apply_to_data_tab = 2 # third tab
        self.job_status_tab = 3 # fourth tab
        self.overlay_tab = 4 # fifth tab
        self.elastic_reg_tab = 5 # sixth tab
        self.keyboard_tab = 6 # seventh tab
        self.apply_to_images_tab = 7  # eight tab
        self.current_index = self.import_project_tab # which tab is currently visible
        # variables needed for app rescaling
        self.widget_dimensions = 0
        self.widgets_list = 0 # list of all widgets in the gui that should be rescaled
        self.original_width = 0 # original width of the gui
        self.original_height = 0 # original height of the gui
        self.scaleCount = 0
        self.padnum = 30 # offset of the image view windows from the edge of the app
        # keyboard shortcut variables
        self.which_key_press = 0
        self.shift_key_active = 0
        self.increase_decrease_brightness_contrast_key = 0
        # variables to keep track of what the user is doing right now
        self.edit_table_active = 0  # is the user currently editing the tables in tab 1
        self.edit_which_pt_color = 0 # if the user is changing point colors, which points are being edited
        self.edit_which_image = 0 # if the tab has two image frames, which one is the user currently editing
        self.edit_which_fid = 0 # if in the fiducials tab, is the user adding fixed or moving image points
        self.add_fiducial_active = False  # flag to track whether the user is adding fiducial points
        self.delete_mode_active = False # flack to track if whether the user is deleting fiducial points
        self.panning_mode_active = 0  # flag to track whether the user is panning
        self.last_mouse_position = QPointF()  # Track the last position of the mouse during panning
        self.potential_deletion = -5 # keep track of which point the user is considering deleting
        # folder and name of images and files to load
        self.job_folder = ""
        self.results_name = ""
        self.fixed_image_folder = ""
        self.moving_image_folder = ""
        self.coordinates_file_folder = ""
        self.moving_image_folder_corresponding_to_coordinates = ""
        self.fixed_image_filename = ""
        self.moving_image_filename = ""
        self.coordinates_filename = ""
        self.fixed_image_filename_for_coordinates_tab = ""
        self.moving_image_filename_corresponding_to_coordinates = ""
        self.loaded_moving_image_filename = "" # keep track of the moving image that is currently loaded
        self.loaded_coordinates_filename = "" # keep track of the coordinates file that is currently loaded
        self.moving_images_list = [] # list of all moving images in this project
        self.num_moving_delete = [[], []] # variable to keep track of a potential moving image to delete
        self.scale_fixed_image = ""
        self.scale_moving_image = ""
        self.scale_coordinates_file = ""
        self.json_scale = 1
        # variables that will hold images - these are cleared when not in use to save RAM
        self.pixmap = [] # the current pixmap being edited (changes based on the current tab)
        self.im_fixed = [] # fixed image
        self.im_moving = [] # unregistered moving image
        self.im_moving_reg = [] # affine registered moving image
        self.im_moving_reg_elastic = []  # elastically registered moving image
        self.im_overlay = [] # overlay of fixed image and unregistered moving image
        self.im_overlay_reg = [] # overlay of fixed image and affine registered moving image
        self.im_overlay_reg_elastic = [] # overlay of fixed image and elastically registered moving image
        self.im_moving_coords = [] # moving image for coordinates tab
        self.im_moving_coords_reg = [] # affine registered moving image for coordinates tab
        self.im_moving_coords_reg_elastic = [] # elastically registered moving image for coordinates tab
        # max and mode intensity of each image
        self.max_intensity = 0
        self.max_intensity_fixed = 0
        self.max_intensity_moving = 0
        self.max_intensity_moving_coords = 0
        self.max_intensity_moving_coords_reg = 0
        self.mode_intensity_fixed = [0, 0, 0]
        self.mode_intensity_moving = [0, 0, 0]
        # variables that help define which image to edit
        self.frame = []
        self.frame_left = []
        self.frame_right = []
        self.label = []
        self.border_left = []
        self.border_right = []
        self.text_left = []
        self.text_right = []
        self.image_width = 0
        self.image_height = 0
        self.fiducial_pts_to_plot = []  # fiducial points to plot over the current image
        self.more_fiducial_pts_to_plot = [] # 2nd set of fiducial points to plot over the current image (for overlays only)
        # image view variables - flip state
        self.flip_state = False
        self.fixed_flip_state = False
        self.moving_flip_state = False
        self.overlay_flip_state = False
        self.overlay_reg_flip_state = False
        self.unregistered_E_flip_state = False
        self.overlay_reg_elastic_flip_state = False
        self.moving_coords_flip_state = False
        # image view variables - rotational angle
        self.rotation_angle = 0
        self.fixed_rotation_angle = 0
        self.moving_rotation_angle = 0
        self.overlay_rotation_angle = 0
        self.overlay_reg_rotation_angle = 0
        self.unregistered_E_rotation_angle = 0
        self.overlay_reg_elastic_rotation_angle = 0
        self.moving_coords_rotation_angle = 0
        # image view variables - brightness (not editable for overlay images)
        self.brightness = 0
        self.fixed_brightness = 0
        self.moving_brightness = 0
        self.moving_coords_brightness = 0
        # image view variables - contrast (not editable for overlay images)
        self.contrast = 1
        self.fixed_contrast = 1
        self.moving_contrast = 1
        self.moving_coords_contrast = 1
        # image view variables - zoom scale to fit the whole image in the image frame
        self.zoom_default = 1
        self.fixed_zoom_default = 1
        self.moving_zoom_default = 1
        self.overlay_zoom_default = 1
        self.overlay_reg_zoom_default = 1
        self.unregistered_E_zoom_default = 1
        self.overlay_reg_elastic_zoom_default = 1
        self.moving_coords_zoom_default = 1
        # image view variables - user's current zoom level
        self.zoom_scale = self.zoom_default
        self.fixed_zoom_scale = self.fixed_zoom_default
        self.moving_zoom_scale = self.moving_zoom_default
        self.overlay_zoom_scale = self.overlay_zoom_default
        self.overlay_reg_zoom_scale = self.overlay_reg_zoom_default
        self.unregistered_E_zoom_scale = self.unregistered_E_zoom_default
        self.overlay_reg_elastic_zoom_scale = self.overlay_reg_elastic_zoom_default
        self.moving_coords_zoom_scale = self.moving_coords_zoom_default
        # image view variables - user's current horizontal pan offset from center
        self.pan_offset_x = 0
        self.fixed_pan_offset_x = 0
        self.moving_pan_offset_x = 0
        self.overlay_pan_offset_x = 0
        self.registered_pan_offset_x = 0
        self.unregistered_E_pan_offset_x = 0
        self.overlay_reg_elastic_pan_offset_x = 0
        self.moving_coords_pan_offset_x = 0
        # image view variables - user's current vertical pan offset from center
        self.pan_offset_y = 0
        self.moving_pan_offset_y = 0
        self.fixed_pan_offset_y = 0
        self.overlay_pan_offset_y = 0
        self.overlay_reg_pan_offset_y = 0
        self.unregistered_E_pan_offset_y = 0
        self.overlay_reg_elastic_pan_offset_y = 0
        self.moving_coords_pan_offset_y = 0
        # fiducial point variables and settings
        self.MIN_NUM_FIDUCIAL_PTS = 6
        self.pts_size = 10
        self.pts_size_fiducial_tab = self.pts_size  # default size of fiducial points
        self.pts_size_overlay_tab_fixed = self.pts_size_fiducial_tab  # default size of fiducial points
        self.pts_size_overlay_tab_moving = int(np.ceil(self.pts_size_fiducial_tab * 0.75))  # default size of fiducial points
        self.pts_size_coordinates_tab = self.pts_size_fiducial_tab  # default size of fiducial points
        self.color_button = [] # name of the current color button in case we need to update it
        self.pts_color = QColor(30, 255, 150)  # default color of fiducial points
        self.pts_color_fiducial_tab = self.pts_color  # default color of fiducial points
        self.pts_color_overlay_tab_fixed = self.pts_color_fiducial_tab  # default color of fiducial points
        self.pts_color_overlay_tab_moving = self.pts_color_fiducial_tab  # default complement color of fiducial points
        self.pts_color_coordinates_tab = self.pts_color_fiducial_tab  # default color of fiducial points
        # coordinate variables
        self.pts_fixed = np.array([[0, 0]], dtype=np.float64)
        self.pts_moving = np.array([[0, 0]], dtype=np.float64)
        self.pts_moving_reg = np.array([[0, 0]], dtype=np.float64)
        self.pts_moving_reg_elastic = np.array([[0, 0]], dtype=np.float64)
        self.pts_coords = []
        self.pts_coords_reg = []
        self.pts_coords_reg_elastic = []
        # registration variables - root mean squared error
        self.rmse_unregistered = 0 # root mean squared error between unregistered images
        self.rmse_reg = 0 # root mean squared error between affine registered images
        self.rmse_reg_elastic = 0 # root mean squared error between elastically registered images
        # registration transforms
        self.flip_im = 0
        self.flip_im_coords = 0
        self.tform = []
        self.tformCoords = []
        self.D = []
        self.Dinv = []
        self.DinvCoords = []
        self.coord_registration_type = []
        # elastic registration info
        self.elastic_tilesize = 250
        self.elastic_tilespacing = 100
        self.view_squares = 1
        self.squaresColor = self.pts_color_overlay_tab_fixed
        self.squaresThickness = 30
        self.xySquare = (1, 1)
        # table inputs for apply to coordinates tab
        self.all_images_checked = 0 # keep track of states the user has checked the points in (unregistered, registered, etc)
        self.max_points = "10000" # default maximum number of points to plot when validating coordinate registration
        self.column_in_coords_file_containing_x_values = 1 # column in the coordinate file containing x values
        self.column_in_coords_file_containing_y_values = 1 # column in the coordinate file containing y values
        self.number_of_first_row_in_coords_file = 0 # allows skipping the first row in the file if it contains titles
        self.coordinate_data = "" # table of all coordinate data read from the coordinate file
        self.which_moving_images_are_registered = [[0], [0]] # keep track of which images have registration data saved
        self.sampled_indices = [] # keep track of which rows of the coordinate file are selected to plot
        # apply to images variables
        self.images_to_register_list = []  # list of all moving images in this project
        self.num_image_delete = [[], []]  # variable to keep track of a potential moving image to delete
        self.image_file_folder = ""
        self.image_filename = ""
        self.num_image_row = 0
        self.num_image_column = 0
        # populate the keyboard shortcuts table
        self.ui.keyboardShortCutsTableWidget.setHorizontalHeaderLabels(["R", "F", "D"])
        self.ui.keyboardShortCutsTableWidget_2.setHorizontalHeaderLabels(["B", "C", "A"])
        self.ui.keyboardShortCutsTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Rotate"))
        self.ui.keyboardShortCutsTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("Flip"))
        self.ui.keyboardShortCutsTableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem("Return to Default"))
        self.ui.keyboardShortCutsTableWidget_2.setItem(0, 0, QtWidgets.QTableWidgetItem("Brightness"))
        self.ui.keyboardShortCutsTableWidget_2.setItem(0, 1, QtWidgets.QTableWidgetItem("Contrast"))
        self.ui.keyboardShortCutsTableWidget_2.setItem(0, 2, QtWidgets.QTableWidgetItem("Auto-adjust"))
        self.ui.keyboardShortCutsTableWidget.setItemDelegate(CenteredItemDelegate())
        self.ui.keyboardShortCutsTableWidget_2.setItemDelegate(CenteredItemDelegate())

        # reference the keyboard shortcuts pop-up dialog so it's ready for later
        self.keyboardShortcutsDialog = None
        self.ui.KeyboardShortcutsButton.clicked.connect(self.show_keyboard_shortcuts)
        self.ui.KeyboardShortcutsButton.setGeometry(625, 620, 130, 30)

        # define the app navigation button settings
        self.ui.NavigationButton.setGeometry(760, 620, 65, 30)
        self.ui.NavigationButton.clicked.connect(self.view_navigation_tab)
        self.ui.CloseNavigationButton.clicked.connect(self.close_navigation_tab)
        self.ui.GoToImportProjectTab.clicked.connect(self.initiate_import_project_tab)
        self.ui.GoToFiducialsTab.clicked.connect(self.initiate_fiducials_tab)
        self.ui.GoToCoordsTab.clicked.connect(self.initiate_apply_to_coords_tab)
        self.ui.GoToJobStatusTab.clicked.connect(self.initiate_job_status_tab)
        self.ui.GoToApplyImageTab.clicked.connect(self.initiate_apply_to_image_tab)
        # set icon pics
        icon_path = os.path.join(os.path.dirname(__file__), 'Folder.jpg')
        self.ui.chooseFixedImageButton.setIcon(QIcon(icon_path))
        self.ui.chooseMovingImageButton.setIcon(QIcon(icon_path))
        self.ui.chooseJobFolderButton.setIcon(QIcon(icon_path))
        self.ui.chooseCoordinatesFileButton.setIcon(QIcon(icon_path))
        self.ui.chooseImageFileButton.setIcon(QIcon(icon_path))

        # import project tab
        self.delegate = CustomDelegateTable(self.ui.setJobTableWidget)
        self.ui.setJobTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedTable.connect(self.handle_value_update_job)
        # apply to coordinates tab
        self.delegate = CustomDelegateTable(self.ui.RegisterCoordinatesTableWidget)
        self.ui.RegisterCoordinatesTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedTable.connect(self.handle_value_update_coordinates)
        # apply to images tab
        self.delegate = CustomDelegateTable(self.ui.ApplyToImageTableWidget)
        self.ui.ApplyToImageTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedTable.connect(self.handle_value_update_image)

        # make the image frames communicate with mouse clicks and scrolls
        # add fiducials tab
        self.fixed_image_label = ClickableLabel(self.ui.FixedImageDisplayFrame)
        self.fixed_image_label.setScaledContents(True)  # Allow scaling to fit the frame
        self.moving_image_label = ClickableLabel(self.ui.MovingImageDisplayFrame)
        self.moving_image_label.setScaledContents(True)  # Allow scaling to fit the frame
        # image overlay tab
        self.overlay0_label = ClickableLabel(self.ui.UnregisteredImageDisplayFrame)
        self.overlay0_label.setScaledContents(True)  # Allow scaling to fit the frame
        self.overlay_label = ClickableLabel(self.ui.RegisteredImageDisplayFrame)
        self.overlay_label.setScaledContents(True)  # Allow scaling to fit the frame
        # elastic registration tab
        self.overlay0_E_label = ClickableLabel(self.ui.FiducialRegisteredImageDisplayFrame)
        self.overlay0_E_label.setScaledContents(True)  # Allow scaling to fit the frame
        self.overlay_E_label = ClickableLabel(self.ui.ElasticRegisteredImageDisplayFrame)
        self.overlay_E_label.setScaledContents(True)  # Allow scaling to fit the frame
        # apply to coordinates tab
        self.coordinates_label = ClickableLabel(self.ui.RegisterCoordsDisplayFrame)
        self.coordinates_label.setScaledContents(True)  # Allow scaling to fit the frame

        # Move some buttons around (easier to move here than in QT Designer)
        # add fiducials tab
        self.ui.ChooseMovingImageFrame.setGeometry(10, 565, 480, 85)
        self.ui.FixedImageFrameHeaderText.setGeometry(self.ui.UnregisteredImageFrameHeaderText.geometry())
        self.ui.MovingImageFrameHeaderText.setGeometry(self.ui.RegisteredImageFrameHeaderText.geometry())
        self.ui.FixedImageDisplayFrame.setGeometry(self.ui.UnregisteredImageDisplayFrame.geometry())
        self.ui.MovingImageDisplayFrame.setGeometry(self.ui.RegisteredImageDisplayFrame.geometry())
        self.ui.FixedImageBorder.setGeometry(self.ui.UnregisteredImageBorder.geometry())
        self.ui.MovingImageBorder.setGeometry(self.ui.RegisteredImageBorder.geometry())
        self.ui.DisableFrame_F1.setGeometry(self.ui.FiducialPointControlsFrame.geometry())
        # registration overlay tab
        self.ui.DisableFrame_O1.setGeometry(self.ui.ImageViewControlsFrame_O.geometry())
        # elastic registration tab
        self.ui.ImageViewControlsFrame_E.setGeometry(self.ui.ImageViewControlsFrame_O.geometry())
        self.ui.SaveRegistrationResultsButton_E.setGeometry(self.ui.SaveRegistrationResultsButton_O.geometry())
        self.ui.ReturnToFiducialsTabButton_E.setGeometry(self.ui.ReturnToFiducialsTab_O.geometry())
        self.ui.QuitElasticRegistrationButton2.setGeometry(self.ui.TryElasticRegButton.geometry())
        self.ui.DisableFrame_E1.setGeometry(self.ui.ImageViewControlsFrame_E.geometry())
        self.ui.DisableFrame_E2.setGeometry(self.ui.ElasticRegistrationControlsFrame.geometry())
        # apply to coordinates tab
        self.ui.DisableFrame_C.setGeometry(self.ui.RegisterCoordinatesFrame.geometry())
        self.ui.DisableFrame_C_2.setGeometry(self.ui.CoordinatesOverlayControlsFrame.geometry())
        self.ui.DisableFrame_C_3.setGeometry(self.ui.ImageViewControlsFrame_C.geometry())
        # apply to images tab
        self.ui.DisableFrame_I1.setGeometry(self.ui.ApplyToImageFrame.geometry())
        self.ui.KeepApplyToImageButton.setGeometry(700, 30, 50, 30)
        self.ui.DeleteApplyToImageButton.setGeometry(755, 30, 50, 30)
        self.ui.ApplyToImageComboBox.setGeometry(605, 36, 200, 25)

        # What functions to call when a button is clicked
        # import project tab
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
        self.ui.JobFolderCheckBox.stateChanged.connect(self.job_folder_checkbox_changed)
        # add fiducials tab
        self.ui.MovingImagesComboBox.currentIndexChanged.connect(self.new_combobox_selection_changed)
        self.ui.OldMovingImagesComboBox.currentIndexChanged.connect(self.old_combobox_selection_changed)
        self.ui.LoadNewMovingImageButton.clicked.connect(self.load_new_moving_image)
        self.ui.LoadOldMovingImageButton.clicked.connect(self.load_old_moving_image)
        self.ui.PickNewMovingImageButton.clicked.connect(self.confirm_load_new_image)
        self.ui.AddFiducialButton.clicked.connect(self.toggle_add_fiducial_mode)
        self.ui.ColorFiducialButton.clicked.connect(self.change_fiducial_color)
        self.ui.ShrinkFiducialButton.clicked.connect(self.decrease_fiducial_size)
        self.ui.GrowFiducialButton.clicked.connect(self.increase_fiducial_size)
        self.ui.DeleteAllButton.clicked.connect(self.delete_fiducials)
        self.ui.AttemptICPRegistrationButton.clicked.connect(self.begin_calculate_icp_tabF)
        # image overlay tab
        self.ui.ReturnToFiducialsTab_O.clicked.connect(self.return_to_fiducials_tab)
        self.ui.SaveRegistrationResultsButton_O.clicked.connect(self.save_registration_results)
        self.ui.TryElasticRegButton.clicked.connect(self.initiate_elastic_registration_tab)
        self.ui.ColorFiducialButton_O.clicked.connect(self.call_change_fiducial_color0)
        self.ui.ColorFiducialButton2_O.clicked.connect(self.call_change_fiducial_color1)
        self.ui.ShrinkFiducialButton_O.clicked.connect(self.call_decrease_fiducial_size0)
        self.ui.ShrinkFiducialButton2_O.clicked.connect(self.call_decrease_fiducial_size1)
        self.ui.GrowFiducialButton_O.clicked.connect(self.call_increase_fiducial_size0)
        self.ui.GrowFiducialButton2_O.clicked.connect(self.call_increase_fiducial_size1)
        # elastic registration tab
        self.ui.ColorFiducialButton_E.clicked.connect(self.call_change_fiducial_color0)
        self.ui.ColorFiducialButton2_E.clicked.connect(self.call_change_fiducial_color1)
        self.ui.ShrinkFiducialButton_E.clicked.connect(self.call_decrease_fiducial_size0)
        self.ui.ShrinkFiducialButton2_E.clicked.connect(self.call_decrease_fiducial_size1)
        self.ui.GrowFiducialButton_E.clicked.connect(self.call_increase_fiducial_size0)
        self.ui.GrowFiducialButton2_E.clicked.connect(self.call_increase_fiducial_size1)
        self.ui.ReturnToFiducialsTabButton_E.clicked.connect(self.initiate_elastic_registration_tab)
        self.ui.SaveRegistrationResultsButton_E.clicked.connect(self.save_registration_results_elastic)
        self.ui.ColorSquaresButton.clicked.connect(self.change_fiducial_color)
        self.ui.GrowTileSizeButton.clicked.connect(self.increase_elastic_tile_size)
        self.ui.ShrinkTileSizeButton.clicked.connect(self.decrease_elastic_tile_size)
        self.ui.GrowTileSpacingButton.clicked.connect(self.increase_elastic_tile_spacing)
        self.ui.ShrinkTileSpacingButton.clicked.connect(self.decrease_elastic_tile_spacing)
        self.ui.CalculateElasticRegistrationButton.clicked.connect(self.call_CODA_elastic_registration)
        self.ui.QuitElasticRegistrationButton.clicked.connect(self.quit_elastic_registration)
        self.ui.QuitElasticRegistrationButton2.clicked.connect(self.quit_elastic_registration)
        # apply registration to coordinates tab
        self.ui.chooseCoordinatesFileButton.clicked.connect(self.browse_for_coordinates_file)
        self.ui.CorrespondingImageComboBox.currentIndexChanged.connect(self.on_combo_box_changed)
        self.ui.LoadCoordinatesButton.clicked.connect(self.load_coordinates_to_register)
        self.ui.SwapXYButton.clicked.connect(self.swap_xy)
        self.ui.EditTableButton.clicked.connect(self.return_to_edit_table)
        self.ui.ViewUnregisteredMovingButton.clicked.connect(self.define_image_unregistered)
        self.ui.ViewRegisteredMovingButton.clicked.connect(self.define_image_registered)
        self.ui.ViewRegisteredEMovingButton.clicked.connect(self.define_image_registered_elastic)
        self.ui.ViewFixedButton.clicked.connect(self.define_image_fixed)
        self.ui.SaveRegisteredCoordinatesButton.clicked.connect(self.call_save_registered_coordinates_ICP)
        self.ui.SaveRegisteredECoordinatesButton.clicked.connect(self.call_save_registered_coordinates_elastic)
        self.ui.UnregisteredMovingCheckBox.stateChanged.connect(self.unregistered_coords_checkbox_changed)
        self.ui.RegisteredMovingCheckBox.stateChanged.connect(self.registered_coords_checkbox_changed)
        self.ui.RegisteredEMovingCheckBox.stateChanged.connect(self.registered_elastic_coords_checkbox_changed)
        self.ui.FixedCheckBox.stateChanged.connect(self.fixed_coords_checkbox_changed)
        self.ui.ColorFiducialButton_C.clicked.connect(self.change_fiducial_color)
        self.ui.ShrinkFiducialButton_C.clicked.connect(self.decrease_fiducial_size)
        self.ui.GrowFiducialButton_C.clicked.connect(self.increase_fiducial_size)
        self.ui.RegisterCoordinatesTableWidget.cellDoubleClicked.connect(self.doubleclick_coordinates_table)
        # apply registration to images tab
        self.ui.ApplyToImageComboBox.currentIndexChanged.connect(self.on_combo_box_changed_image)
        self.ui.chooseImageFileButton.clicked.connect(self.browse_for_image_to_register)
        self.ui.RegisterImageButton.clicked.connect(self.apply_registration_to_an_image)
        self.ui.ApplyToImageTableWidget.cellDoubleClicked.connect(self.doubleclick_image_table)
        self.ui.DeleteApplyToImageButton.clicked.connect(self.delete_apply_to_image)
        self.ui.KeepApplyToImageButton.clicked.connect(self.keep_apply_to_image)

        # define some style sheets that we will use later
        self.define_some_stylesheets()

        # make some tab headers invisible
        self.ui.tabWidget.setTabVisible(self.keyboard_tab, False)
        self.ui.tabWidget.setTabVisible(self.elastic_reg_tab, False)
        self.ui.tabWidget.setTabVisible(self.overlay_tab, False)

        # initiate tab 1 inside the app
        self.default_model_name()
        self.ui.tabWidget.tabBar().installEventFilter(self)
        self.initiate_import_project_tab()

    def define_some_stylesheets(self):
        """Predefine some style sheets so we can reference them later
        Used at app start-up only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will define some stylesheets
        """
        self.dialog_style = """
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
                            """
        self.active_button_style = """
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
        self.inactive_button_style = """ QPushButton {
                                                background-color: #5a5a5a;
                                                border: 1px solid #424242;
                                                color: #424242;
                                                border-radius: 5px; /* Optional: Rounded corners */
                                                padding: 5px; /* Optional: Padding around text */
                                            }
                                                        """
        self.active_label_style = """ QLabel { 
                                                background-color: transparent;
                                                border: 5px solid #40ad40; /* Border  */
                                            }
                                                    """

        self.inactive_label_style = """ QLabel { 
                                                background-color: transparent;
                                                border: 3px solid #e6e6e6; /* Border  */
                                            }
                                                    """
        self.active_frame_style = """ QFrame { 
                                            background-color: #375c46;
                                        }
                                                    """

        self.inactive_frame_style = """ QFrame { 
                                                background-color: #4b4b4b;
                                            }
                                                    """
        self.active_text_label_style = """ QLabel { 
                                                background-color: transparent;
                                                color: #40ad40; /* Text color */
                                                border: 0px solid #e6e6e6; /* Border  */
                                                qproperty-alignment: 'AlignCenter';
                                            }
                                                    """
        self.inactive_text_label_style = """ QLabel { 
                                                    background-color: transparent;
                                                    color: #e6e6e6; /* Text color */
                                                    border: 0px solid #e6e6e6; /* Border  */
                                                    qproperty-alignment: 'AlignCenter';
                                                }
                                                        """
        self.style_button_green = """ QPushButton {
                                                    background-color: #447544;
                                                    color: #e6e6e6; /* Text color */
                                                    border: 1px solid #e6e6e6; /* Border  */
                                                    border-radius: 5px; /* Optional: Rounded corners */
                                                    padding: 5px; /* Optional: Padding around text */
                                                }

                                                QPushButton:hover {
                                                    background-color: #488a48; /* Grey-blue when hovered */
                                                }

                                                QPushButton:pressed {
                                                    background-color: #49a349; /* More blue when pressed */
                                                }
                                                            """
        self.quest_box_style = """
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

    def promote_text_to_clickable_label(self, text_widget, click_handler):
        """Make each of the image frames clickable so they interact with mouse commands
        Used at app start-up only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will define some stylesheets
        """
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

    def define_edit_frame(self, make_pixmap=None):
        """Define the current image and image view variables depending on which tab is open
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but calculates the elastic registration and updates tab 6 view
        """
        if make_pixmap is None:
            make_pixmap = 0

        # current tab
        self.current_index = self.ui.tabWidget.currentIndex()

        if self.current_index == self.fiducials_tab:
            # point view variables
            self.pts_size = self.pts_size_fiducial_tab
            self.pts_color = self.pts_color_fiducial_tab
            self.color_button = self.ui.ColorFiducialButton
            # frame variables
            self.border_left = self.ui.FixedImageBorder
            self.border_right = self.ui.MovingImageBorder
            self.text_left = self.ui.FixedImageFrameHeaderText
            self.text_right = self.ui.MovingImageFrameHeaderText
            self.frame_left = self.ui.FixedImageDisplayFrame
            self.frame_right = self.ui.MovingImageDisplayFrame
            if self.edit_which_image == 0:  # fixed image
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
                self.fiducial_pts_to_plot = self.pts_fixed
                self.more_fiducial_pts_to_plot = []
                self.max_intensity = self.max_intensity_fixed
                try:
                    self.image_height = self.im_fixed.height()
                    self.image_width = self.im_fixed.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
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
                self.fiducial_pts_to_plot = self.pts_moving
                self.more_fiducial_pts_to_plot = []
                self.max_intensity = self.max_intensity_moving
                try:
                    self.image_height = self.im_moving.height()
                    self.image_width = self.im_moving.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
        elif self.current_index == self.overlay_tab:
            # point view variables
            if self.edit_which_pt_color == 0:
                self.color_button = self.ui.ColorFiducialButton_O
                self.pts_color = self.pts_color_overlay_tab_fixed
                self.pts_size = self.pts_size_overlay_tab_fixed
            else:
                self.color_button = self.ui.ColorFiducialButton2_O
                self.pts_color = self.pts_color_overlay_tab_moving
                self.pts_size = self.pts_size_overlay_tab_moving
            # frame variables
            self.border_left = self.ui.UnregisteredImageBorder
            self.border_right = self.ui.RegisteredImageBorder
            self.text_left = self.ui.UnregisteredImageFrameHeaderText
            self.text_right = self.ui.RegisteredImageFrameHeaderText
            self.frame_left = self.ui.UnregisteredImageDisplayFrame
            self.frame_right = self.ui.RegisteredImageDisplayFrame
            self.max_intensity = 255
            if self.edit_which_image == 0:  # unregistered image
                # image view variables
                self.flip_state = self.overlay_flip_state
                self.rotation_angle = self.overlay_rotation_angle
                self.brightness = 0
                self.contrast = 1
                self.zoom_default = self.overlay_zoom_default
                self.zoom_scale = self.overlay_zoom_scale
                self.pan_offset_x = self.overlay_pan_offset_x
                self.pan_offset_y = self.overlay_pan_offset_y
                self.label = self.overlay0_label
                self.fiducial_pts_to_plot = self.pts_fixed
                self.more_fiducial_pts_to_plot = self.pts_moving
                try:
                    self.image_height = self.im_overlay.height()
                    self.image_width = self.im_overlay.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
            else:  # registered image
                # image view variables
                self.flip_state = self.overlay_reg_flip_state
                self.rotation_angle = self.overlay_reg_rotation_angle
                self.brightness = 0
                self.contrast = 1
                self.zoom_default = self.overlay_reg_zoom_default
                self.zoom_scale = self.overlay_reg_zoom_scale
                self.pan_offset_x = self.registered_pan_offset_x
                self.pan_offset_y = self.overlay_reg_pan_offset_y
                self.label = self.overlay_label
                self.fiducial_pts_to_plot = self.pts_fixed
                self.more_fiducial_pts_to_plot = self.pts_moving_reg
                try:
                    self.image_height = self.im_overlay_reg.height()
                    self.image_width = self.im_overlay_reg.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
        elif self.current_index == self.elastic_reg_tab:
            # point view variables
            if self.view_squares > 0:
                self.color_button = self.ui.ColorSquaresButton
                self.pts_color = self.squaresColor
            else:
                if self.edit_which_pt_color == 0:
                    self.color_button = self.ui.ColorFiducialButton_E
                    self.pts_color = self.pts_color_overlay_tab_fixed
                    self.pts_size = self.pts_size_overlay_tab_fixed
                else:
                    self.color_button = self.ui.ColorFiducialButton2_E
                    self.pts_color = self.pts_color_overlay_tab_moving
                    self.pts_size = self.pts_size_overlay_tab_moving
            # frame variables
            self.border_left = self.ui.FiducialRegisteredImageBorder
            self.border_right = self.ui.ElasticRegisteredImageBorder
            self.text_left = self.ui.FiducialRegisteredImageFrameHeaderText
            self.text_right = self.ui.ElasticRegisteredImageFrameHeaderText
            self.frame_left = self.ui.FiducialRegisteredImageDisplayFrame
            self.frame_right = self.ui.ElasticRegisteredImageDisplayFrame
            self.max_intensity = 255
            if self.edit_which_image == 0:  # fiducials registered image
                # image view variables
                self.flip_state = self.unregistered_E_flip_state
                self.rotation_angle = self.unregistered_E_rotation_angle
                self.brightness = 0
                self.contrast = 1
                self.zoom_default = self.unregistered_E_zoom_default
                self.zoom_scale = self.unregistered_E_zoom_scale
                self.pan_offset_x = self.unregistered_E_pan_offset_x
                self.pan_offset_y = self.unregistered_E_pan_offset_y
                self.label = self.overlay0_E_label
                self.fiducial_pts_to_plot = self.pts_fixed
                self.more_fiducial_pts_to_plot = self.pts_moving_reg
                try:
                    self.image_height = self.im_overlay_reg.height()
                    self.image_width = self.im_overlay_reg.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
            else:  # registered image
                # image view variables
                self.flip_state = self.overlay_reg_elastic_flip_state
                self.rotation_angle = self.overlay_reg_elastic_rotation_angle
                self.brightness = 0
                self.contrast = 1
                self.zoom_default = self.overlay_reg_elastic_zoom_default
                self.zoom_scale = self.overlay_reg_elastic_zoom_scale
                self.pan_offset_x = self.overlay_reg_elastic_pan_offset_x
                self.pan_offset_y = self.overlay_reg_elastic_pan_offset_y
                self.label = self.overlay_E_label
                self.fiducial_pts_to_plot = self.pts_fixed
                self.more_fiducial_pts_to_plot = self.pts_moving_reg_elastic
                try:
                    self.image_height = self.im_overlay_reg_elastic.height()
                    self.image_width = self.im_overlay_reg_elastic.width()
                except:
                    self.image_height = 0
                    self.image_width = 0

        elif self.current_index == self.apply_to_data_tab:  # apply to coordinates tab
            # point view variables
            self.pts_size = self.pts_size_coordinates_tab
            self.pts_color = self.pts_color_coordinates_tab
            self.color_button = self.ui.ColorFiducialButton_C
            # frame variables
            self.border_left = self.ui.RegisterCoordsImageBorder
            self.border_right = self.ui.RegisterCoordsImageBorder
            self.text_left = self.ui.RegisterCoordsFrameHeaderText
            self.text_right = self.ui.RegisterCoordsFrameHeaderText
            self.frame_left = self.ui.RegisterCoordsDisplayFrame
            self.frame_right = self.ui.RegisterCoordsDisplayFrame

            # image view variables
            self.flip_state = self.moving_coords_flip_state
            self.rotation_angle = self.moving_coords_rotation_angle
            self.brightness = self.moving_coords_brightness
            self.contrast = self.moving_coords_contrast
            self.zoom_default = self.moving_coords_zoom_default
            self.zoom_scale = self.moving_coords_zoom_scale
            self.pan_offset_x = self.moving_coords_pan_offset_x
            self.pan_offset_y = self.moving_coords_pan_offset_y
            self.label = self.coordinates_label
            if self.edit_which_image == 0:
                self.fiducial_pts_to_plot = self.pts_coords
                self.max_intensity = self.max_intensity_moving_coords
                try:
                    self.image_height = self.im_moving_coords.height()
                    self.image_width = self.im_moving_coords.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
            elif self.edit_which_image == 1:
                self.fiducial_pts_to_plot = self.pts_coords_reg
                self.max_intensity = self.max_intensity_moving_coords_reg
                try:
                    self.image_height = self.im_moving_coords_reg.height()
                    self.image_width = self.im_moving_coords_reg.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
            elif self.edit_which_image == 2:
                self.fiducial_pts_to_plot = self.pts_coords_reg
                self.max_intensity = self.max_intensity_fixed
                try:
                    self.image_height = self.im_fixed.height()
                    self.image_width = self.im_fixed.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
            else:
                self.fiducial_pts_to_plot = self.pts_coords_reg_elastic
                self.max_intensity = self.max_intensity_moving_coords_reg
                try:
                    self.image_height = self.im_moving_coords_reg_elastic.height()
                    self.image_width = self.im_moving_coords_reg_elastic.width()
                except:
                    self.image_height = 0
                    self.image_width = 0
            self.more_fiducial_pts_to_plot = []
        else:
            return

        if self.edit_which_image == 0:
            self.frame = self.frame_left
        else:
            self.frame = self.frame_right

        if make_pixmap == 1:
            if self.current_index == self.fiducials_tab:
                if self.edit_which_image == 0:  # fiducials tab fixed image
                    self.pixmap = self.im_fixed
                else:  # fiducials tab moving image
                    self.pixmap = self.im_moving

            elif self.current_index == self.overlay_tab:
                if self.edit_which_image == 0:  # overlay tab unregistered images
                    self.pixmap = self.im_overlay
                else:  # overlay tab registered images
                    self.pixmap = self.im_overlay_reg  # self.imMovingReg

            elif self.current_index == self.apply_to_data_tab:
                if self.edit_which_image == 0:  # register coordinates tab unregistered moving image
                    self.pixmap = self.im_moving_coords
                elif self.edit_which_image == 1:  # register coordinates tab registered moving image
                    self.pixmap = self.im_moving_coords_reg
                elif self.edit_which_image == 2:  # Apply to coordinates tab fixed image
                    self.pixmap = self.im_fixed
                else:
                    self.pixmap = self.im_moving_coords_reg_elastic

            elif self.current_index == self.elastic_reg_tab:
                if self.edit_which_image == 0:  # overlay tab unregistered images
                    self.pixmap = self.im_overlay_reg
                else:  # overlay tab registered images
                    self.pixmap = self.im_overlay_reg_elastic

    def return_edit_frame(self):
        """Return the current image and image view variables depending on which tab is open
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but calculates the elastic registration and updates tab 6 view
        """
        # current tab
        self.current_index = self.ui.tabWidget.currentIndex()

        if self.current_index == self.fiducials_tab:
            # point view variables
            self.pts_size_fiducial_tab = self.pts_size
            self.pts_color_fiducial_tab = self.pts_color
            self.ui.ColorFiducialButton = self.color_button
            # frame variables
            self.ui.FixedImageBorder = self.border_left
            self.ui.MovingImageBorder = self.border_right
            self.ui.FixedImageFrameHeaderText = self.text_left
            self.ui.MovingImageFrameHeaderText = self.text_right
            self.ui.FixedImageDisplayFrame = self.frame_left
            self.ui.MovingImageDisplayFrame = self.frame_right

            if self.edit_which_image == 0:  # fixed image
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
            if self.edit_which_pt_color == 0:
                self.pts_color_overlay_tab_fixed = self.pts_color
                self.ui.ColorFiducialButton_O = self.color_button
                self.pts_size_overlay_tab_fixed = self.pts_size
            else:
                self.pts_color_overlay_tab_moving = self.pts_color
                self.ui.ColorFiducialButton2_O = self.color_button
                self.pts_size_overlay_tab_moving = self.pts_size
            # frame variables
            self.ui.UnregisteredImageBorder = self.border_left
            self.ui.RegisteredImageBorder = self.border_right
            self.ui.UnregisteredImageFrameHeaderText = self.text_left
            self.ui.RegisteredImageFrameHeaderText = self.text_right
            self.ui.UnregisteredImageDisplayFrame = self.frame_left
            self.ui.RegisteredImageDisplayFrame = self.frame_right

            if self.edit_which_image == 0:  # unregistered image
                # image view variables
                self.overlay_flip_state = self.flip_state
                self.overlay_rotation_angle = self.rotation_angle
                self.overlay_zoom_default = self.zoom_default
                self.overlay_zoom_scale = self.zoom_scale
                self.overlay_pan_offset_x = self.pan_offset_x
                self.overlay_pan_offset_y = self.pan_offset_y
            else:  # registered image
                # image view variables
                self.overlay_reg_flip_state = self.flip_state
                self.overlay_reg_rotation_angle = self.rotation_angle
                self.overlay_reg_zoom_default = self.zoom_default
                self.overlay_reg_zoom_scale = self.zoom_scale
                self.registered_pan_offset_x = self.pan_offset_x
                self.overlay_reg_pan_offset_y = self.pan_offset_y

        elif self.current_index == self.elastic_reg_tab:
            # point view variables
            if self.view_squares > 0:
                self.ui.ColorSquaresButton = self.color_button
                self.squaresColor = self.pts_color
            else:
                if self.edit_which_pt_color == 0:
                    self.ui.ColorFiducialButton_O = self.color_button
                    self.pts_color_overlay_tab_fixed = self.pts_color
                    self.pts_size_overlay_tab_fixed = self.pts_size
                else:
                    self.ui.ColorFiducialButton2_O = self.color_button
                    self.pts_color_overlay_tab_moving = self.pts_color
                    self.pts_size_overlay_tab_moving = self.pts_size

            # frame variables
            self.ui.FiducialRegisteredImageBorder = self.border_left
            self.ui.ElasticRegisteredImageBorder = self.border_right
            self.ui.FiducialRegisteredImageFrameHeaderText = self.text_left
            self.ui.ElasticRegisteredImageFrameHeaderText = self.text_right
            self.ui.FiducialRegisteredImageDisplayFrame = self.frame_left
            self.ui.ElasticRegisteredImageDisplayFrame = self.frame_right

            if self.edit_which_image == 0:  # unregistered image
                # image view variables
                self.unregistered_E_flip_state = self.flip_state
                self.unregistered_E_rotation_angle = self.rotation_angle
                self.unregistered_E_zoom_default = self.zoom_default
                self.unregistered_E_zoom_scale = self.zoom_scale
                self.unregistered_E_pan_offset_x = self.pan_offset_x
                self.unregistered_E_pan_offset_y = self.pan_offset_y
            else:  # registered image
                # image view variables
                self.overlay_reg_elastic_flip_state = self.flip_state
                self.overlay_reg_elastic_rotation_angle = self.rotation_angle
                self.overlay_reg_elastic_zoom_default = self.zoom_default
                self.overlay_reg_elastic_zoom_scale = self.zoom_scale
                self.overlay_reg_elastic_pan_offset_x = self.pan_offset_x
                self.overlay_reg_elastic_pan_offset_y = self.pan_offset_y

        elif self.current_index == self.apply_to_data_tab:
            # point view variables
            self.pts_size_coordinates_tab = self.pts_size
            self.pts_color_coordinates_tab = self.pts_color
            self.ui.ColorFiducialButton_C = self.color_button
            # frame variables
            self.ui.RegisterCoordsImageBorder = self.border_left
            self.ui.RegisterCoordsFrameHeaderText = self.text_left
            self.ui.RegisterCoordsDisplayFrame = self.frame_left

            # image view variables
            self.moving_coords_flip_state = self.flip_state
            self.moving_coords_rotation_angle = self.rotation_angle
            self.moving_coords_brightness = self.brightness
            self.moving_coords_contrast = self.contrast
            self.moving_coords_zoom_default = self.zoom_default
            self.moving_coords_zoom_scale = self.zoom_scale
            self.moving_coords_pan_offset_x = self.pan_offset_x
            self.moving_coords_pan_offset_y = self.pan_offset_y
        else:
            return

        self.pixmap = []

    def show_keyboard_shortcuts(self):
        """Create a pop-up window with keyboard shortcuts.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # Check if the dialog already exists and is visible.
        if hasattr(self, 'keyboardShortcutsDialog') and self.keyboardShortcutsDialog is not None:
            if self.keyboardShortcutsDialog.isVisible():
                self.keyboardShortcutsDialog.raise_()
                self.keyboardShortcutsDialog.activateWindow()
                return
            else:
                # If it's not visible (e.g. closed), reset the reference.
                self.keyboardShortcutsDialog = None

        # Create a non-modal pop-up dialog.
        keyboardDialog = QDialog(self)
        keyboardDialog.setWindowTitle("Keyboard Shortcuts Cheatsheet")
        keyboardDialog.setModal(False)

        # Remove the frame from its current parent by reparenting it.
        self.ui.KeyboardShortcutsControlsFrame.setParent(keyboardDialog)

        # Adjust the dialog's size to ensure it fits the frame.
        keyboardDialog.adjustSize()

        # Connect the dialog's destroyed signal to clear the reference when closed.
        keyboardDialog.destroyed.connect(lambda: setattr(self, 'keyboardShortcutsDialog', None))
        keyboardDialog.show()

        # Keep a reference to the dialog so we don't create a new one each time.
        self.keyboardShortcutsDialog = keyboardDialog

    def change_fiducial_color(self):
        """Open a color picker dialog to change the fiducial color.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.define_edit_frame()

        # Open the color dialog
        color_dialog = QColorDialog(self.pts_color, self)

        # Set a stylesheet to change the font color to white
        color_dialog.setStyleSheet(self.dialog_style)

        # Open the color dialog and check if a valid color is selected
        if color_dialog.exec():
            color = color_dialog.selectedColor()

            if color.isValid():
                if self.current_index == self.fiducials_tab:  # fiducials tab
                    self.pts_color_fiducial_tab = color
                elif self.current_index == self.overlay_tab:  # image overlay tab
                    if self.edit_which_pt_color == 0:
                        self.pts_color_overlay_tab_fixed = color
                    else:
                        self.pts_color_overlay_tab_moving = color
                elif self.current_index == self.apply_to_data_tab:  # apply to coordinates tab
                    self.pts_color_coordinates_tab = color
                elif self.current_index == self.elastic_reg_tab:  # elastic registration tab
                    if self.view_squares == 1:
                        self.squaresColor = color
                    else:
                        if self.edit_which_pt_color == 0:
                            self.pts_color_overlay_tab_fixed = color
                        else:
                            self.pts_color_overlay_tab_moving = color

                self.update_button_color()

                # update image views
                self.update_both_images()

                # if currently in fiducial mode, update the cursor color
                if self.add_fiducial_active and self.current_index == self.fiducials_tab:
                    crosshair_cursor = self.create_large_crosshair_cursor()
                    self.setCursor(crosshair_cursor)

    def update_button_color(self):
        """Update the button background and font color to match the selected fiducial color.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # get the current frame info
        self.define_edit_frame()

        # Calculate the average of the RGB values
        avg_rgb = (self.pts_color.red() + self.pts_color.green() + self.pts_color.blue()) / 3

        # Determine font color based on the average RGB value
        font_color = "white" if avg_rgb < 125 else "black"
        color_rgb = f"rgb({self.pts_color.red()}, {self.pts_color.green()}, {self.pts_color.blue()})"
        tmp = f"background-color: {color_rgb}; color: {font_color};border: 1px solid  #e6e6e6;border-radius: 5px;padding: 5px;"
        self.color_button.setStyleSheet(tmp)
        self.edit_which_pt_color = 0

    def update_zoom_default(self):
        """Determines the initial zoom settings to fit the image entirely within the image frame.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.define_edit_frame()
        if self.image_width == 0 or self.image_height == 0:
            return

        width_scale = self.frame.width() / self.image_width
        height_scale = self.frame.height() / self.image_height

        zoom_default0 = self.zoom_default
        zoom_scale0 = self.zoom_scale
        zz = zoom_scale0 / zoom_default0
        self.zoom_default = min(width_scale, height_scale)
        self.zoom_scale = zz * self.zoom_default
        self.return_edit_frame()

    def initiate_import_project_tab(self):
        """Populate and navigate to tab 1, import project tab
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update tab 1
        """
        # move the navigation tab
        self.ui.WhatNextControlFrame.setParent(self.ui.ImportProjectTabName)
        self.ui.NavigationButton.setParent(self.ui.ImportProjectTabName)
        self.close_navigation_tab()

        # save the current fiducial points and view settings if the user is in the fiducials tab
        self.save_fiducial_state()

        # initiate the tables
        self.ui.tabWidget.setCurrentIndex(self.import_project_tab)
        self.ui.fixedImageTableWidget.setHorizontalHeaderLabels(["Filename", "Folder"])
        self.ui.movingImageTableWidget.setHorizontalHeaderLabels(["Filename", "Folder"])
        self.ui.setJobTableWidget.setHorizontalHeaderLabels(["Results Name", "Folder"])
        self.ui.fixedImageTableWidget.setVerticalHeaderLabels([""])
        self.ui.movingImageTableWidget.setVerticalHeaderLabels(["1"])
        self.ui.setJobTableWidget.setVerticalHeaderLabels([""])
        self.ui.setJobTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(self.results_name))
        self.populate_fixed_table()
        self.populate_moving_table()
        self.populate_project_table()
        # some initial settings
        self.ui.deleteFixedImageButton.setVisible(False)
        self.ui.deleteMovingImageButton.setVisible(False)
        self.ui.keepFixedImageButton.setVisible(False)
        self.ui.keepMovingImageButton.setVisible(False)

        # go to import project tab
        self.ui.tabWidget.setCurrentIndex(self.import_project_tab)
        # check status of tables
        self.check_if_tables_are_complete_import_project_tab()

    def initiate_fiducials_tab(self):
        """Populate and navigate to tab 2, fiducials tab
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update tab 2
        """
        # move the navigation tab
        self.ui.WhatNextControlFrame.setParent(self.ui.AlignImageTabName)
        self.ui.NavigationButton.setParent(self.ui.AlignImageTabName)
        self.ui.KeyboardShortcutsButton.setParent(self.ui.AlignImageTabName)
        self.close_navigation_tab()
        # reset keyboard shortcut settings
        self.shift_key_active = 0
        self.which_key_press = 0
        self.increase_decrease_brightness_contrast_key = 0
        # save the current fiducial points and view settings if the user is in the fiducials tab
        self.save_fiducial_state()

        # save job settings in a template file
        self.save_template_file()

        # initial button settings
        self.ui.DisableFrame_F1.setVisible(False)
        self.ui.ChooseMovingImageFrame.setVisible(True)
        self.ui.LoadNewMovingImageButton.setEnabled(False)
        self.ui.LoadOldMovingImageButton.setEnabled(False)
        self.ui.FiducialPointControlsFrame.setVisible(False)
        self.ui.PickNewMovingImageButton.setVisible(False)
        self.ui.PickNewMovingImageButton.setEnabled(True)
        self.ui.PickNewMovingImageButton.setStyleSheet(self.active_button_style)
        self.ui.AttemptICPRegistrationButton.setVisible(False)
        self.ui.AttemptICPRegistrationButton.setEnabled(True)
        self.ui.AttemptICPRegistrationButton.setStyleSheet(self.style_button_green)
        self.ui.FiducialTabUpdateText.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        QtWidgets.QApplication.processEvents()

        # populate dropdown lists
        self.populate_moving_images_combo_box()
        self.ui.LoadNewMovingImageButton.setStyleSheet(self.inactive_button_style)
        self.ui.LoadOldMovingImageButton.setStyleSheet(self.inactive_button_style)

        # load and display fixed image
        image_path = os.path.join(self.fixed_image_folder, self.fixed_image_filename)
        if self.fixed_image_filename != self.fixed_image_filename_for_coordinates_tab:
            self.im_fixed, self.max_intensity_fixed, self.mode_intensity_fixed = self.load_image(image_path)  # store the original pixmap
            self.fixed_image_filename_for_coordinates_tab = self.fixed_image_filename

        # Calculate zoom_default
        width_scale = self.ui.FixedImageDisplayFrame.width() / self.im_fixed.width()
        height_scale = self.ui.FixedImageDisplayFrame.height() / self.im_fixed.height()
        self.fixed_zoom_default = min(width_scale, height_scale)

        # go to fiducials tab
        self.ui.tabWidget.setCurrentIndex(self.fiducials_tab)
        self.update_button_color()

        # set fiducial point count
        self.pts_fixed = np.array([[0, 0]], dtype=np.float64)
        self.pts_moving = np.array([[0, 0]], dtype=np.float64)
        self.edit_which_image = 0
        self.add_fiducial_active = 0
        self.highlight_current_frame()

        # display image
        self.im_moving = []
        self.moving_zoom_default = 1
        self.edit_which_image = 1
        self.reset_transformations()
        self.edit_which_image = 0
        self.reset_transformations()

    def initiate_overlay_tab(self):
        """Populate and navigate to tab 5, image overlay tab
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update tab 5
        """
        # move the navigation tab
        self.ui.WhatNextControlFrame.setParent(self.ui.ViewOverlayTabName)
        self.ui.NavigationButton.setParent(self.ui.ViewOverlayTabName)
        self.ui.KeyboardShortcutsButton.setParent(self.ui.ViewOverlayTabName)
        self.close_navigation_tab()
        # reset keyboard shortcut settings
        self.shift_key_active = 0
        self.which_key_press = 0
        self.increase_decrease_brightness_contrast_key = 0

        # initial button settings
        self.ui.SaveRegistrationResultsButton_O.setStyleSheet(self.style_button_green)
        self.ui.SavingRegistrationResultsText.setVisible(False)
        self.ui.SaveRegistrationResultsButton_O.setEnabled(True)
        self.ui.ReturnToFiducialsTab_O.setEnabled(True)
        self.ui.ImageViewControlsFrame_O.setEnabled(True)
        self.ui.ElasticRegistrationControlsFrame.setVisible(False)
        self.ui.CalculateElasticRegistrationButton.setVisible(False)
        self.ui.ViewElasticCheckBox.setVisible(False)
        self.ui.TryElasticRegButton.setEnabled(False)
        self.ui.TryElasticRegButton.setStyleSheet(self.inactive_button_style)
        self.ui.DisableFrame_O1.setVisible(False)
        self.close_navigation_tab()
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.squaresColor = self.pts_color_overlay_tab_fixed
        self.add_fiducial_active = False
        self.delete_mode_active = False

        # fill in text
        self.ui.UnregisteredImageFrameHeaderText.setText(
            f"Pre-Registration Overlay (RMSE: {round(self.rmse_unregistered)} pixels).")
        self.ui.RegisteredImageFrameHeaderText.setText(
            f"Fiducial Registration Overlay (RMSE: {round(self.rmse_reg)} pixels).")
        # go to overlay tab
        self.ui.tabWidget.setCurrentIndex(self.overlay_tab)

        # create and display the overlay image
        self.pts_color_overlay_tab_fixed = self.pts_color_fiducial_tab
        self.pts_color_overlay_tab_moving = QColor(255 - self.pts_color_overlay_tab_fixed.red(),
                                                   255 - self.pts_color_overlay_tab_fixed.green(),
                                                   255 - self.pts_color_overlay_tab_fixed.blue())
        self.update_button_color()
        self.edit_which_pt_color = 1
        self.update_button_color()
        pixmap_fixed = self.adjust_brightness_contrast(self.im_fixed, self.fixed_contrast, self.fixed_brightness)
        pixmap_moving = self.adjust_brightness_contrast(self.im_moving, self.moving_contrast, self.moving_brightness)
        self.im_overlay = self.make_overlay_image(pixmap_fixed, pixmap_moving)
        self.edit_which_image = 0
        self.reset_transformations()

        # register the moving image
        size_fixed_image = [self.im_fixed.width(), self.im_fixed.height()]
        self.im_moving_reg = self.transform_image(self.im_moving, self.tform, self.flip_im, size_fixed_image, self.mode_intensity_moving)
        pixmap_moving_reg = self.adjust_brightness_contrast(self.im_moving_reg, self.moving_contrast, self.moving_brightness)

        # make the desired overlay image
        # self.imOverlay = self.make_greyscale_overlay(pixmap_fixed, pixmap_moving, pixmap_moving_reg)
        # plot registered overlay
        self.im_overlay_reg = self.make_overlay_image(pixmap_fixed, pixmap_moving_reg)

        self.edit_which_image = 1
        self.reset_transformations()

    def initiate_elastic_registration_tab(self):
        """Populate and navigate to tab 6, elastic registration tab
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update tab 6
        """
        # move the navigation tab
        self.ui.WhatNextControlFrame.setParent(self.ui.AlignElasticTabName)
        self.ui.NavigationButton.setParent(self.ui.AlignElasticTabName)
        self.ui.KeyboardShortcutsButton.setParent(self.ui.AlignElasticTabName)
        self.close_navigation_tab()
        # reset keyboard shortcut settings
        self.shift_key_active = 0
        self.which_key_press = 0
        self.increase_decrease_brightness_contrast_key = 0

        # enter elastic registration mode
        self.ui.SaveRegistrationResultsButton_E.setEnabled(True)
        self.ui.SaveRegistrationResultsButton_E.setVisible(False)
        self.ui.SaveRegistrationResultsButton_E.setStyleSheet(self.style_button_green)
        self.ui.ReturnToFiducialsTabButton_E.setVisible(False)
        self.ui.CalculateElasticRegistrationButton.setVisible(True)
        self.ui.CalculateElasticRegistrationButton.setEnabled(True)
        self.ui.CalculateElasticRegistrationButton.setStyleSheet(self.style_button_green)
        self.ui.QuitElasticRegistrationButton.setVisible(True)
        self.ui.QuitElasticRegistrationButton.setEnabled(True)
        self.ui.QuitElasticRegistrationButton.setStyleSheet(self.active_button_style)
        self.ui.QuitElasticRegistrationButton2.setVisible(False)
        self.ui.ViewElasticCheckBox.setVisible(True)
        self.ui.ViewElasticCheckBox.setCheckState(Qt.Unchecked)
        self.ui.ElasticRegistrationControlsFrame.setVisible(True)
        self.ui.CalculatingElasticRegistrationText.setVisible(False)
        self.ui.DisableFrame_E1.setVisible(False)
        self.ui.DisableFrame_E2.setVisible(False)
        self.ui.ImageViewControlsFrame_E.setVisible(False)
        self.ui.ClockFrame_E.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.TileSizeText.setHtml(f"<div align='right'>Size:<br>{self.elastic_tilesize}</div>")
        self.ui.TileSpacingText.setHtml(f"<div align='right'>Spacing:<br>{self.elastic_tilespacing}</div>")
        self.view_squares = 1

        # populate text above the images
        self.ui.FiducialRegisteredImageFrameHeaderText.setText(
            f"Fiducial Registration Overlay.")
        self.ui.ElasticRegisteredImageFrameHeaderText.setText(
            f"Fiducial + Elastic Registration Overlay.")

        # go to elastic registration tab
        self.ui.tabWidget.setCurrentIndex(self.elastic_reg_tab)
        self.update_button_color()

        # show the global registration image with boxes overlaid for tilesize and spacing
        # self.imOverlay0 = self.make_overlay_image(pixmap_fixed, pixmap_moving)
        self.edit_which_image = 0
        self.reset_transformations()
        self.update_both_images()

    def initiate_apply_to_coords_tab(self):
        """Populate and navigate to tab 3, apply to coordinates tab
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update tab 3
        """
        # move the navigation tab
        self.ui.WhatNextControlFrame.setParent(self.ui.AlignDataTabName)
        self.ui.NavigationButton.setParent(self.ui.AlignDataTabName)
        self.ui.KeyboardShortcutsButton.setParent(self.ui.AlignDataTabName)
        self.close_navigation_tab()
        # reset keyboard shortcut settings
        self.shift_key_active = 0
        self.which_key_press = 0
        self.increase_decrease_brightness_contrast_key = 0

        # save the current fiducial points and view settings if the user is in the fiducials tab
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
        self.ui.ViewRegisteredEMovingButton.setEnabled(True)
        self.ui.RegisteredEMovingCheckBox.setEnabled(True)
        self.ui.LoadCoordinatesButton.setVisible(False)
        self.ui.BrowseForCoordinatesFileText.setEnabled(False)
        self.ui.CorrespondingImageText.setEnabled(False)
        self.ui.DisableFrame_C.setVisible(False)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.SaveRegisteredCoordinatesButton.setVisible(False)
        self.ui.SaveRegisteredECoordinatesButton.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.SaveRegisteredCoordinatesButton.setStyleSheet(self.style_button_green)
        self.ui.SaveRegisteredECoordinatesButton.setStyleSheet(self.style_button_green)
        self.ui.PlottingImageText.setText("Replotting the Image. Please Wait...")
        self.ui.RegisterCoordsFrameHeaderText.setText("Unregistered Moving Image")

        # uncheck the check boxes
        self.ui.UnregisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredEMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.FixedCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredEMovingCheckBox.setCheckState(Qt.Unchecked)
        self.all_images_checked = 0

        # clear large variables to save memory
        self.im_moving = []
        self.im_moving_reg = []
        self.im_moving_reg_elastic = []
        self.moving_image_filename = []

        # initiate coordinates variables
        self.coordinates_file_folder = ""
        self.coordinates_filename = ""
        self.moving_image_folder_corresponding_to_coordinates = ""
        self.moving_image_filename_corresponding_to_coordinates = ""
        self.loaded_moving_image_filename = ""
        self.loaded_coordinates_filename = ""
        self.coordinate_data = ""
        self.im_moving_coords = []
        self.im_moving_coords_reg = []
        self.im_moving_coords_reg_elastic = []
        self.scale_coordinates_file = ""
        self.column_in_coords_file_containing_x_values = ""
        self.column_in_coords_file_containing_y_values = ""
        self.max_points = "10000" # default maximum set of coordinates to plot when checking coordinate registration
        self.tformCoords = []
        self.DinvCoords = []
        self.pts_coords = []
        self.pts_coords_reg = []
        self.pts_coords_reg_elastic = []
        self.sampled_indices = []
        self.pts_size_coordinates_tab = np.ceil(float(self.pts_size_fiducial_tab) / 5)
        self.json_scale = 1

        # populate dropdown list
        self.populate_coordinates_combo_box()
        self.update_button_color()

        # populate the blank table
        self.ui.RegisterCoordinatesTableWidget.setHorizontalHeaderLabels(
            ["Data Filename", "Moving Image Filename", "Scale", "X Column", "Y Column", "# Points to Plot", " "])
        if self.moving_image_filename_corresponding_to_coordinates or self.coordinates_filename:
            self.ui.RegisterCoordinatesTableWidget.setVerticalHeaderLabels([""])
        self.populate_coordinates_table()

    def initiate_apply_to_image_tab(self):
        """Populate and navigate to tab 7, apply to images tab
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update tab 3
        """
        # move the navigation tab
        self.ui.WhatNextControlFrame.setParent(self.ui.ApplyToImageTabName)
        self.ui.NavigationButton.setParent(self.ui.ApplyToImageTabName)
        self.close_navigation_tab()

        # save the current fiducial points and view settings if the user is in the fiducials tab
        self.save_fiducial_state()

        # move to apply to coordinates tab
        self.ui.tabWidget.setCurrentIndex(self.apply_to_images_tab)

        # initial view settings
        self.ui.DisableFrame_I1.setVisible(False)
        self.ui.RegisterImageButton.setVisible(False)
        self.ui.ApplyToImageText_1.setVisible(False) #self.ui.RegisterCoordsFrameHeaderText.setText("Unregistered Moving Image")
        self.ui.ApplyToImageText_2.setVisible(False)
        self.ui.ApplyToImageText_3.setVisible(False)
        self.ui.ApplyToImageText_4.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.SaveRegisteredCoordinatesButton.setStyleSheet(self.style_button_green)
        self.ui.ApplyToImageComboBox.setVisible(False)
        self.ui.KeepApplyToImageButton.setVisible(False)
        self.ui.DeleteApplyToImageButton.setVisible(False)

        # clear large variables to save memory
        self.im_moving = []
        self.im_moving_reg = []
        self.im_moving_reg_elastic = []
        self.im_moving_coords = []
        self.im_moving_coords_reg = []
        self.im_moving_coords_reg_elastic = []
        self.moving_image_filename = []
        self.num_image_row = 0
        self.num_image_column = 0

        # initiate coordinates variables
        self.image_file_folder = ""
        self.image_filename = ""

        # populate the blank table
        self.ui.ApplyToImageTableWidget.setHorizontalHeaderLabels(
            ["Image Filename", "Corresponding Moving Image", "Apply Which Registration", "Status"])
        if self.image_filename:
            self.ui.ApplyToImageTableWidget.setVerticalHeaderLabels([""])
        self.populate_image_table()

    def apply_registration_to_an_image(self):
        """Let the user browse for a .csv coordinates file.
        Used in tab 7 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will save a registered image.
        """

        self.ui.DisableFrame_I1.setVisible(True)
        self.ui.NavigationButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        QtWidgets.QApplication.processEvents()

        # go through the list of images
        n_rows = self.images_to_register_list.shape[0]
        for i in range(n_rows):
            self.ui.ApplyToImageText_1.setVisible(False)
            self.ui.ApplyToImageText_2.setVisible(False)
            self.ui.ApplyToImageText_3.setVisible(False)
            self.ui.ApplyToImageText_4.setVisible(False)

            # check if affine or elastic registration is requested
            apply_elastic = self.images_to_register_list[i, 4]

            # check if the registered image already exists
            self.image_filename = self.images_to_register_list[i, 0]
            self.image_file_folder = self.images_to_register_list[i, 1]
            if apply_elastic == 'Affine':
                output_folder = os.path.join(self.image_file_folder, "Apply_" + self.results_name)
            else:
                output_folder = os.path.join(self.image_file_folder, "Apply_" + self.results_name, "Elastic")
            # Check if the folder exists, and create it if it doesn't
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            filename = self.image_filename
            outfile = os.path.join(output_folder, filename)
            if os.path.exists(outfile):
                self.images_to_register_list[i][5] = "Already Done!"
                self.populate_image_table()
                continue

            # load the image
            self.ui.ApplyToImageText_1.setText(f"Step 1 of 3. Loading Image: {self.image_filename}...")
            self.ui.ApplyToImageText_1.setVisible(True)
            QtWidgets.QApplication.processEvents()
            corresponding_moving_image_filename = self.images_to_register_list[i, 2]
            image_path = os.path.join(self.image_file_folder, self.image_filename)
            im_moving_apply, max_intensity, mode_intensity_moving_apply = self.load_image(image_path)  # store the original pixmap

            # load the affine registration variables
            filename, _ = os.path.splitext(corresponding_moving_image_filename)
            self.ui.ApplyToImageText_2.setText(f"Step 2 of 3. Applying Registration Metadata from Image: "
                                               f"{corresponding_moving_image_filename}...")
            self.ui.ApplyToImageText_2.setVisible(True)
            QtWidgets.QApplication.processEvents()
            data_filename = filename + ".pkl"
            data_folder = os.path.join(self.job_folder, self.results_name, "Registration transforms")
            outfile = os.path.join(data_folder, data_filename)
            with open(outfile, 'rb') as file:
                data = pickle.load(file)
            tform = data.get('tform')
            flip_im = data.get('flip_im')
            size_fixed_image = data.get('size_fixed_image')
            size_moving_image = data.get('size_moving_image')

            # determine the difference in size between this image and the original moving image
            scale_width = im_moving_apply.width() / size_moving_image[0]
            scale_height = im_moving_apply.height() / size_moving_image[1]
            rescale_to_new_image_size = (scale_width + scale_height) / 2

            # remove the scaling portion of tform, and account for the different image size of the loaded image
            affine_scale_factor = np.linalg.norm(tform[:2, 0])
            tform_noscale = np.eye(3)
            tform_noscale[:2, :2] = tform[:2, :2] / affine_scale_factor
            tform_noscale[:2, 2] = (tform[:2, 2] / affine_scale_factor) * rescale_to_new_image_size

            # apply affine registration to the image
            size_in = [int(round(size_fixed_image[0] * rescale_to_new_image_size)),
                                int(round(size_fixed_image[1] * rescale_to_new_image_size))]
            size_out = [round(size_fixed_image[0] / affine_scale_factor * rescale_to_new_image_size),
                        round(size_fixed_image[1] / affine_scale_factor * rescale_to_new_image_size)]
            registered_mask = self.transform_image(im_moving_apply, tform_noscale, flip_im, size_in, mode_intensity_moving_apply, size_out)
            self.debug_show_image(self.pixmap_to_array(registered_mask), 1)

            # apply elastic registration if requested
            if apply_elastic == "Elastic":
                # load the elastic registration variables
                data_folder = os.path.join(self.job_folder, self.results_name, "Registration transforms", "Elastic")
                outfile = os.path.join(data_folder, data_filename)
                with open(outfile, 'rb') as file:
                    data = pickle.load(file)
                D = data.get('D')

                # apply the elastic registration
                scale_elastic = rescale_to_new_image_size / affine_scale_factor
                registered_mask = self.register_image_elastic(self.pixmap_to_array(registered_mask), D, mode_intensity_moving_apply, scale_elastic)
                registered_mask = self.array_to_pixmap(registered_mask)

            # save the registered image
            self.ui.ApplyToImageText_3.setText("Step 3 of 3. Saving Registered Image...")
            self.ui.ApplyToImageText_3.setVisible(True)
            QtWidgets.QApplication.processEvents()

            filetype = self.image_filename.lower()
            outfile = os.path.join(output_folder, self.image_filename)
            if filetype.endswith(('.tif', '.png')):
                registered_mask.save(outfile, format='TIFF')
            else:
                registered_mask.save(outfile, 'JPG')

            self.ui.ApplyToImageText_4.setText("Done!")
            self.ui.ApplyToImageText_4.setVisible(True)
            self.images_to_register_list[i][5] = "Done!"
            self.populate_image_table()
            QtWidgets.QApplication.processEvents()

        self.ui.DisableFrame_I1.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        QtWidgets.QApplication.processEvents()

    def initiate_job_status_tab(self):
        """Populate and navigate to tab 5, job status tab
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update tab 5
        """
        # move the navigation tab
        self.ui.WhatNextControlFrame.setParent(self.ui.JobStatusTabName)
        self.ui.NavigationButton.setParent(self.ui.JobStatusTabName)
        self.close_navigation_tab()

        # set some buttons
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)

        # save the current fiducial points and view settings if the user is in the fiducials tab
        self.save_fiducial_state()

        num_rows = self.moving_images_list.shape[0] + 1
        self.ui.JobStatusTableWidget.setRowCount(num_rows)

        # populate the rows of the table with the info in moving_images_list
        self.ui.JobStatusTableWidget.setHorizontalHeaderLabels(
            ["Image Name", "# Fiducials", "ICP Registration", "Elastic Registration", "Coordinates Registered"])
        self.ui.JobStatusTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"Fixed image: {self.fixed_image_filename}  "))
        self.ui.JobStatusTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(" - "))
        self.ui.JobStatusTableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(" - "))
        self.ui.JobStatusTableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(" - "))

        row_count = 1
        for row in self.moving_images_list:
            self.ui.JobStatusTableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(f"Moving image {row_count}:  {row[0]}  "))
            row_count += 1

        # check if corresponding files exist
        check_file_status = np.zeros((self.moving_images_list.shape[0], 4), dtype=int)
        folder_1 = os.path.join(self.job_folder, self.results_name, "Fiducial point selection")
        folder_2 = os.path.join(self.job_folder, self.results_name, "Registration transforms")
        folder_3 = os.path.join(self.job_folder, self.results_name, "Registration transforms", "Elastic")
        folder_4 = os.path.join(self.job_folder, self.results_name, "Registered Coordinate Data", "log")
        for i, row in enumerate(self.moving_images_list):
            image_file = row[0]
            image_name, _ = os.path.splitext(image_file)

            # Construct the expected .pkl filenames
            outfile = os.path.join(folder_1, f"{image_name}.pkl")
            # check # of fiducial points
            if os.path.exists(outfile):
                with open(outfile, 'rb') as file:
                    data = pickle.load(file)
                pts = data.get('pts_F')
                if pts.shape[0] >= self.MIN_NUM_FIDUCIAL_PTS:
                    check_file_status[i, 0] = pts.shape[0]

            # check if icp registration transform exists
            outfile = os.path.join(folder_2, f"{image_name}.pkl")
            if os.path.exists(outfile):
                with open(outfile, 'rb') as file:
                    data = pickle.load(file)
                RMSE = data.get('RMSE')
                check_file_status[i, 1] = RMSE
            else:
                check_file_status[i, 1] = -50

            # check if elastic registration transform exists
            outfile = os.path.join(folder_3, f"{image_name}.pkl")
            if os.path.exists(outfile):
                with open(outfile, 'rb') as file:
                    data = pickle.load(file)
                RMSE_Elastic = data.get('RMSE_Elastic')
                check_file_status[i, 2] = RMSE_Elastic
            else:
                check_file_status[i, 2] = -50

            # check if coordinates have been registered
            outfile = os.path.join(folder_4, f"{image_name}.pkl")
            if os.path.exists(outfile):
                with open(outfile, 'rb') as file:
                    data = pickle.load(file)
                coord_registration_type = data.get('coord_registration_type')
                check_file_status[i, 3] = coord_registration_type
            else:
                check_file_status[i, 3] = -50

        row_count = 1
        for row in check_file_status:
            # Fiducial point setting
            self.ui.JobStatusTableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(f"{row[0]} pairs"))
            # RMSE from ICP registration
            if row[1] != -50:
                self.ui.JobStatusTableWidget.setItem(row_count, 2,
                                                     QtWidgets.QTableWidgetItem(f"RMSE: {str(row[1])} pixels"))
            else:
                self.ui.JobStatusTableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(""))
            # RMSE from elastic registration
            if row[2] != -50:
                self.ui.JobStatusTableWidget.setItem(row_count, 3,
                                                     QtWidgets.QTableWidgetItem(f"RMSE: {str(row[2])} pixels"))
            else:
                self.ui.JobStatusTableWidget.setItem(row_count, 3, QtWidgets.QTableWidgetItem(""))
            # Coordinates saved
            if row[3] != -50:
                self.ui.JobStatusTableWidget.setItem(row_count, 4, QtWidgets.QTableWidgetItem("Saved!"))
            else:
                self.ui.JobStatusTableWidget.setItem(row_count, 4, QtWidgets.QTableWidgetItem(""))
            row_count += 1

        # go to job status tab
        self.ui.tabWidget.setCurrentIndex(self.job_status_tab)
        self.ui.JobStatusTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def reset_transformations(self, keep_contrast=None):
        """Reset all transformations to the image view to their defaults.
        Used in multiple tabs
        Args:
            keep_contrast: (optional) if yes, do not change contrast back to default
        Returns:
            no variables output, but app view changes
        """
        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index not in {self.fiducials_tab, self.overlay_tab, self.apply_to_data_tab, self.elastic_reg_tab}:
            return

        self.flip_state = False
        self.rotation_angle = 0
        self.zoom_scale = self.zoom_default
        self.pan_offset_x = 0
        self.pan_offset_y = 0
        if keep_contrast is None:
            self.brightness = 0
            self.contrast = 1
        self.return_edit_frame()
        self.update_image_view()

    def flip_image_y(self):
        """Flip the image horizontally while ensuring it fits within bounds.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index not in {self.fiducials_tab, self.overlay_tab, self.apply_to_data_tab, self.elastic_reg_tab}:
            return

        # flip
        self.flip_state = not self.flip_state
        self.pan_offset_x = -self.pan_offset_x
        self.return_edit_frame()
        self.update_image_view()

    def rotate_label_ui(self):
        """Rotate the image while ensuring pan offsets align with the rotation.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index not in {self.fiducials_tab, self.overlay_tab, self.apply_to_data_tab, self.elastic_reg_tab}:
            return

        # rotate
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.return_edit_frame()
        self.update_image_view()

    def change_brightness(self, delta_val=0):
        """Change the image brightness.
        Used in multiple tabs
        Args:
            delta_val: number to increase or decrease the brightness by
        Returns:
            no variables output, but app view changes
        """
        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index not in {self.fiducials_tab, self.apply_to_data_tab}:
            return

        self.brightness = self.brightness + delta_val
        self.return_edit_frame()
        self.update_image_view()
        #print(f"brightness: {self.brightness}, contrast: {self.contrast}")

    def change_contrast(self, delta_val=0):
        """Change the image contrast.
        Used in multiple tabs
        Args:
            delta_val: number to increase or decrease the brightness by
        Returns:
            no variables output, but app view changes
        """
        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index not in {self.fiducials_tab, self.apply_to_data_tab, self.overlay_tab, self.elastic_reg_tab}:
            return

        self.contrast = self.contrast + delta_val
        self.return_edit_frame()
        self.update_image_view()
        #print(f"brightness: {self.brightness}, contrast: {self.contrast}")

    def auto_adjust_contrast(self):
        """Estimate a good contrast to adjust the image by, using the maximum intensity of the image.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # skip if we aren't in an image view tab
        self.define_edit_frame()
        if self.current_index not in {self.fiducials_tab, self.apply_to_data_tab, self.overlay_tab, self.elastic_reg_tab}:
            return

        # calculate the maximum image intensity
        image_max_intensity = self.max_intensity + self.brightness

        # determine the contrast to increase the maximum intensity to 255
        contrast_old = self.contrast
        self.contrast = 255 / min(image_max_intensity, 255)
        #print(f"  new auto contrast is {self.contrast}, adjusted from {contrast_old}")
        self.return_edit_frame()
        self.update_image_view()

    def call_increase_fiducial_size0(self):
        """Handle increase the fiducial size of the first of the fiducial pairs in an overlay image.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.edit_which_pt_color = 0  # color 1
        self.increase_fiducial_size()

    def call_increase_fiducial_size1(self):
        """Handle increase the fiducial size of the second of the fiducial pairs in an overlay image.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.edit_which_pt_color = 1  # color 1
        self.increase_fiducial_size()

    def call_decrease_fiducial_size0(self):
        """Handle decrease the fiducial size of the first of the fiducial pairs in an overlay image.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.edit_which_pt_color = 0  # color 1
        self.decrease_fiducial_size()

    def call_decrease_fiducial_size1(self):
        """Handle decrease the fiducial size of the second of the fiducial pairs in an overlay image.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.edit_which_pt_color = 1  # color 1
        self.decrease_fiducial_size()

    def increase_fiducial_size(self):
        """Increase the fiducial size.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.define_edit_frame()
        self.pts_size = self.pts_size + 1
        self.return_edit_frame()
        self.edit_which_pt_color = 0
        self.update_both_images()

    def decrease_fiducial_size(self):
        """Decrease the fiducial size.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.define_edit_frame()
        self.pts_size = max([self.pts_size - 1, 1])
        self.return_edit_frame()
        self.edit_which_pt_color = 0
        self.update_both_images()

    def make_greyscale_overlay(self, im_fixed, im_moving, im_moving_reg):
        """Make an overlay of two RGB images. Overlay keeps the RGB colors of imFixed, and fully substitutes
        pixels of imFixed where imMovingReg contains tissue.
        Used in multiple tabs
        Args:
            im_fixed: image 1
            im_moving: image 2
            im_moving_reg: image 3
        Returns:
            im_overlay: combined overlay image made from imFixed and imMoving
        """
        # register a mask of the moving image
        array = self.pixmap_to_array(im_moving)
        array_mask = np.ones_like(array, dtype=np.uint8)
        array_mask = self.array_to_pixmap(array_mask)
        size_fixed_image = [self.im_fixed.width(), self.im_fixed.height()]
        registered_mask = self.transform_image(array_mask, self.tform, self.flip_im, size_fixed_image, [0, 0, 0])
        registered_mask = self.pixmap_to_array(registered_mask)  # [..., :3]

        # Convert pixmaps to arrays
        moving_array = self.pixmap_to_array(im_moving_reg)
        overlay_array = self.pixmap_to_array(im_fixed)
        gray_values = overlay_array[..., :3].mean(axis=-1).astype(np.uint8)  # Mean of RGB channels
        gray_values = (gray_values / gray_values.max() * 255).astype(np.uint8)  # Normalize brightness to match original
        overlay_array = np.stack([gray_values] * overlay_array.shape[-1], axis=-1)
        overlay_array[registered_mask == 1] = moving_array[registered_mask == 1]
        overlay_array = np.ascontiguousarray(overlay_array[..., :3])  # remove the alpha channel
        im_overlay = self.array_to_pixmap(overlay_array)

        return im_overlay

    def make_overlay_image(self, im_fixed, im_moving):
        """Make an overlay of two RGB images. Overlay is a direct combination of both images
        Used in multiple tabs
        Args:
            im_fixed: image 1
            im_moving: image 2
        Returns:
            im_overlay: combined overlay image made from imFixed and imMoving
        """
        # pad images to be the same size
        height = max([im_fixed.height(), im_moving.height()])
        width = max([im_fixed.width(), im_moving.width()])

        # pad the fixed image
        im_fixed_pad, im_fixed_pad_grey = self.pad_images(im_fixed, width, height, self.mode_intensity_fixed)
        mode_fixed = np.mean(np.array(self.mode_intensity_fixed))

        # pad the moving image
        im_moving_pad, im_moving_pad_grey = self.pad_images(im_moving, width, height, self.mode_intensity_moving)
        mode_moving = np.mean(np.array(self.mode_intensity_moving))

        # if one image is brightfield and the other is fluorescent, complement one image so the overlay is clear
        if mode_moving < 25 < mode_fixed:
            im_moving_pad_grey = 255 - im_moving_pad_grey
        if mode_fixed < 25 < mode_moving:
            im_fixed_pad_grey = 255 - im_fixed_pad_grey

        # make the combined overlay image
        combined_array = np.stack((im_moving_pad_grey, im_fixed_pad_grey, im_moving_pad_grey), axis=-1)  # (H, W, 3)
        im_overlay = QImage(combined_array.data, width, height, 3 * width, QImage.Format_RGB888)
        im_overlay = QPixmap.fromImage(im_overlay)

        return im_overlay

    def pixmap_to_array(self, pixmap):
        """Convert a QPixmap to a numpy array.
        Used in multiple tabs
        Args:
            pixmap: pixmap to convert to an image array
        Returns:
            image: numpy array converted from pixmap
        """
        # get information from pixmap to convert to a numpy array
        image = pixmap.toImage()
        width = image.width()
        height = image.height()
        bytes_per_line = image.bytesPerLine()
        ptr = image.bits()
        channels = int(np.size(ptr) / width / height)
        ptr = np.array(ptr).reshape((height, bytes_per_line))  # Convert memory view to NumPy array
        array = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width, channels))

        # if channels == 4:
        #    array = array[:, :, :3]
        #    print("  remove 4th channel")

        return array

    def array_to_pixmap(self, array):
        """Convert a numpy array to QPixmap.
        Used in multiple tabs
        Args:
            array: numpy array to convert to a pixmap
        Returns:
            pixmap: pixmap converted from image
        """
        # get the shape information from the image to convert to an 8-bit RGB pixmap
        height, width, channels = array.shape[:3]
        bytes_per_line = array.strides[0]
        qimage = QImage(array.data, width, height, bytes_per_line,
                        QImage.Format_ARGB32 if channels == 4 else QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        return pixmap

    def pad_images(self, pixmap, width, height, mode_vals, border=None):
        """pads a pixmap image to a defined width and height.
        Used in multiple tabs
        Args:
            pixmap: image in a pixmap object
            width: desired width to pad the image to
            height: desired height to pad the image to
            mode_vals: RGB triplet of mode intensity of each channel of pixmap
            border: logical input, if yes add a white border around pixmap
        Returns:
            image_pad: padded image array
            image_pad_grey: greyscale padded image array
        """
        # Convert pixmap to image
        image = self.pixmap_to_array(pixmap)
        height0, width0 = image.shape[:2]

        if border is not None:
            # add a white border
            image[:15, :, :] = 255  # Top border
            image[-15:, :, :] = 255  # Bottom border
            image[:, :15, :] = 255  # Left border
            image[:, -15:, :] = 255  # Right border

        # Pad each channel to the desired width and height
        pad_width = ((0, height - height0), (0, width - width0))  # Padding for height and width
        r_pad = np.pad(image[..., 0], pad_width, mode='constant', constant_values=mode_vals[0])
        g_pad = np.pad(image[..., 1], pad_width, mode='constant', constant_values=mode_vals[1])
        b_pad = np.pad(image[..., 2], pad_width, mode='constant', constant_values=mode_vals[2])

        # Combine the padded channels into a single RGB array and a grayscale array
        image_pad = np.stack((b_pad, g_pad, r_pad), axis=-1)

        # Flatten the image and calculate the mode
        image_pad_gray = np.mean(image_pad, axis=-1).astype(np.uint8)

        return image_pad, image_pad_gray

    def update_both_images(self):
        """Will call the appropriate functions to update the image view of all images present in the current tab.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the image views in the current tab
        """

        self.define_edit_frame()
        if self.current_index == self.fiducials_tab or self.current_index == self.overlay_tab:  # fiducials tab
            self.edit_which_image = not self.edit_which_image
            self.update_image_view()
            self.edit_which_image = not self.edit_which_image
            self.update_image_view()
        elif self.current_index == self.apply_to_data_tab:  # apply to coordinates tab
            self.update_image_view()
        elif self.current_index == self.elastic_reg_tab:
            if self.view_squares == 1:
                self.im_overlay_reg_elastic = []
                self.edit_which_image = 1
                self.update_image_view()
                self.edit_which_image = 0
                self.update_image_view()
            else:
                self.edit_which_image = not self.edit_which_image
                self.update_image_view()
                self.edit_which_image = not self.edit_which_image
                self.update_image_view()

    def update_image_view(self):
        """Update the image view with all transformations (flip, rotate, zoom, and pan),
           and overlays (fiducial points and square outlines) preserved.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the image view in the current tab
        """

        # define the current frame variables and pixmap
        self.update_zoom_default()
        define_pixmap = 1
        self.define_edit_frame(define_pixmap)
        if self.current_index in {self.fiducials_tab, self.overlay_tab, self.elastic_reg_tab}:
            self.fiducial_pts_to_plot = np.delete(self.fiducial_pts_to_plot, 0, axis=0)  # remove the first point
        elif self.current_index == self.apply_to_data_tab:
            # randomly subsample the coordinate points
            if isinstance(self.sampled_indices, np.ndarray):
                self.fiducial_pts_to_plot = self.fiducial_pts_to_plot[self.sampled_indices]
            else:
                return
        else:
            return

        zoom_ratio = self.zoom_scale / self.zoom_default
        if self.pixmap is not None:
            if not self.pixmap:
                self.label.clear()
                return

            if self.brightness != 0 or self.contrast != 1:
                self.pixmap = self.adjust_brightness_contrast(self.pixmap, self.contrast, self.brightness)

            size_pt = max(
                [int(np.ceil(max([self.pixmap.width(), self.pixmap.height()]) / 1000 / zoom_ratio * self.pts_size)), 1])
            if self.current_index == self.elastic_reg_tab and self.view_squares > 0:
                if self.view_squares == 1:
                    self.pixmap = self.add_squares_to_image(self.pixmap)
                elif self.view_squares == 2:
                    self.pixmap = self.add_square_to_image(self.pixmap, self.xySquare)
            else:
                self.pixmap = self.add_points_to_image(self.pixmap, self.fiducial_pts_to_plot, size_pt, self.pts_color)

            if self.current_index == self.fiducials_tab:  # if in fiducials tab, overlay the potential deletion point if required
                # update the fiducial point count
                count = self.pts_moving.shape[0] - 1
                self.ui.FiducialFrameHeaderText.setText(f"Fiducial Point View (# Pairs : {count})")
                if count >= self.MIN_NUM_FIDUCIAL_PTS:
                    self.ui.AttemptICPRegistrationButton.setVisible(True)
                    self.ui.AttemptICPRegistrationButton.setEnabled(True)
                    self.ui.AttemptICPRegistrationButton.setStyleSheet(self.style_button_green)
                else:
                    self.ui.AttemptICPRegistrationButton.setEnabled(False)
                    self.ui.AttemptICPRegistrationButton.setStyleSheet(self.inactive_button_style)

                # highlight the point to be deleted, if applicable
                if self.delete_mode_active and self.potential_deletion != -5:
                    size_pt = size_pt * 2
                    color = QColor(round(self.pts_color.red() * 0.5), round(self.pts_color.green() * 0.5),
                                   round(self.pts_color.blue() * 0.5))
                    self.pixmap = self.add_points_to_image(self.pixmap, [self.fiducial_pts_to_plot[self.potential_deletion]],
                                                           size_pt, color)
            elif self.current_index == self.overlay_tab or (
                    self.current_index == self.elastic_reg_tab and self.view_squares == 0):  # if in overlay tab, also overlay the fiducial points of the moving image
                self.pts_size = self.pts_size_overlay_tab_moving
                size_pt = max(
                    [int(np.ceil(max([self.pixmap.width(), self.pixmap.height()]) / 1000 / zoom_ratio * self.pts_size)), 1])
                if self.current_index == self.overlay_tab and self.edit_which_image == 0:
                    self.more_fiducial_pts_to_plot = np.delete(self.more_fiducial_pts_to_plot, 0, axis=0)

                color = self.pts_color_overlay_tab_moving
                self.pixmap = self.add_points_to_image(self.pixmap, self.more_fiducial_pts_to_plot, size_pt, color)

            # Create a transformation matrix to apply the view settings flip, rotation, and zoom
            transform = QTransform()
            if self.flip_state:
                transform.scale(-1, 1)
            transform.rotate(self.rotation_angle)
            transform.scale(self.zoom_scale, self.zoom_scale)
            transformed_pixmap = self.pixmap.transformed(transform, mode=Qt.SmoothTransformation)

            # plot the image
            self.label.setPixmap(transformed_pixmap)
            self.label.resize(transformed_pixmap.size())

            # Apply pan offsets
            offset_x, offset_y = self._apply_flip_and_rotation()
            parent_rect = self.label.parent().rect()
            new_x = offset_x + (parent_rect.width() - self.label.width()) // 2
            new_y = offset_y + (parent_rect.height() - self.label.height()) // 2
            self.label.move(int(new_x), int(new_y))

    def _apply_flip_and_rotation(self):
        """Updates image flip and rotate image view variables when the corresponding key is pressed.
        Used in multiple tabs
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the image view variables to apply flip and rotation
        """
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

    def is_file_an_image(self, file_path):
        """Determines whether the selected file is an image.
        Used in multiple tabs
        Args:
            file_path: folder and name of the file in question
        Returns:
            True or False: is the file an image
        """
        try:
            with Image.open(file_path) as img:
                img.verify()  # Verify that it is an image
            return True
        except (IOError, SyntaxError):
            text = "The selected file is not an image. Please select an image"
            self.show_error_message(text)
            return False

    def add_points_to_image(self, pixmap, pts, pt_size, color):
        """Embed points into the image pixmap object.
        Used in multiple tabs
        Args:
            pixmap: pixmap object containing the image to edit
            pts: points to embed in the image
            pt_size: size to award to each point (in pixels) in the image
            color: RGB color triplet for the points
        Returns:
            pixmap_pts: pixmap object containing the image with points overlayed
        """
        pts = np.round(pts).astype(int)

        # Convert QImage to NumPy array
        image = self.pixmap_to_array(pixmap)
        height, width, channels = image.shape[:3]

        # Define the square region bounds
        pt_x_start = np.maximum(pts[:, 0] - pt_size, 0)  # Ensure within image bounds
        pt_x_end = np.minimum(pts[:, 0] + pt_size + 1, width)  # Ensure within image bounds
        pt_y_start = np.maximum(pts[:, 1] - pt_size, 0)  # Ensure within image bounds
        pt_y_end = np.minimum(pts[:, 1] + pt_size + 1, height)  # Ensure within image bounds
        mask = np.zeros(image.shape[:2], dtype=bool)
        for x_s, x_e, y_s, y_e in zip(pt_x_start, pt_x_end, pt_y_start, pt_y_end):
            mask[y_s:y_e, x_s:x_e] = True

        # Apply changes to all pixels in the mask
        image[mask, 0] = color.blue()  # Blue channel
        image[mask, 1] = color.green()  # Green channel
        image[mask, 2] = color.red()  # Red channel

        # Convert the modified array back to QImage
        pixmap_pts = self.array_to_pixmap(image)

        return pixmap_pts

    def adjust_brightness_contrast(self, pixmap, contrast, brightness):
        """Change the brightness and contrast of the image as desired.
        Used in multiple tabs
        Args:
            pixmap: pixmap object containing the image to edit
            contrast: contrast factor to multiply the image by
            brightness: brightness value to add to the image
        Returns:
            pixmap: brightness and contrast adjusted image as a pixmap object
        """
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

    def eventFilter(self, source, event):
        """
        Intercept events on the tab bar to block mouse clicks or scrolls on the tab titles.
        Used in multiple apps
        Args:
            source: defines where in the app the moues is
            event: logs whether  a mouse click or wheel scroll event occured
        Returns:
            no variables output, but will prevent the tab changing based on a mouse scroll or click
        """
        if source == self.ui.tabWidget.tabBar() and event.type() in (QEvent.MouseButtonPress, QEvent.Wheel):
            # Ignore mouse clicks on the tab bar to prevent tab switching
            return True  # Stops the event from propagating further
        return super().eventFilter(source, event)

    def view_navigation_tab(self):
        """Opens the navigation bar so the user can navigate between apps.
        Used in multiple apps
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will change the view of the app
        """
        # button view settings
        self.ui.WhatNextControlFrame.setVisible(True)
        self.ui.NavigationButton.setVisible(False)
        self.ui.KeyboardShortcutsButton.setVisible(False)

        if not self.ui.FiducialPointControlsFrame.isVisible():
            self.ui.ChooseMovingImageFrame.setVisible(False)

    def close_navigation_tab(self):
        """Closes the navigation bar.
        Used in multiple apps
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will change the view of the app
        """

        # button view settings
        self.ui.WhatNextControlFrame.setVisible(False)
        self.ui.NavigationButton.setVisible(True)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setVisible(True)
        self.ui.KeyboardShortcutsButton.setEnabled(True)

        if not self.ui.FiducialPointControlsFrame.isVisible():
            self.ui.ChooseMovingImageFrame.setVisible(True)

    def mousePressEvent(self, event):
        """Handle mouse press events for adding fiducial points and panning.
        Used in multiple tabs
        Args:
            event: mouse press event occurred
        Returns:
            no variables output, but if panning mode is active the image view will change
        """

        # skip if the current tab does not contain an image
        if self.current_index not in {self.fiducials_tab, self.overlay_tab, self.apply_to_data_tab,
                                      self.elastic_reg_tab}:
            return

        if self.add_fiducial_active:
            self.edit_which_image = self.edit_which_fid
        self.define_edit_frame()

        # figure out which image to edit
        frame_info_left = self.frame_left.geometry()
        frame_info_right = self.frame_right.geometry()
        cursor_pos = self.mapFromGlobal(event.globalPosition().toPoint())
        position_x = cursor_pos.x()
        position_y = cursor_pos.y() - self.padnum
        in_left_x = frame_info_left.x() < position_x < frame_info_left.x() + frame_info_left.width()
        in_left_y = frame_info_left.y() < position_y < frame_info_left.y() + frame_info_left.height()
        in_right_x = frame_info_right.x() < position_x < frame_info_right.x() + frame_info_right.width()
        in_right_y = frame_info_right.y() < position_y < frame_info_right.y() + frame_info_right.height()

        # left click to pan
        if event.button() == Qt.LeftButton:
            if in_left_x and in_left_y:
                if self.current_index != self.apply_to_data_tab:
                    self.edit_which_image = 0
            elif in_right_x and in_right_y:
                if self.current_index != self.apply_to_data_tab:
                    self.edit_which_image = 1
            else:
                return

            # Get the mouse position relative to the target label
            self.define_edit_frame()
            self.panning_mode_active = 1
            self.last_mouse_position = event.globalPosition()  # Store the initial mouse position

    def mouseMoveEvent(self, event):
        """Handle mouse move events for panning.
        Used in multiple tabs
        Args:
            event: mouse release event occurred
        Returns:
            no variables output, but if panning mode is active the image view will change
        """
        # if panning
        if self.panning_mode_active != 0:
            self.panning_mode_active += self.panning_mode_active  # the mouse was clicked and now moved
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

            # update pan offsets
            self.pan_offset_x += offset_x
            self.pan_offset_y += offset_y
            self.return_edit_frame()

            # reapply transformations
            self.update_image_view()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events.
        Used in multiple tabs
        Args:
            event: mouse release event occured
        Returns:
            no variables output.
               if panning mode was active, this event will end panning mode at the current position
               if fiducial point mode was active, this event will trigger a new fiducial point
        """

        if event.button() == Qt.LeftButton:
            if self.panning_mode_active < 3 and self.current_index == self.fiducials_tab and (
                    self.add_fiducial_active or self.delete_mode_active):
                if self.add_fiducial_active:
                    self.edit_which_image = self.edit_which_fid
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
                if self.add_fiducial_active:  # add a fiducial
                    if in_left_x and in_left_y and self.edit_which_fid == 0:
                        self.handle_fiducial_click(local_pos.x(), local_pos.y(), event)
                    elif in_right_x and in_right_y and self.edit_which_fid == 1:
                        self.handle_fiducial_click(local_pos.x(), local_pos.y(), event)
                elif self.delete_mode_active and self.current_index == self.fiducials_tab:
                    cursor_pos = self.mapFromGlobal(event.globalPosition().toPoint())
                    self.handle_fiducial_click(cursor_pos.x(), cursor_pos.y(), event)
                else:
                    return
        self.panning_mode_active = 0

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming.
        Used in multiple tabs
        Args:
            event: mouse wheel event occurred
        Returns:
            no variables output, if the mouse was hovering over an image when the wheel event occured,
            the zoom of that image will update
        """

        self.define_edit_frame()
        if self.current_index not in {self.fiducials_tab, self.overlay_tab, self.apply_to_data_tab,
                                      self.elastic_reg_tab}:
            return

        # figure out if the mouse is hovering over one of the image frames
        frame_info_left = self.frame_left.geometry()
        frame_info_right = self.frame_right.geometry()
        cursor_pos = self.mapFromGlobal(event.globalPosition().toPoint())
        position_x = cursor_pos.x()
        position_y = cursor_pos.y() - self.padnum
        in_left_x = frame_info_left.x() < position_x < frame_info_left.x() + frame_info_left.width()
        in_left_y = frame_info_left.y() < position_y < frame_info_left.y() + frame_info_left.height()
        in_right_x = frame_info_right.x() < position_x < frame_info_right.x() + frame_info_right.width()
        in_right_y = frame_info_right.y() < position_y < frame_info_right.y() + frame_info_right.height()

        # apply the zoom to the left image frame
        if in_left_x and in_left_y:
            if self.current_index != self.apply_to_data_tab:
                self.edit_which_image = 0
        # apply the zoom to the right image frame
        elif in_right_x and in_right_y:
            if self.current_index != self.apply_to_data_tab:
                self.edit_which_image = 1
        # ignore the wheel event
        else:
            return

        # get the mouse position relative to the target label
        self.define_edit_frame()
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

        # adjust zoom scale based on scroll direction
        delta = event.angleDelta().y()
        scale_factor = 1.1 if delta > 0 else 0.9
        new_zoom_scale = self.zoom_scale * scale_factor
        new_zoom_scale = max(0.1, min(new_zoom_scale, 10.0))  # Clamp between 0.1 and 10.0

        # calculate the image scaling factor and adjust pan offsets
        scale_change = new_zoom_scale / self.zoom_scale
        self.pan_offset_x += zoom_focus_x * (1 - scale_change)
        self.pan_offset_y += zoom_focus_y * (1 - scale_change)
        self.zoom_scale = new_zoom_scale

        # update the zoom scale and pan offsets
        self.return_edit_frame()

        # reapply transformations
        self.update_image_view()

    def show_error_message(self, text):
        """Displays a pop-up window error message for various errors within the app.
        Used in multiple tabs
        Args:
            text: text string to display within the error window
        Returns:
            no variables output, but will display a pop-up error message
        """
        # set up the error message window
        msg_box = QtWidgets.QMessageBox()  # create a message box
        msg_box.setWindowTitle("ERROR MESSAGE")  # set the window title
        msg_box.setText(text)  # set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)  # add Yes and Cancel buttons

        # apply custom stylesheet for background and font color
        msg_box.setStyleSheet(self.quest_box_style)

        # show the error message box
        msg_box.exec()

    def keyReleaseEvent(self, event):
        """Handle key release events. Determine which combination of keys was
        pressed and perform the corresponding action.
        Used in multiple tabs
        Args:
            event: the user pressed a key on the keyboard
        Returns:
            none
        """
        # Update key states on release
        if event.key() == Qt.Key_Shift:
            self.shift_key_active = 0
        elif event.key() in {Qt.Key_R, Qt.Key_F, Qt.Key_D, Qt.Key_B, Qt.Key_C, Qt.Key_A, Qt.Key_S}:
            self.which_key_press = 0
        elif event.key() in {44, 46, 60, 62, 75, 76}:  # {< > K L shift+< shift+>}
            self.increase_decrease_brightness_contrast_key = 0

    def keyPressEvent(self, event):
        """Handle key press events. Determine which combination of keys was
        pressed and perform the corresponding action.
        Used in multiple tabs
        Args:
            event: the user pressed a key on the keyboard
        Returns:
            none
        """
        self.current_index = self.ui.tabWidget.currentIndex()

        # check if the Esc key is pressed
        if event.key() == Qt.Key_Escape:
            if self.add_fiducial_active:
                self.toggle_add_fiducial_mode()
        # check if shift key is pressed
        elif event.key() == Qt.Key_Shift:
            self.shift_key_active = 1  # apply change to the right image frame
        # handle image view key presses
        elif event.key() == Qt.Key_R:
            self.which_key_press = 1  # rotate image
        elif event.key() == Qt.Key_F:
            self.which_key_press = 2  # flip image
        elif event.key() == Qt.Key_D:
            self.which_key_press = 3  # return image to default view
        elif event.key() == Qt.Key_B:
            self.which_key_press = 4  # change brightness
        elif event.key() == Qt.Key_C:
            self.which_key_press = 5  # change contrast
        elif event.key() == Qt.Key_A:
            self.which_key_press = 6  # auto-adjust contrast
        elif event.key() == Qt.Key_S:
            self.which_key_press = 7  # save a screenshot of the app
        # define whether to increase or decrease brightness or contrast
        elif event.key() in {44, 60}:  # small decrease
            self.increase_decrease_brightness_contrast_key = 1
        elif event.key() in {46, 62}:  # small increase
            self.increase_decrease_brightness_contrast_key = 2
        elif event.key() == Qt.Key_K:  # large decrease
            self.increase_decrease_brightness_contrast_key = 3
        elif event.key() == Qt.Key_L:  # large increase
            self.increase_decrease_brightness_contrast_key = 4
        else:
            # Pass the event to the base class for default handling
            super().keyPressEvent(event)

        # set the action to apply to the left or right image frame
        if self.current_index != self.apply_to_data_tab:
            ff = [0, 1]
            self.edit_which_image = ff[self.shift_key_active]
        # call the correct function depending on which key was pressed
        if self.which_key_press == 1:
            self.rotate_label_ui()
        elif self.which_key_press == 2:
            self.flip_image_y()
        elif self.which_key_press == 3:
            self.reset_transformations()
        elif self.which_key_press == 4:  # brightness
            bb = [0, -5, 5, -20, 20]
            self.change_brightness(bb[self.increase_decrease_brightness_contrast_key])
        elif self.which_key_press == 5:  # contrast
            cc = [0, -0.05, 0.05, -5, 5]
            self.change_contrast(cc[self.increase_decrease_brightness_contrast_key])
        elif self.which_key_press == 6:
            self.auto_adjust_contrast()
        elif self.which_key_press == 7:
            self.save_screenshot()

    def load_image(self, image_path):
        """Loads an image file and converts it to an RGB pixmap object.
        Used in multiple tabs
        Args:
            image_path: folder and filename of the image to laod
        Returns:
            pixmap: the loaded image in pixmap form
            max_intensity: the maximum pixel intensity of the image
            mode_intensity_rgb: the mode pixel intensity of each of the r,g,b channels
        """
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # convert the image to 8-bit RGB
        if len(image.shape) == 2:
            # Grayscale image: Convert to RGB
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:
            # RGBA image: Convert to RGB
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        elif image.shape[2] == 3:
            # Convert BGR to RGB (OpenCV loads images in BGR format)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if image.dtype == np.uint16:
            image = (image / 65535.0 * 255).astype(np.uint8)
        elif image.dtype == np.float32 or image.dtype == np.float64:
            image = np.clip(image, 0, 1)  # Ensure values are in [0,1] before scaling
            image = (image * 255).astype(np.uint8)

        # calculate the maximum intensity of the image
        image_max_intensity = np.max(image)

        # calculate the mode intensity of each channel of the image
        r = mode(image[..., 0].flatten(), axis=None).mode
        g = mode(image[..., 1].flatten(), axis=None).mode
        b = mode(image[..., 2].flatten(), axis=None).mode
        mode_intensity_rgb = [r, g, b]

        # convert the image to a pixmap
        pixmap = self.array_to_pixmap(image)

        return pixmap, image_max_intensity, mode_intensity_rgb

    def save_screenshot(self):
        """Save a screenshot of the app in the pre-defined job folder when the user presses 's'.
        Used in multiple tabs
        Args:
            none, triggered when the user presses 's'
        Returns:
            No variables returned, a .png screenshot of the app will be saved in the job folder.
        """
        if self.job_folder == "":
            print("no screenshot for you")
            # return

        # Define the folder where screenshots will be saved
        folder = os.path.join(self.job_folder, self.results_name, "Screenshots")
        #folder = r'C:\Users\Ashley\Documents\sample data\HE\screenshots for paper'
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Grab a screenshot of the entire main window
        screenshot = self.grab()

        # Save the screenshot to the folder (you can change the filename as needed)
        now = datetime.now()
        filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        filename = os.path.join(folder, filename)
        screenshot.save(filename, "png")

    def resizeEvent(self, event):
        """Resizes the app contents dynamically given a change in the app window size.
        Used in multiple tabs
        Args:
            event: app rescaling action by user
        Returns:
            No variables returned, app contents will rescale.
        """
        # Get the new size of the main window
        new_size = event.size()

        # calculate scaling factors based on the new size of tabWidget
        if self.scaleCount == 0:
            num_children = len(self.ui.tabWidget.findChildren(QWidget))
            self.widget_dimensions = np.zeros((4, num_children + 1))
            self.widget_dimensions[0, 0] = self.width()
            self.widget_dimensions[1, 0] = self.height()
            self.original_width = new_size.width()
            self.original_height = new_size.height()
        scale_width = new_size.width() / self.original_width
        scale_height = new_size.height() / self.original_height

        self.padnum = self.ui.tabWidget.tabBar().sizeHint().height() # offset of the image view windows from the edge of the app

        # scale the main window proportionally
        self.resize(self.widget_dimensions[0, 0] * scale_width, self.widget_dimensions[1, 0] * scale_height)

        # make a list of all objects in the tab widget and keep only certain types of objects
        if self.scaleCount == 0:
            self.widgets_list = [
                self.ui.centralWidget,
                self.ui.tabWidget]
            # append children of self.ui.tabWidget with "Text" or "Button" in their name
            for child in self.ui.tabWidget.findChildren(QWidget):
                if any(sub in child.objectName() for sub in
                       ("Widget", "Tab", "Frame", "Text", "Button", "CheckBox", "ComboBox", "Image")):
                    if not "Name" in child.objectName():
                        self.widgets_list.append(child)

        # iterate over the selected child widgets of tabWidget and scale them
        for idx, child in enumerate(self.widgets_list):

            # document widget dimensions on the first scale event
            if self.scaleCount == 0:
                self.widget_dimensions[0, idx + 1] = child.width()  # Store width in row 0
                self.widget_dimensions[1, idx + 1] = child.height()  # Store height in row 1
                self.widget_dimensions[2, idx + 1] = child.x()  # top left x position
                self.widget_dimensions[3, idx + 1] = child.y()  # top left y position

            child_width = self.widget_dimensions[0, idx + 1] * scale_width
            child_height = self.widget_dimensions[1, idx + 1] * scale_height
            child.resize(int(child_width), int(child_height))

            # reposition the child widgets proportionally
            child_x = self.widget_dimensions[2, idx + 1] * scale_width
            child_y = self.widget_dimensions[3, idx + 1] * scale_height
            child.move(int(child_x), int(child_y))

        self.ui.DisableFrame_F1.setGeometry(self.ui.FiducialPointControlsFrame.geometry())
        self.ui.DisableFrame_O1.setGeometry(self.ui.ImageViewControlsFrame_O.geometry())
        self.ui.DisableFrame_E1.setGeometry(self.ui.ImageViewControlsFrame_E.geometry())
        self.ui.DisableFrame_E2.setGeometry(self.ui.ElasticRegistrationControlsFrame.geometry())
        self.ui.DisableFrame_C.setGeometry(self.ui.RegisterCoordinatesFrame.geometry())
        self.ui.DisableFrame_C_2.setGeometry(self.ui.CoordinatesOverlayControlsFrame.geometry())
        self.ui.DisableFrame_C_3.setGeometry(self.ui.ImageViewControlsFrame_C.geometry())
        self.ui.DisableFrame_I1.setGeometry(self.ui.ApplyToImageFrame.geometry())

        # document that we have scaled the app at least once
        self.scaleCount = self.scaleCount + 1
        self.update_both_images()
        super().resizeEvent(event)  # call the base class's resizeEvent

    def register_points_elastic(self, pts, szz, inverted_displacement_field, scale=None):
        """Applies the inverted nonlinear displacement field to an image to perform elastic registration
        Used in multiple tabs
        Args:
            pts: coordinate points (x, y) to apply the registration to
            szz: the size of the image that the coordinate points were extracted from
            inverted_displacement_field: inverse of the displacement field calculated during elastic registration
            scale: the scale between the points and the image that the elastic registration was calculated on
        Returns:
            pts_elastic: elastically registered points
        """
        if scale is None:
            scale = 1

        inverted_displacement_field_resized = resize(inverted_displacement_field, (szz[0], szz[1], 2),
                                                     preserve_range=True) * scale
        inverted_displacement_field_a = inverted_displacement_field_resized[:, :, 0]
        inverted_displacement_field_b = inverted_displacement_field_resized[:, :, 1]

        # get the nearest row and column for each point, and clip any indices that exceed the dimensions of the image
        pp = np.round(pts).astype(int)
        row_indices = np.clip(pp[:, 1] - 1, 0, inverted_displacement_field_a.shape[0] - 1)
        col_indices = np.clip(pp[:, 0] - 1, 0, inverted_displacement_field_a.shape[1] - 1)

        # Use advanced indexing to retrieve the displacement for each coordinate.
        pts_move = np.column_stack((
            inverted_displacement_field_a[row_indices, col_indices],
            inverted_displacement_field_b[row_indices, col_indices])
        )
        pts_elastic = pts + pts_move

        return pts_elastic

    def register_image_elastic(self, image, displacement_field, mode_vals=None, scale=None):
        """Applies the nonlinear displacement field to an image to perform elastic registration
        Used in multiple tabs
        Args:
            image: an image array to be registered
            displacement_field: a nonlinear dispacement field corresponding to image
            mode_vals: mode intensity of each rgb channel of the moving image
            scale: the scale between the image and the image that the elastic registration was calculated on

        Returns:
            image_elastic: elastically registered image
        """
        # rescale the transformation matrix
        displacement_field = cv2.resize(displacement_field, (image.shape[1], image.shape[0]),
                                        interpolation=cv2.INTER_LINEAR)
        if mode_vals is None:
            mode_vals = [241, 241, 241]

        if scale is not None and scale != 1:
            displacement_field = displacement_field * scale

        # Create the base coordinate grid
        base_x, base_y = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))

        # Convert the displacement map to absolute coordinates
        map_x = (base_x + displacement_field[..., 0]).astype(np.float32)
        map_y = (base_y + displacement_field[..., 1]).astype(np.float32)
        remapped_channels = [
            cv2.remap(channel, map_x, map_y, interpolation=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT,borderValue=float(mode_vals[i-1]))
            for i, channel in enumerate(cv2.split(image))
        ]
        image_elastic = cv2.merge(remapped_channels)
        image_elastic = cv2.cvtColor(image_elastic, cv2.COLOR_BGR2RGB)

        return image_elastic

    def debug_show_image(self, image, adapt_brightness=None):
        """plot the input image for debugging purposes.
        Used in multiple tabs
        Args:
            image: numpy array image to plot
            adapt_brightness: if given, scale color intensities to the min and max intensity of the array
        Returns:
            no variables output, but plots the image
        """

        if adapt_brightness is None:
            plt.imshow(image)
        else:
            plt.imshow(image, cmap='gray',
                       vmin=image.min(),
                       vmax=image.max())
            plt.colorbar()
        plt.axis("off")
        plt.show()

    def transform_image(self, pixmap, tform, flip_im, size_fixed_image, mode_vals, size_out=None):
        """Register an image using pixmap and other metadata inputs.
        Used in multiple tabs
        Args:
            pixmap: image to register in pixmap format
            tform: transformation matrix
            flip_im: logical input, flip image along vertical axis of not
            mode_vals: mode of each channel of the RGB pixmap
            size_fixed_image: size of image to pad the moving image to before registration
            size_out: (optional) pixel size of target registered image
        Returns:
            registered_pixmap: registered version of the input pixmap, also in pixmap format
        """
        if size_out is None:
            size_out = size_fixed_image

        if flip_im:
            transform = QTransform().scale(-1, 1)  # Horizontal flip
            pixmap = pixmap.transformed(transform, mode=Qt.SmoothTransformation)

        # Pad the image to the size of the fixed image
        width = max([size_fixed_image[0], pixmap.width()])
        height = max([size_fixed_image[1], pixmap.height()])
        array, array_g = self.pad_images(pixmap, width, height, mode_vals)

        # Apply the adjusted transformation and crop the image to the size of the fixed image
        fv1, fv2, fv3 = int(mode_vals[0]), int(mode_vals[1]), int(mode_vals[2])
        #transformed_array = cv2.warpAffine(array, tform[:2, :], szz, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=[fv1, fv2, fv3])
        transformed_array = cv2.warpAffine(array, tform[:2, :], size_out, flags=cv2.INTER_NEAREST,
            borderMode=cv2.BORDER_CONSTANT, borderValue=[fv1, fv2, fv3])
        if transformed_array.shape[1] > size_out[1] or transformed_array.shape[0] > size_out[0]:
            transformed_array = transformed_array[:size_out[1], :size_out[0]]
        transformed_array = np.ascontiguousarray(transformed_array)

        # Convert back to pixmap
        height = transformed_array.shape[1]
        width = transformed_array.shape[0]
        ss = transformed_array.strides[0]
        registered_image = QImage(transformed_array.data, height, width, ss, QImage.Format_RGB888)
        registered_pixmap = QPixmap.fromImage(registered_image)

        return registered_pixmap

    def browse_for_fixed_image(self):
        """Allows the user to select a file to serve as the fixed image for the job.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the first table of tab 1.
        """
        # if the fixed image is already defined, confirm that the user wants to replace it
        if self.fixed_image_filename:
            msg_box = QtWidgets.QMessageBox()  # Create a message box
            msg_box.setWindowTitle("Fixed Image Already Defined")  # Set the window title
            msg_box.setText("Would you like to Replace the Current Fixed Image?")  # Set the message text
            msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
            msg_box.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons

            # Apply custom stylesheet for background and font color
            msg_box.setStyleSheet(self.quest_box_style)

            # Show the message box and get the response
            response = msg_box.exec()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        # extract the filename selected by the user and update table 1 in the app
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Fixed Image File", "")
        if self.is_file_an_image(file_path):  # if a file is selected
            self.fixed_image_folder = os.path.normpath(os.path.dirname(file_path))  # Extract the folder
            self.fixed_image_filename = os.path.basename(file_path)  # Extract the filename

            # check if the scale factor is saved in the same folder
            csv_filename = os.path.splitext(self.fixed_image_filename)[0] + '.csv'
            csv_path = os.path.join(self.fixed_image_folder, csv_filename)
            if os.path.exists(csv_path):
                try:
                    with open(csv_path, "r") as f:
                        lines = f.readlines()
                    self.scale_fixed_image = lines[1].strip()
                except:
                    self.scale_fixed_image = ""
            self.populate_fixed_table()

    def browse_for_moving_image(self):
        """Allows the user to select a file to serve as the fixed image for the job.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the second table of tab 1.
        """
        # extract the filename selected by the user and update table 2 in the app
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select Moving Image Files", "")

        if file_paths:  # If a file is selected
            for file_path in file_paths:
                # file_path = os.path.join(self.pthMoving, self.nmMoving)
                if self.is_file_an_image(file_path):
                    self.moving_image_folder = os.path.normpath(os.path.dirname(file_path))  # Extract the folder
                    self.moving_image_filename = os.path.basename(file_path)  # Extract the filename

                    # check if the scale factor is saved in the same folder
                    csv_filename = os.path.splitext(self.moving_image_filename)[0] + '.csv'
                    csv_path = os.path.join(self.moving_image_folder, csv_filename)
                    if os.path.exists(csv_path):
                        try:
                            with open(csv_path, "r") as f:
                                lines = f.readlines()
                            self.scale_moving_image = lines[1].strip()
                        except:
                            self.scale_moving_image = ""
                    self.populate_moving_table()

                    if len(self.moving_images_list) == 0:
                        self.moving_images_list = np.array([[self.moving_image_filename, self.scale_moving_image, self.moving_image_folder]], dtype=object)
                    else:
                        add_to_list = np.array([self.moving_image_filename, self.scale_moving_image, self.moving_image_folder])
                        self.moving_images_list = np.vstack([self.moving_images_list, add_to_list])
                    self.populate_moving_table()

    def browse_for_job_folder(self):
        """Allows the user to select a folder to serve as the job folder.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the third table of tab 1.
        """
        # if the project folder is already defined, confirm that the user wants to replace it
        if self.job_folder:
            msg_box = QtWidgets.QMessageBox()  # Create a message box
            msg_box.setWindowTitle("Job Folder Already Defined")  # Set the window title
            msg_box.setText("Would you like to Replace the Current Job Folder?")  # Set the message text
            msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
            msg_box.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons

            # apply custom stylesheet for background and font color
            msg_box.setStyleSheet(self.quest_box_style)

            # show the message box and get the response
            response = msg_box.exec()
            if response == QtWidgets.QMessageBox.Cancel:
                return

        # extract the folder selected by the user and update table 3 in the app
        folder = QFileDialog.getExistingDirectory(self, "Select Job Folder", "")
        if folder:  # If a file is selected
            self.job_folder = os.path.normpath(folder)
            self.populate_project_table()

    def populate_fixed_table(self):
        """Populates the first table in the import project tab, where the fixed image folder,
           filename,  and scale are defined.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the first table of tab 1.
        """
        # Populate the first row with the variables' values
        self.ui.fixedImageTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{self.fixed_image_filename}  "))
        self.ui.fixedImageTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{self.fixed_image_folder}  "))

        # allow the user to set the job folder to the fixed image folder if the fixed image folder is defined
        if len(self.fixed_image_folder) > 0:
            self.ui.JobFolderCheckBox.setVisible(True)
        else:
            self.ui.JobFolderCheckBox.setVisible(False)

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_tables_are_complete_import_project_tab()
        if self.fixed_image_filename:
            self.ui.fixedImageTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def populate_moving_table(self):
        """Populates the second table in the import project tab, where the moving image folders, filenames,
           and scales are defined.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the second table of tab 1.
        """
        # set the number of rows in the table to the current number of moving images
        if len(self.moving_images_list) == 0:
            self.ui.movingImageTableWidget.setRowCount(0)
            return
        num_rows = self.moving_images_list.size / 3
        self.ui.movingImageTableWidget.setRowCount(num_rows)

        # populate the rows of the table with the info in movingIMS
        row_count = 0
        for row in self.moving_images_list:
            self.ui.movingImageTableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(f"{row[0]}  "))
            self.ui.movingImageTableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(f"{row[2]}  "))
            row_count += 1

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_tables_are_complete_import_project_tab()
        if self.moving_images_list.shape[0] > 0:
            self.ui.movingImageTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def populate_project_table(self):
        """populates the third table in the import project tab, where the job folder and results name are populated.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the third table of tab 1.
        """
        # update the results name and job folder in the table
        self.ui.setJobTableWidget.setRowCount(1)
        self.ui.setJobTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{self.results_name}  "))
        self.ui.setJobTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{self.job_folder}  "))

        # turn the frame green if all inputs are defined correctly
        self.check_if_tables_are_complete_import_project_tab()
        if self.results_name:
            self.ui.setJobTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def check_if_tables_are_complete_import_project_tab(self):
        """Determines whether the three tables in the import project tab are correctly filled.
           If so, allow the user to move on.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but tables updated as follows: blank tables colored grey, incorrect tables colored
            red, and correct tables colored green. If all tables are completed correctly, the navigate button will be
            enabled, allowing the user to advance through the app.
        """
        # is the fixed image table complete
        fixed_frame_done = int(len(self.fixed_image_filename) > 0) + int(len(self.fixed_image_folder) > 0)
        # is the job folder table complete
        job_frame_done = int(len(self.job_folder) > 0) + int(len(self.results_name) > 0)
        # is the moving image table complete
        moving_frame_done = 1  # complete
        if len(self.moving_images_list) == 0:
            moving_frame_done = 0  # not started

        # update the fixed image frame color based on the completion
        if fixed_frame_done == 2:  # fully complete = green
            self.ui.DefineFixedImageFrame.setStyleSheet("background-color: #375c46;")  # 3d4a3d
        else: # fixed_frame_done == 0:  # not started = grey
            self.ui.DefineFixedImageFrame.setStyleSheet("background-color: #4b4b4b;")

        # update the moving image frame color based on the completion
        if moving_frame_done == 1:  # fully complete = green
            self.ui.DefineMovingImageFrame.setStyleSheet("background-color: #375c46;")
        else: # moving_frame_done == 0:  # not started = grey
            self.ui.DefineMovingImageFrame.setStyleSheet("background-color: #4b4b4b;")

        # update the job folder frame color based on the completion
        if job_frame_done == 2:  # fully complete = green
            self.ui.SetJobFolderFrame.setStyleSheet("background-color: #375c46;")
            self.ui.JobFolderCheckBox.setStyleSheet("background-color: #375c46;")
            self.ui.JobFolderCheckBox.setStyleSheet("color: #e6e6e6;")
        else:  # not started = grey
            self.ui.SetJobFolderFrame.setStyleSheet("background-color: #4b4b4b;")
            self.ui.JobFolderCheckBox.setStyleSheet("background-color: #4b4b4b;")
            self.ui.JobFolderCheckBox.setStyleSheet("color: #e6e6e6;")

        # enable app navigation if all frames are completed
        if fixed_frame_done == 2 and job_frame_done == 2 and moving_frame_done == 1:
            self.close_navigation_tab()
            self.ui.NavigationButton.setEnabled(True)
            self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        else:
            self.close_navigation_tab()
            self.ui.NavigationButton.setEnabled(False)
            self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)

    def browse_for_template(self):
        """Open a file explorer dialog to choose a template file to load.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but updates the App view
        """
        # user brose for a .csv file. If a file is found, load it
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Template .csv File", "",
                                                             "Data Files (*.csv)")
        if file_path:
            self.load_template_info(file_path)

    def save_template_file(self):
        """Load the project definitions from a template.csv file selected by the user.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but save a 'template.csv' file in the user-defined job folder
        """
        # define the first 6 lines of the csv file
        line1 = ['', 'filename', 'scale factor', 'path']
        line2 = ['Fixed image', '', '', '']
        line3 = ['', self.fixed_image_filename, self.scale_fixed_image, self.fixed_image_folder]
        line4 = ['Output folder', '', '', '']
        line5 = ['', self.results_name, '', self.job_folder]
        line6 = ['Moving images', '', '', '']
        all_lines_concat = np.row_stack([line1, line2, line3, line4, line5, line6])

        # define lines 7 - end of the csv file (depends on the number of moving images
        for num in range(0, self.moving_images_list.shape[0]):
            tmp = ['', self.moving_images_list[num, 0], self.moving_images_list[num, 1],
                   self.moving_images_list[num, 2]]
            all_lines_concat = np.row_stack([all_lines_concat, tmp])

        # make sure the output folder exists
        output_folder = os.path.join(self.job_folder, self.results_name)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # save the file
        outfile = os.path.join(output_folder, "template.csv")
        np.savetxt(outfile, all_lines_concat, delimiter=",", fmt="%s")

    def load_template_info(self, file_path):
        """Load the project definitions from a template.csv file selected by the user.
        Used in tab 1 only
        Args:
            file_path: the folder and file name of the user-chosen .csv file
        Returns:
            no variables output, but will populate the three tables in the import project tab of the app
        """
        # Read the CSV file
        X = pd.read_csv(file_path, header=None).values

        # Get location and name of fixed image
        self.fixed_image_filename = X[2, 1]
        self.scale_fixed_image = X[2, 2]
        self.fixed_image_folder = os.path.normpath(X[2, 3])

        # correct for nan
        if pd.isna(self.scale_fixed_image):
            self.scale_fixed_image = ""

        # Get location of output folder
        self.results_name = X[4, 1]
        self.job_folder = os.path.normpath(X[4, 3])
        if not os.path.isdir(self.job_folder):
            os.makedirs(self.job_folder)

        # Get a list of all moving images
        self.moving_images_list = X[6:, [1, 2, 3]]
        self.moving_images_list[:, 2] = [os.path.normpath(p) for p in self.moving_images_list[:, 2]]
        self.moving_images_list = np.vectorize(self.replace_nan)(self.moving_images_list)

        self.populate_fixed_table()
        self.populate_moving_table()
        self.populate_project_table()

    def replace_nan(self, val):
        return "" if isinstance(val, float) and np.isnan(val) else val

    def default_model_name(self):
        """Set the initial text of the model_name text box to today's date.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but updates the App view
        """
        today = datetime.now()
        self.results_name = "Registration_results_" + today.strftime("%m_%d_%Y")

    def doubleclick_fixed_table(self, row, column):
        """Enable editing of the fixed image variables in table 1
        Used in tab 1 only
        Args:
            row: row of the table that the user double-clicked on
            column: column of the table that the user double-clicked on
        Returns:
            no variables output, but allows the user to edit the fixed image parameters
        """

        # if the table is populated and table edit mode is not already active
        if len(self.fixed_image_filename) > 0 and self.edit_table_active == 0:
            # turn on edit table mode
            self.edit_table_active = 1  # fixed image
            self.enter_edit_table()

            # make delete visible
            self.ui.keepFixedImageButton.setVisible(True)
            self.ui.deleteFixedImageButton.setVisible(True)

    def doubleclick_moving_table(self, row, column):
        """Enable editing of the moving image variables in table 2
        Used in tab 1 only
        Args:
            row: row of the table that the user double-clicked on
            column: column of the table that the user double-clicked on
        Returns:
            no variables output, but allows the user to edit the moving image parameters
        """

        # if the table is populated and table edit mode is not already active
        if len(self.moving_images_list) > 0 and self.edit_table_active == 0:

            # turn on edit table mode
            self.edit_table_active = 2  # moving image
            self.enter_edit_table()
            self.num_moving_delete = row

            # make delete visible
            self.ui.keepMovingImageButton.setVisible(True)
            self.ui.deleteMovingImageButton.setVisible(True)

    def doubleclick_job_table(self, row, column):
        """Enable editing of the define job name in the first table in tab one
        Used in tab 1 only
        Args:
            row: row of the table that the user double-clicked on
            column: column of the table that the user double-clicked on
        Returns:
            no variables output, but allows the user to input a new job name
        """

        # if table edit mode is not already active
        if self.edit_table_active == 0:

            # if editing the job name
            if column == 0:
                item = self.ui.setJobTableWidget.item(row, column)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Enable editing
                    self.ui.setJobTableWidget.editItem(item)  # Put the cell into edit mode

    def handle_value_update_job(self, new_value, row, column):
        """Make sure that the folder name input by the user is valid.
        Used in tab 1 only
        Args:
            new_value: new value input by the user for this cell of the table
            row: row of the table that the user double-clicked on
            column: column of the table that the user double-clicked on
        Returns:
            no variables output, but confirms the validity of the job name before updating the table
        """

        # exit unless the user edited the job name
        if column != 0:
            return

        # check the length, letters present, and reserved folder names
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
            self.results_name = new_value.strip()
        self.populate_project_table()

    def enter_edit_table(self):
        """Updates the table view settings for all tables in tab 1 when entering edit table mode.
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the first and second tables of tab 1
        """

        # app-wide buttons
        self.close_navigation_tab()
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)

        # disable some buttons
        if self.edit_table_active == 5:
            self.ui.chooseImageFileButton.setEnabled(False)
            self.ui.RegisterImageButton.setVisible(False)
            if self.num_image_column == 0: # keep vs delete
                self.ui.KeepApplyToImageButton.setVisible(True)
                self.ui.DeleteApplyToImageButton.setVisible(True)
        else:
            self.ui.setJobTableWidget.setEnabled(False)
            self.ui.chooseFixedImageButton.setEnabled(False)
            self.ui.chooseMovingImageButton.setEnabled(False)
            self.ui.loadTemplateButton.setEnabled(False)
            if self.edit_table_active == 1:
                self.ui.DefineMovingImageFrame.setEnabled(False)
            elif self.edit_table_active == 2:
                self.ui.DefineFixedImageFrame.setEnabled(False)

    def exit_edit_table(self):
        """Updates the table view settings for all tables in tab 1 when exiting edit table mode
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the first and second tables of tab 1
        """

        # app-wide buttons
        if self.current_index != 0:
            self.ui.NavigationButton.setEnabled(True)
            self.ui.NavigationButton.setStyleSheet(self.active_button_style)
            self.ui.KeyboardShortcutsButton.setEnabled(True)
            self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)

        if self.edit_table_active == 5:
            self.ui.chooseImageFileButton.setEnabled(True)
            if self.num_image_column == 0:  # keep vs delete
                self.ui.KeepApplyToImageButton.setVisible(False)
                self.ui.DeleteApplyToImageButton.setVisible(False)
            self.populate_image_table()
        else:
            # make disabled buttons enabled again
            self.ui.DefineFixedImageFrame.setEnabled(True)
            self.ui.DefineMovingImageFrame.setEnabled(True)
            self.ui.setJobTableWidget.setEnabled(True)
            self.ui.chooseFixedImageButton.setEnabled(True)
            self.ui.chooseMovingImageButton.setEnabled(True)
            self.ui.loadTemplateButton.setEnabled(True)

            # make the keep and delete buttons invisible
            self.ui.keepFixedImageButton.setVisible(False)
            self.ui.deleteFixedImageButton.setVisible(False)
            self.ui.keepMovingImageButton.setVisible(False)
            self.ui.deleteMovingImageButton.setVisible(False)

        # turn off edit table active
        self.edit_table_active = 0

    def keep_fixed_image(self):
        """Exits edit table mode without removing the fixed image
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the second table of tab 1
        """

        # update the table view
        self.exit_edit_table()

    def delete_fixed_image(self):
        """Removes the fixed image, updates the table, and exits edit table mode
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the first table of tab 1
        """

        # delete the body of the table
        self.fixed_image_filename = ""
        self.fixed_image_folder = ""
        self.scale_fixed_image = ""
        # update the table view and remove the job folder if it was set to the fixed image folder
        self.populate_fixed_table()
        if self.ui.JobFolderCheckBox.isChecked():
            self.ui.JobFolderCheckBox.setChecked(False)
            self.job_folder = ""
            self.populate_project_table()
        self.exit_edit_table()

    def keep_apply_to_image(self):
        """Exits edit table mode without removing the selected moving image
        Used in tab 7 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the second table of tab 1
        """

        # update the table view
        self.exit_edit_table()

    def delete_apply_to_image(self):
        """Removes the desired moving image, updates the list of moving images,
           updates the table, and exits edit table mode
        Used in tab 7 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the second table of tab 1
        """

        # remove the selected image from the table
        self.images_to_register_list = np.delete(self.images_to_register_list, self.num_image_row , axis=0)

        # update the table view
        self.populate_image_table()
        self.exit_edit_table()

    def keep_moving_image(self):
        """Exits edit table mode without removing the selected moving image
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the second table of tab 1
        """

        # update the table view
        self.exit_edit_table()

    def delete_moving_image(self):
        """Removes the desired moving image, updates the list of moving images,
           updates the table, and exits edit table mode
        Used in tab 1 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the second table of tab 1
        """

        # remove the selected image from the table
        self.moving_images_list = np.delete(self.moving_images_list, self.num_moving_delete, axis=0)

        # update the table view
        self.populate_moving_table()
        self.exit_edit_table()

    def job_folder_checkbox_changed(self, state):
        """Updates the job folder table in tab one based on the checkbox state.
        Used in tab 1 only
        Args:
            state: state of the corresponding textbox
        Returns:
            no variables output, but will update the job folder in the third table of tab 1
        """
        # set the job folder to the fixed image folder
        if state > 0:
            self.job_folder = self.fixed_image_folder
        # wipe the current job folder so the user can choose a new folder
        else:
            self.job_folder = ""
        self.populate_project_table()

    def find_closest_row(self, pts, clicked_x, clicked_y):
        """When deleting a fiducial point pair, determine the closest point to the place the user clicked in the frame.
        Used in tab 2 only
        Args:
            pts: current fiducial point pairs
            clicked_x: location in x clicked by the user
            clicked_y: location in y clicked by the user
        Returns:
            closest_index: row inside pts containing the nearest point
            target_pts: points nearest the clicked coordinate
        """
        # Ensure pts is a NumPy array with float data type
        pts = np.asarray(pts, dtype=np.float64)

        # Calculate the Euclidean distance to (image_x, image_y) for all rows in pts
        distances = np.sqrt((pts[:, 0] - clicked_x) ** 2 + (pts[:, 1] - clicked_y) ** 2)
        closest_index = np.argmin(distances)  # Index of the row with the minimum distance
        target_pts = pts[closest_index]

        return closest_index, target_pts

    def highlight_current_frame(self):
        """Highlight the currently active image frame when add fiducial mode is active.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but calculates the elastic registration and updates tab 6 view
        """
        # highlight the frame to add a fiducial point to
        if self.add_fiducial_active:
            self.edit_which_image = self.edit_which_fid
            self.define_edit_frame()
            if self.edit_which_image == 0:  # left image
                self.border_left.setStyleSheet(self.active_label_style)
                tmp = self.frame_left.geometry()
                self.border_left.setGeometry(tmp.x() - 5, tmp.y() - 5, tmp.width() + 10, tmp.height() + 10)
                self.text_left.setStyleSheet(self.active_text_label_style)
                self.frame_left.setStyleSheet(self.active_frame_style)

                self.border_right.setStyleSheet(self.inactive_label_style)
                tmp = self.frame_right.geometry()
                self.border_right.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
                self.text_right.setStyleSheet(self.inactive_text_label_style)
                self.frame_right.setStyleSheet(self.inactive_frame_style)
            else:  # right image
                self.border_left.setStyleSheet(self.inactive_label_style)
                tmp = self.frame_left.geometry()
                self.border_left.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
                self.text_left.setStyleSheet(self.inactive_text_label_style)
                self.frame_left.setStyleSheet(self.inactive_frame_style)

                self.border_right.setStyleSheet(self.active_label_style)
                tmp = self.frame_right.geometry()
                self.border_right.setGeometry(tmp.x() - 5, tmp.y() - 5, tmp.width() + 10, tmp.height() + 10)
                self.text_right.setStyleSheet(self.active_text_label_style)
                self.frame_right.setStyleSheet(self.active_frame_style)
        # make sure neither frame is highlighted
        else:
            self.define_edit_frame()
            self.border_left.setStyleSheet(self.inactive_label_style)
            self.text_left.setStyleSheet(self.inactive_text_label_style)
            self.frame_left.setStyleSheet(self.inactive_frame_style)
            tmp = self.frame_left.geometry()
            self.border_left.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
            self.border_right.setStyleSheet(self.inactive_label_style)
            self.text_right.setStyleSheet(self.inactive_text_label_style)
            self.frame_right.setStyleSheet(self.inactive_frame_style)
            tmp = self.frame_right.geometry()
            self.border_right.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)

    def save_pts_to_csv(self):

        combined = np.hstack((self.pts_moving, self.pts_fixed))  # shape [N x 4]
        columns = ['moving_x', 'moving_y', 'fixed_x', 'fixed_y']
        df = pd.DataFrame(combined, columns=columns)
        df = df.iloc[1:]

        folder = r'\\10.99.134.183\kiemen-lab-data\admin\papers\fiducial point registration\final data\OHSU data\PIVOT_validation_points\coordinates'
        base_name = os.path.splitext(self.moving_image_filename)[0]
        csv_filename = f"{base_name}.csv"
        csv_path = os.path.join(folder, csv_filename)

        # Save the CSV
        df.to_csv(csv_path, index=False)

    def toggle_add_fiducial_mode(self):
        """Toggle fiducial selection mode to enable or disable adding points.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """

        #self.save_pts_to_csv()
        if self.current_index != self.fiducials_tab:
            return
        self.add_fiducial_active = not self.add_fiducial_active

        if self.delete_mode_active:
            self.delete_mode_active = False

        if self.add_fiducial_active:
            self.ui.AddFiducialButton.setText("Quit")

            # start by selecting a point on the fixed image
            self.edit_which_image = 0
            self.edit_which_fid = 0
            self.highlight_current_frame()
            crosshair_cursor = self.create_large_crosshair_cursor()
            self.setCursor(crosshair_cursor)
        else:
            # Reset the cursor to default
            self.ui.AddFiducialButton.setText("Add")
            self.setCursor(Qt.ArrowCursor)

            # remove point from fixed image list if necessary
            if self.edit_which_fid == 1:  # moving image
                self.pts_fixed = np.delete(self.pts_fixed, -1, axis=0)
                self.edit_which_image = 0
                self.highlight_current_frame()
                self.update_image_view()

    def closeEvent(self, event):
        """Change the cursor back from a crosshair when exiting fiducial selection mode.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # Reset the cursor to default before closing
        self.setCursor(Qt.ArrowCursor)
        super().closeEvent(event)

    def create_large_crosshair_cursor(self):
        """Change the cursor to a crosshair to indicate the app is in fiducial selection mode.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # Create a larger pixmap for the crosshair
        pixmap_size = 512  # Increase the size of the pixmap
        pixmap = QPixmap(pixmap_size, pixmap_size)
        pixmap.fill(Qt.transparent)  # Transparent background

        # Extract RGB values from self.ptColor
        r, g, b = self.pts_color_fiducial_tab.red(), self.pts_color_fiducial_tab.green(), self.pts_color_fiducial_tab.blue()
        ff = 0.6
        crosshair_color = QColor(int(r * ff), int(g * ff), int(b * ff))

        # Draw the extended crosshair
        painter = QPainter(pixmap)
        pen = QPen(crosshair_color)  # set the color to match the fiducial points
        pen.setWidth(2)  # Set the thickness (e.g., 5px)
        painter.setPen(pen)

        # Vertical line
        painter.drawLine(pixmap_size // 2, 0, pixmap_size // 2, pixmap_size)
        # Horizontal line
        painter.drawLine(0, pixmap_size // 2, pixmap_size, pixmap_size // 2)
        painter.end()

        # Set the center of the crosshair to the hotspot
        return QCursor(pixmap, pixmap_size // 2, pixmap_size // 2)

    def delete_fiducials(self):
        """Determine whether the user wants to delete one or all fiducial pairs.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # Exit fiducial and zoom / pan mode if necessary
        if self.add_fiducial_active:
            self.toggle_add_fiducial_mode()

        # create a pop-up message box and get the users response
        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("Delete fiducial pairs?")  # Set the window title
        msg_box.setText("Would you like to delete one point or all points?")  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        delete_one_button = msg_box.addButton("Delete One", QtWidgets.QMessageBox.ActionRole)
        delete_all_button = msg_box.addButton("Delete All", QtWidgets.QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QtWidgets.QMessageBox.Cancel)
        msg_box.setStyleSheet(self.quest_box_style)
        response = msg_box.exec()

        # Handle the response
        if msg_box.clickedButton() == delete_one_button:
            self.delete_one_point()
        elif msg_box.clickedButton() == delete_all_button:
            self.delete_all_points()
        elif response == cancel_button:
            return

    def delete_one_point(self):
        """Enables the user to click on an image to identify a fiducial point to delete.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        # set labels to inactive
        self.ui.FixedImageBorder.setStyleSheet(self.inactive_label_style)
        self.ui.FixedImageFrameHeaderText.setStyleSheet(self.inactive_text_label_style)
        self.ui.FixedImageDisplayFrame.setStyleSheet(self.inactive_frame_style)
        tmp = self.ui.FixedImageDisplayFrame.geometry()
        self.ui.FixedImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
        self.ui.MovingImageBorder.setStyleSheet(self.inactive_label_style)
        self.ui.MovingImageFrameHeaderText.setStyleSheet(self.inactive_text_label_style)
        self.ui.MovingImageDisplayFrame.setStyleSheet(self.inactive_frame_style)
        tmp = self.ui.MovingImageDisplayFrame.geometry()
        self.ui.MovingImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)

        # set cursor to active
        self.delete_mode_active = True
        crosshair_cursor = self.create_large_crosshair_cursor()
        self.setCursor(crosshair_cursor)

    def delete_all_points(self):
        """Enables the user to delete all fiducial points.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("Confirm deletion")  # Set the window title
        msg_box.setText("Are you sure you want to delete ALL fiducial points?")  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        msg_box.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons
        msg_box.setStyleSheet(self.quest_box_style)

        # Show the message box and get the response
        response = msg_box.exec()
        if response == QtWidgets.QMessageBox.Cancel:
            return
        else:
            self.pts_fixed = np.array([[0, 0]], dtype=np.float64)
            self.pts_moving = np.array([[0, 0]], dtype=np.float64)
            self.update_both_images()

    def call_change_fiducial_color0(self):
        """Lets the user change the color of the first set of the fiducial pairs.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.edit_which_pt_color = 0  # color 1
        self.change_fiducial_color()

    def call_change_fiducial_color1(self):
        """Lets the user change the color of the second set of the fiducial pairs.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but app view changes
        """
        self.edit_which_pt_color = 1  # color 2
        self.change_fiducial_color()

    def handle_fiducial_click(self, x, y, event):
        """Either appends a fiducial point to the list or deletes a point, depending on active mode.
        Used in tab 2 only
        Args:
            x: x coordinate clicked on the image
            y: y coordinate clickedo n the image
            event: mouse click event
        Returns:
            no variables output, but app view changes
        """
        if self.add_fiducial_active:
            self.edit_which_image = self.edit_which_fid
            if self.edit_which_image == 0:  # Fixed image
                zz = self.fixed_zoom_scale / self.fixed_zoom_default
                image_W = self.im_fixed.width()  # width of image in pixels
                image_H = self.im_fixed.height()  # height of image in pixels
                frame_size_W = self.ui.FixedImageDisplayFrame.width()  # round(image_W / scale)
                frame_size_H = self.ui.FixedImageDisplayFrame.height()  # round(image_H / scale)
                flip = self.fixed_flip_state
                ang = self.fixed_rotation_angle
            else:  # Moving image
                zz = self.moving_zoom_scale / self.moving_zoom_default
                image_W = self.im_moving.width()  # width of image in pixels
                image_H = self.im_moving.height()  # height of image in pixels
                frame_size_W = self.ui.MovingImageDisplayFrame.width()  # round(image_W / scale)
                frame_size_H = self.ui.MovingImageDisplayFrame.height()  # round(image_H / scale)
                flip = self.moving_flip_state
                ang = self.moving_rotation_angle

            # remove the effect of zoom, then rescale x and y from label space to image space
            scale = max(
                [image_H / frame_size_H, image_W / frame_size_W, frame_size_W / image_W, frame_size_H / image_H])
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
            if self.edit_which_image == 0:  # Fixed image
                self.pts_fixed = np.vstack([self.pts_fixed, add_to_list])
            else:  # Moving image
                self.pts_moving = np.vstack([self.pts_moving, add_to_list])

            # plot
            self.update_image_view()

            # take the next step
            self.edit_which_fid = not self.edit_which_fid
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
                    self.edit_which_image = 0
            elif in_right_x and in_right_y:
                if self.current_index != self.apply_to_data_tab:
                    self.edit_which_image = 1
            else:
                return

            if in_left_x and in_left_y:
                image_type = 0  # fixed image
                zz = self.fixed_zoom_scale / self.fixed_zoom_default
                image_W = self.im_fixed.width()  # width of image in pixels
                image_H = self.im_fixed.height()  # height of image in pixels
                frame_size_W = self.ui.FixedImageDisplayFrame.width()  # round(image_W / scale)
                frame_size_H = self.ui.FixedImageDisplayFrame.height()  # round(image_H / scale)
                flip = self.fixed_flip_state
                ang = self.fixed_rotation_angle
                local_pos = self.fixed_image_label.mapFromGlobal(event.globalPosition().toPoint())
                x = local_pos.x()
                y = local_pos.y()
                pts = self.pts_fixed
            elif in_right_x and in_right_y:
                image_type = 1  # moving image
                zz = self.moving_zoom_scale / self.moving_zoom_default
                image_W = self.im_moving.width()  # width of image in pixels
                image_H = self.im_moving.height()  # height of image in pixels
                frame_size_W = self.ui.MovingImageDisplayFrame.width()  # round(image_W / scale)
                frame_size_H = self.ui.MovingImageDisplayFrame.height()  # round(image_H / scale)
                flip = self.moving_flip_state
                ang = self.moving_rotation_angle
                local_pos = self.moving_image_label.mapFromGlobal(event.globalPosition().toPoint())
                x = local_pos.x()
                y = local_pos.y()
                pts = self.pts_moving
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
            scale = max(
                [image_H / frame_size_H, image_W / frame_size_W, frame_size_W / image_W, frame_size_H / image_H])
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
            msg_box.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons
            msg_box.setStyleSheet(self.quest_box_style)

            # Show the message box and get the response
            response = msg_box.exec()
            if response == QtWidgets.QMessageBox.Yes:
                # remove the selected fiducial then return to normal mode
                self.pts_fixed = np.delete(self.pts_fixed, self.potential_deletion + 1, axis=0)
                self.pts_moving = np.delete(self.pts_moving, self.potential_deletion + 1, axis=0)

            # delete the point or keep it, then replot the images
            self.potential_deletion = -5
            self.update_both_images()
            self.setCursor(Qt.ArrowCursor)
            self.delete_mode_active = False

    def populate_moving_images_combo_box(self):
        """Populate the tab 2 combobox with filenames present in the moving_images_list variable
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, the moving image view settings will be saved in a .pkl file
        """

        # Clear the current items in the combo box
        self.ui.MovingImagesComboBox.clear()
        self.ui.OldMovingImagesComboBox.clear()

        # initialize the combo box list
        self.ui.MovingImagesComboBox.addItem("Select")
        self.ui.OldMovingImagesComboBox.addItem("Select")
        self.num_moving_delete = [[], []]

        # add items from column 1 of self.moving_images_list
        for index, row in enumerate(self.moving_images_list):
            if len(row) > 1:  # Ensure the row has at least two columns
                # filename, _ = os.path.splitext(row[0]) # Get the filename from column 1
                # filename = filename + ".pkl"
                filename = row[0]
                datafile = os.path.splitext(filename)[0] + '.pkl'
                filepath = os.path.join(self.job_folder, self.results_name, "Registration transforms", datafile)

                if os.path.isfile(filepath): # Check if the file exists
                    self.ui.OldMovingImagesComboBox.addItem(filename)  # Add to OldMovingImagesComboBox
                    self.num_moving_delete[0].append(index)
                else:
                    self.ui.MovingImagesComboBox.addItem(filename)  # Add to MovingImagesComboBox
                    self.num_moving_delete[1].append(index)

    def new_combobox_selection_changed(self):
        """Enable loading of the selected, unregistered moving image.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, the moving image view settings will be saved in a .pkl file
        """

        # enable loading of the selected image
        if self.ui.MovingImagesComboBox.currentText() == "Select":
            self.ui.LoadNewMovingImageButton.setEnabled(False)
            self.ui.LoadNewMovingImageButton.setStyleSheet(self.inactive_button_style)
        else:
            self.ui.OldMovingImagesComboBox.setCurrentIndex(0)
            self.ui.LoadOldMovingImageButton.setEnabled(False)
            self.ui.LoadOldMovingImageButton.setStyleSheet(self.inactive_button_style)

            self.ui.LoadNewMovingImageButton.setEnabled(True)
            self.ui.LoadNewMovingImageButton.setStyleSheet(self.active_button_style)

    def old_combobox_selection_changed(self):
        """Enable loading of the selected, already registered moving image.
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, the moving image view settings will be saved in a .pkl file
        """

        # enable loading of the selected image
        if self.ui.OldMovingImagesComboBox.currentText() == "Select":
            self.ui.LoadOldMovingImageButton.setEnabled(False)
            self.ui.LoadOldMovingImageButton.setStyleSheet(self.inactive_button_style)
        else:
            self.ui.MovingImagesComboBox.setCurrentIndex(0)
            self.ui.LoadNewMovingImageButton.setStyleSheet(self.inactive_button_style)

            self.ui.LoadOldMovingImageButton.setEnabled(True)
            self.ui.LoadOldMovingImageButton.setStyleSheet(self.active_button_style)

    def load_new_moving_image(self):
        """Extract the information about the moving image to load for a non-registered image
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, the moving image view settings will be saved in a .pkl file
        """
        # get the current filename and index from the droplist
        current_index_in_table = self.ui.MovingImagesComboBox.currentIndex()
        row = self.num_moving_delete[1]
        row = row[current_index_in_table - 1]

        # define the moving image parameters
        self.moving_image_filename = self.moving_images_list[row][0]
        self.scale_moving_image = self.moving_images_list[row][1]
        self.moving_image_folder = self.moving_images_list[row][2]
        file_path = os.path.join(self.moving_image_folder, self.moving_image_filename)
        self.import_moving_image(file_path)

    def load_old_moving_image(self):
        """extract the information about the moving image to load for an image that was already registered
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, the moving image view settings will be saved in a .pkl file
        """
        # get the current filename and index from the droplist
        current_index_in_table = self.ui.OldMovingImagesComboBox.currentIndex()
        row = self.num_moving_delete[0]
        row = row[current_index_in_table - 1]

        # define the moving image parameters
        self.moving_image_filename = self.moving_images_list[row][0]
        self.scale_moving_image = self.moving_images_list[row][1]
        self.moving_image_folder = self.moving_images_list[row][2]
        file_path = os.path.join(self.moving_image_folder, self.moving_image_filename)
        self.import_moving_image(file_path)

    def import_moving_image(self, file_path):
        """Load the previous image view settings when loading a new moving image
        Used in tab 2 only
        Args:
            file_path: folder and filename of the moving image
        Returns:
            no variables output, the moving image will be loaded into memory
        """

        # load the image
        if not os.path.exists(file_path):
            print(f"Image file not found: {file_path}")
            return
        self.im_moving, self.max_intensity_moving, self.mode_intensity_moving = self.load_image(file_path)  # store the original pixmap

        # check if saved fiducial points exist
        filename, _ = os.path.splitext(self.moving_image_filename)  # Get the filename from column 1
        filename = filename + ".pkl"
        output_folder = os.path.join(self.job_folder, self.results_name, "Fiducial point selection")
        output_file = os.path.join(output_folder, filename)
        if os.path.exists(output_file):
            self.load_previous_settings(output_file)
            self.update_both_images()
        else:
            # Calculate zoom_default
            width_scale = self.ui.MovingImageDisplayFrame.width() / self.im_moving.width()
            height_scale = self.ui.MovingImageDisplayFrame.height() / self.im_moving.height()
            self.moving_zoom_default = min(width_scale, height_scale)

            self.edit_which_image = 0
            self.reset_transformations(0)
            self.edit_which_image = 1
            self.reset_transformations()

        # display image
        self.update_button_color()

        # change some view settings
        self.ui.ChooseMovingImageFrame.setVisible(False)
        self.ui.FiducialPointControlsFrame.setVisible(True)
        self.ui.PickNewMovingImageButton.setVisible(True)

    def save_fiducial_state(self):
        """Save the current moving image view settings so they can be reloaded later
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, the moving image view settings will be saved in a .pkl file
        """
        self.define_edit_frame()
        if self.current_index == self.fiducials_tab and self.pts_fixed.shape[0] > 1:
            # save fiducial info
            filename, _ = os.path.splitext(self.moving_image_filename)  # Get the filename from column 1
            filename = filename + ".pkl"
            output_folder = os.path.join(self.job_folder, self.results_name, "Fiducial point selection")
            output_file = os.path.join(output_folder, filename)

            # check if the folder exists, and create it if it doesn't
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # save variables to the pkl file
            with open(output_file, 'wb') as file:
                pickle.dump({'panx_F': self.fixed_pan_offset_x,
                             'pany_F': self.fixed_pan_offset_y,
                             'rot_F': self.fixed_rotation_angle,
                             'flip_F': self.fixed_flip_state,
                             'zoom_F': self.fixed_zoom_scale,
                             'zoom0_F': self.fixed_zoom_default,
                             'con_F': self.fixed_contrast,
                             'bri_F': self.fixed_brightness,
                             'panx_M': self.moving_pan_offset_x,
                             'pany_M': self.moving_pan_offset_y,
                             'rot_M': self.moving_rotation_angle,
                             'flip_M': self.moving_flip_state,
                             'zoom_M': self.moving_zoom_scale,
                             'zoom0_M': self.moving_zoom_default,
                             'con_M': self.moving_contrast,
                             'bri_M': self.moving_brightness,
                             'pts_F': self.pts_fixed,
                             'pts_M': self.pts_moving,
                             'pts_size': self.pts_size_fiducial_tab,
                             'pts_color': self.pts_color_fiducial_tab,
                             }, file)

    def load_previous_settings(self, file_path):
        """Load the previous image view settings when loading a new moving image
        Used in tab 2 only
        Args:
            file_path: folder and filename of .pkl file containing the image view settings
        Returns:
            no variables output, the view settings for the current moving image will be loaded
        """
        with open(file_path, 'rb') as file:
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

        self.pts_fixed = data.get('pts_F')
        self.pts_moving = data.get('pts_M')
        self.pts_size_fiducial_tab = data.get('pts_size')
        self.pts_color_fiducial_tab = data.get('pts_color')

    def confirm_load_new_image(self):
        """Create a pop-up window to confirm that the user wishes to  open a new moving image
        Used in tab 2 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update view of tab 2
        """

        # turn off fiducial mode if it's active
        if self.add_fiducial_active:
            self.toggle_add_fiducial_mode()

        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("Load a new moving image?")  # Set the window title
        msg_box.setText(
            "Are you sure you want to load a new image? (the current fiducials will be saved)")  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        msg_box.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons

        # Apply custom stylesheet for background and font color
        msg_box.setStyleSheet(self.quest_box_style)

        # Show the message box and get the response
        response = msg_box.exec()
        if response == QtWidgets.QMessageBox.Cancel:
            return

        # save the fiducial points
        self.save_fiducial_state()
        self.initiate_fiducials_tab()

    def browse_for_image_to_register(self):
        """Allows the user to select a file to serve as the fixed image for the job.
        Used in tab 7 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but will update the second table of tab 7.
        """
        # extract the filename selected by the user and update table 2 in the app
        open_to = os.path.join(self.job_folder, self.results_name)
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select an image to register",
                                                             open_to, "All Files (*.*)")

        if not self.is_file_an_image(file_path):
            return

        if file_path:  # If a file is selected
            image_file_folder = os.path.normpath(os.path.dirname(file_path))  # Extract the folder
            image_filename = os.path.basename(file_path)  # Extract the filename
            emp = ""
            # file_path = os.path.join(self.pthMoving, self.nmMoving)
            if self.is_file_an_image(file_path):
                if len(self.images_to_register_list) == 0:
                    self.images_to_register_list = np.array([[image_filename, image_file_folder, emp, emp, emp, emp]], dtype=object)
                else:
                    add_to_list = np.array([image_filename, image_file_folder, emp, emp, emp, emp])
                    self.images_to_register_list = np.vstack([self.images_to_register_list, add_to_list])
                self.populate_image_table()

    def browse_for_coordinates_file(self):
        """Let the user browse for a .csv coordinates file.
        Used in tab 3
        Args:
            none, draws from self
        Returns:
            no variables output, but App view changes.
        """

        open_to = os.path.join(self.job_folder, self.results_name)
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select .csv or .xlsx file containing coordinates",
                                                             open_to, "Data Files (*.csv *.xlsx);;All Files (*)")
        if not file_path:
            return

        self.coordinates_file_folder = os.path.normpath(os.path.dirname(file_path))  # Extract the folder
        self.coordinates_filename = os.path.basename(file_path)  # Extract the filename
        self.column_in_coords_file_containing_x_values = ""
        self.column_in_coords_file_containing_y_values = ""

        # automatically load the scale factor if this is a visium file
        try:
            self.load_visium_scale()
        except:
            self.json_scale = 1

        self.populate_coordinates_table()

    def load_visium_scale(self):
        """If the coordinates file is for visium, load the scale factor automatically.
        Used in tab 3 only
        Args:
            none, draws from self
        Returns:
            no variables output, but the coordinate scale factor may change.
        """

        coords_filename = os.path.basename(self.coordinates_filename)
        if 'tissue_positions' in coords_filename:

            scalefactors_path = os.path.join(self.coordinates_file_folder, 'scalefactors_json.json')
            if os.path.exists(scalefactors_path):
                # load JSON data
                with open(scalefactors_path, 'r') as f:
                    scalefactors = json.load(f)

                # Determine the image filename and assign the correct scale
                moving_img_name = os.path.basename(self.moving_image_filename_corresponding_to_coordinates)
                if 'tissue_hires_image' in moving_img_name:
                    self.json_scale = scalefactors.get('tissue_hires_scalef', "")
                    current_index_in_table = self.ui.CorrespondingImageComboBox.currentIndex()
                    row_number = self.which_moving_images_are_registered[0]
                    row_number = row_number[current_index_in_table - 1]
                    if self.moving_images_list[row_number][1] == '':
                        num = 1
                    else:
                        num = float(self.moving_images_list[row_number][1])
                    scaled_value = num * self.json_scale
                    self.scale_coordinates_file = str(scaled_value)
                elif 'tissue_lowres_image' in moving_img_name:
                    self.json_scale = scalefactors.get('tissue_lowres_scalef', "")
                    current_index_in_table = self.ui.CorrespondingImageComboBox.currentIndex()
                    row_number = self.which_moving_images_are_registered[0]
                    row_number = row_number[current_index_in_table - 1]
                    if self.moving_images_list[row_number][1] == '':
                        num = 1
                    else:
                        num = float(self.moving_images_list[row_number][1])
                    scaled_value = num * self.json_scale
                    self.scale_coordinates_file = str(scaled_value)

    def unregistered_coords_checkbox_changed(self, state):
        """Handle the unregistered image checkbox state change.
        Used in tab 3 only
        Args:
            state: current state of the checkbox
        Returns:
            no variables output, but App view changes.
        """
        if state > 0:
            self.all_images_checked += 1
        else:
            self.all_images_checked -= 1

        if self.all_images_checked == 4:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(True)
            self.ui.SaveRegisteredECoordinatesButton.setVisible(True)
        else:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(False)
            self.ui.SaveRegisteredECoordinatesButton.setVisible(False)

    def registered_elastic_coords_checkbox_changed(self, state):
        """Handle the elastic registered image checkbox state change.
        Used in tab 3 only
        Args:
            state: current state of the checkbox
        Returns:
            no variables output, but App view changes.
        """
        if state > 0:
            self.all_images_checked += 1
        else:
            self.all_images_checked -= 1

        if self.all_images_checked == 4:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(True)
            self.ui.SaveRegisteredECoordinatesButton.setVisible(True)
        else:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(False)
            self.ui.SaveRegisteredECoordinatesButton.setVisible(False)

    def registered_coords_checkbox_changed(self, state):
        """Handle the registered image checkbox state change.
        Used in tab 3 only
        Args:
            state: current state of the checkbox
        Returns:
            no variables output, but App view changes.
        """
        if state > 0:
            self.all_images_checked += 1
        else:
            self.all_images_checked -= 1

        if self.all_images_checked == 4:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(True)
            self.ui.SaveRegisteredECoordinatesButton.setVisible(True)
        else:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(False)
            self.ui.SaveRegisteredECoordinatesButton.setVisible(False)

    def fixed_coords_checkbox_changed(self, state):
        """Handle the fixed image checkbox state change.
        Used in tab 3 only
        Args:
            state: current state of the checkbox
        Returns:
            no variables output, but App view changes.
        """
        if state > 0:
            self.all_images_checked += 1
        else:
            self.all_images_checked -= 1

        if self.all_images_checked == 4:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(True)
            self.ui.SaveRegisteredECoordinatesButton.setVisible(True)
        else:
            self.ui.SaveRegisteredCoordinatesButton.setVisible(False)
            self.ui.SaveRegisteredECoordinatesButton.setVisible(False)

    def populate_coordinates_combo_box(self):
        """Populate the QComboBox with strings from column 1 of self.moving_images_list.
        Used in tab 3 and tab 7 only
        Args:
        Returns:
            no variables output, but App view changes.
        """

        self.define_edit_frame()
        if self.current_index == self.apply_to_data_tab:
            combo_box = self.ui.CorrespondingImageComboBox
        elif self.current_index == self.apply_to_images_tab:
            combo_box = self.ui.ApplyToImageComboBox
        else:
            return

        # Clear the current items in the combo box
        combo_box.clear()
        # initialize the combo box list
        combo_box.addItem("Select")

        if self.num_image_column == 2: # make sure elastic exists
            # allow selection if the elastic registration exists, else pick affine automatically
            image_name = self.images_to_register_list[self.num_image_row][2]
            image_name, _ = os.path.splitext(image_name)  # Get the filename from column 1
            image_name = image_name + ".jpg"
            filename = os.path.join(self.job_folder, self.results_name, "Registered images", "Elastic", image_name)
            if os.path.exists(filename):
                combo_box.addItem("Affine")
                combo_box.addItem("Elastic")
            else:
                self.ui.ApplyToImageComboBox.setVisible(False)

        elif self.num_image_column in [0, 1]:
            self.which_moving_images_are_registered = [[], []]

            # Add items from column 1 of self.moving_images_list
            for index, row in enumerate(self.moving_images_list):
                if len(row) > 1:  # Ensure the row has at least two columns
                    filename = row[0]  # Get the filename from column 1
                    filename, _ = os.path.splitext(filename)
                    filename_out1 = filename + ".pkl"
                    filename_out2 = filename + ".jpg"

                    # check if fiducial points, a transform, and a registered image exists
                    filepath1 = os.path.join(self.job_folder, self.results_name, "Fiducial point selection",
                                             filename_out1)  # os.path.join(self.jobFolder, self.ResultsName, "aligned_stack", filename_out)
                    filepath2 = os.path.join(self.job_folder, self.results_name, "Registration transforms",
                                             filename_out1)
                    filepath3 = os.path.join(self.job_folder, self.results_name, "Registered images", filename_out2)

                    if os.path.isfile(filepath1) and os.path.isfile(filepath2) and os.path.isfile(
                            filepath3):  # Check if the file exists
                        combo_box.addItem(filename)  # Add to OldMovingImagesComboBox
                        self.which_moving_images_are_registered[0].append(index)
                    else:
                        self.which_moving_images_are_registered[1].append(index)

    def on_combo_box_changed_image(self):
        """Grab the name of the moving image filename selected from the pull down window.
        Used in tab 7
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """

        combo_box = self.ui.ApplyToImageComboBox

        # get the current filename and index from the droplist
        current_index_in_table = combo_box.currentIndex()
        if current_index_in_table in {-1, 0}:
            return
        elif self.num_image_column == 1:
            row_number = self.which_moving_images_are_registered[0]
            row_number = row_number[current_index_in_table - 1]
            moving_filename = self.moving_images_list[row_number][0]
            moving_folder = self.moving_images_list[row_number][2]
            self.images_to_register_list[self.num_image_row][2] = moving_filename
            self.images_to_register_list[self.num_image_row][3] = moving_folder
            self.images_to_register_list[self.num_image_row][4] = "" # remove the registration choice if it exists
            self.ui.ApplyToImageComboBox.setVisible(False)

            # pick affine registration automatically if the elastic registration does not exist
            image_name = self.images_to_register_list[self.num_image_row][2]
            image_name, _ = os.path.splitext(image_name)  # Get the filename from column 1
            image_name = image_name + ".jpg"
            filename = os.path.join(self.job_folder, self.results_name, "Registered images", "Elastic", image_name)
            if not os.path.exists(filename):
                self.images_to_register_list[self.num_image_row][4] = "Affine"

        elif self.num_image_column == 2:
            if current_index_in_table == 1:
                self.images_to_register_list[self.num_image_row][4] = "Affine"
            elif current_index_in_table == 2:
                self.images_to_register_list[self.num_image_row][4] = "Elastic"
            self.ui.ApplyToImageComboBox.setVisible(False)
        else:
            return

        # update the table
        self.populate_image_table()

        # exit edit table mode
        self.exit_edit_table()

    def on_combo_box_changed(self):
        """Grab the name of the moving image filename selected from the pull down window.
        Used in tab 3
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """

        combo_box = self.ui.CorrespondingImageComboBox

        # get the current filename and index from the droplist
        current_index_in_table = combo_box.currentIndex()
        if current_index_in_table in {-1, 0}:
            moving_filename = ""
            moving_folder = ""
            scale = ""
        else:
            row_number = self.which_moving_images_are_registered[0]
            row_number = row_number[current_index_in_table - 1]

            moving_filename = self.moving_images_list[row_number][0]
            moving_folder = self.moving_images_list[row_number][2]
            scale = self.moving_images_list[row_number][1]

        self.moving_image_filename_corresponding_to_coordinates = moving_filename
        self.moving_image_folder_corresponding_to_coordinates = moving_folder
        self.scale_coordinates_file = scale

        # automatically load the scale factor if this is a visium file
        try:
            self.load_visium_scale()
        except:
            self.json_scale = 1

        # update the table
        self.populate_coordinates_table()

    def populate_image_table(self):
        """Fill in values from the variables in the coordinates table. Turn the table green when complete.
        Used in tab 7
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """

        # set the number of rows in the table to the current number of moving images
        if len(self.images_to_register_list) == 0:
            self.ui.ApplyToImageTableWidget.setRowCount(0)
            return
        num_rows = self.images_to_register_list.size / 6
        self.ui.ApplyToImageTableWidget.setRowCount(num_rows)

        # populate the rows of the table with the info in movingIMS
        row_count = 0
        for row in self.images_to_register_list:
            #print(row)
            self.ui.ApplyToImageTableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(f"{row[0]}  "))
            self.ui.ApplyToImageTableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(f"{row[2]}  "))
            self.ui.ApplyToImageTableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(f"{row[4]}  "))
            self.ui.ApplyToImageTableWidget.setItem(row_count, 3, QtWidgets.QTableWidgetItem(f"{row[5]}  "))
            row_count += 1

        if self.images_to_register_list.shape[0] > 0:
            self.ui.ApplyToImageTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_table_is_complete_image_tab()

    def check_if_table_is_complete_image_tab(self):
        """Determines if the table is correctly filled. If yes, allow the user to load the coordinates and image.
        Used in tab 7
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """

        image_frame_done = 1  # complete
        if len(self.images_to_register_list) == 0:
            image_frame_done = 0  # not started
        else:
            for row in self.images_to_register_list:
                row_count = 1
                for cell in row:
                    if (not isinstance(cell, str) or not cell.strip()) and row_count != 6:
                        image_frame_done = 2  # incomplete
                    row_count = row_count + 1

        # make fixed frame green if completed
        if image_frame_done == 1: # complete
            self.ui.ApplyToImageFrame.setStyleSheet("background-color: #375c46;")
            self.ui.RegisterImageButton.setVisible(True)
        elif image_frame_done == 0: # not started
            self.ui.ApplyToImageFrame.setStyleSheet("background-color: #4b4b4b;")
            self.ui.RegisterImageButton.setVisible(False)
        else: # incomplete
            self.ui.ApplyToImageFrame.setStyleSheet("background-color: #5c3737;")
            self.ui.RegisterImageButton.setVisible(False)

    def populate_coordinates_table(self):
        """Fill in values from the variables in the coordinates table. Turn the table green when complete.
        Used in tab 3
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """

        # Populate the first row with the variables' values
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{self.coordinates_filename}  "))
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{self.moving_image_filename_corresponding_to_coordinates}  "))  # Convert scale to string if necessary
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(self.scale_coordinates_file))
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem(self.column_in_coords_file_containing_x_values))
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem(self.column_in_coords_file_containing_y_values))
        self.ui.RegisterCoordinatesTableWidget.setItem(0, 5, QtWidgets.QTableWidgetItem(str(self.max_points)))
        self.ui.RegisterCoordinatesTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_table_is_complete_coords_tab()

    def check_if_table_is_complete_coords_tab(self):
        """Determines if the table is correctly filled. If yes, allow the user to load the coordinates and image.
        Used in tab 3
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """

        coordsFrameDone = (len(self.coordinates_filename) > 0
            and len(self.moving_image_filename_corresponding_to_coordinates) > 0
            and len(self.scale_coordinates_file) > 0
            and len(self.column_in_coords_file_containing_x_values) > 0
            and len(self.column_in_coords_file_containing_y_values) > 0 and len(self.max_points) > 0)

        # make fixed frame green if completed
        if coordsFrameDone:
            self.ui.RegisterCoordinatesFrame.setStyleSheet("background-color: #375c46;")
            self.ui.LoadCoordinatesButton.setVisible(True)
        else:
            self.ui.RegisterCoordinatesFrame.setStyleSheet("background-color: #4b4b4b;")
            self.ui.LoadCoordinatesButton.setVisible(False)

    def doubleclick_coordinates_table(self, row, column):
        """Handle the user double-clicking the coordinates table.
        Used in tab 3 only
        Args:
            row: row in the table selected
            column: column in the table selected
        Returns:
            no variables output, but App view changes.
        """

        # don't allow if table edit mode is active
        if self.edit_table_active == 5:
            return

        # if the table is populated and table edit mode is not already active
        if len(self.coordinates_filename) > 0 or len(self.moving_image_filename_corresponding_to_coordinates) > 0:

            # if editing the scale
            if column in [2, 3, 4, 5]: # editing the scale, x, y, or # points
                self.ui.LoadCoordinatesButton.setVisible(False)
                # enable text input to the scale window
                item = self.ui.RegisterCoordinatesTableWidget.item(row, column)
                if item:
                    item.setFlags(item.flags() | Qt.ItemIsEditable)  # Enable editing
                    self.ui.RegisterCoordinatesTableWidget.editItem(item)  # Put the cell into edit mode

    def doubleclick_image_table(self, row, column):
        """Enable editing of the moving image variables in table 2
        Used in tab 7 only
        Args:
            row: row of the table that the user double-clicked on
            column: column of the table that the user double-clicked on
        Returns:
            no variables output, but allows the user to edit the image to register parameters
        """

        # disable doubleclicking in the table during other edit actions
        if self.edit_table_active == 5:
            return

        # if the table is populated
        if len(self.images_to_register_list) > 0:

            self.num_image_row = row
            self.num_image_column = column
            if column == 0: # enable the user to keep or delete the image TO DO
                self.edit_table_active = 5
                self.enter_edit_table()
            elif column == 1: # enable combobox to choose the image
                self.edit_table_active = 5
                self.enter_edit_table()
                self.ui.ApplyToImageComboBox.setVisible(True)
                self.populate_coordinates_combo_box()
            elif column == 2: # choose affine or elastic registration TO DO
                # only allow registration style selection after the image is chosen
                txt = self.images_to_register_list[self.num_image_row][2]
                if txt is None or txt == '':
                    return
                self.edit_table_active = 5
                self.enter_edit_table()
                self.ui.ApplyToImageComboBox.setVisible(True)
                self.populate_coordinates_combo_box()


    def handle_value_update_image(self, new_value, row, column):
        """Make sure that the moving image table inputs are valid.
        Used in tab 7 only
        Args:
            new_value: new value input by the user for this cell of the table
            row: row of the table that the user double-clicked on
            column: column of the table that the user double-clicked on
        Returns:
            no variables output, but updates table 2
        """

        print("handle value update image table")

        # Optionally update other variables or UI elements
        if column == 1:
            print(" clicked in column 2")
            self.populate_moving_table()
        elif column == 2:
            print(" clicked in column 3")
            self.populate_moving_table()

    def handle_value_update_coordinates(self, new_value, row, column):
        """Check that the inputted scale value is compatible, if not throw an error message.
        Used in tab 3 only
        Args:
            new_value: inputted scale value
            row: row in the table selected
            column: column in the table selected
        Returns:
            no variables output, but App view changes.
        """

        if column == 2: # scale
            try:
                float(new_value)
                self.scale_coordinates_file = new_value
            except:
                if new_value != "":
                    text = "The entered value is not a number. Please enter a number"
                    self.show_error_message(text)
        elif column == 3: # x column
            col_num = self.get_column_number(new_value)
            if not col_num:
                text = "Enter fully numeric (e.g. '5') or alphabetical (e.g. 'AB') text"
                self.show_error_message(text)
            elif col_num > 0:
                self.column_in_coords_file_containing_x_values = new_value
            else:
                text = "Enter fully numeric (e.g. '5') or alphabetical (e.g. 'AB') text"
                self.show_error_message(text)
        elif column == 4: # y column
            col_num = self.get_column_number(new_value)
            if not col_num:
                text = "Enter fully numeric (e.g. '5') or alphabetical (e.g. 'AB') text"
                self.show_error_message(text)
            elif col_num > 0:
                self.column_in_coords_file_containing_y_values = new_value
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

    def return_to_edit_table(self):
        """Stop viewing the coordinates and return to editing the coordinates table.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """
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
        """View the imported coordinates overlaid on the unregistered moving image.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """
        self.edit_which_image = 0
        self.close_navigation_tab()
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        self.reset_transformations()
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.RegisterCoordsFrameHeaderText.setText("Unregistered Moving Image")

    def define_image_registered(self):
        """View the imported coordinates overlaid on the affine registered image.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """
        self.edit_which_image = 1
        self.close_navigation_tab()
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        self.reset_transformations()
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.RegisterCoordsFrameHeaderText.setText("Registered Moving Image")

    def define_image_fixed(self):
        """View the imported coordinates overlaid on the fixed image.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """
        self.edit_which_image = 2
        self.close_navigation_tab()
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        self.reset_transformations()
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.RegisterCoordsFrameHeaderText.setText("Fixed Image")

    def define_image_registered_elastic(self):
        """View the imported coordinates overlaid on the elastically registered image.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """
        self.edit_which_image = 3
        self.close_navigation_tab()
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        self.reset_transformations()
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.RegisterCoordsFrameHeaderText.setText("Elastically Registered Moving Image")

    def load_coordinates_to_register(self):
        """Loads the coordinates and image data defined in the table.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """
        # change some view settings while the data loads
        self.ui.MakingCoordOverlayText.setVisible(True)
        self.ui.MakingCoordOverlayText.setText("Making the Coordinate Overlay Image. Please Wait...")
        self.ui.DisableFrame_C.setVisible(True)
        QtWidgets.QApplication.processEvents()

        # load the fixed image and the unregistered and registered moving images
        image_path_fixed = os.path.join(self.fixed_image_folder, self.fixed_image_filename)
        image_path_moving = os.path.join(self.moving_image_folder_corresponding_to_coordinates, self.moving_image_filename_corresponding_to_coordinates)
        filename, _ = os.path.splitext(self.moving_image_filename_corresponding_to_coordinates)
        image_nm = filename + ".jpg"
        image_path_reg = os.path.join(self.job_folder, self.results_name, "Registered images", image_nm)
        image_path_reg_elastic = os.path.join(self.job_folder, self.results_name, "Registered images", "Elastic", image_nm)

        # uncheck the check boxes
        self.ui.UnregisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredEMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.FixedCheckBox.setCheckState(Qt.Unchecked)
        self.all_images_checked = 0

        # load the desired images
        if self.moving_image_filename_corresponding_to_coordinates != self.loaded_moving_image_filename:
            try:
                self.coord_registration_type = 0
                self.im_fixed, self.max_intensity_fixed, self.mode_intensity_fixed = self.load_image(image_path_fixed)         # load the fixed image
                self.im_moving_coords, self.max_intensity_moving_coords, self.mode_intensity_moving = self.load_image(image_path_moving)  # load the moving image
                self.im_moving_coords_reg, self.max_intensity_moving_coords_reg, mode_MovingReg = self.load_image(image_path_reg)  # load the registered moving image
                self.loaded_moving_image_filename = self.moving_image_filename_corresponding_to_coordinates
                if os.path.exists(image_path_reg_elastic):
                    self.im_moving_coords_reg_elastic, MI_MovingCoordsRegE, mode_MovingRegE = self.load_image(image_path_reg_elastic)  # load the elastic registered moving image
                    self.coord_registration_type = 1
            except:
                text = "One or more images could not be loaded."
                self.show_error_message(text)

            self.ui.SaveRegisteredCoordinatesButton.setStyleSheet(self.style_button_green)
            self.ui.SaveRegisteredECoordinatesButton.setStyleSheet(self.style_button_green)
            self.ui.ViewRegisteredEMovingButton.setStyleSheet(self.active_button_style)
            self.ui.SaveRegisteredECoordinatesButton.setEnabled(True)
            self.ui.ViewRegisteredEMovingButton.setEnabled(True)
            self.ui.RegisteredEMovingCheckBox.setEnabled(True)
            if self.coord_registration_type == 0:
                self.ui.ViewRegisteredEMovingButton.setEnabled(False)
                self.ui.RegisteredEMovingCheckBox.setEnabled(False)
                self.ui.SaveRegisteredECoordinatesButton.setEnabled(False)
                self.ui.RegisteredEMovingCheckBox.setCheckState(Qt.Checked)
                self.ui.ViewRegisteredEMovingButton.setStyleSheet(self.inactive_button_style)
                self.ui.SaveRegisteredECoordinatesButton.setStyleSheet(self.inactive_button_style)

        # define the first settings
        self.edit_which_image = 0 # unregistered moving image
        self.moving_coords_flip_state = 0
        self.moving_coords_rotation_angle = 0
        self.moving_coords_brightness = 0
        self.moving_coords_contrast = 1
        self.moving_coords_pan_offset_x = 0
        self.moving_coords_pan_offset_y = 0

        # set the zoom default
        width_scale = self.ui.RegisterCoordsDisplayFrame.width() / self.im_moving_coords.width()
        height_scale = self.ui.RegisterCoordsDisplayFrame.height() / self.im_moving_coords.height()
        self.moving_coords_zoom_default = min(width_scale, height_scale)
        self.moving_coords_zoom_scale = self.moving_coords_zoom_default

        # load and subsample the coordinates
        coords_loaded = self.get_coordinates_from_file()
        if coords_loaded == 0:
            return

        downsample_num = min([self.pts_coords.shape[0], int(self.max_points)])
        self.max_points = str(downsample_num)
        self.populate_coordinates_table()
        self.sampled_indices = np.random.choice(self.pts_coords.shape[0], size=downsample_num, replace=False)

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

    def call_save_registered_coordinates_ICP(self):
        """Handle saving the affine registered coordinate data.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but defines that affine registered coordinate data is saved.
        """
        self.coord_registration_type = 0 # save ICP registered coordinates
        self.save_registered_coordinates()

    def call_save_registered_coordinates_elastic(self):
        """Handle saving the elastically registered coordinate data.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but defines that elastically registered coordinate data is saved.
        """
        self.coord_registration_type = 1 # save elastic registered coordinates
        self.save_registered_coordinates()

    def save_registered_coordinates(self):
        """Saves registered coordinate data to a .csv file.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but saves registered coordinates to the job folder
        """
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        self.ui.PlottingImageText.setText("Saving the Coordinates. Please Wait...")
        QtWidgets.QApplication.processEvents()

        # load the coordinates again
        xCol = self.get_column_number(self.column_in_coords_file_containing_x_values) - 1
        yCol = self.get_column_number(self.column_in_coords_file_containing_y_values) - 1

        # Save the updated matrix to a new file in a specified folder
        output_folder = os.path.join(self.job_folder, self.results_name, "Registered coordinate data")
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
        image_name, _ = os.path.splitext(self.fixed_image_filename)

        # Substitute the registered coordinates into the X matrix
        X = self.coordinate_data
        if self.coord_registration_type == 0: # save ICP registration
            X[self.number_of_first_row_in_coords_file:, [xCol, yCol]] = self.pts_coords_reg
            self.ui.SaveRegisteredCoordinatesButton.setStyleSheet(self.inactive_button_style)
            self.ui.SaveRegisteredCoordinatesButton.setEnabled(False)
            output_file = os.path.join(output_folder, f"Global_Registered_{self.coordinates_filename}")
        else: # save elastic registration
            X[self.number_of_first_row_in_coords_file:, [xCol, yCol]] = self.pts_coords_reg_elastic
            self.ui.SaveRegisteredECoordinatesButton.setStyleSheet(self.inactive_button_style)
            self.ui.SaveRegisteredECoordinatesButton.setEnabled(False)
            output_file = os.path.join(output_folder, f"Elastic_Registered_{self.coordinates_filename}")

        # Save the updated X matrix as a CSV file
        pd.DataFrame(X).to_csv(output_file, header=None, index=False)

        # save a pkl file logging whether the coordinates were icp or elastically registered
        filename, _ = os.path.splitext(self.moving_image_filename_corresponding_to_coordinates)
        filename = filename + ".pkl"
        output_folder = os.path.join(self.job_folder, self.results_name, "Registered coordinate data", "log")
        outfile = os.path.join(output_folder, filename)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        coord_registration_type = self.coord_registration_type
        # Save variables to the pkl file
        with open(outfile, 'wb') as file:
            pickle.dump({'coord_registration_type': coord_registration_type}, file)

        # change the view settings
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)
        self.ui.PlottingImageText.setText("Registered coordinates saved!")

    def get_coordinates_from_file(self):
        """Imports coordinate data, image data, and registration data. registers coordinates and
           overlays them on the fixed image.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but saves registered coordinates to the job folder
        """
        # load the coordinates
        x_column = self.get_column_number(self.column_in_coords_file_containing_x_values) - 1
        y_column = self.get_column_number(self.column_in_coords_file_containing_y_values) - 1

        file_path = os.path.join(self.coordinates_file_folder, self.coordinates_filename)
        file_ext = os.path.splitext(file_path)[1]
        if self.coordinates_filename != self.loaded_coordinates_filename:
            if file_ext == ".csv":
                self.coordinate_data = pd.read_csv(file_path, header=None).values
            elif file_ext in [".xlsx", ".xls"]:
                self.coordinate_data = pd.read_excel(file_path, header=None).values
            self.loaded_coordinates_filename = self.coordinates_filename

        # Check if the first row contains text labels
        coords_loaded = 0
        try:
            float(self.coordinate_data[0, x_column])
            float(self.coordinate_data[0, y_column])
            self.number_of_first_row_in_coords_file = 0
        except (ValueError, IndexError):
            # try removing the top row in case it contains text headers
            self.number_of_first_row_in_coords_file = 1
            try:
                float(self.coordinate_data[1, x_column])
                float(self.coordinate_data[1, y_column])
            except (ValueError, IndexError):
                text = "Coordinate data not found in the columns and csv file provided. Please double check your inputs."
                self.show_error_message(text)
                self.return_to_edit_table()
                return coords_loaded

        self.pts_coords = self.coordinate_data[self.number_of_first_row_in_coords_file:, [x_column, y_column]].astype(float)
        self.pts_coords = np.round(self.pts_coords)
        self.pts_coords = self.pts_coords * float(self.scale_coordinates_file)

        # Load the transformation data and register the coordinates
        filename, _ = os.path.splitext(self.moving_image_filename_corresponding_to_coordinates)
        filename = filename + ".pkl"
        output_folder = os.path.join(self.job_folder, self.results_name, "Registration transforms")
        outfile = os.path.join(output_folder, filename)
        with open(outfile, 'rb') as file:
            data = pickle.load(file)
        self.tformCoords = data.get('tform')
        self.flip_im_coords = data.get('flip_im')

        # flip the coordinates if required before registration
        if self.flip_im_coords == 1:
            image_width = self.im_moving_coords.width()
            pts_coords_reg = np.column_stack([image_width - self.pts_coords[:, 0], self.pts_coords[:, 1]])
        else:
            pts_coords_reg = self.pts_coords
        self.pts_coords_reg = (self.tformCoords[:2, :2] @ pts_coords_reg.T).T + self.tformCoords[:2, 2]

        # if it exists, load the elastic registration data and register the coordinates
        outfile = os.path.join(output_folder, "Elastic", filename)
        if os.path.exists(outfile):
            with open(outfile, 'rb') as file:
                data = pickle.load(file)
            self.DinvCoords = data.get('Dinv')
            szz = (self.im_fixed.height(), self.im_fixed.width())
            self.pts_coords_reg_elastic = self.register_points_elastic(self.pts_coords_reg, szz, self.DinvCoords)
        coords_loaded = 1

        return coords_loaded

    def get_column_number(self, alphabetical_column_index):
        """Determines the numberical equivalent to a column defined alphabetically.
        Used in tab 3 only
        Args:
            alphabetical_column_index: alphabetical column index
        Returns:
            numerical_column_index: numerical column index corresponding to an alphabetical column definition (A=1, E=5, AE=31, etc.)
        """
        if alphabetical_column_index.isdigit():  # Check if the input is fully numeric
            return int(alphabetical_column_index)
        elif alphabetical_column_index.isalpha():  # Check if the input is fully alphabetic
            alphabetical_column_index = alphabetical_column_index[::-1]  # Reverse the string
            numerical_column_index = 0
            for b, xb in enumerate(alphabetical_column_index):
                asc = ord(xb.upper()) - ord('A') + 1  # Convert character to 1-based index
                numerical_column_index += asc * (26 ** b) # Multiply by 26^(position-1)
            #numerical_column_index = numerical_column_index - 1  # because python
            return numerical_column_index
        else:
            # Raise an error for mixed inputs
            return

    def swap_xy(self):
        """Switch the x and y coordinate column numbers and replot the coordinate overlay on the fixed image.
        Used in tab 3 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but coordinates are replotted on the overlay image
        """
        tmp = self.column_in_coords_file_containing_x_values
        self.column_in_coords_file_containing_x_values = self.column_in_coords_file_containing_y_values
        self.column_in_coords_file_containing_y_values = tmp

        # update the table
        self.populate_coordinates_table()

        # change some visibility settings
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        self.ui.PlottingImageText.setVisible(True)
        self.ui.DisableFrame_C_2.setVisible(True)
        self.ui.DisableFrame_C_3.setVisible(True)
        QtWidgets.QApplication.processEvents()

        # load and subsample the coordinates
        self.get_coordinates_from_file()

        # replot the image
        self.update_image_view()

        # make buttons clickable again
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.PlottingImageText.setVisible(False)
        self.ui.DisableFrame_C_2.setVisible(False)
        self.ui.DisableFrame_C_3.setVisible(False)

        # uncheck the checkboxes
        self.ui.FixedCheckBox.setCheckState(Qt.Unchecked)
        self.ui.UnregisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        self.ui.RegisteredMovingCheckBox.setCheckState(Qt.Unchecked)
        if self.coord_registration_type == 1: # elastic registration exists
            self.ui.RegisteredEMovingCheckBox.setCheckState(Qt.Unchecked)
            self.all_images_checked = 0
        else:
            self.all_images_checked = 1

    def icp_registration(self, pts_fixed, pts_moving):
        """Perform a simple ICP registration of self.ptsMoving into self.ptsFixed space.
        Used in tab 5 only
        Args:
            pts_fixed: coordinate points 1
            pts_moving: coordinate points 2
        Returns:
            registered_pts (np.ndarray): The registered points in the self.ptsFixed space.
            tform (np.ndarray): The 3x3 transformation matrix combining rotation and translation.
            RMSE_unregistered (float): RMSE of the points before registration.
            RMSE_registered (float): RMSE of the points after registration.
        """
        pts_moving0 = pts_moving

        # compute the initial RMSE (unregistered points)
        dist = (pts_fixed[:, 0] - pts_moving0[:, 0]) ** 2 + (pts_fixed[:, 1] - pts_moving0[:, 1]) ** 2
        rmse0 = round(np.sqrt(np.mean(dist)))

        # scale is the ratio of the mean distance from the centroid
        centroid_fixed = np.mean(pts_fixed, axis=0)
        centroid_moving = np.mean(pts_moving0, axis=0)
        dist_fixed = np.sqrt(np.sum((pts_fixed - centroid_fixed) ** 2, axis=1))
        dist_moving = np.sqrt(np.sum((pts_moving0 - centroid_moving) ** 2, axis=1))
        scale_val = np.mean(dist_fixed) / np.mean(dist_moving)

        # point cloud calculation for known point pairs
        pts_moving = pts_moving0 * scale_val
        centroid_moving = np.mean(pts_moving, axis=0)
        centered_moving = pts_moving - np.mean(pts_moving, axis=0)
        centered_fixed = pts_fixed - np.mean(pts_fixed, axis=0)
        H = centered_moving.T @ centered_fixed

        # compute the Singular Value Decomposition (SVD), rotation, and translation
        U, _, Vt = np.linalg.svd(H)
        rotation_matrix = Vt.T @ U.T
        if np.linalg.det(rotation_matrix) < 0:  # Handle reflection case
            Vt[-1, :] *= -1
            rotation_matrix = Vt.T @ U.T
        xy_translation = centroid_fixed - rotation_matrix @ centroid_moving

        # construct the final transformation matrix
        rotation_matrix_scaled = rotation_matrix * scale_val
        tform = np.eye(3)
        tform[:2, :2] = rotation_matrix_scaled
        tform[:2, 2] = xy_translation

        # apply the transform to the points
        registered_pts = (tform[:2, :2] @ pts_moving0.T).T + tform[:2, 2]

        # compute the RMSE of the registered points
        dist = (pts_fixed[:, 0] - registered_pts[:, 0]) ** 2 + (pts_fixed[:, 1] - registered_pts[:, 1]) ** 2
        rmse = round(np.sqrt(np.mean(dist)))

        return registered_pts, tform, rmse, rmse0


    def return_to_fiducials_tab(self):
        """Exits the image overlay tab and navigates back to the fiducials tab.
        Used in tab 5 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but changes the app view
        """
        # move navigation button
        self.close_navigation_tab()
        self.ui.WhatNextControlFrame.setParent(self.ui.AlignImageTabName)
        self.ui.NavigationButton.setParent(self.ui.AlignImageTabName)
        self.ui.KeyboardShortcutsButton.setParent(self.ui.AlignImageTabName)
        self.close_navigation_tab()

        # initial button settings
        self.ui.DisableFrame_F1.setVisible(False)
        self.ui.FiducialTabUpdateText.setVisible(False)
        self.ui.LoadNewMovingImageButton.setEnabled(False)
        self.ui.LoadOldMovingImageButton.setEnabled(False)
        self.ui.ChooseMovingImageFrame.setVisible(False)
        self.ui.FiducialPointControlsFrame.setVisible(True)
        self.ui.AttemptICPRegistrationButton.setVisible(True)
        self.ui.AttemptICPRegistrationButton.setEnabled(False)
        self.ui.AttemptICPRegistrationButton.setStyleSheet(self.active_button_style)
        self.ui.PickNewMovingImageButton.setVisible(True)
        self.ui.PickNewMovingImageButton.setEnabled(True)
        self.ui.PickNewMovingImageButton.setStyleSheet(self.active_button_style)
        QtWidgets.QApplication.processEvents()

        # go to fiducials tab and update the images
        self.ui.tabWidget.setCurrentIndex(self.fiducials_tab)
        self.populate_moving_images_combo_box()
        self.update_button_color()
        self.update_both_images()

    def save_registration_results(self):
        """Saves point-cloud registration metadata.
        Used in tab 5 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but save registration metadata in a .pkl file in the job folder
        """
        # turn off active labels
        self.ui.UnregisteredImageBorder.setStyleSheet(self.inactive_label_style)
        self.ui.UnregisteredImageFrameHeaderText.setStyleSheet(self.inactive_text_label_style)
        self.ui.UnregisteredImageDisplayFrame.setStyleSheet(self.inactive_frame_style)
        self.ui.RegisteredImageBorder.setStyleSheet(self.inactive_label_style)
        self.ui.RegisteredImageFrameHeaderText.setStyleSheet(self.inactive_text_label_style)
        self.ui.RegisteredImageDisplayFrame.setStyleSheet(self.inactive_frame_style)
        ref_frame_a = self.ui.UnregisteredImageDisplayFrame.geometry()
        ref_frame_b = self.ui.RegisteredImageDisplayFrame.geometry()
        self.ui.UnregisteredImageBorder.setGeometry(ref_frame_a.x() - 3, ref_frame_a.y() - 3,
                                                    ref_frame_a.width() + 6, ref_frame_a.height() + 6)
        self.ui.RegisteredImageBorder.setGeometry(ref_frame_b.x() - 3, ref_frame_b.y() - 3,
                                                  ref_frame_b.width() + 6, ref_frame_b.height() + 6)

        # disable some buttons
        self.close_navigation_tab()
        self.ui.SaveRegistrationResultsButton_O.setStyleSheet(self.inactive_button_style)
        self.ui.SaveRegistrationResultsButton_O.setEnabled(False)
        self.ui.ReturnToFiducialsTab_O.setEnabled(False)
        self.ui.ImageViewControlsFrame_O.setEnabled(False)
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        self.ui.DisableFrame_O1.setVisible(True)
        QtWidgets.QApplication.processEvents()

        # save registration info
        filename, _ = os.path.splitext(self.moving_image_filename)
        filename = filename + ".pkl"
        output_folder = os.path.join(self.job_folder, self.results_name, "Registration transforms")
        outfile = os.path.join(output_folder, filename)
        save_results = 1

        # check if the folder exists, and create it if it doesn't
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if os.path.isfile(outfile):
            # load the previous affine registration results to see if they are the same
            with open(outfile, 'rb') as file:
                data = pickle.load(file)

                # check the rmse and tform to see if either has changed
                tform_old = data.get('tform')
                flip_im_old = data.get('flip_im')
                rmse_reg_old = data.get('RMSE')
                rmse_unregistered_old = data.get('RMSE0')

                old_reg_equals_new_reg = all([
                    self.rmse_unregistered == rmse_unregistered_old,
                    self.rmse_reg == rmse_reg_old,
                    self.flip_im == flip_im_old,
                    np.array_equal(self.tform, tform_old)
                ])

                # if registration has changed since the previous version, ask the user to confirm the update
                if old_reg_equals_new_reg:
                    # no need to save the results as this has already been done, skip the save and continue
                    save_results = 0

                    # what to do next
                    self.ui.SaveRegistrationResultsButton_O.setEnabled(True)
                    self.ui.ReturnToFiducialsTab_O.setEnabled(True)
                    self.ui.ImageViewControlsFrame_O.setEnabled(True)
                    self.ui.NavigationButton.setEnabled(True)
                    self.ui.NavigationButton.setStyleSheet(self.active_button_style)
                    self.ui.KeyboardShortcutsButton.setEnabled(True)
                    self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
                    self.ui.TryElasticRegButton.setEnabled(True)
                    self.ui.TryElasticRegButton.setStyleSheet(self.style_button_green)
                    self.ui.DisableFrame_O1.setVisible(False)
                else:
                    msg_box = QtWidgets.QMessageBox()  # Create a message box
                    msg_box.setWindowTitle("Confirm update of registration")  # Set the window title
                    msg_box.setText("Registration results already exist for this image pair. If you continue those "
                                    "results will be replaced, and elastic registration metadata will be deleted if "
                                    "it exists. Are you sure you want to proceed?")  # Set the message text
                    msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
                    msg_box.setStandardButtons(
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons
                    msg_box.setStyleSheet(self.quest_box_style)

                    # show the message box and get the response
                    response = msg_box.exec()
                    if response == QtWidgets.QMessageBox.Cancel:
                        # the registration results have changed and the user does not want to replace them. abort
                        self.ui.SaveRegistrationResultsButton_O.setStyleSheet(self.active_button_style)
                        self.ui.SaveRegistrationResultsButton_O.setEnabled(True)
                        self.ui.ReturnToFiducialsTab_O.setEnabled(True)
                        self.ui.ImageViewControlsFrame_O.setEnabled(True)
                        self.ui.NavigationButton.setEnabled(True)
                        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
                        self.ui.KeyboardShortcutsButton.setEnabled(True)
                        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
                        self.ui.DisableFrame_O1.setVisible(False)
                        QtWidgets.QApplication.processEvents()
                        return
                    else:
                        # check if elastic registration results exist and delete them if they do
                        output_folder_image_elastic = os.path.join(self.job_folder, self.results_name, "Registered images", "Elastic")
                        filename, _ = os.path.splitext(self.moving_image_filename)
                        filename_image_elastic = filename + ".jpg"
                        outfile_image_elastic = os.path.join(output_folder_image_elastic, filename_image_elastic)
                        outfile_elastic = os.path.join(self.job_folder, self.results_name, "Registration transforms", "Elastic", filename)
                        # delete the elastically registered image
                        if os.path.isfile(outfile_image_elastic):
                            os.remove(outfile_image_elastic)
                        # delete the pkl metadata file
                        if os.path.isfile(outfile_elastic):
                            os.remove(outfile_elastic)

        save_results = 1
        # save the registration results to the .pkl file as long as the user does not cancel
        if save_results == 1:
            size_fixed_image = [self.im_fixed.width(), self.im_fixed.height()]
            size_moving_image = [self.im_moving.width(), self.im_moving.height()]
            # save variables to the pkl file
            with open(outfile, 'wb') as file:
                pickle.dump({'tform': self.tform, 'flip_im': self.flip_im, 'size_fixed_image': size_fixed_image,
                    'size_moving_image': size_moving_image,'RMSE': self.rmse_reg, 'RMSE0': self.rmse_unregistered}, file)

            # save the images
            self.save_registered_images()

            # what to do next
            self.ui.SaveRegistrationResultsButton_O.setEnabled(True)
            self.ui.ReturnToFiducialsTab_O.setEnabled(True)
            self.ui.ImageViewControlsFrame_O.setEnabled(True)
            self.ui.NavigationButton.setEnabled(True)
            self.ui.NavigationButton.setStyleSheet(self.active_button_style)
            self.ui.KeyboardShortcutsButton.setEnabled(True)
            self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
            self.ui.TryElasticRegButton.setEnabled(True)
            self.ui.TryElasticRegButton.setStyleSheet(self.style_button_green)
            self.ui.DisableFrame_O1.setVisible(False)

    def begin_calculate_icp_tabF(self):
        """Calculate the point-cloud registration of the fiducial points and apply the transform to the moving image.
        Used in tab 5 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but App view changes.
        """
        # turn off active labels
        self.ui.FixedImageBorder.setStyleSheet(self.inactive_label_style)
        self.ui.FixedImageFrameHeaderText.setStyleSheet(self.inactive_text_label_style)
        self.ui.FixedImageDisplayFrame.setStyleSheet(self.inactive_frame_style)
        tmp = self.ui.FixedImageDisplayFrame.geometry()
        self.ui.FixedImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)
        self.ui.MovingImageBorder.setStyleSheet(self.inactive_label_style)
        self.ui.MovingImageFrameHeaderText.setStyleSheet(self.inactive_text_label_style)
        self.ui.MovingImageDisplayFrame.setStyleSheet(self.inactive_frame_style)
        tmp = self.ui.MovingImageDisplayFrame.geometry()
        self.ui.MovingImageBorder.setGeometry(tmp.x() - 3, tmp.y() - 3, tmp.width() + 6, tmp.height() + 6)

        if self.add_fiducial_active:
            self.toggle_add_fiducial_mode()

        # button view settings
        self.close_navigation_tab()
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        self.ui.DisableFrame_F1.setVisible(True)
        self.ui.ChooseMovingImageFrame.setVisible(False)
        self.ui.PickNewMovingImageButton.setEnabled(False)
        self.ui.PickNewMovingImageButton.setStyleSheet(self.inactive_button_style)
        self.ui.AttemptICPRegistrationButton.setEnabled(False)
        self.ui.AttemptICPRegistrationButton.setStyleSheet(self.inactive_button_style)
        self.ui.FiducialTabUpdateText.setVisible(True)
        self.ui.FiducialTabUpdateText.setText(f"Calculating Point Cloud Registration. Please Wait...")
        QtWidgets.QApplication.processEvents()

        # save the fiducial points
        self.save_fiducial_state()

        pts_fixed = np.delete(self.pts_fixed, 0, axis=0)
        pts_moving = np.delete(self.pts_moving, 0, axis=0)
        width = self.im_moving.width()

        # try registration of the fixed and moving image
        pts_moving_0 = pts_moving
        pts_out_noflip, tform_noflip, rmse_noflip, rmse0 = self.icp_registration(pts_fixed, pts_moving_0)

        # try registration of the fixed and 'flipped' moving image
        pts_moving_flip_image = np.column_stack([width - pts_moving[:, 0], pts_moving[:, 1]])
        pts_out_flip_image, tform_flip_image, rmse_flip_image, rmse0 = self.icp_registration(pts_fixed, pts_moving_flip_image)

        self.rmse_unregistered = rmse0
        if rmse_noflip < rmse_flip_image:
            self.pts_moving_reg = pts_out_noflip
            self.rmse_reg = rmse_noflip
            self.tform = tform_noflip
            self.flip_im = 0
        else:
            self.pts_moving_reg = pts_out_flip_image
            self.rmse_reg = rmse_flip_image
            self.tform = tform_flip_image
            self.flip_im = 1

        self.initiate_overlay_tab()

    def save_registered_images(self):
        """Saves the affine registered moving image to the user-defined job folder.
        Used in tab 5 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but an image is saved.
        """
        # save registered moving image
        output_folder = os.path.join(self.job_folder, self.results_name, "Registered images")
        # Check if the folder exists, and create it if it doesn't
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        filename, _ = os.path.splitext(self.moving_image_filename)
        filename = filename + ".jpg"
        outfile = os.path.join(output_folder, filename)
        self.im_moving_reg.save(outfile, "JPG")

        # save the fixed image if it does not already exist
        filename, _ = os.path.splitext(self.fixed_image_filename)
        filename = filename + ".jpg"
        outfile = os.path.join(output_folder, filename)
        if not os.path.exists(outfile):
            self.im_fixed.save(outfile, "JPG")

    def call_CODA_elastic_registration(self):
        """Calls CODA elastic registration and handles visual updates to tab six
        Used in tab 6 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but calculates the elastic registration and updates tab 6 view
        """
        # disable some buttons
        self.ui.CalculatingElasticRegistrationText.setVisible(True)
        self.ui.CalculatingElasticRegistrationText.setText("Calculating Elastic Registration. Please Wait...")
        self.ui.DisableFrame_E2.setVisible(True)
        self.ui.ViewElasticCheckBox.setVisible(False)
        self.ui.CalculateElasticRegistrationButton.setEnabled(False)
        self.ui.CalculateElasticRegistrationButton.setStyleSheet(self.inactive_button_style)
        self.ui.QuitElasticRegistrationButton.setEnabled(False)
        self.ui.QuitElasticRegistrationButton.setStyleSheet(self.inactive_button_style)
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        QtWidgets.QApplication.processEvents()
        self.view_squares = 2

        # set up fixed image for elastic registration
        im_ref = self.pixmap_to_array(self.im_fixed)
        im_ref_grey, mask_ref, = self.make_tissue_mask(im_ref, self.mode_intensity_fixed)

        # set up moving image for elastic registration
        im_moving = self.pixmap_to_array(self.im_moving_reg)
        im_moving = im_moving[:, :, :3]
        im_moving_grey, mask_moving, = self.make_tissue_mask(im_moving, self.mode_intensity_moving)

        # elastic registration settings
        tile_size = self.elastic_tilesize
        buffer_pix_size = 50
        inter_tile_distance = self.elastic_tilespacing

        # self.debug_show_image(im_moving_grey)
        # self.debug_show_image(mask_moving)
        # self.debug_show_image(im_ref_grey)
        # self.debug_show_image(mask_ref)

        # Took below section from pyCODA:
        D = self.calculate_elastic_registration(im_ref_grey, im_moving_grey, mask_ref, mask_moving, tile_size,
                                                buffer_pix_size, inter_tile_distance)
        self.D = D.astype(np.float32)

        #start_time = time.time()
        #self.Dinv = self.invert_D(self.D)
        #end_time = time.time()
        #print(f"Inversion completed in {end_time - start_time:.2f} seconds")

        #start_time = time.time()
        self.Dinv = self.invert_D_optimized(D)
        #end_time = time.time()
        #print(f"Optimized inversion completed in {end_time - start_time:.2f} seconds")

        # apply elastic registration to the moving image
        self.ui.CalculatingElasticRegistrationText.setText(
            "Applying the transform to generate the registered image. Please Wait...")
        QtWidgets.QApplication.processEvents()
        im_moving_elastic = self.register_image_elastic(im_moving, self.D)
        self.im_moving_reg_elastic = self.array_to_pixmap(im_moving_elastic)

        # apply elastic registration to the fiducial points
        self.ui.CalculatingElasticRegistrationText.setText("Applying the transform to the fiducial points. Please Wait...")
        QtWidgets.QApplication.processEvents()
        szz = (self.im_fixed.width(), self.im_fixed.height())
        self.pts_moving_reg_elastic = self.register_points_elastic(self.pts_moving_reg, szz, self.Dinv, scale=None)

        # calculate the RMSE for the elastically registered points
        pts_fixed = np.delete(self.pts_fixed, 0, axis=0)
        dist = (pts_fixed[:, 0] - self.pts_moving_reg_elastic[:, 0]) ** 2 + (pts_fixed[:, 1] - self.pts_moving_reg_elastic[:, 1]) ** 2
        self.rmse_reg_elastic = round(np.sqrt(np.mean(dist)))

        # convert the elastically registered image back to a pixmap and view an overlay
        pixmap_fixed = self.adjust_brightness_contrast(self.im_fixed, self.fixed_contrast, self.fixed_brightness)
        pixmap_moving = self.adjust_brightness_contrast(self.im_moving_reg_elastic, self.moving_contrast,
                                                        self.moving_brightness)
        self.im_overlay_reg_elastic = self.make_overlay_image(pixmap_fixed, pixmap_moving)

        # update the text labels above the images
        self.ui.FiducialRegisteredImageFrameHeaderText.setText(
            f"Fiducial Registration Overlay (RMSE: {round(self.rmse_reg)} pixels).")
        self.ui.ElasticRegisteredImageFrameHeaderText.setText(
            f"Fiducial + Elastic Registration Overlay (RMSE: {round(self.rmse_reg_elastic)} pixels).")

        # update the tab view and button accessability
        self.ui.DisableFrame_E2.setVisible(False)
        self.ui.CalculatingElasticRegistrationText.setVisible(False)
        self.ui.ClockFrame_E.setVisible(False)
        self.ui.ElasticRegistrationControlsFrame.setVisible(False)
        self.ui.CalculateElasticRegistrationButton.setVisible(False)
        self.ui.QuitElasticRegistrationButton.setVisible(False)
        self.ui.QuitElasticRegistrationButton2.setVisible(True)
        self.ui.QuitElasticRegistrationButton2.setEnabled(True)
        self.ui.QuitElasticRegistrationButton2.setStyleSheet(self.active_button_style)
        self.ui.SaveRegistrationResultsButton_E.setVisible(True)
        self.ui.SaveRegistrationResultsButton_E.setEnabled(True)
        self.ui.SaveRegistrationResultsButton_E.setStyleSheet(self.style_button_green)
        self.ui.ReturnToFiducialsTabButton_E.setVisible(True)
        self.ui.ReturnToFiducialsTabButton_E.setEnabled(True)
        self.ui.ReturnToFiducialsTabButton_E.setStyleSheet(self.active_button_style)
        self.ui.ImageViewControlsFrame_E.setVisible(True)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.view_squares = 0
        self.edit_which_image = 0
        self.reset_transformations()
        self.update_button_color()
        self.edit_which_image = 1
        self.reset_transformations()
        self.edit_which_pt_color = 1
        self.update_button_color()
        self.ui.UnregisteredImageFrameHeaderText.setText("Test view elastic reg overlay (ignore fiducials)")
        QtWidgets.QApplication.processEvents()

    def invert_D_optimized(self, D, skk=5, skk2=5):
        """Fast inverse of a dense displacement field"""
        rows, cols, _ = D.shape

        # Generate full coordinates
        xx, yy = np.meshgrid(np.arange(1, cols + 1), np.arange(1, rows + 1))
        xnew = xx + D[:, :, 0]
        ynew = yy + D[:, :, 1]

        # Subsample
        x_flat = xnew[::skk, ::skk].ravel()
        y_flat = ynew[::skk, ::skk].ravel()
        D1_flat = D[::skk, ::skk, 0].ravel()
        D2_flat = D[::skk, ::skk, 1].ravel()

        # Points and values
        points_sub = np.column_stack((x_flat, y_flat))
        values_D1 = -D1_flat
        values_D2 = -D2_flat

        # Coarse grid
        xx_coarse, yy_coarse = np.meshgrid(
            np.arange(1, cols + 1, skk2), np.arange(1, rows + 1, skk2)
        )
        grid_points = np.column_stack((xx_coarse.ravel(), yy_coarse.ravel()))

        # Interpolate using griddata (much faster than LinearNDInterpolator)
        d0_interp = griddata(points_sub, values_D1, grid_points, method='linear', fill_value=0.0)
        d1_interp = griddata(points_sub, values_D2, grid_points, method='linear', fill_value=0.0)

        # Reshape
        d0_interp = d0_interp.reshape(xx_coarse.shape)
        d1_interp = d1_interp.reshape(yy_coarse.shape)

        # Resize back to full resolution (anti-aliasing disabled for speed)
        d0_full = resize(d0_interp, (rows, cols), preserve_range=True, anti_aliasing=False)
        d1_full = resize(d1_interp, (rows, cols), preserve_range=True, anti_aliasing=False)

        inverted_displacement_field = np.stack((d0_full, d1_full), axis=-1)
        return np.nan_to_num(inverted_displacement_field)

    def invert_D(self, D):
        """Calculates the inverted displacement field
        Used in tab 6 only
        Args:
            D: elastic registration displacement field
        Returns:
            inverted_displacement_field: inverse of displacement field
        """
        # downsample factors for the inversion
        skk = 5  # to speed up processing
        skk2 = 5  # to speed up processing

        # create grids starting at 1, shift each pixel by the displacement, and flatten
        rows, cols, _ = D.shape
        xx, yy = np.meshgrid(np.arange(1, cols + 1), np.arange(1, rows + 1))
        xnew = xx + D[:, :, 0]
        ynew = yy + D[:, :, 1]

        # flatten the displacement field
        D1 = D[:, :, 0].ravel()
        D2 = D[:, :, 1].ravel()
        xnew2 = xnew.ravel()
        ynew2 = ynew.ravel()

        # subsample the data (take every skk-th element)
        points_sub = np.column_stack((xnew2[::skk], ynew2[::skk]))
        values_D1_sub = D1[::skk]
        values_D2_sub = D2[::skk]

        # create interpolators for each displacement component
        F1 = LinearNDInterpolator(points_sub, values_D1_sub)
        F2 = LinearNDInterpolator(points_sub, values_D2_sub)

        # evaluate the interpolants on a coarse grid
        xx_coarse, yy_coarse = np.meshgrid(np.arange(1, cols + 1, skk2),
                                           np.arange(1, rows + 1, skk2))
        points_coarse = np.column_stack((xx_coarse.ravel(), yy_coarse.ravel()))

        # evaluate and negate the transform
        d0_interp = -F1(points_coarse)
        d1_interp = -F2(points_coarse)
        d0_interp = d0_interp.reshape(xx_coarse.shape)
        d1_interp = d1_interp.reshape(yy_coarse.shape)

        # resize the interpolated displacement field to the original resolution
        inverted_displacement_field = np.zeros((rows, cols, 2))
        inverted_displacement_field[:, :, 0] = resize(d0_interp, (rows, cols), preserve_range=True)
        inverted_displacement_field[:, :, 1] = resize(d1_interp, (rows, cols), preserve_range=True)
        inverted_displacement_field = np.nan_to_num(inverted_displacement_field)

        return inverted_displacement_field


    def quit_elastic_registration(self):
        """Exits the elastic registration tab and returns to tab 5
        Used in tab 6 only
        Args:
            none, draws from 'self'
        Returns:
            No variables returned, the app will return to the icp-registration overlay in tab 5.
        """
        # update location of navigation button and keyboard shortcuts
        self.ui.WhatNextControlFrame.setParent(self.ui.ViewOverlayTabName)
        self.ui.NavigationButton.setParent(self.ui.ViewOverlayTabName)
        self.ui.KeyboardShortcutsButton.setParent(self.ui.ViewOverlayTabName)

        # close navigation button
        self.close_navigation_tab()

        # go to overlay tab
        self.ui.tabWidget.setCurrentIndex(self.overlay_tab)


    def increase_elastic_tile_size(self):
        """Increases the tile size setting for the elastic registration calculation
        Used in tab 6 only
        Args:
            none, draws from 'self'
        Returns:
            No variables returned, tile size setting will be increased.
        """
        # increase the tile size for elastic registration
        self.elastic_tilesize = self.elastic_tilesize + 25
        self.ui.TileSizeText.setHtml(f"<div align='right'>Size:<br>{self.elastic_tilesize}</div>")
        self.edit_which_image = 0
        self.update_image_view()


    def decrease_elastic_tile_size(self):
        """Deduces the tile size setting for the elastic registration calculation
        Used in tab 6 only
        Args:
            none, draws from 'self'
        Returns:
            No variables returned, tile size setting will be decreased.
        """
        # decrease the tile size for elastic registration
        self.elastic_tilesize = self.elastic_tilesize - 25
        self.ui.TileSizeText.setHtml(f"<div align='right'>Size:<br>{self.elastic_tilesize}</div>")
        self.edit_which_image = 0
        self.update_image_view()


    def increase_elastic_tile_spacing(self):
        """Increases the tile spacing setting for the elastic registration calculation
        Used in tab 6 only
        Args:
            none, draws from 'self'
        Returns:
            No variables returned, tile spacing setting will be increased.
        """
        # increase the tile spacing for elastic registration
        self.elastic_tilespacing = self.elastic_tilespacing + 25
        self.ui.TileSpacingText.setHtml(f"<div align='right'>Spacing:<br>{self.elastic_tilespacing}</div>")
        self.edit_which_image = 0
        self.update_image_view()


    def decrease_elastic_tile_spacing(self):
        """Reduces the tile spacing setting for the elastic registration calculation
        Used in tab 6 only
        Args:
            none, draws from 'self'
        Returns:
            No variables returned, tile spacing setting will be decreased.
        """
        # decrease the tile spacing for elastic registration
        self.elastic_tilespacing = self.elastic_tilespacing - 25
        self.ui.TileSpacingText.setHtml(f"<div align='right'>Spacing:<br>{self.elastic_tilespacing}</div>")
        self.edit_which_image = 0
        self.update_image_view()


    def add_square_to_image(self, pixmap, xy):
        """Embed a single square outline into pixmap image objects.
        Used in tab 6 only
        Args:
            pixmap: pixmap object containing the image to edit
            xy: center of the current elastic registration tile
        Returns:
            pixmap_square: pixmap object containing the image with squares overlayed
        """
        image = self.pixmap_to_array(pixmap)
        thickness = self.squaresThickness
        cc = self.squaresColor
        outline_color = (cc.blue(), cc.green(), cc.red(), 255)

        # calculate the centers and offsets of the squares
        image_center_x = xy[0]
        image_center_y = xy[1]
        rad = self.elastic_tilesize // 2

        # draw the outline of the square
        top_left = (image_center_x - rad, image_center_y - rad)
        bottom_right = (image_center_x + rad, image_center_y + rad)
        if xy[2] == 1:  # this tile contains tissue (was analyzed in elastic registration)
            # draw a filled square
            cv2.rectangle(image, top_left, bottom_right, outline_color, -1)  # -1 for filled
        else:  # this tile does not contain tissue (was not analyzed in elastic registration)
            # draw an outlined square
            cv2.rectangle(image, top_left, bottom_right, outline_color, thickness)

        # Convert the modified array back to QImage
        pixmap_square = self.array_to_pixmap(image)

        return pixmap_square


    def add_squares_to_image(self, pixmap):
        """Embed two square outlines into pixmap image objects.
        Used in tab 6 only
        Args:
            pixmap: pixmap object containing the image to edit
        Returns:
            pixmap_square: pixmap object containing the image with squares overlayed
        """
        image = self.pixmap_to_array(pixmap)
        thickness = self.squaresThickness
        cc = self.squaresColor
        outline_color = (cc.blue(), cc.green(), cc.red(), 255)

        # calculate the centers and offsets of the squares
        image_height, image_width, _ = image.shape  # Image dimensions
        image_center_x = image_width // 2
        image_center_y = image_height // 2
        offset = self.elastic_tilespacing // 2
        centers = [(image_center_x - offset, image_center_y - offset), (image_center_x + offset, image_center_y + offset)]
        square_radius = self.elastic_tilesize // 2

        # draw the outline of the square
        for cx, cy in centers:
            top_left = (cx - square_radius, cy - square_radius)
            bottom_right = (cx + square_radius, cy + square_radius)
            cv2.rectangle(image, top_left, bottom_right, outline_color, thickness)

        # convert the modified array back to QImage
        pixmap_square = self.array_to_pixmap(image)

        return pixmap_square


    def make_tissue_mask(self, image, mode_val):
        """Calculates a logical image identifying tissue regions of the image
        Used in tab 6 only
        Args:
            image: RGB image used to calculate the tissue mask
            mode_val: mode of each channel of image
        Returns:
            image_grey: greyscale version of image
            image_mask: logical tissue mask of image
        """
        # determine whether the image is brightfield or flourescent and make the tissue mask
        image_grey = np.mean(image[:, :, :3], axis=-1).astype(np.uint8)  # im_ref = im_ref[:, :, :3]

        mode_val = sum(mode_val) / len(mode_val)
        if mode_val < 200:  # flourescent image
            image_mask = image_grey > 10
            image_grey = 255 - image_grey
        else:  # brightfield image
            image_mask = image_grey < 215

        return image_grey, image_mask


    def save_registration_results_elastic(self):
        """Saves the elastic registration metadata
        Used in tab 6 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but saves the elastic registration metadata as a .pkl file
        """
        # change some visibility settings
        self.close_navigation_tab()
        self.ui.DisableFrame_E1.setVisible(True)
        self.ui.SaveRegistrationResultsButton_E.setEnabled(False)
        self.ui.SaveRegistrationResultsButton_E.setStyleSheet(self.inactive_button_style)
        self.ui.QuitElasticRegistrationButton2.setEnabled(False)
        self.ui.QuitElasticRegistrationButton2.setStyleSheet(self.inactive_button_style)
        self.ui.ReturnToFiducialsTabButton_E.setEnabled(False)
        self.ui.ReturnToFiducialsTabButton_E.setStyleSheet(self.inactive_button_style)
        self.ui.NavigationButton.setEnabled(False)
        self.ui.NavigationButton.setStyleSheet(self.inactive_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(False)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.inactive_button_style)
        QtWidgets.QApplication.processEvents()

        # save registration info
        filename, _ = os.path.splitext(self.moving_image_filename)
        filename = filename + ".pkl"
        output_folder = os.path.join(self.job_folder, self.results_name, "Registration transforms", "Elastic")
        file_path = os.path.join(output_folder, filename)

        # Check if the folder exists, and create it if it doesn't
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save variables to the pkl file
        with open(file_path, 'wb') as file:
            pickle.dump({
                'D': self.D,
                'Dinv': self.Dinv,
                'RMSE_Elastic': self.rmse_reg_elastic,
                'elastic_tilesize': self.elastic_tilespacing,
                'elastic_tilespacing': self.elastic_tilesize,
                'n_buffer_pix': 50},
                file)

        # save the images
        self.save_registered_image_elastic()

        # what to do next
        self.ui.DisableFrame_E1.setVisible(False)
        self.ui.ReturnToFiducialsTabButton_E.setEnabled(True)
        self.ui.ReturnToFiducialsTabButton_E.setStyleSheet(self.active_button_style)
        self.ui.NavigationButton.setEnabled(True)
        self.ui.NavigationButton.setStyleSheet(self.active_button_style)
        self.ui.KeyboardShortcutsButton.setEnabled(True)
        self.ui.KeyboardShortcutsButton.setStyleSheet(self.active_button_style)
        self.ui.QuitElasticRegistrationButton2.setEnabled(True)
        self.ui.QuitElasticRegistrationButton2.setStyleSheet(self.active_button_style)


    def save_registered_image_elastic(self):
        """Saves the elastically registered image
        Used in tab 6 only
        Args:
            none, draws from 'self'
        Returns:
            no variables output, but saves the elastically registered image as a .jpg file
        """
        # save registered moving image
        output_folder = os.path.join(self.job_folder, self.results_name, "Registered images", "Elastic")
        # Check if the folder exists, and create it if it doesn't
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        filename, _ = os.path.splitext(self.moving_image_filename)
        filename = filename + ".jpg"
        filepath = os.path.join(output_folder, filename)
        self.im_moving_reg_elastic.save(filepath, "JPG")

        # save the fixed image if it does not already exist
        filename, _ = os.path.splitext(self.fixed_image_filename)
        filename = filename + ".jpg"
        filepath = os.path.join(output_folder, filename)
        if not os.path.exists(filepath):
            self.im_fixed.save(filepath, "JPG")


    @staticmethod
    def _reg_ims_elastic(im_ref_arr: np.ndarray, im_moving_arr: np.ndarray, rescale: int) -> np.ndarray:
        """Calculates registration translation only for a pair of tissue images.
        Original MATLAB function called "reg_ims_ELS". Original function also included a
        flag to return the registered moving image and the correlation coefficient.
        From Maggie pyCODA package
        Used in tab 6 only
        Args:
            im_ref_arr: Reference image.
            im_moving_arr: Moving image.
            rescale: Resize factor for downsampling.
        Returns:
            Displacement in x and y directions.
        """
        a_ref = cv2.resize(
            im_ref_arr,
            (round(im_ref_arr.shape[1] / rescale), round(im_ref_arr.shape[0] / rescale)),
            interpolation=cv2.INTER_LINEAR,
        )
        amv = cv2.resize(
            im_moving_arr,
            (
                round(im_moving_arr.shape[1] / rescale),
                round(im_moving_arr.shape[0] / rescale),
            ),
            interpolation=cv2.INTER_LINEAR,
        )
        xyt = MainWindow.calculate_dislocation(a_ref, amv)
        return -(xyt * rescale)


    @staticmethod
    def _get_nn_grids(grid: np.ndarray) -> np.ndarray:
        """Get nearest neighbor grids for a displacement map.
        From Maggie pyCODA package
        Used in tab 6 only
        Args:
            grid: Displacement map.
        Returns:
            Nearest neighbor grids.
        """

        NN_GRIDS_FILTERS = [
            np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),
            np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]]),
            np.array([[0, 0, 1], [0, 0, 0], [0, 0, 0]]),
            np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]]),
            np.array([[0, 0, 0], [0, 0, 1], [0, 0, 0]]),
            np.array([[0, 0, 0], [0, 0, 0], [1, 0, 0]]),
            np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0]]),
            np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]]),
        ]

        if grid.dtype == bool or grid.dtype == np.bool_:
            grid = grid.astype(np.uint8)
        nn_grids = [
            cv2.filter2D(grid, -1, f, borderType=cv2.BORDER_CONSTANT)
            for f in NN_GRIDS_FILTERS
        ]
        return np.stack(nn_grids, axis=-1)


    @staticmethod
    def _fill_vals(xgg: np.ndarray, ygg: np.ndarray, cc: np.ndarray, xystd: bool = False
                   ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Fill in values in the displacement map that are outside the tissue region.
        From Maggie pyCODA package
        Used in tab 6 only
        Args:
            xgg: X displacement map to smooth.
            ygg: Y displacement map to smooth.
            cc: Boolean map of which locations in xgg/ygg should be smoothed.
            xystd: True if standard deviation of x and y should be calculated and returned.
        Returns:
            Smoothed x displacement map, smoothed y displacement map, denominator map for
            smoothing, standard deviation of x displacement map, standard deviation of y
            displacement map.
        """
        FILL_VALS_SURROUNDING_PIXELS = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

        denom = cv2.filter2D(
            (~cc).astype(np.uint8),
            -1,
            FILL_VALS_SURROUNDING_PIXELS,
            borderType=cv2.BORDER_CONSTANT,
        )
        if xystd:
            grid_x = MainWindow._get_nn_grids(xgg)
            grid_y = MainWindow._get_nn_grids(ygg)
            grid_d = MainWindow._get_nn_grids(~cc)
            grid_x = (grid_x - xgg[:, :, np.newaxis]) ** 2 * grid_d
            grid_y = (grid_y - ygg[:, :, np.newaxis]) ** 2 * grid_d
            sxgg = np.sqrt(
                np.divide(
                    np.sum(grid_x, axis=-1),
                    denom,
                    out=np.zeros_like(grid_x[:, :, 0]),
                    where=denom != 0,
                )
            )
            sygg = np.sqrt(
                np.divide(
                    np.sum(grid_y, axis=-1),
                    denom,
                    out=np.zeros_like(grid_y[:, :, 0]),
                    where=denom != 0,
                )
            )
            sxgg[cc] = 0
            sygg[cc] = 0
        else:
            sxgg = np.array([])
            sygg = np.array([])
        denom[denom == 0] = 1
        dxgg = (
                cv2.filter2D(
                    xgg, -1, FILL_VALS_SURROUNDING_PIXELS, borderType=cv2.BORDER_CONSTANT
                )
                / denom
        )
        dygg = (
                cv2.filter2D(
                    ygg, -1, FILL_VALS_SURROUNDING_PIXELS, borderType=cv2.BORDER_CONSTANT
                )
                / denom
        )
        return dxgg, dygg, denom, sxgg, sygg


    @staticmethod
    def get_bright_spot_centroid(
            image_array: np.ndarray,
            max_locs: Tuple[np.ndarray, ...],
            window_size: int = 25,
            threshold_percentile: float = 95.0,
            brightness_weight: float = 1.5,
    ) -> np.ndarray:
        """Calculates the centroid of the brightest spot in an image to sub-pixel accuracy.
        From Maggie pyCODA package
        Used in tab 6 only
        Args:
            image_array: Image to process. Particle should be bright spots on dark
                background with little noise. Often a bandpass filtered brightfield image
                or a nice fluorescent image.
            max_locs: Locations of local maxima to pixel-level accuracy. (Tuple of
                (y_locs, x_locs))
            window_size: Diameter of the window over which to average to calculate the
                centroid. Should be big enough to capture the whole particle but not so big
                that it captures others. If initial guess of center is far from the
                centroid, the window will need to be larger than the particle size.
            threshold_percentile: Pixels within the window around each candidate location
                will be excluded if they are more dim than this percentile within the
                window.
            brightness_weight: Exponent to weight the brightness values. Higher values give
                more weight to brighter pixels. 1.0 corresponds to a normal center of mass
                calculation.
        Returns:
            Centroid of the bright spots to sub-pixel accuracy.
        """
        mx = np.array(list(max_locs)).reshape(1, -1)
        kk = round(window_size / 2)
        image_max_intensity = 0
        brightest_region_mask = None
        brightest_cand_i = None
        for cand_i in range(mx.shape[0]):
            # Slice the window around the candidate
            window_im = image_array[
                        mx[cand_i, 0] - kk: mx[cand_i, 0] + kk + 1,
                        mx[cand_i, 1] - kk: mx[cand_i, 1] + kk + 1,
                        ]
            # Calculate the percentile-based threshold
            try:
                threshold = np.percentile(window_im[window_im > 0], threshold_percentile)
            except IndexError:
                # If the window is empty, skip this candidate
                continue
            # Create a mask using the threshold
            _, mask = cv2.threshold(window_im, threshold, 1, cv2.THRESH_BINARY)
            # Label the connected regions in the mask
            num_features, labeled_array, _, _ = cv2.connectedComponentsWithStats(
                mask.astype(np.uint8), connectivity=8
            )
            # Find the brightest region for this candidate
            for label_i in range(1, num_features):  # Skip the background label 0
                region_intensity = np.sum(window_im[labeled_array == label_i])
                if region_intensity > image_max_intensity:
                    image_max_intensity = region_intensity
                    brightest_region_mask = labeled_array == label_i
                    brightest_cand_i = cand_i
        if brightest_region_mask is None:
            # If no bright region was found, return the first max location
            return np.array([mx[0, 0], mx[0, 1]])
        # Calculate the weighted center of mass based on brightness for the brightest region
        offset = np.array([mx[brightest_cand_i, 0] - kk, mx[brightest_cand_i, 1] - kk])
        region_intensity = image_array[
                           offset[0]: offset[0] + window_size,
                           offset[1]: offset[1] + window_size,
                           ][brightest_region_mask]
        weighted_intensity = region_intensity ** brightness_weight
        sum_weights = np.sum(weighted_intensity)
        y_coords, x_coords = np.nonzero(brightest_region_mask)
        center_of_mass = np.array(
            [
                np.sum(y_coords * weighted_intensity) / sum_weights,
                np.sum(x_coords * weighted_intensity) / sum_weights,
            ]
        )
        # if the center of mass is outside the mask, return the max location within the mask
        if brightest_region_mask[int(center_of_mass[0]), int(center_of_mass[1])] == 0:
            return (
                    np.unravel_index(np.argmax(region_intensity), region_intensity.shape)
                    + offset
            )
        # otherwise return the center of mass
        brightest_centroid = center_of_mass + offset
        return brightest_centroid


    @staticmethod
    def calculate_dislocation(
            im_ref_arr: np.ndarray,
            im_moving_arr: np.ndarray,
            ref_yx: Optional[np.ndarray] = None,
            moving_yx: Optional[np.ndarray] = None,
            rm: Optional[np.ndarray] = None,
            rs: Optional[np.ndarray] = None,
            rg: Optional[int] = None,
    ) -> np.ndarray:
        """Estimate the dislocation between two images using cross correlation.
        From Maggie pyCODA package
        Used in tab 6 only
        Args:
            im_ref_arr: Static image array.
            im_moving_arr: Moving image array.
            ref_yx: Central point of the image pattern in the reference image (default is
                the center of the reference image).
            moving_yx: Central point of the image pattern in the moving image (default is
                the center of the moving image).
            rm: Size (y, x) of the image pattern (default is 95% of the image size to
                exclude edge effects).
            rs: Size (y, x) of the search range (default is 95% of the image size to exclude
                edge effects).
            rg: Search range (default is the max dimension of the images).
        Returns:
            np.ndarray: Estimated dislocation (x, y) of imnxt with respect to im.
        """
        imly = min(im_ref_arr.shape[0], im_moving_arr.shape[0])
        imlx = min(im_ref_arr.shape[1], im_moving_arr.shape[1])
        center_yx = np.array([imly, imlx]) // 2
        # rounding in line below is for excluding edge effects
        def_rm_rs = np.round(0.95 * center_yx).astype(int)
        # set default argument values
        if ref_yx is None:
            ref_yx = np.array([im_ref_arr.shape[0], im_ref_arr.shape[1]]) // 2
        if moving_yx is None:
            moving_yx = np.array([im_moving_arr.shape[0], im_moving_arr.shape[1]]) // 2
        if rm is None:
            rm = def_rm_rs
        if rs is None:
            rs = def_rm_rs
        if rg is None:
            rg = max(imly, imlx)
        # Slice out the ranges of the reference and moving images
        imptn = im_ref_arr[ref_yx[0] - rm[0]: ref_yx[0] + rm[0] + 1, ref_yx[1] - rm[1]: ref_yx[1] + rm[1] + 1]
        imgrid = im_moving_arr[moving_yx[0] - rs[0]: moving_yx[0] + rs[0] + 1,
                 moving_yx[1] - rs[1]: moving_yx[1] + rs[1] + 1]
        # intensity normalization (may help to take off scale effects,
        # expecially for fft-based transformation)
        imptn = (imptn - np.mean(imptn)) / np.std(imptn)
        imgrid = (imgrid - np.mean(imgrid)) / np.std(imgrid)
        cross_corr = scipy.signal.correlate(imptn, imgrid, method="fft")
        msk = cv2.circle(  # type: ignore[call-overload]
            np.zeros(cross_corr.shape, dtype=np.uint8),
            center=(cross_corr.shape[1] // 2, cross_corr.shape[0] // 2),
            radius=rg // 2,
            color=1,  # values in the circle set to 1
            thickness=-1,  # fully filled in
        )
        cross_corr_m = cross_corr * msk
        # Get the location of the centroid of the bright spot to subpixel accuracy
        centroid_yx = MainWindow.get_bright_spot_centroid(
            cross_corr_m, np.where(cross_corr_m == np.max(cross_corr_m))
        )
        # Calculate the translation from the centroid to the reference point
        translation_yx = centroid_yx - rs - rm
        return translation_yx[[1, 0]]  # Swap to xy


    @staticmethod
    def make_final_grids(
            xgg0: np.ndarray,
            ygg0: np.ndarray,
            bf: int,
            x: np.ndarray,
            y: np.ndarray,
            szim: Tuple[int, int],
    ) -> np.ndarray:
        """Creates final nonlinear image registration matrices for a pair of registered images.
        From Maggie pyCODA package
        Used in tab 6 only
        Args:
            xgg0: Initial x displacement map.
            ygg0: Initial y displacement map.
            bf: size of buffer to add to displacement maps.
            x: tile x coordinates.
            y: tile y coordinates.
            szim: Image size.
        Returns:
            Displacement map.
        """
        xgg = np.copy(xgg0)
        ygg = np.copy(ygg0)
        mxy = 75  # 50 # allow no translation larger than this cutoff
        xgg[(np.abs(xgg) > mxy) | (np.abs(ygg) > mxy)] = -5000  # non-continuous values
        # find points where registration was calculated
        cempty = xgg == -5000
        xgg[cempty] = 0
        ygg[cempty] = 0
        # replace non-continuous values with mean of neighbors
        dxgg, dygg, _, sxgg, sygg = MainWindow._fill_vals(xgg, ygg, cempty, True)
        m1 = np.divide(
            np.abs(xgg - dxgg), np.abs(dxgg), out=np.zeros_like(xgg),
            where=dxgg != 0)  # percent difference between x and mean of surrounding
        m2 = np.divide(
            np.abs(ygg - dygg), np.abs(dygg), out=np.zeros_like(ygg), where=dygg != 0)
        dd = (
                     ((sxgg > 50) | (sygg > 50))  # large standard deviation
                     | ((m1 > 5) | (m2 > 5))  # large percent difference
             ) & ~cempty
        xgg[dd] = dxgg[dd]
        ygg[dd] = dygg[dd]
        # fill in values outside tissue region with mean of neighbors
        count = 1
        while np.sum(cempty) > 0 and count < 500:
            dxgg, dygg, denom, _, _ = MainWindow._fill_vals(xgg, ygg, cempty)
            cfill = (denom > 2) & cempty  # touching 3+ numbers and needs to be filled
            xgg[cfill] = dxgg[cfill]
            ygg[cfill] = dygg[cfill]
            cempty = cempty & ~cfill  # needs to be filled and has not been filled
            count += 1

        xgg = cv2.GaussianBlur(xgg, (0, 0), 1, borderType=cv2.BORDER_REPLICATE)
        ygg = cv2.GaussianBlur(ygg, (0, 0), 1, borderType=cv2.BORDER_REPLICATE)
        # add buffer to outline of displacement map to avoid discontinuity
        xgg = np.pad(xgg, ((1, 1), (1, 1)), mode="edge")
        ygg = np.pad(ygg, ((1, 1), (1, 1)), mode="edge")
        x = np.concatenate(([1], np.unique(x) - bf, [szim[1]]))
        y = np.concatenate(([1], np.unique(y) - bf, [szim[0]]))
        # get interpolated displacement map
        xq, yq = np.meshgrid(np.arange(szim[1]) + 1, np.arange(szim[0]) + 1)
        xmesh, ymesh = np.meshgrid(x, y)
        points = np.column_stack((xmesh.flatten(), ymesh.flatten()))
        xgq = scipy.interpolate.griddata(points, xgg.flatten(), (xq, yq), method="cubic")
        ygq = scipy.interpolate.griddata(points, ygg.flatten(), (xq, yq), method="cubic")
        D = np.stack((xgq, ygq), axis=-1)

        return D


    def calculate_elastic_registration(self,
                                       im_ref: np.ndarray,
                                       im_moving: np.ndarray,
                                       mask_ref: np.ndarray,
                                       mask_moving: np.ndarray,
                                       tile_size: int,
                                       n_buffer_pix: int,
                                       intertile_distance: int,
                                       cutoff: float = 0.15,
                                       skipstep: int = 1,
                                       ) -> np.ndarray:
        """Iterative calculation of registration translation on small tiles for
           determination of nonlinear alignment of globally aligned images.
        Adapted from Maggie pyCODA package
        Used in tab 6 only
        Args:
            im_ref: Reference image.
            im_moving: Moving image.
            mask_ref: Reference mask.
            mask_moving: Moving mask.
            tile_size: Size of tiles for elastic registration.
            n_buffer_pix: number of buffer pixels (border for padding images).
            intertile_distance: Distance between registration points/tiles.
            cutoff: Minimum fraction of tissue in registration ROI.
            skipstep: Step size for the regional window around each tile.
        Returns:
            Displacement map.
        """
        szim = np.array(im_moving.shape)
        m = round(tile_size / 2)
        # pad and blur images and pad masks
        im_moving = im_moving.astype(np.float32)
        im_moving = np.pad(
            im_moving,
            pad_width=n_buffer_pix,
            mode="constant",
            constant_values=mode(im_moving[..., 0].flatten(), axis=None).mode,
        )
        im_moving = cv2.GaussianBlur(im_moving, (0, 0), 3)
        im_ref = im_ref.astype(np.float32)
        im_ref = np.pad(
            im_ref,
            pad_width=n_buffer_pix,
            mode="constant",
            constant_values=mode(im_ref[..., 0].flatten(), axis=None).mode,  # scipy.stats.mode(im_ref).mode[0]
        )
        im_ref = cv2.GaussianBlur(im_ref, (0, 0), 3)
        mask_moving = np.pad(
            mask_moving, pad_width=n_buffer_pix, mode="constant", constant_values=0
        )
        mask_ref = np.pad(
            mask_ref, pad_width=n_buffer_pix, mode="constant", constant_values=0
        )
        # make grid for registration points
        n1 = random.randint(0, round(intertile_distance / 2)) + n_buffer_pix + m
        n2 = random.randint(0, round(intertile_distance / 2)) + n_buffer_pix + m
        x, y = np.meshgrid(
            np.arange(n1, im_moving.shape[1] - m - n_buffer_pix, intertile_distance),
            np.arange(n2, im_moving.shape[0] - m - n_buffer_pix, intertile_distance),
        )
        x = x.ravel()
        y = y.ravel()
        unique_x_len = len(np.unique(x))
        unique_y_len = len(np.unique(y))
        xgg0 = -5000 * np.ones((unique_y_len, unique_x_len))
        ygg0 = -5000 * np.ones((unique_y_len, unique_x_len))
        # for each window
        num_true = 0

        # make a progress bar
        geo = self.ui.FiducialRegisteredImageDisplayFrame.geometry()
        hh = geo.height() * 0.02
        total = len(x)
        progress_step = total // 100 if total >= 100 else 1
        perc_step = 0
        perc_int = progress_step / total
        for w_i, (x_cent, y_cent) in enumerate(zip(x, y)):

            # Check if we're at a progress step
            if (w_i + 1) % progress_step == 0:
                perc_step = perc_step + perc_int
                self.ui.ClockFrame_E.setVisible(True)
                self.ui.ClockFrame_E.setGeometry(geo.x(), geo.y() + geo.height() + hh, geo.width() * perc_step,
                                                 geo.height() * 0.06)
                QtWidgets.QApplication.processEvents()

            # get the slice for the indices in the window
            window_slice = np.s_[
                           y_cent - m: y_cent + m: skipstep, x_cent - m: x_cent + m: skipstep
                           ]
            # check if there is enough tissue in the window
            if np.sum(mask_ref[window_slice]) < cutoff * (tile_size ** 2) or np.sum(mask_moving[window_slice]) < cutoff * (
                    tile_size ** 2):
                skip_this = 1
                self.xySquare = (x_cent, y_cent, 0)
            else:
                skip_this = 0
                self.xySquare = (x_cent, y_cent, 1)

                if self.ui.ViewElasticCheckBox.isChecked():
                    self.update_image_view()
                    QtWidgets.QApplication.processEvents()

            if skip_this == 1:
                continue

            num_true += 1
            # calculate registration translation
            displacements_x, displacements_y = MainWindow._reg_ims_elastic(
                im_ref[window_slice], im_moving[window_slice], 2
            )
            xgg0[w_i // unique_x_len, w_i % unique_x_len] = displacements_x
            ygg0[w_i // unique_x_len, w_i % unique_x_len] = displacements_y

        # smooth registration grid and make interpolated displacement map
        if np.max(szim) > 4000:
            szimout = np.round(szim / 5)
            x = np.round(x / 5)
            y = np.round(y / 5)
            n_buffer_pix = round(n_buffer_pix / 5)
        else:
            szimout = szim

        D = MainWindow.make_final_grids(xgg0, ygg0, n_buffer_pix, x, y, szimout)

        return D

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    from base.CODApivot_v0 import Ui_MainWindow

    window = MainWindow()
    window.show()
    sys.exit(app.exec())