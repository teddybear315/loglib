del /f /s /q dist build
rmdir /s /q dist build
python -m build --sdist --wheel
twine check dist/*
