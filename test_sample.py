import pytest
from time import sleep
import gui
from PyQt5.QtCore import *

def testgui(qtbot):
    window = gui.App()
    qtbot.addWidget(window)
    window.show()
    assert window.isVisible()