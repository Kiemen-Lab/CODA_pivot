"""
Author: Ashley Kiemen (Johns Hopkins)
Date: October 23, 2024
"""
import os
import numpy as np
import pandas as pd
from datetime import datetime
from PySide6 import QtWidgets
from CODApivot_v0 import Ui_MainWindow
from PySide6.QtGui import QPixmap, QTransform, QImage, QPainter, QCursor
from PySide6.QtWidgets import QStyledItemDelegate, QFileDialog, QLabel
from PySide6.QtCore import Qt, QPointF, Signal, QPoint
from PIL import Image


class CustomDelegateMoving(QStyledItemDelegate):
    # Define a custom signal
    valueUpdatedMoving = Signal(str, int, int)  # Emit new_value, row, and column

    def __init__(self, parent=None):
        super().__init__(parent)

    def setModelData(self, editor, model, index):
        """Capture the value when exiting edit mode."""
        # Retrieve the new value entered by the user
        new_value = editor.text()
        row = index.row()
        column = index.column()

        # Emit the signal with the new value and cell coordinates
        self.valueUpdatedMoving.emit(new_value, row, column)
        # print(f"Emitted new moving value: {new_value} from ({row}, {column})")

        # Call the base class method to set the data in the model
        super().setModelData(editor, model, index)


class CustomDelegateFixed(QStyledItemDelegate):
    # Define a custom signal
    valueUpdatedFixed = Signal(str, int, int)  # Emit new_value, row, and column

    def __init__(self, parent=None):
        super().__init__(parent)

    def setModelData(self, editor, model, index):
        """Capture the value when exiting edit mode."""
        # Retrieve the new value entered by the user
        new_value = editor.text()
        row = index.row()
        column = index.column()

        # Emit the signal with the new value and cell coordinates
        self.valueUpdatedFixed.emit(new_value, row, column)
        # print(f"Emitted new fixed value: {new_value} from ({row}, {column})")

        # Call the base class method to set the data in the model
        super().setModelData(editor, model, index)

