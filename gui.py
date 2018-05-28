import sys, random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import GetFromJson
import PandasModel

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
        self.setGeometry(20, 20, 800, 600)
        self.app_widget = App()
        self.setCentralWidget(self.app_widget)
        self.setWindowTitle('PyQAR Project')

        #Global Menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
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
        viewQAR = QAction('View Association Rules', self, checkable=True)
        viewQAR.setChecked(True)
        viewQAR.triggered.connect(self.toggleQAR)
        viewMenu.addAction(viewQAR)

        viewPlot = QAction('View Plot', self, checkable=True)
        viewPlot.setChecked(True)
        viewPlot.triggered.connect(self.togglePlot)
        viewMenu.addAction(viewPlot)

        #Tools Menu
        globalSettingsButton = QAction('Global Settings', self)
        toolsMenu.addAction(globalSettingsButton)

        #Help Menu
        documentationButton = QAction('Documentation', self )
        documentationButton.triggered.connect(self.doclink)
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

    #Documentation Function
    def doclink(self):
        QDesktopServices.openUrl(QUrl('https://github.com/jpniels/Bachelor'))

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
    
    def toggleQAR(self, state):
        if state:
            self.app_widget.supportbutton.show()
            self.app_widget.allbutton.show()
            self.app_widget.liftbutton.show()
            self.app_widget.confidencebutton.show()
            self.app_widget.tableWidget.show()
        else:
            self.app_widget.supportbutton.hide()
            self.app_widget.allbutton.hide()
            self.app_widget.liftbutton.hide()
            self.app_widget.confidencebutton.hide()
            self.app_widget.tableWidget.hide()

    def togglePlot(self, state):
        if state:
            self.app_widget.canvas.show()
        else:
            self.app_widget.canvas.hide()

