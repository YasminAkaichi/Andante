# Andante

Andante is a Python package for exploring Inductive Logic Programming. Its
documentation can be found as a [standard
pdf](./documentation/Documentation/main.pdf) but also as a [sphinx
autodocumentation](./sphinx-autodocumentation/html/index.html).

[Jupyter notebooks](./jupyter-notebooks) are also available as a mean to
illustrate the use of the andante package.

## Requirements

### Python
Andante is written in Python and, as such, Python must be installed for Andante
to work. Installation guidelines can be found in the [official
website](https://www.python.org).

For Ubuntu, if not already installed, python can be installed with the
following command:
```bash
sudo apt install python3
```

### Git
Git is a widely used tool for version control. Its installation varies
depending on one's OS. For more information, please consult the [official
website](https://git-scm.com).

Installation for Ubuntu:
```bash
sudo apt install git
```

Using git is a skill to be learned. The most fundamental git commands can be
found in the git-fundamentals.md file.

### Jupyter notebook
Jupyter Notebook is a web application that runs Python. It is needed to run the
notebooks available in the jupyter-notebooks folder. For any problem during the
installation, steps, please refer to their [official
website](https://jupyter.org).

Jupyter notebook should be installed through the following command:
```bash
pip3 install notebook
```
To run Jupyter Notebook:
```bash
jupyter notebook
```

## Installation

### Step 1: Downloading the git repository 
```bash
git clone https://gitlab.unamur.be/sijacque/andante.git path/to/repo
```

### Step 2: Installing the andante package
```bash
pip install -e path/to/repo
```

