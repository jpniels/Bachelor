import sys, random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import GetFromJson

#Main Window
class mainWindow(QMainWindow):
    #Application Stylesheet
    def mainStyle(self):
        self.setStyleSheet("""
            background-color: #2A3036;
            color: #FFF;
        """)
 
    def __init__(self):
        super().__init__(parent=None)
        self.mainStyle()
        self.app_widget = App()
        self.setCentralWidget(self.app_widget)
        

        #Global Menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        #File Menu
        openFileButton = QAction('Open File', self)
        openFileButton.setShortcut('Ctrl+O')
        openFileButton.triggered.connect(self.openFile)
        fileMenu.addAction(openFileButton)

        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        #Edit Menu
        undoButton = QAction('Undo', self)
        undoButton.setShortcut('Ctrl+Z')
        editMenu.addAction(undoButton)

        redoButton = QAction('Redo', self)
        redoButton.setShortcut('Ctrl+Y')
        editMenu.addAction(redoButton)

        #View Menu
        somethingButton = QAction('View Something', self)
        viewMenu.addAction(somethingButton)

        #Tools Menu
        globalSettingsButton = QAction('Global Settings', self)
        toolsMenu.addAction(globalSettingsButton)

        #Help Menu
        documentationButton = QAction('Documentation', self )
        helpMenu.addAction(documentationButton)
        aboutButton = QAction('About', self)
        aboutButton.triggered.connect(self.about)
        helpMenu.addAction(aboutButton)

    #About Function
    def about(self):
        QMessageBox.information(self, "About", "Version: 1.0.0.0.0.0.0.0.1 \n Program made by: \n \n Sebastian Nørgaard \n Jonas Phillip Nielsen \n ")

    #Open File Function
    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            GetFromJson.read_file_path(fileName)
    
    #Settings Function
    def globalSettings(self):
        print('hej')

    #Global CloseEvent function
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit Dialog',
            "\n Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.Cancel, QMessageBox.Cancel)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

#Central widget within mainWindow
class App(QWidget):
    #Application Stylesheet
    def appStyle(self):
        self.setStyleSheet("""
        .QWidget {
            background-color: #2A3036;

        }

        .QComboBox, .QLineEdit, .QSpinBox{
            background-color: #434C55;
            color: #fff;
            height: 30px;
            selection-background-color: #FFB36C;
        }
        .QHBoxLayout {
            background-color: white;
        }
        .QLabel {
            color: darkgrey;
        }
        """)
 
    #Global initialization
    def __init__(self):
        super().__init__()
        self.title = 'Bachelor Project'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 600
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.initUI()
        self.appStyle()

    def initUI(self):
        #Plot Styling
        plt.style.use('seaborn-pastel')
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = 'Ubuntu'
        plt.rcParams['font.monospace'] = 'Ubuntu Mono'
        plt.rcParams['font.size'] = 10
        plt.rcParams['xtick.color'] = '#96A391'
        plt.rcParams['ytick.color'] = '#96A391'
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.labelweight'] = 'bold'
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 12
        plt.rcParams['figure.facecolor'] = '#2A3036'
        plt.rcParams['axes.edgecolor'] = '#96A391'
        plt.rcParams['axes.linewidth'] = 1
        plt.rcParams['axes.facecolor'] = '#2A3036'
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.color'] = '#343B43'

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        l = QGridLayout(self)
        self.figure = plt.figure(figsize=(10,5))    
        self.canvas = FigureCanvas(self.figure)   
        l.addWidget(self.canvas, 0,0,1,0)
        subverticallayout = QHBoxLayout()
        subverticallayout.setSpacing(2)
        subverticallayout.setAlignment(Qt.AlignCenter)
        sublayout = QVBoxLayout()
        sublayout2 = QVBoxLayout()
        sublayout.setAlignment(Qt.AlignTop)
        sublayout2.setAlignment(Qt.AlignTop)

        #Room Box
        self.roomBoxlabel = QLabel("Select Room:")
        self.roomBox = QComboBox(self)
        for element in GetFromJson.getRooms():
            self.roomBox.addItem(element)
        self.roomBox.currentTextChanged.connect(self.roomBoxChanged)
        self.roomBox.setFixedWidth(230)
        sublayout.addWidget(self.roomBoxlabel)
        sublayout.addWidget(self.roomBox)
        
        #Media Box
        self.mediaBoxlabel = QLabel("Select Media:")
        self.mediaBox = QComboBox(self)
        self.mediaBox.setEnabled(False)
        self.mediaBox.currentTextChanged.connect(self.outlierToggle)
        self.mediaBox.setFixedWidth(230)
        sublayout2.addWidget(self.mediaBoxlabel)
        sublayout2.addWidget(self.mediaBox)

        #Outliers Radiobutton
        self.outlierBtn = QRadioButton("Detect Outliers", self)
        self.outlierBtn.setChecked(True)
        self.outlierBtn.toggled.connect(self.outlierToggle)
        sublayout.addWidget(self.outlierBtn)

        #Line edit
        self.smthing = QLineEdit(self)
        self.smthing.setFixedWidth(230)
        sublayout.addWidget(self.smthing)

        #Intervals spinbox
        self.spinbox = QSpinBox(self)
        self.spinbox.setFixedWidth(230)
        sublayout.addWidget(self.spinbox)

        subverticallayout.addLayout(sublayout)
        subverticallayout.addLayout(sublayout2)

        sizeable = QWidget()
        sizeable.setLayout(subverticallayout)
        sizeable.setFixedWidth(700)
        l.addWidget(sizeable, 103, 1, 1, 2)

        self.compute_initial_figure()

    #When a room is selected get the medias and show them
    def roomBoxChanged(self):
        self.mediaBox.setEnabled(True)
        self.mediaBox.clear()
        medialist = []
        for k, v in GetFromJson.getMedias(self.roomBox.currentText()).items():
            if v not in medialist:
                medialist.append(v)
        self.mediaBox.addItems(medialist)

    #Handle Outlier toggle
    def outlierToggle(self):
        if self.outlierBtn.isChecked() == True:
            self.plot()
        else:
            print('hej')
    
    #Dont mess with this shit, just the initial empty plot.. useless
    def compute_initial_figure(self):
        axes=self.figure.add_subplot(111)
        axes.plot(1,1)
        self.canvas.draw()

    #Plotting the data selected
    def plot(self):
        test = GetFromJson.getMediaIndex(self.mediaBox.currentText(), self.roomBox.currentText())
        df = GetFromJson.getDataframe(test)
        df = GetFromJson.getDataframeFreq(df, "1M")
        df = GetFromJson.removeOutliers(df)
        axes=self.figure.add_subplot(111)
        axes.cla()
        axes.plot(df.index.values, df['readings'], 'r-', linewidth=1, linestyle='-', label='Testing', color='#E9B955')
        self.canvas.draw()


