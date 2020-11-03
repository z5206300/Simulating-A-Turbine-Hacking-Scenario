import PyQt5.QtWidgets as Q
import PyQt5.QtCore as Qt

class Turbine():

    def __init__(self):
        self.RPM = 0
        self.power = 0
        self.target = 0
        self.mode = 0
        self.hold = 0
    def getValues(self):
        data = {'targetrpm':self.target}
        return(data)
    def setValues(self,data):
        self.RPM = data.get('rpm')
        self.power = data.get('pwm')
        self.update()
    def setRPM(self, rpm):
        self.RPM=rpm
    def setPower(self, power):
        self.power=power
    def update(self):
        self.RPMVal.setText(str(self.RPM))
        self.powerOut.setValue(self.power)
        self.targetVal.setText(str(self.target))
        self.targetSlide.setValue(self.target)
    def enableAuto(self):
        self.mode=0
        self.targetSlide.setEnabled(False)
        self.update()
    def enableManual(self):
        self.mode=1
        self.targetSlide.setEnabled(True)
        self.update()
    def setTarget(self):
        self.target=self.targetSlide.value()
        self.update()
    def startTurbine(self):
        self.target=self.hold
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.update()
    def stopTurbine(self):
        self.hold=self.target
        self.target=1
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.update()
    def createFuncBox(self,number):

        turbineBox = Q.QGroupBox("Turbine " + number)

        modeSelect = Q.QGroupBox("Mode:")
        autoRadioButton = Q.QRadioButton("Auto")
        autoRadioButton.setChecked(True)
        autoRadioButton.toggled.connect(self.enableAuto)
        manRadioButton = Q.QRadioButton("Manual")
        manRadioButton.toggled.connect(self.enableManual)

        modeLayout = Q.QHBoxLayout()
        modeLayout.addWidget(autoRadioButton)
        modeLayout.addWidget(manRadioButton)
        modeSelect.setLayout(modeLayout)

        paramDisp = Q.QGroupBox()
        paramLayout = Q.QGridLayout()

        self.RPMLabel = Q.QLabel(paramDisp)
        self.RPMLabel.setText("RPM:")
        self.RPMVal = Q.QLabel(paramDisp)
        self.RPMVal.setText(str(self.RPM))
        self.powerLabel = Q.QLabel(paramDisp)
        self.powerLabel.setText("Steam Pressure:")
        self.powerOut = Q.QProgressBar()
        self.powerOut.setRange(0,800)
        self.powerOut.setTextVisible(False)
        self.powerOut.setValue(self.power)
        self.targetLabel = Q.QLabel(paramDisp)
        self.targetLabel.setText("Target RPM:")
        self.targetVal = Q.QLabel(paramDisp)
        self.targetVal.setText(str(self.target))
        self.targetSlide = Q.QSlider(Qt.Qt.Horizontal,paramDisp)
        self.targetSlide.setValue(self.target)
        self.targetSlide.setMaximum(800)
        self.targetSlide.setMinimum(0)
        self.targetSlide.setEnabled(False)
        self.targetSlide.valueChanged.connect(self.setTarget)
        self.startButton = Q.QPushButton("START")
        self.startButton.setEnabled(False)
        self.startButton.clicked.connect(self.startTurbine)
        self.stopButton = Q.QPushButton("STOP")
        self.stopButton.clicked.connect(self.stopTurbine)
        paramLayout = Q.QGridLayout()
        paramLayout.addWidget(self.RPMLabel, 0,0,1,1)
        paramLayout.addWidget(self.RPMVal, 0,4,1,1)
        paramLayout.addWidget(self.powerLabel, 1,0,1,1)
        paramLayout.addWidget(self.powerOut, 2,0,1,-1)
        paramLayout.addWidget(self.targetLabel, 3,0,1,1)
        paramLayout.addWidget(self.targetVal, 3,4,1,1)
        paramLayout.addWidget(self.targetSlide, 4,0,1,-1)
        paramLayout.addWidget(self.startButton, 5,0,2,2)
        paramLayout.addWidget(self.stopButton, 5,3,2,2)

        paramDisp.setLayout(paramLayout)

        layout = Q.QGridLayout()
        layout.addWidget(modeSelect,0,0,1,5)
        layout.addWidget(paramDisp,1,0,6,5)
        turbineBox.setLayout(layout)
        
        return(turbineBox)
