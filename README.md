# CODApivot

CODApivot is an intuitive, Python-powered graphical application for streamlined image registration and transformation. Whether you're working with histology slides, spatial datasets, or medical imaging, CODApivot simplifies the process of aligning, transforming, and visualizing data — all through an elegant GUI.

---
## 🚀 Key Features

* **Project-Based Workflow:** Organize your fixed and moving images, results, and associated data within structured job folders.
* **Interactive Fiducial Point Selection:** Add, move, and remove fiducial points directly on your images — fast and visually intuitive.
* **Smart Image Viewer:** Dynamically adjust brightness, contrast, zoom, pan, flip, and rotate to tailor your view.
* **Robust Registration Algorithms:**

  * Perform affine registration using Iterative Closest Point (ICP) based on fiducial points.
  * Execute elastic registration for capturing complex non-linear deformations.
* **Transformation Engine:**

  * Apply saved transformations to coordinate datasets (CSV, Excel).
  * Transfer registrations seamlessly to new images.
* **Overlay Visualization:** Instantly visualize overlays of fixed and moving images, plus transformed fiducials, to verify alignment quality.
* **Keyboard Shortcuts:** Work efficiently with built-in shortcut support for most actions.

---
## ⚙️ Installation Guide

### 📅 Step 1: Install Miniconda

Begin by downloading and installing Miniconda from the official [Miniconda website](https://docs.anaconda.com/miniconda/).

### 🐍 Step 2: Set Up the CODApivot Environment

Create a new environment and activate it:

```bash
    conda create -n CODApivot python>3.8
    conda activate CODApivot
```

### 📦 Step 3: Install CODApivot

Install the CODApivot package via Git:

```bash
  pip install -e git+https://github.com/Kiemen-Lab/CODA_pivot.git#egg=CODApivot
```

> ⚠️ **Note:** Ensure Git is installed. If not, download it from [git-scm.com](https://git-scm.com/downloads/win). After installation, restart your IDE or terminal and reactivate the environment.

### 🖼️ Step 4: Launch the CODApivot Interface

To open the application, execute the `CODApivot.py` script in your terminal or IDE.

After launching, follow the built-in instructions or refer to the [CODA pivot user guide (PDF)](./CODA%20pivot%20user%20guide.pdf)` for a comprehensive walkthrough.

---
## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for details.
