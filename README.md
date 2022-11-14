# INF1600MainProject

## Getting Started

## Prerequisites

- Make sure to install `GPU` drivers in your system if you want to use `GPU` . Follow [driver installation](Driver-Installations.md) for further instructions.
- Make sure you have [MS Build tools](https://aka.ms/vs/17/release/vs_BuildTools.exe) installed in system if using windows. 
- [Download git for windows](https://git-scm.com/download/win) if not installed.

**1. Installation:**

For `Linux`

```shell
python3 -m venv .env
source .env/bin/activate

pip install numpy Cython
pip install cython-bbox
pip install asone
pip install playsound


# for CPU
pip install torch torchvision

# for GPU
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu113

```

For `Windows 10/11`

```shell
python -m venv .env
.env\Scripts\activate

pip install numpy Cython
pip install -e git+https://github.com/samson-wang/cython_bbox.git#egg=cython-bbox
pip install asone
pip install playsound

# for CPU
pip install torch torchvision

# for GPU
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cu113
or
pip install torch==1.10.1+cu113 torchvision==0.11.2+cu113 torchaudio===0.10.1+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```

## Running the program
Run `main.py` from the root folder with `python src/main.py`