#Central widget within mainWindow
class App(QWidget):
    #Application Stylesheet
    def appStyle(self):
        self.setStyleSheet("""
        .QWidget {
            background-color: #2A3036;
        }

        .QComboBox, .QLineEdit, .QSpinBox, .QDoubleSpinBox{
            background-color: #434C55;
            color: #fff;
            height: 30px;
            selection-color: #434C55;
            selection-background-color: #FFB36C;
        }
        .QTableView {
            selection-color: #434C55;
            selection-background-color: #FFB36C;
            border: none;
            width: 100%;
        }
        .QRadioButton {
            color: #fff;
        }
        .QRadioButton::indicator::unchecked{
            border: 1px solid #5C656E; 
            background-color: #434C55;
            height: 13px;
        }
        .QRadioButton::indicator::checked{
            border: 1px solid #434C55; 
            background-color: #FFB36C; 
            height: 13px;
        }
        .QLabel {
            color: darkgrey;
        }
        """)
 
    #Global initialization
    def __init__(self):
        super().__init__()
        self.initUI()
        self.appStyle()

    def initUI(self):
        #Plot Styling
        plt.style.use('seaborn-pastel')
        plt.rcParams['font.monospace'] = 'Ubuntu Mono'
        plt.rcParams['font.size'] = 10
        plt.rcParams['xtick.color'] = '#96A391'
        plt.rcParams['ytick.color'] = '#96A391'
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.labelcolor'] = 'darkgrey'
        plt.rcParams['axes.labelweight'] = 'normal'
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
        plt.rcParams['text.color'] = 'darkgrey'
        plt.xticks(rotation=90)

        #Grid/layout handling
        l = QGridLayout(self)
        subhorizontallayout = QHBoxLayout()
        sublayout = QVBoxLayout()
        sublayout2 = QVBoxLayout()
        sublayout3 = QVBoxLayout()
        sublayout.setAlignment(Qt.AlignTop)
        sublayout2.setAlignment(Qt.AlignTop)
        sublayout3.setAlignment(Qt.AlignTop)
        subsublayout1 = QHBoxLayout()
        subsublayout2 = QVBoxLayout()
        subsublayout3 = QVBoxLayout()
        subsublayout2.setAlignment(Qt.AlignTop)
        subsublayout3.setAlignment(Qt.AlignTop)
        self.figure = plt.figure(figsize=(5,7))   
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setMinimumWidth(800)
        self.canvas.setMaximumHeight(800)
        sublayout2.addWidget(self.canvas)

        self.threshold = QDoubleSpinBox(self)
        self.threshold.setValue(0.1)
        self.threshold.valueChanged.connect(self.plot)
        self.threshold.setFixedWidth(250)
        self.threshold.setSuffix(' Threshold')
        self.threshold.setRange(0.1, 5)
        self.threshold.setSingleStep(0.1)
        subsublayout2.addWidget(self.threshold)

        #Support Button
        self.supportbutton = QRadioButton("Calculate Support", self)
        self.supportbutton.toggled.connect(self.aprioritoggled)
        subsublayout2.addWidget(self.supportbutton)

        #Conviction Button
        self.confidencebutton = QRadioButton("Calculate Confidence", self)
        self.confidencebutton.toggled.connect(self.aprioritoggled)
        subsublayout2.addWidget(self.confidencebutton)

        #Lift Button
        self.liftbutton = QRadioButton("Calculate Lift", self)
        self.liftbutton.toggled.connect(self.aprioritoggled)
        subsublayout2.addWidget(self.liftbutton)

        #Conviction Button
        self.convictionbutton = QRadioButton("Calculate Conviction", self)
        self.convictionbutton.toggled.connect(self.aprioritoggled)
        subsublayout2.addWidget(self.convictionbutton)

        #Lift Button
        self.allbutton = QRadioButton("Calculate All", self)
        self.allbutton.toggled.connect(self.aprioritoggled)
        subsublayout2.addWidget(self.allbutton)

        ####################################################################################################################
        ### Grid 1
        #################################################################################################################### 

        #Room Box 1
        self.roomBoxlabel = QLabel("Select Room:")
        self.roomBox = QComboBox(self)
        self.roomBox.addItem('Room')
        self.roomBox.model().item(0).setEnabled(False)
        for element in GetFromJson.getRooms():
            self.roomBox.addItem(element)
        self.roomBox.currentTextChanged.connect(self.roomBoxChanged)
        self.roomBox.setFixedWidth(250)
        sublayout.addWidget(self.roomBoxlabel)
        sublayout.addWidget(self.roomBox)
        
        #Media Box 1
        self.mediaBoxlabel = QLabel("Select Media:")
        self.mediaBox = QComboBox(self)
        self.mediaBox.setEnabled(False)
        self.mediaBox.addItem('Media')
        self.mediaBox.model().item(0).setEnabled(False)
        self.mediaBox.currentTextChanged.connect(self.plot)
        self.mediaBox.setFixedWidth(250)
        sublayout.addWidget(self.mediaBoxlabel)
        sublayout.addWidget(self.mediaBox)

        #Outliers Radiobutton 1
        self.outlierBtn = QRadioButton("Remove Outliers", self)
        self.outlierBtn.setAutoExclusive(False)
        self.outlierBtn.toggled.connect(self.outlierstoggled)
        sublayout.addWidget(self.outlierBtn)

        #Outliers Selection Box
        self.outliermethod = QComboBox(self)
        self.outliermethod.hide()
        self.outliermethod.addItem('Standard Deviation')
        self.outliermethod.addItem('Interquartile Range')
        self.outliermethod.currentTextChanged.connect(self.plot)
        self.outliermethod.setFixedWidth(250)
        sublayout.addWidget(self.outliermethod)

        #Interolate Radiobutton 1
        self.interpolateBtn = QRadioButton("Interpolate data", self)
        self.interpolateBtn.setAutoExclusive(False)
        self.interpolateBtn.toggled.connect(self.interpolatetoggled)
        sublayout.addWidget(self.interpolateBtn)

        #Interpolate Selection Box
        self.interpolateBox = QComboBox(self)
        self.interpolateBox.hide()
        self.interpolateBox.addItem('5Min')
        self.interpolateBox.addItem('15Min')
        self.interpolateBox.addItem('30Min')
        self.interpolateBox.addItem('45Min')
        self.interpolateBox.addItem('1H')
        self.interpolateBox.addItem('2H')
        self.interpolateBox.currentTextChanged.connect(self.plot)
        self.interpolateBox.setFixedWidth(250)
        sublayout.addWidget(self.interpolateBox)

        #Intervals Radiobutton 1
        self.intervalsBtn = QRadioButton("Use intervals", self)
        self.intervalsBtn.setAutoExclusive(False)
        self.intervalsBtn.toggled.connect(self.intervalstoggled)
        sublayout.addWidget(self.intervalsBtn)

        #Intervals spinbox 1
        self.spinbox = QSpinBox(self)
        self.spinbox.setValue(1)
        self.spinbox.valueChanged.connect(self.plot)
        self.spinbox.hide()
        self.spinbox.setFixedWidth(250)
        self.spinbox.setSuffix(' Intervals')
        self.spinbox.setRange(1, 25)
        sublayout.addWidget(self.spinbox)

        #Time Frequency Radiobutton
        self.freqButton = QRadioButton("Set Time Frequency", self)
        self.freqButton.setAutoExclusive(False)
        self.freqButton.toggled.connect(self.frequencytoggled)
        sublayout.addWidget(self.freqButton)

        #Time Frequency Box
        self.timefreqBox = QComboBox(self)
        self.timefreqBox.hide()
        self.timefreqBox.addItem('30Min')
        self.timefreqBox.addItem('1H')
        self.timefreqBox.addItem('2H')
        self.timefreqBox.addItem('12H')
        self.timefreqBox.addItem('1D')
        self.timefreqBox.addItem('1W')
        self.timefreqBox.addItem('2W')
        self.timefreqBox.addItem('1M')
        self.timefreqBox.currentTextChanged.connect(self.plot)
        self.timefreqBox.setFixedWidth(250)
        sublayout.addWidget(self.timefreqBox)

        #Calendar From Widget
        self.dateTimelabel = QLabel("Select Start Date: ")
        self.calendar = QCalendarWidget(self)
        format = QTextCharFormat()
        format.setBackground(QColor('#434C55'))
        weekendformat = QTextCharFormat()
        weekendformat.setForeground(QColor('#fff'))
        self.calendar.setHeaderTextFormat(format)
        self.calendar.setStyleSheet('selection-background-color: #FFB36C; selection-color: #434C55;')
        self.calendar.setWeekdayTextFormat(Qt.Saturday, weekendformat)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, weekendformat)
        self.calendar.setFixedWidth(250)
        self.calendar.setMaximumHeight(220)
        sublayout.addWidget(self.dateTimelabel)
        sublayout.addWidget(self.calendar)

        #Date time From widget for converting to ms - nonvisible
        self.datetime = QDateTimeEdit()
        self.datetime.setCalendarPopup(True)
        self.datetime.setCalendarWidget(self.calendar)
        self.datetime.dateTimeChanged.connect(self.plot)
        self.datetime.setVisible(False)

        sublayout.addStretch()

        ####################################################################################################################
        ### Grid 2
        #################################################################################################################### 

        #Room Box 2
        self.roomBoxlabel2 = QLabel("Select Second Room:")
        self.roomBox2 = QComboBox(self)
        self.roomBox2.addItem('Room')
        self.roomBox2.model().item(0).setEnabled(False)
        for element in GetFromJson.getRooms():
            self.roomBox2.addItem(element)
        self.roomBox2.currentTextChanged.connect(self.roomBox2Changed)
        self.roomBox2.setFixedWidth(250)
        sublayout3.addWidget(self.roomBoxlabel2)
        sublayout3.addWidget(self.roomBox2)
        
        #Media Box 2
        self.mediaBoxlabel2 = QLabel("Select Second Media:")
        self.mediaBox2 = QComboBox(self)
        self.mediaBox2.setEnabled(False)
        self.mediaBox2.addItem('Media')
        self.mediaBox2.model().item(0).setEnabled(False)
        self.mediaBox2.currentTextChanged.connect(self.plot)
        self.mediaBox2.setFixedWidth(250)
        sublayout3.addWidget(self.mediaBoxlabel2)
        sublayout3.addWidget(self.mediaBox2)

        #Outliers Radiobutton 2
        self.outlierBtn2 = QRadioButton("Remove Outliers", self)
        self.outlierBtn2.setAutoExclusive(False)
        self.outlierBtn2.toggled.connect(self.outlierstoggled2)
        sublayout3.addWidget(self.outlierBtn2)

        #Outliers Selection Box
        self.outliermethod2 = QComboBox(self)
        self.outliermethod2.hide()
        self.outliermethod2.addItem('Standard Deviation', 1)
        self.outliermethod2.addItem('Interquartile Range', 2)
        self.outliermethod2.currentTextChanged.connect(self.plot)
        self.outliermethod2.setFixedWidth(250)
        sublayout3.addWidget(self.outliermethod2)

        #Interpolate Radiobutton 2
        self.interpolateBtn2 = QRadioButton("Interpolate data", self)
        self.interpolateBtn2.setAutoExclusive(False)
        self.interpolateBtn2.toggled.connect(self.interpolatetoggled2)
        sublayout3.addWidget(self.interpolateBtn2)

        #Interpolate Selection Box
        self.interpolateBox2 = QComboBox(self)
        self.interpolateBox2.hide()
        self.interpolateBox2.addItem('5Min')
        self.interpolateBox2.addItem('15Min')
        self.interpolateBox2.addItem('30Min')
        self.interpolateBox2.addItem('45Min')
        self.interpolateBox2.addItem('1H')
        self.interpolateBox2.addItem('2H')
        self.interpolateBox2.currentTextChanged.connect(self.plot)
        self.interpolateBox2.setFixedWidth(250)
        sublayout3.addWidget(self.interpolateBox2)

        #Intervals Radiobutton 2
        self.intervalsBtn2 = QRadioButton("Use intervals", self)
        self.intervalsBtn2.setAutoExclusive(False)
        self.intervalsBtn2.toggled.connect(self.intervalstoggled2)
        sublayout3.addWidget(self.intervalsBtn2)

        #Intervals spinbox 2
        self.spinbox2 = QSpinBox(self)
        self.spinbox2.setValue(1)
        self.spinbox2.valueChanged.connect(self.plot)
        self.spinbox2.hide()
        self.spinbox2.setFixedWidth(250)
        self.spinbox2.setSuffix(' Intervals')
        self.spinbox2.setRange(1, 25)
        sublayout3.addWidget(self.spinbox2)

        #Time Frequency Radiobutton
        self.freqButton2 = QRadioButton("Set Time Frequency", self)
        self.freqButton2.setAutoExclusive(False)
        self.freqButton2.toggled.connect(self.frequencytoggled2)
        sublayout3.addWidget(self.freqButton2)

        #Time Frequency Box 2
        self.timefreqBox2 = QComboBox(self)
        self.timefreqBox2.hide()
        self.timefreqBox2.addItem('30Min')
        self.timefreqBox2.addItem('1H')
        self.timefreqBox2.addItem('2H')
        self.timefreqBox2.addItem('12H')
        self.timefreqBox2.addItem('1D')
        self.timefreqBox2.addItem('1W')
        self.timefreqBox2.addItem('2W')
        self.timefreqBox2.addItem('1M')
        self.timefreqBox2.currentTextChanged.connect(self.plot)
        self.timefreqBox2.setFixedWidth(250)
        sublayout3.addWidget(self.timefreqBox2)

        #Calendar To Widget
        self.dateTimelabelto = QLabel("Select End Date: ")
        self.calendarto = QCalendarWidget(self)
        self.calendarto.setHeaderTextFormat(format)
        self.calendarto.setStyleSheet('selection-background-color: #FFB36C; selection-color: #434C55;')
        self.calendarto.setWeekdayTextFormat(Qt.Saturday, weekendformat)
        self.calendarto.setWeekdayTextFormat(Qt.Sunday, weekendformat)
        self.calendarto.setFixedWidth(250)
        self.calendarto.setMaximumHeight(220)
        sublayout3.addWidget(self.dateTimelabelto)
        sublayout3.addWidget(self.calendarto)

        #Date time From widget for converting to ms - nonvisible
        self.datetimeto = QDateTimeEdit(QDate.currentDate())
        self.datetimeto.setCalendarPopup(True)
        self.datetimeto.setCalendarWidget(self.calendarto)
        self.datetimeto.dateTimeChanged.connect(self.plot)
        self.datetimeto.setVisible(False)

        sublayout3.addStretch()
        ##########################################################################################################################

        #Table Widget
        self.tableWidget = QTableView()
        self.header = self.tableWidget.horizontalHeader()
        self.header.setStretchLastSection(True)
        subsublayout3.addWidget(self.tableWidget)

        #Add layouts to grid
        subsublayout1.addLayout(subsublayout2)
        subsublayout1.addLayout(subsublayout3)
        sublayout2.addLayout(subsublayout1)

        subhorizontallayout.addLayout(sublayout)
        subhorizontallayout.addLayout(sublayout2)
        subhorizontallayout.addLayout(sublayout3)

        sizeable = QWidget()
        sizeable.setLayout(subhorizontallayout)
        l.addWidget(sizeable, 1, 1, 1, 1)
        l.setAlignment(Qt.AlignCenter)

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

    #Same as above for room2 selected
    def roomBox2Changed(self):
        self.mediaBox2.setEnabled(True)
        self.mediaBox2.clear()
        medialist2 = []
        for k, v in GetFromJson.getMedias(self.roomBox2.currentText()).items():
            if v not in medialist2:
                medialist2.append(v)
        self.mediaBox2.addItems(medialist2)

    def outlierstoggled(self, state):
        if state:
            if self.mediaBox.currentText() != 'Media': 
                self.outliermethod.show()
                self.plot()
            else:
                self.outlierBtn.setChecked(False)
                QMessageBox.warning(self, "Error", "You must pick a room and media before using this function.")
        else:
            self.outliermethod.hide()
            self.plot()

    def interpolatetoggled(self, state):
        if state:
            if self.mediaBox.currentText() != 'Media': 
                self.interpolateBox.show()
                self.plot()
            else:
                self.interpolateBtn.setChecked(False)
                QMessageBox.warning(self, "Error", "You must pick a room and media before using this function.")
        else:
            self.interpolateBox.hide()
            self.plot()

    def intervalstoggled(self, state):
        if state:
            if self.mediaBox.currentText() != 'Media': 
                self.spinbox.show()
                self.plot()
            else:
                self.intervalsBtn.setChecked(False)
                QMessageBox.warning(self, "Error", "You must pick a room and media before using this function.")
        else:
            self.spinbox.hide()
            self.plot()

    def frequencytoggled(self, state):
        if state:
            if self.mediaBox.currentText() != 'Media': 
                self.timefreqBox.show()
                self.plot()
            else:
                self.freqButton.setChecked(False)
                QMessageBox.warning(self, "Error", "You must pick a room and media before using this function.")
        else:
            self.timefreqBox.hide()
            self.plot()

    def outlierstoggled2(self, state):
        if state:
            if self.mediaBox2.currentText() != 'Media': 
                self.outliermethod2.show()
                self.plot()
            else:
                self.outlierBtn2.setChecked(False)
                QMessageBox.warning(self, "Error", "You must pick a room and media before using this function.")
        else:
            self.outliermethod2.hide()
            self.plot()

    def interpolatetoggled2(self, state):
        if state:
            if self.mediaBox2.currentText() != 'Media': 
                self.interpolateBox2.show()
                self.plot()
            else:
                self.interpolateBtn2.setChecked(False)
                QMessageBox.warning(self, "Error", "You must pick a room and media before using this function.")
        else:
            self.interpolateBox2.hide()
            self.plot()

    def intervalstoggled2(self, state):
        if state:
            if self.mediaBox2.currentText() != 'Media': 
                self.spinbox2.show()
                self.plot()
            else:
                self.intervalsBtn2.setChecked(False)
                QMessageBox.warning(self, "Error", "You must pick a room and media before using this function.")
        else:
            self.spinbox2.hide()
            self.plot()

    def frequencytoggled2(self, state):
        if state:
            if self.mediaBox2.currentText() != 'Media': 
                self.timefreqBox2.show()
                self.plot()
            else:
                self.freqButton2.setChecked(False)
                QMessageBox.warning(self, "Error", "You must pick a room and media before using this function.")
        else:
            self.timefreqBox2.hide()
            self.plot()

    def aprioritoggled(self, state):
        if state:
            if self.mediaBox.currentText() != 'Media' or self.mediaBox2.currentText() != 'Media':
                self.plot()
            else:
                QMessageBox.warning(self, "Error", "You must pick two rooms and medias before using this function.")
        else:
            self.plot()

    
    #Dont mess with this shit, just the initial empty plot.. useless
    def compute_initial_figure(self):
        axes=self.figure.add_subplot(111)
        axes.plot(1,1)
        self.canvas.draw()

    #Plotting the data selected
    def plot(self):
        axes=self.figure.add_subplot(111)
        axes.cla()
        
        test = GetFromJson.getMediaIndex(self.mediaBox.currentText(), self.roomBox.currentText())
        df = GetFromJson.getDataframe(test)
        df = GetFromJson.dataframeFromTime(df, self.datetime.dateTime().toMSecsSinceEpoch(), self.datetimeto.dateTime().toMSecsSinceEpoch())


        if self.outlierBtn.isChecked() == True:
            if self.outliermethod.currentText() == 'Standard Deviation':
                df = GetFromJson.removeOutliersSD(df)
            else:
                df = GetFromJson.removeOutliersIQR(df)
        if self.interpolateBtn.isChecked() == True:
            df = GetFromJson.createInterpolation(df, self.interpolateBox.currentText())
        if self.freqButton.isChecked() == True:
            df = GetFromJson.getDataframeFreq(df, self.timefreqBox.currentText())
        if self.intervalsBtn.isChecked() == True:
            df = GetFromJson.setReadingIntervals(df, self.spinbox.value())
            df['readings'] = df['readings'].astype(str)

        axes.plot(df.index.values, df['readings'], 'r-', linewidth=1, linestyle='-', color='#E9B955')
        self.canvas.draw()
    
        test2 = GetFromJson.getMediaIndex(self.mediaBox2.currentText(), self.roomBox2.currentText())
        df2 = GetFromJson.getDataframe(test2)
        df2 = GetFromJson.dataframeFromTime(df2, self.datetime.dateTime().toMSecsSinceEpoch(), self.datetimeto.dateTime().toMSecsSinceEpoch())
        
        if self.outlierBtn2.isChecked() == True:
            if self.outliermethod2.currentText() == 'Standard Deviation':
                df2 = GetFromJson.removeOutliersSD(df2)
            else:
                df2 = GetFromJson.removeOutliersIQR(df2)
        if self.interpolateBtn2.isChecked() == True:
            df2 = GetFromJson.createInterpolation(df2, self.interpolateBox2.currentText())
        if self.freqButton2.isChecked() == True:
            df2 = GetFromJson.getDataframeFreq(df2, self.timefreqBox2.currentText())
        if self.intervalsBtn2.isChecked() == True:
            df2 = GetFromJson.setReadingIntervals(df2, self.spinbox2.value())
            df2['readings'] = df2['readings'].astype(str)
        

        #Plot the graph
        
        axes.plot(df2.index.values, df2['readings'], 'r-', linewidth=1, linestyle='-', color='#2D4CC5')
        axes.set_title(self.mediaBox.currentText() + ' & ' + self.mediaBox2.currentText() + ' in rooms ' + self.roomBox.currentText() + ', ' + self.roomBox2.currentText())
        axes.set_xlabel('Time')
        axes.set_ylabel('Readings')


        #Fill table testing!
        if self.liftbutton.isChecked() == True:
            df3 = GetFromJson.getBooleanAssociationRules(df, df2)
            df3 = GetFromJson.ap.apriori(df3, 0.1)
            df3 = GetFromJson.ap.allLift(df3, 0)
            model = PandasModel.PandasModel(df3)
            self.tableWidget.setModel(model)
        if self.supportbutton.isChecked() == True:
            df = GetFromJson.getBooleanAssociationRules(df, df2)
            df = GetFromJson.ap.apriori(df, self.threshold.value())
            model = PandasModel.PandasModel(df)
            self.tableWidget.setModel(model)

        if self.confidencebutton.isChecked() == True:
            df3 = GetFromJson.getBooleanAssociationRules(df, df2)
            df3 = GetFromJson.ap.apriori(df3, 0)
            df3 = GetFromJson.ap.allConfidence(df3, self.threshold.value())
            model = PandasModel.PandasModel(df3)
            self.tableWidget.setModel(model)
        
        if self.convictionbutton.isChecked() == True:
            df3 = GetFromJson.getBooleanAssociationRules(df, df2)
            supp = GetFromJson.ap.apriori(df3, 0)
            conf = GetFromJson.ap.allConfidence(supp, self.threshold.value())
            df3 = GetFromJson.ap.allConviction(supp, conf)
            model = PandasModel.PandasModel(df3)
            self.tableWidget.setModel(model)


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
        self.setWindowTitle('PyQAR Login')
        self.mainWindow = mainWindow()
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