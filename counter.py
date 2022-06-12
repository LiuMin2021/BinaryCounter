#!/usr/bin/env python3
# 2021 nr@bulme.at

from gpiozero import LEDBoard, Button
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber,
    QVBoxLayout, QApplication)

DOWN_PIN = 22
RESET_PIN = 27
UP_PIN = 17 

LED0 = 18
LED1 = 23
LED2 = 24
LED3 = 25



class QtButton(QObject):
    changed = pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.button = Button(pin) 
        self.button.when_pressed = self.gpioChange        

    def gpioChange(self):
        self.changed.emit()

class Counter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count = 0
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0

    def initUi(self):
        self.lcd = QLCDNumber()
        self.lcd.display(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)

        self.setLayout(vbox)
        self.setMinimumSize(400, 200)
        self.setWindowTitle('Counter')
        self.show()


    def countUp(self):
        self.count += 1
        self.D += 1
        if self.D==2:
            self.D=0
            self.C+=1
        if self.C==2:
            self.C=0
            self.B+=1
        if self.B==2:
            self.B=0
            self.A=1
        if self.count == 16:
            self.count = 0
            self.A = 0
            self.B = 0
            self.C = 0
            self.D = 0
        self.lcd.display(self.count)
        leds.value = (self.A, self.B, self.C, self.D)
        
    def countDown(self):
        self.count -= 1
        self.D -= 1
        if self.D == -1:
            self.D=1
            self.C-=1
        if self.C == -1:
            self.C=1
            self.B-=1
        if self.B == -1:
            self.B=1
            self.A=0
        if self.count == -1:
            self.count = 15
            self.A = 1
            self.B = 1
            self.C = 1
            self.D = 1
        self.lcd.display(self.count)
        leds.value = (self.A, self.B, self.C, self.D)
        
    def countReset(self):
        self.count = 0
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.lcd.display(self.count)
        leds.value = (self.A, self.B, self.C, self.D)

 

if __name__ ==  '__main__':
    app = QApplication([])
    gui = Counter()
    button = QtButton(UP_PIN)
    button.changed.connect(gui.countUp)
    button = QtButton(DOWN_PIN)
    button.changed.connect(gui.countDown)    
    button = QtButton(RESET_PIN)
    button.changed.connect(gui.countReset)
    leds = LEDBoard(LED0, LED1, LED2, LED3)
    app.exec_()
    
