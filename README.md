# CODApivot

CODApivot is a user interface guided tool for multi-omic image and coordinate registration

---
## 🚀 Key Features

* **Project-Based Workflow:** Organize your fixed and moving images, results, and associated data in project files within the GUI.
* **Interactive Fiducial Point Selection:** Dynamically adjust brightness, contrast, zoom, pan, flip, and rotate images to streamline fiducial point pair selection.
* **Nonlinear Finetuning Registration:** Optionally fine tune your fiducial point-based affine registration using automated nonlinear registration.
* **Registration of coordinate data:** Apply registration transforms directly to coordinate points directly in the app.
* 


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

After launching, follow the built-in instructions or refer to the [CODA pivot user guide (PDF)](./CODA%20pivot%20user%20guide.pdf) for a comprehensive walkthrough.

---
## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for details.