class LoginWindow(QMainWindow):
    #Login Stylesheet
    def loginStyle(self):
        self.setStyleSheet("""
        .QPushButton {
            background-color: #1AB186;
            height: 25px;
        }
        .QLineEdit {
            background-color: #fff;
            height: 25px;
        }
        """)
 
    #Login Window
    def __init__(self):
        super().__init__()
        self.title = 'Bachelor Project'
        self.mainWindow = mainWindow()
        #Layout Styling
        centralWidget = QWidget()   
        self.setFixedSize(320,200)       
        self.setCentralWidget(centralWidget)   
        gridLayout = QGridLayout()   
        centralWidget.setLayout(gridLayout)
        self.loginStyle()

        #Login Image
        label = QLabel(self)
        label.resize(275, 73)
        pixmap = QPixmap('assets/SDU.png')
        pixmap = pixmap.scaled(179, 50)
        label.setPixmap(pixmap) 
 
        #Login Form
        self.uName = QLineEdit(self)
        self.uName.setPlaceholderText('Username')
        self.pWord = QLineEdit(self)
        self.pWord.setPlaceholderText('Password')
        self.pWord.setEchoMode(QLineEdit.Password)
        loginBtn = QPushButton('Login', self)
        loginBtn.clicked.connect(self.loginHandler)
        layout = QVBoxLayout()
        layout.addWidget(self.uName)
        layout.addWidget(self.pWord)
        layout.addWidget(loginBtn)

        #Add elements to Grid Layout
        gridLayout.addWidget(label, 0, 0, Qt.AlignCenter)
        gridLayout.addItem(layout, 1, 0, Qt.AlignCenter)
    
    #Handle Login Button
    def loginHandler(self):
        if (self.uName.text() == 'foo' and
            self.pWord.text() == 'bar'):
            self.mainWindow.show()
            self.close()
        else:
            QMessageBox.warning(
                self, 'Error', 'Bad username or password')
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = LoginWindow()
    ex.show()
    sys.exit(app.exec_())