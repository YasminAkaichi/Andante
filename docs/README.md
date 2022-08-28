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

Run make with html as argument in the andante/docs/ folder:
```bash
make html
```

## See output html

Go to the _build/html and open index.html.
```bash
cd _build/html ; open index.html
```


