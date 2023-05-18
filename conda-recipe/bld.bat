"%PYTHON%"  setup.py build_external -vv
"%PYTHON%" setup.py sdist install
if errorlevel 1 exit 1