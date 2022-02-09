print('hello world!')


import sys, os 
from main_window import Main
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) #get project root directory
# start the GUI
app = QApplication(sys.argv)
Main(ROOT_DIR + '\\gui\\main.ui')
sys.exit(app.exec_())

print('bye bye')