# **Project Setup Instructions**

## **1. Prerequisites**
Before setting up the environment, ensure you have the following installed:
- **Miniconda** or **Anaconda**: [Download Here](https://docs.conda.io/en/latest/miniconda.html)
- **Python 3.10+** (Handled by Conda)

## **2. Create and Activate the Conda Environment**
Run the following command to create a Conda environment named `flask-env`:

```bash
conda create --name flask-env python=3.10 -y
conda activate flask-env
```

## **3. Install Dependencies**
First, install packages available in Conda:

```bash
conda install flask flask-cors numpy=1.26.4 werkzeug opencv -y
```

Then, install the remaining dependencies using `pip`:

```bash
pip install flask-socketio ultralytics python-engineio python-socketio
```

## **4. Verify Installation**
Check if all required packages are installed correctly:

```bash
pip list
```

Ensure NumPy is version **1.x** (not 2.x):

```bash
python -c "import numpy; print(numpy.__version__)"
```

## **5. Running the Project**
To start the Flask-SocketIO server, run:

```bash
python socket_server.py
```

## **6. Deactivating the Environment**
When you're done, deactivate the Conda environment:

```bash
conda deactivate
```

## **7. Troubleshooting Common Errors**
### **OpenMP Error: `libiomp5.dylib already initialized`**
If you encounter the following error:

```
OMP: Error #15: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized.
```

This happens due to multiple OpenMP libraries being loaded. To fix it:

#### **Option 1: Remove Conflicting OpenMP Libraries (Recommended)**
```bash
conda remove intel-openmp -y
```

#### **Option 2: Use an Environment Variable (Temporary Fix)**
```bash
export KMP_DUPLICATE_LIB_OK=TRUE
python socket_server.py
```

#### **Option 3: Reinstall Dependencies**
```bash
pip uninstall opencv-python numpy torch
conda install numpy=1.26.4 opencv -y
pip install torch
```

Restart your terminal and try running the script again.

Let me know if you need further assistance! 🚀