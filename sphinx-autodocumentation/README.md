# Sphinx documentation

## Installation

Get Sphinx:
```bash
sudo apt-get install python3-sphinx
```

Get some dependencies:
```bash
pip install MarkupSafe
pip install --upgrade aws-sam-cli
```

Get the sphinx theme: 
```bash
pip install sphinx_rtd_theme
```

## Produce output

Run make with html as argument in the current folder:
```bash
make html
```

## See output html

Go to the html folder and open index.html.
```bash
cd html ; open index.html
```