class ClickableLabel(QLabel):
    doubleClicked = Signal()  # Custom signal for double-click

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.doubleClicked.emit()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  # Use super() to initialize the parent class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setCentralWidget(self.ui.centralwidget)  # Set the central widget
        self.setWindowTitle("CODApivot")

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

        # tab 2 variables
        self.editWhichImage = 0
        self.fixed_flip_state = False
        self.fixed_rotation_angle = 0
        self.moving_flip_state = False
        self.moving_rotation_angle = 0
        self.pan_active = False  # Flag to track pan activation
        self.panning = False  # Flag to indicate if panning is in progress
        self.last_mouse_position = QPointF()  # Track the last position of the mouse
        self.fixed_pan_offset_x = 0
        self.fixed_pan_offset_y = 0
        self.moving_pan_offset_x = 0
        self.moving_pan_offset_y = 0
        self.zoom_active = False  # Flag to track zoom activation
        self.fixed_zoom_default = 1
        self.moving_zoom_default = 1
        self.fixed_brightness = 0
        self.moving_brightness = 0
        self.fixed_contrast = 1
        self.moving_contrast = 1
        self.fixed_zoom_scale = self.fixed_zoom_default  # Initialize zoom scale
        self.moving_zoom_scale = self.moving_zoom_default  # Initialize zoom scale
        self.imFixed0 = []
        self.imMoving0 = []

        # fiducial point variables
        self.ptsFixed = []
        self.add_fiducial_active = False  # Flag to track fiducial selection mode

        # Set some initial settings
        self.ui.tabWidget.setCurrentIndex(0)
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

        # Tab 2 settings
        self.fixed_image_label = ClickableLabel(self.ui.FixedImageDisplayFrame)
        self.fixed_image_label.setScaledContents(True)  # Allow scaling to fit the frame
        self.moving_image_label = ClickableLabel(self.ui.MovingImageDisplayFrame)
        self.moving_image_label.setScaledContents(True)  # Allow scaling to fit the frame

        # Tab 1 what functions to call when a button is clicked
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
        self.ui.JobFolderCheckBox.stateChanged.connect(self.checkbox_changed)
        self.ui.goToFiducialPointTabButton.clicked.connect(self.initiate_tab_2)

        # Tab 2 what functions to call when a button is clicked
        self.ui.MovingImagesComboBox.currentIndexChanged.connect(self.new_combobox_selection_changed)
        self.ui.OldMovingImagesComboBox.currentIndexChanged.connect(self.old_combobox_selection_changed)
        self.ui.LoadNewMovingImageButton.clicked.connect(self.load_new_moving_image)
        self.ui.LoadOldMovingImageButton.clicked.connect(self.load_old_moving_image)
        self.ui.PickNewMovingImageButton.clicked.connect(self.confirm_load_new_image)
        # image view settings
        self.ui.FlipButton.clicked.connect(self.flip_image_y)
        self.ui.RotateButton.clicked.connect(self.rotate_label_ui)
        self.ui.ZoomPanButton.clicked.connect(self.toggle_zoom_mode)
        self.ui.brightnessDownButton.clicked.connect(self.decrease_brightness)
        self.ui.brightnessUpButton.clicked.connect(self.increase_brightness)
        self.ui.contrastDownButton.clicked.connect(self.decrease_contrast)
        self.ui.contrastUpButton.clicked.connect(self.increase_contrast)
        self.ui.RevertButton.clicked.connect(self.reset_transformations)
        #self.promote_text_to_clickable_label(self.ui.fixed_image_border, self.doubleclick_fixed_image_tab2)
        #self.promote_text_to_clickable_label(self.ui.moving_image_border, self.doubleclick_moving_image_tab2)
        #self.fixed_image_label.pointClicked.connect(self.handle_fiducial_click)
        self.fixed_image_label.raise_()
        self.fixed_image_label.doubleClicked.connect(self.doubleclick_fixed_image_tab2)
        self.moving_image_label.doubleClicked.connect(self.doubleclick_moving_image_tab2)
        self.fixed_image_label.setAlignment(Qt.AlignCenter)
        self.ui.AddFiducialButton.clicked.connect(self.toggle_add_fiducial_mode)

        # Create and set the custom delegate, connect the delegate's signal to a slot in MainWindow
        self.delegate = CustomDelegateFixed(self.ui.fixedImageTableWidget)
        self.ui.fixedImageTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedFixed.connect(self.handle_value_update_fixed)
        self.delegate = CustomDelegateMoving(self.ui.movingImageTableWidget)
        self.ui.movingImageTableWidget.setItemDelegate(self.delegate)
        self.delegate.valueUpdatedMoving.connect(self.handle_value_update_moving)

        # initial populate of tables
        self.populate_fixed_table()
        self.populate_moving_table()
        self.populate_project_table()

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
        self.inactiveButton = """
                                    QPushButton {
                                        background-color: #5a5a5a;
                                        border: 1px solid #424242;
                                        color: #424242;
                                        border-radius: 5px; /* Optional: Rounded corners */
                                        padding: 5px; /* Optional: Padding around text */
                                    }
                                                """
        self.activeLabel = """
                                    QLabel { 
                                        background-color: transparent;
                                        border: 5px solid #40ad40; /* Border  */
                                    }
                                            """

        self.inactiveLabel = """
                                    QLabel { 
                                        background-color: transparent;
                                        border: 3px solid #e6e6e6; /* Border  */
                                    }
                                            """
        self.activeFrame = """
                                QFrame { 
                                    background-color: #3d4a3d;
                                }
                                            """

        self.inactiveFrame = """ # 
                                    QFrame { 
                                        background-color: #4b4b4b;
                                    }
                                            """

    def handle_fiducial_click(self, x, y):

        #local_pos = self.fixed_image_label.mapFromGlobal(event.globalPosition().toPoint())

        if self.add_fiducial_active:
            # Get the label's global top-left position
            label_global_top_left = self.fixed_image_label.mapToGlobal(
                self.fixed_image_label.rect().topLeft()
            )
            # Calculate position relative to the label
            label_x = x - label_global_top_left.x()
            label_y = y - label_global_top_left.y()

            print(f"Clicked global position: ({x}, {y})")
            print(f"Label global top-left position: ({label_global_top_left.x()}, {label_global_top_left.y()})")
            print(f"Label-relative position (manual calc): ({label_x}, {label_y})")

            # Check if click is within the QLabel bounds
            if not (0 <= label_x < self.fixed_image_label.width() and
                    0 <= label_y < self.fixed_image_label.height()):
                print("Clicked outside the image bounds.")
                return

            # Adjust for the displayed image scaling (e.g., aspect ratio adjustments)
            pixmap = self.fixed_image_label.pixmap()
            if not pixmap:
                print("No image loaded in QLabel.")
                return

            pixmap_width, pixmap_height = pixmap.width(), pixmap.height()
            label_width, label_height = self.fixed_image_label.width(), self.fixed_image_label.height()

            # Compute offsets if the image is centered with padding
            scale_factor = min(label_width / pixmap_width, label_height / pixmap_height)
            image_display_width = pixmap_width * scale_factor
            image_display_height = pixmap_height * scale_factor
            x_offset = (label_width - image_display_width) / 2
            y_offset = (label_height - image_display_height) / 2

            # Adjust coordinates to image space
            image_x = (label_x - x_offset) / scale_factor
            image_y = (label_y - y_offset) / scale_factor

            # Ensure click is within image bounds
            if not (0 <= image_x < pixmap_width and 0 <= image_y < pixmap_height):
                print("Clicked outside the displayed image bounds.")
                return

            # Adjust for pan and zoom transformations
            adjusted_x = (image_x - self.fixed_pan_offset_x) / self.fixed_zoom_scale
            adjusted_y = (image_y - self.fixed_pan_offset_y) / self.fixed_zoom_scale

            print(f"Adjusted image coordinates: ({adjusted_x:.2f}, {adjusted_y:.2f})")
            self.ptsFixed.append((adjusted_x, adjusted_y))
            self.draw_fiducial_marker(adjusted_x, adjusted_y)

    def draw_fiducial_marker(self, x, y):
        """Draw a marker on the fixed image at the specified coordinates."""
        pixmap = self.fixed_image_label.pixmap()
        if pixmap:
            painter = QPainter(pixmap)
            painter.setPen(Qt.red)
            painter.setBrush(Qt.red)
            radius = 5  # Radius of the marker
            painter.drawEllipse(QPointF(x, y), radius, radius)
            painter.end()
            self.fixed_image_label.setPixmap(pixmap)

    def toggle_add_fiducial_mode(self):
        """Toggle fiducial selection mode."""
        self.add_fiducial_active = not self.add_fiducial_active

        if self.add_fiducial_active:
            print("Fiducial selection mode activated. Click on the image to add points.")
            # Use the custom large crosshair cursor
            crosshair_cursor = self.create_large_crosshair_cursor()
            self.setCursor(crosshair_cursor)
        else:
            print("Fiducial selection mode deactivated.")
            # Reset the cursor to default
            self.setCursor(Qt.ArrowCursor)

    def closeEvent(self, event):
        # Reset the cursor to default before closing
        self.setCursor(Qt.ArrowCursor)
        super().closeEvent(event)

    def create_large_crosshair_cursor(self):
        # Create a larger pixmap for the crosshair
        pixmap_size = 512  # Increase the size of the pixmap
        pixmap = QPixmap(pixmap_size, pixmap_size)
        pixmap.fill(Qt.transparent)  # Transparent background

        # Draw the extended crosshair
        painter = QPainter(pixmap)
        painter.setPen(Qt.black)  # Black color for the crosshair
        # Vertical line
        painter.drawLine(pixmap_size // 2, 0, pixmap_size // 2, pixmap_size)
        # Horizontal line
        painter.drawLine(0, pixmap_size // 2, pixmap_size, pixmap_size // 2)
        painter.end()

        # Set the center of the crosshair to the hotspot
        return QCursor(pixmap, pixmap_size // 2, pixmap_size // 2)

    def increase_brightness(self):
        # Exit zoom or pan mode if necessary
        self.zoom_active = False
        self.pan_active = False
        self.panning = False  # Reset panning state
        self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text

        if self.editWhichImage == 0:  # fixed image
            self.fixed_brightness = self.fixed_brightness + 5
        else:  # moving image
            self.moving_brightness = self.moving_brightness + 5
        self.update_image_view()

    def decrease_brightness(self):
        # Exit zoom or pan mode if necessary
        self.zoom_active = False
        self.pan_active = False
        self.panning = False  # Reset panning state
        self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text

        if self.editWhichImage == 0:  # fixed image
            self.fixed_brightness = self.fixed_brightness - 5
        else:  # moving image
            self.moving_brightness = self.moving_brightness - 5
        self.update_image_view()

    def increase_contrast(self):
        # Exit zoom or pan mode if necessary
        self.zoom_active = False
        self.pan_active = False
        self.panning = False  # Reset panning state
        self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text

        if self.editWhichImage == 0:  # fixed image
            self.fixed_contrast = self.fixed_contrast + 0.05
        else:  # moving image
            self.moving_contrast = self.moving_contrast + 0.05
        self.update_image_view()

    def decrease_contrast(self):
        # Exit zoom or pan mode if necessary
        self.zoom_active = False
        self.pan_active = False
        self.panning = False  # Reset panning state
        self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text

        if self.editWhichImage == 0:  # fixed image
            self.fixed_contrast = self.fixed_contrast - 0.05
        else:  # moving image
            self.moving_contrast = self.moving_contrast - 0.05
        self.update_image_view()

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

    def slider_value_changed(self):

        # Exit zoom or pan mode if necessary
        self.zoom_active = False
        self.pan_active = False
        self.panning = False  # Reset panning state
        self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text

        if self.editWhichImage == 0:  # fixed image
            self.ui.fixed_image_border.setStyleSheet(self.activeLabel)
            self.ui.moving_image_border.setStyleSheet(self.inactiveLabel)
            self.ui.FixedImageDisplayFrame.setStyleSheet(self.activeFrame)
            self.ui.MovingImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        else:  # moving image
            self.ui.fixed_image_border.setStyleSheet(self.inactiveLabel)
            self.ui.moving_image_border.setStyleSheet(self.activeLabel)
            self.ui.FixedImageDisplayFrame.setStyleSheet(self.inactiveFrame)
            self.ui.MovingImageDisplayFrame.setStyleSheet(self.activeFrame)

    def initiate_tab_2(self):

        # initial button settings
        self.ui.ChooseMovingImageFrame.setVisible(True)
        self.ui.CalculatingICPText.setVisible(False)
        self.ui.LoadNewMovingImageButton.setEnabled(False)
        self.ui.LoadOldMovingImageButton.setEnabled(False)
        self.ui.ImageViewControlsFrame.setVisible(False)
        self.ui.FiducialPointControlsFrame.setVisible(False)
        self.ui.PickNewMovingImageButton.setVisible(False)
        self.ui.fixed_image_border.setStyleSheet(self.inactiveLabel)
        self.ui.moving_image_border.setStyleSheet(self.inactiveLabel)
        self.ui.FixedImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        self.ui.MovingImageDisplayFrame.setStyleSheet(self.inactiveFrame)

        # make the text black for disabled buttons
        self.ui.LoadNewMovingImageButton.setStyleSheet(self.inactiveButton)
        self.ui.LoadOldMovingImageButton.setStyleSheet(self.inactiveButton)

        # populate dropdown lists
        self.populate_moving_images_combo_box()

        # load and display fixed image
        image_path = os.path.join(self.pthFixed, self.nmFixed)

        # Load the image
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return
        self.imFixed0 = QPixmap(image_path)  # store the original pixmap

        # Calculate zoom_default
        image_width = self.imFixed0.width()
        image_height = self.imFixed0.height()
        frame_width = self.ui.FixedImageDisplayFrame.width()
        frame_height = self.ui.FixedImageDisplayFrame.height()
        width_scale = frame_width / image_width
        height_scale = frame_height / image_height
        self.fixed_zoom_default = min(width_scale, height_scale)

        # display image
        self.editWhichImage = 0
        self.reset_transformations()
        self.update_image_view()
        self.editWhichImage = 1
        self.imMoving0 = []
        self.reset_transformations()
        self.update_image_view()

        # go to Tab 2
        self.ui.tabWidget.setCurrentIndex(1)

    def flip_image_y(self):
        """Flip the image horizontally while ensuring it fits within bounds."""

        # exit zoom or pan mode if necessary
        self.zoom_active = False
        self.pan_active = False
        self.panning = False  # Reset panning state
        self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text

        # Toggle the flip state
        if self.editWhichImage == 0:  # Fixed image
            self.fixed_flip_state = not self.fixed_flip_state
            self.fixed_pan_offset_x = -self.fixed_pan_offset_x
        else:  # Moving image
            self.moving_flip_state = not self.moving_flip_state
            self.moving_pan_offset_x = -self.moving_pan_offset_x

        # Update the view
        self.update_image_view()

    def rotate_label_ui(self):
        """Rotate the image while ensuring pan offsets align with the rotation."""

        # Exit zoom or pan mode if necessary
        self.zoom_active = False
        self.pan_active = False
        self.panning = False  # Reset panning state
        self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text

        # Update the rotation angle
        if self.editWhichImage == 0:  # Fixed image
            self.fixed_rotation_angle = (self.fixed_rotation_angle + 90) % 360
        else:  # Moving image
            self.moving_rotation_angle = (self.moving_rotation_angle + 90) % 360

        # Apply transformations
        self.update_image_view()

    def toggle_zoom_mode(self):
        """Toggle zoom mode on or off."""
        self.zoom_active = not self.zoom_active
        self.pan_active = not self.pan_active
        self.panning = not self.panning  # Reset panning state
        if self.zoom_active:
            self.ui.ZoomPanButton.setText("Quit")
        else:
            self.ui.ZoomPanButton.setText("Zoom/Pan")

    def update_image_view(self):
        """Update the image view with all transformations (flip, rotate, zoom, and pan) preserved."""
        # Determine which image is being edited
        if self.editWhichImage == 0:  # Fixed image
            pixmap = self.imFixed0
            label = self.fixed_image_label
            flip_state = self.fixed_flip_state
            rotation_angle = self.fixed_rotation_angle
            zoom_scale = self.fixed_zoom_scale
            cc = self.fixed_contrast
            bb = self.fixed_brightness
        else:  # Moving image
            pixmap = self.imMoving0
            label = self.moving_image_label
            flip_state = self.moving_flip_state
            rotation_angle = self.moving_rotation_angle
            zoom_scale = self.moving_zoom_scale
            cc = self.moving_contrast
            bb = self.moving_brightness

        if pixmap is not None:
            if pixmap == []:
                label.clear()
                return

            if bb != 0 or cc != 1:
                pixmap = self.adjust_brightness_contrast(pixmap, cc, bb)

            # Create a transformation matrix
            transform = QTransform()

            # Apply flip, rotation, and zoom
            if flip_state:
                transform.scale(-1, 1)
            transform.rotate(rotation_angle)
            transform.scale(zoom_scale, zoom_scale)
            transformed_pixmap = pixmap.transformed(transform, mode=Qt.SmoothTransformation)
            label.setPixmap(transformed_pixmap)
            label.resize(transformed_pixmap.size())

            # Apply pan offsets
            offset_x, offset_y = self._apply_flip_and_rotation()
            parent_rect = label.parent().rect()
            new_x = offset_x + (parent_rect.width() - label.width()) // 2
            new_y = offset_y + (parent_rect.height() - label.height()) // 2
            label.move(int(new_x), int(new_y))

            # add current fiducial points

    def adjust_brightness_contrast(self, pixmap, contrast, brightness):
        # Convert QPixmap to QImage
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format_RGB888)

        # Get width, height
        width = image.width()
        height = image.height()

        # Create a NumPy array from the image bits
        ptr = image.bits()
        array = np.array(ptr, dtype=np.uint8).reshape((height, width, 3))  # Ensure correct shape

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
        if self.pan_active and event.button() == Qt.LeftButton:
            self.panning = True
            self.last_mouse_position = event.globalPosition()  # Store the initial mouse position
        elif self.add_fiducial_active:
            print("add fiducial point")
            local_pos = self.fixed_image_label.mapFromGlobal(event.globalPosition().toPoint())
            self.handle_fiducial_click(local_pos.x(), local_pos.y())

    def mouseMoveEvent(self, event):
        """Handle mouse move events for panning."""

        if self.add_fiducial_active:
            return
        elif self.pan_active and self.panning:
            delta = event.globalPosition() - self.last_mouse_position
            self.last_mouse_position = event.globalPosition()

            # get flip and angle
            if self.editWhichImage == 0:  # Fixed image
                angle = self.fixed_rotation_angle
                flip = self.fixed_flip_state
            else:  # moving image
                angle = self.moving_rotation_angle
                flip = self.moving_flip_state

            # remove the effect of rotation and flipping
            if angle == 90:
                if flip:
                    offset_x = -delta.y()
                    offset_y = delta.x()
                else:
                    offset_x = delta.y()
                    offset_y = -delta.x()
            elif angle == 180:
                offset_x = -delta.x()
                offset_y = -delta.y()
            elif angle == 270:
                if flip:
                    offset_x = delta.y()
                    offset_y = -delta.x()
                else:
                    offset_x = -delta.y()
                    offset_y = delta.x()
            else:
                offset_x = delta.x()
                offset_y = delta.y()

            # Update pan offsets
            if self.editWhichImage == 0:  # Fixed image
                self.fixed_pan_offset_x += offset_x
                self.fixed_pan_offset_y += offset_y
            else:  # moving image
                self.moving_pan_offset_x += offset_x
                self.moving_pan_offset_y += offset_y

            # Reapply transformations
            self.update_image_view()

    def _apply_flip_and_rotation(self):

        if self.editWhichImage == 0:  # Fixed image
            angle = self.fixed_rotation_angle
            flip = self.fixed_flip_state
            offset_x = self.fixed_pan_offset_x
            offset_y = self.fixed_pan_offset_y
        else:  # moving image
            angle = self.moving_rotation_angle
            flip = self.moving_flip_state
            offset_x = self.moving_pan_offset_x
            offset_y = self.moving_pan_offset_y

        # account for the effect of rotation
        if angle == 90:
            if flip:
                return offset_y, -offset_x
            else:
                return -offset_y, offset_x
        elif angle == 180:
            return -offset_x, -offset_y
        elif angle == 270:
            if flip:
                return -offset_y, offset_x
            else:
                return offset_y, -offset_x
        else:  # 0 degrees
            return offset_x, offset_y

    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        if self.pan_active and event.button() == Qt.LeftButton:
            self.panning = False

    def reset_transformations(self):
        """Reset all transformations to their defaults."""

        # Exit zoom or pan mode if necessary
        self.zoom_active = False
        self.pan_active = False
        self.panning = False  # Reset panning state
        self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text

        if self.editWhichImage == 0:  # Fixed image
            self.fixed_flip_state = False
            self.fixed_rotation_angle = 0
            self.fixed_zoom_scale = self.fixed_zoom_default
            self.fixed_pan_offset_x = 0
            self.fixed_pan_offset_y = 0
            self.fixed_brightness = 0
            self.fixed_contrast = 1
        else:  # Moving image
            self.moving_flip_state = False
            self.moving_rotation_angle = 0
            self.moving_zoom_scale = self.moving_zoom_default
            self.moving_pan_offset_x = 0
            self.moving_pan_offset_y = 0
            self.moving_brightness = 0
            self.moving_contrast = 1
        self.update_image_view()

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming."""
        if not self.zoom_active:
            return

        # Determine the image being edited (fixed or moving)
        if self.editWhichImage == 0:  # Fixed image
            zoom_scale = self.fixed_zoom_scale
            label = self.fixed_image_label
            angle = self.fixed_rotation_angle
            flip = self.fixed_flip_state
            pan_offset_x = self.fixed_pan_offset_x
            pan_offset_y = self.fixed_pan_offset_y
        else:  # Moving image
            zoom_scale = self.moving_zoom_scale
            label = self.moving_image_label
            angle = self.moving_rotation_angle
            flip = self.moving_flip_state
            pan_offset_x = self.moving_pan_offset_x
            pan_offset_y = self.moving_pan_offset_y

        # Get the mouse position relative to the label
        cursor_pos = label.mapFromGlobal(event.globalPosition().toPoint())

        # remove the effect of rotation and flipping
        if angle == 90:
            if flip:
                zoom_focus_x = -(cursor_pos.y() - label.height() / 2)
                zoom_focus_y = (cursor_pos.x() - label.width() / 2)
            else:
                zoom_focus_x = (cursor_pos.y() - label.height() / 2)
                zoom_focus_y = -(cursor_pos.x() - label.width() / 2)
        elif angle == 180:
            zoom_focus_x = -(cursor_pos.x() - label.width() / 2)
            zoom_focus_y = -(cursor_pos.y() - label.height() / 2)
        elif angle == 270:
            if flip:
                zoom_focus_x = (cursor_pos.y() - label.height() / 2)
                zoom_focus_y = -(cursor_pos.x() - label.width() / 2)
            else:
                zoom_focus_x = -(cursor_pos.y() - label.height() / 2)
                zoom_focus_y = (cursor_pos.x() - label.width() / 2)
        else:
            zoom_focus_x = (cursor_pos.x() - label.width() / 2)
            zoom_focus_y = (cursor_pos.y() - label.height() / 2)

        # Adjust zoom scale based on scroll direction
        delta = event.angleDelta().y()
        scale_factor = 1.1 if delta > 0 else 0.9
        new_zoom_scale = zoom_scale * scale_factor
        new_zoom_scale = max(0.1, min(new_zoom_scale, 10.0))  # Clamp between 0.1 and 10.0

        # Calculate scaling factor and adjust pan offsets
        scale_change = new_zoom_scale / zoom_scale
        pan_offset_x += zoom_focus_x * (1 - scale_change)
        pan_offset_y += zoom_focus_y * (1 - scale_change)

        # Update the zoom scale and pan offsets
        if self.editWhichImage == 0:
            self.fixed_zoom_scale = new_zoom_scale
            self.fixed_pan_offset_x = pan_offset_x
            self.fixed_pan_offset_y = pan_offset_y
        else:
            self.moving_zoom_scale = new_zoom_scale
            self.moving_pan_offset_x = pan_offset_x
            self.moving_pan_offset_y = pan_offset_y

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

        # Add items from column 1 of self.movingIMS
        for index, row in enumerate(self.movingIMS):
            if len(row) > 1:  # Ensure the row has at least two columns
                filename = row[0]  # Get the filename from column 1
                dot_index = filename.find(".")
                filename_out = "moving_image_" + filename[:dot_index] + ".png"
                filepath = os.path.join(self.jobFolder, self.ResultsName, "aligned_stack", filename_out)

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
        current_index = self.ui.MovingImagesComboBox.currentIndex()
        row_number = self.numMovingDelete[1]
        row_number = row_number[current_index - 1]
        self.nmMoving = self.movingIMS[row_number][0]
        self.scaleMoving = self.movingIMS[row_number][1]
        self.pthMoving = self.movingIMS[row_number][2]

        # load the image
        image_path = os.path.join(self.pthMoving, self.nmMoving)
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return
        self.imMoving0 = QPixmap(image_path)  # store the original pixmap

        # Calculate zoom_default
        image_width = self.imMoving0.width()
        image_height = self.imMoving0.height()
        frame_width = self.ui.MovingImageDisplayFrame.width()
        frame_height = self.ui.MovingImageDisplayFrame.height()
        width_scale = frame_width / image_width
        height_scale = frame_height / image_height
        self.moving_zoom_default = min(width_scale, height_scale)

        # display image
        self.editWhichImage = 1
        self.reset_transformations()
        self.update_image_view()
        self.editWhichImage = 0
        self.ui.fixed_image_border.setStyleSheet(self.activeLabel)
        self.ui.moving_image_border.setStyleSheet(self.inactiveLabel)
        self.ui.FixedImageDisplayFrame.setStyleSheet(self.activeFrame)
        self.ui.MovingImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        self.slider_value_changed()

        # change some view settings
        self.ui.ChooseMovingImageFrame.setVisible(False)
        self.ui.ImageViewControlsFrame.setVisible(True)
        self.ui.FiducialPointControlsFrame.setVisible(True)
        self.ui.PickNewMovingImageButton.setVisible(True)

    def load_old_moving_image(self):

        # get the current filename and index from the droplist
        current_index = self.ui.OldMovingImagesComboBox.currentIndex()
        row_number = self.numMovingDelete[0]
        row_number = row_number[current_index - 1]
        self.nmMoving = self.movingIMS[row_number][0]
        self.scaleMoving = self.movingIMS[row_number][1]
        self.pthMoving = self.movingIMS[row_number][2]

        # load the image
        image_path = os.path.join(self.pthMoving, self.nmMoving)
        if not os.path.exists(image_path):
            print(f"Image file not found: {image_path}")
            return
        self.imMoving0 = QPixmap(image_path)  # store the original pixmap

        # Calculate zoom_default
        image_width = self.imMoving0.width()
        image_height = self.imMoving0.height()
        frame_width = self.ui.MovingImageDisplayFrame.width()
        frame_height = self.ui.MovingImageDisplayFrame.height()
        width_scale = frame_width / image_width
        height_scale = frame_height / image_height
        self.moving_zoom_default = min(width_scale, height_scale)

        # display image
        self.editWhichImage = 1
        self.reset_transformations()
        self.update_image_view()
        self.editWhichImage = 0
        self.ui.fixed_image_border.setStyleSheet(self.activeLabel)
        self.ui.moving_image_border.setStyleSheet(self.inactiveLabel)
        self.ui.FixedImageDisplayFrame.setStyleSheet(self.activeFrame)
        self.ui.MovingImageDisplayFrame.setStyleSheet(self.inactiveFrame)
        self.slider_value_changed()

        # change some view settings
        self.ui.ChooseMovingImageFrame.setVisible(False)
        self.ui.ImageViewControlsFrame.setVisible(True)
        self.ui.FiducialPointControlsFrame.setVisible(True)
        self.ui.PickNewMovingImageButton.setVisible(True)

    def confirm_load_new_image(self):
        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("Load a new moving image?")  # Set the window title
        msg_box.setText("Are you sure you want to load a new image? This will delete current fiducial data")  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        msg_box.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)  # Add Yes and Cancel buttons

        # Apply custom stylesheet for background and font color
        msg_box.setStyleSheet("""
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
                                """)

        # Show the message box and get the response
        response = msg_box.exec()
        if response == QtWidgets.QMessageBox.Cancel:
            return
        self.initiate_tab_2()

    def doubleclick_fixed_image_tab2(self):
        self.editWhichImage = 0 # focus on the fixed image
        self.slider_value_changed()

    def doubleclick_moving_image_tab2(self):
        self.editWhichImage = 1 # focus on the moving image
        self.slider_value_changed()

    def handle_value_update_fixed(self, new_value, row, column):
        """Handle the new value emitted by the delegate."""

        # Optionally update other variables or UI elements
        if column == 1:  # For example, update ScaleFixed if editing the Scale column
            # Check if the string is a number
            try:
                float(new_value)
                self.ScaleFixed = new_value
            except:
                self.scale_error_message()
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
                self.scale_error_message()
            self.populate_moving_table()

    def doubleclick_moving_table(self, row, column):
        # cell_value = self.ui.movingImageTableWidget.item(row, column).text()
        # print(f"Double-clicked moving table at ({row}, {column}) with value: {cell_value}")

        # if the table is populated and table edit mode is not already active
        if len(self.movingIMS) > 0:

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
        # print(f"Double-clicked fixed table at ({row}, {column}) with value: {cell_value}")

        # if the table is populated and table edit mode is not already active
        if len(self.nmFixed) > 0:
            # cell_value = self.ui.fixedImageTableWidget.item(row, column).text()

            # if editing the scale
            if column == 1:
                # enable text input to the scale window
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

    def enter_edit_table(self):

        # disable other buttons
        self.ui.SetJobFolderFrame.setEnabled(False)
        self.ui.chooseFixedImageButton.setEnabled(False)
        self.ui.chooseMovingImageButton.setEnabled(False)
        self.ui.loadTemplateButton.setEnabled(False)
        self.ui.goToFiducialPointTabButton.setEnabled(False)
        self.ui.goToApplyRegistrationTabButton.setEnabled(False)

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
        self.ui.SetJobFolderFrame.setEnabled(True)
        self.ui.chooseFixedImageButton.setEnabled(True)
        self.ui.chooseMovingImageButton.setEnabled(True)
        self.ui.loadTemplateButton.setEnabled(True)
        self.ui.goToFiducialPointTabButton.setEnabled(True)
        self.ui.goToApplyRegistrationTabButton.setEnabled(True)

        # make delete invisible
        self.ui.keepFixedImageButton.setVisible(False)
        self.ui.deleteFixedImageButton.setVisible(False)
        self.ui.keepMovingImageButton.setVisible(False)
        self.ui.deleteMovingImageButton.setVisible(False)

    def checkbox_changed(self, state):
        """Handle the checkbox state change."""
        if state > 0:
            self.jobFolder = self.pthFixed
        else:
            self.jobFolder = ""
        self.populate_project_table()

    def scale_error_message(self):
        msg_box = QtWidgets.QMessageBox()  # Create a message box
        msg_box.setWindowTitle("Scale factor is not a number")  # Set the window title
        msg_box.setText("The entered value is not a number. Please enter a number")  # Set the message text
        msg_box.setIcon(QtWidgets.QMessageBox.Question)  # Set the icon
        msg_box.setStandardButtons(
            QtWidgets.QMessageBox.Ok)  # Add Yes and Cancel buttons

        # Apply custom stylesheet for background and font color
        msg_box.setStyleSheet("""
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
                        """)

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
            msg_box.setStyleSheet("""
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
                """)

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
            msg_box.setStyleSheet("""
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
                """)

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
        # if num_rows == 1:
        # self.ui.movingImageTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(self.movingIMS[0]))
        # self.ui.movingImageTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(self.movingIMS[1]))
        # self.ui.movingImageTableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(self.movingIMS[2]))
        # else:
        row_count = 0
        for row in self.movingIMS:
            self.ui.movingImageTableWidget.setItem(row_count, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.ui.movingImageTableWidget.setItem(row_count, 1, QtWidgets.QTableWidgetItem(
                row[1]))  # Convert scale to string if necessary
            self.ui.movingImageTableWidget.setItem(row_count, 2, QtWidgets.QTableWidgetItem(row[2]))
            row_count += 1

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_tables_are_complete()

    def populate_fixed_table(self):

        # Populate the first row with the variables' values
        self.ui.fixedImageTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(self.nmFixed))
        self.ui.fixedImageTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(
            self.ScaleFixed))  # Convert scale to string if necessary
        self.ui.fixedImageTableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem(self.pthFixed))

        if len(self.pthFixed) > 0:
            self.ui.JobFolderCheckBox.setVisible(True)
        else:
            self.ui.JobFolderCheckBox.setVisible(False)

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_tables_are_complete()

    def populate_project_table(self):
        self.ui.setJobTableWidget.setRowCount(1)
        self.ui.setJobTableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(self.ResultsName))
        self.ui.setJobTableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(self.jobFolder))

        # turn the frame green if all fixed image inputs are defined correctly
        self.check_if_tables_are_complete()

    def check_if_tables_are_complete(self):
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
            self.ui.goToFiducialPointTabButton.setVisible(True)
            self.ui.goToApplyRegistrationTabButton.setVisible(True)
        else:
            self.ui.goToFiducialPointTabButton.setVisible(False)
            self.ui.goToApplyRegistrationTabButton.setVisible(False)

    def browse_for_template(self):
        """Choose a template file to load."""

        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Template .csv File", "",
                                                             "Data Files (*.csv)")
        if file_path:
            self.load_template_info(file_path)

    def load_template_info(self, file_path):
        # Read the CSV file
        X = pd.read_csv(file_path, header=None).values  # Using pandas to read the file

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

    def keyPressEvent(self, event):
        """Handle key press events."""
        # Check if the Esc key is pressed
        if event.key() == Qt.Key_Escape:
            # exit zoom and pan mode if they are active
            if self.zoom_active or self.pan_active:
                self.zoom_active = False
                self.pan_active = False
                self.panning = False  # Reset panning state
                self.ui.ZoomPanButton.setText("Zoom/Pan")  # Reset the button text
            else:
                return
        else:
            # Pass the event to the base class for default handling
            super().keyPressEvent(event)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())