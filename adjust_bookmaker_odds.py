from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtWidgets import QWidget

class AdjustBookmakerOdds(QWidget):

    def __init__(self, ui_file):
        super(AdjustBookmakerOdds, self).__init__()
        self.window = uic.loadUi(ui_file, self)
        self.window.show()
