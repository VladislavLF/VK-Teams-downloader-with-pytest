## Automated testing of VK Teams installation and launch
This program is a set of automated tests to check:
- Downloading the VK Teams installation file
- Correct installation of the application
- Successful launch of the application after installation

## Technologies
- Programming language: Python
- Testing framework: pytest
## Additional libraries:
- pywinauto - for automating GUI work
- psutil - for working with system processes
- requests - for downloading the installation file
- keyboard - for emulating keystrokes

## Prerequisites
1. Windows 10/11 (64-bit)
2. Python 3.8+
3. Administrator rights
4. Stable internet connection
5. At least 500 MB of free disk space
6. Installed dependencies: `pip install -r requirements.txt`

# Running tests
## Standard Run
``pytest -s``
## With verbose output
``pytest -s -v``
## With HTML report generation
``pytest -s --html-report=./report.html``
