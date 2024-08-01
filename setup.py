import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages":["arcade", "random", "math", "os", "time", "datetime"]}

setup(name = "Test" , version = "1.0" , description = "Mein erstes Spiel" , executables = [Executable("Blocket.py")])