import sys, random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import GetFromJson
 
class App(QMainWindow):
    #Application Stylesheet
    def mainStyle(self):
        self.setStyleSheet("""
        .QWidget {
            background-color: #999;

        }

        .QTextEdit{
            background-color: #fff;
            color: #f5f5f5;
            border: 1px #9e9e9e solid;
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
        self.mainStyle()
        self.mainWindow()
        #QApplication.installEventFilter(self)
        

    #Main Window
    def mainWindow(self):
        #Window itself
        self.m = PlotCanvas(self, width=10, height=6)

        #Rooms combobox
        self.roomBox = QComboBox(self)
        for element in GetFromJson.getRooms():
            self.roomBox.addItem(element)
        self.roomBox.move(50, 340)
        self.roomBox.currentTextChanged.connect(self.roomBoxChanged)
        

        self.mediaBox = QComboBox(self)
        self.mediaBox.move(150, 340)

        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.StrongFocus)
        sld.setGeometry(60, 40, 100, 30)
        sld.setTickPosition(QSlider.TicksBothSides)
        sld.setTickInterval(10)
        sld.setSingleStep(1)
        sld.move(50, 300)

        b1 = QRadioButton("Detect Outliers", self)
        b1.setChecked(True)
        b1.move(50, 370)

        items = QDockWidget("Dockable", self)
        listWidget = QListWidget()
        listWidget.addItem("item1")
        listWidget.addItem("item2")
        listWidget.addItem("item3")
        listWidget.move(50,450)

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

    def roomBoxChanged(self, text):
        self.mediaBox.setEnabled(True)
        self.mediaBox.clear() 
        for k, v in GetFromJson.getMedias(self.roomBox.currentText()).items():
            self.mediaBox.addItem(str(v))

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
        self.mainWindow = App()
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
        pixmap = QPixmap('SDU.png')
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
    
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=2, dpi=100): 
        #Plot styling
        plt.style.use('fivethirtyeight')
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = 'Ubuntu'
        plt.rcParams['font.monospace'] = 'Ubuntu Mono'
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.labelweight'] = 'bold'
        plt.rcParams['xtick.labelsize'] = 8
        plt.rcParams['ytick.labelsize'] = 8
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 12

        #Plot initialize
        fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.plot()
        self.plot2()

    #Plotting data
    def plot(self):
        #data = [random.randint(0,20) for i in range(20)]
        ax = self.figure.add_subplot(2, 2, 2)
        test = GetFromJson.getMediaIndex('temperature', 'e21-602-0')
        df = GetFromJson.getDataframe(test)
        ax.plot(df['timestamp'], df['readings'], 'r-', linewidth=1, linestyle='-', label='Testing', color='blue')
        ax.set_title('Plot 1')
        self.draw()

    #Plotting data2
    def plot2(self):
        data = [random.randint(0,20) for i in range(20)]
        data2 = [random.randint(8,12) for i in range(20)]
        ax = self.figure.add_subplot(2, 2, 1)
        ax.plot(data, 'r-', linewidth=1, linestyle='-', label='Testing', color='blue')
        ax.plot(data2, 'r-', linewidth=1, linestyle='-', label='Testing', color='orange')
        ax.set_title('Plot 2')
        self.draw()

#Launcher
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ex = LoginWindow()
    ex.show()
    sys.exit(app.exec_())