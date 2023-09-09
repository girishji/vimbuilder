#!/bin/sh

# source <script>

deactivate 2> /dev/null
rm -rf .venv docs
python -m venv .venv
source .venv/bin/activate
python -m pip install sphinx
python -m pip install blurb
pip install sphinxext-opengraph==0.7.5
pip install python-docs-theme>=2023.3.1,!=2023.7

pip install -i https://test.pypi.org/simple/ vimbuilder

sphinx-build --version
sphinx-quickstart --sep -p Test -a TestAuthor -r 0.1 -l en docs
sed -e 's/extensions = \[\]/extensions = \["vimbuilder.builder"\]/' docs/source/conf.py > tempfile
mv tempfile docs/source/conf.py
sphinx-build -b vimhelp docs/source/ docs/build/vimhelp

