# 컴퓨터(python)
# 	INPUT
# 		센서 값
# 	OUTPUT
# 		현재 시간, 설정 값, 지정시간, 제어 값, + DB에 현재온도 기록(서브옵션)
# 	GUI(qt)
# 		input
# 			배식시간 설정, 배식량(횟수) 설정, 온도범위 설정, 배식버튼, 물추가 버튼
# 		output	
# 			배식시간 상태, 현재온도, 현재 수질상태, 수질오염 경고, 현재 수위 상태, + 지난 6시간 간의 온도 그래프(서브옵션)


# 통신 (유선)


# 아두이노	
# 	INPUT
# 		현재 시간, 지정시간, 제어 값, 설정 값
# 	OUTPUT
# 		센서 값, 모터 제어

import serial as sri
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic



    
class Thread(QThread) :
    update = pyqtSignal()
    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = False


    def run(self):
        count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(0.05)


path = "./iotProject.ui"
from_class = uic.loadUiType(path)[0]
class iotComputer(QMainWindow, from_class):

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("control_app")
        
        self.pySerial = sri.Serial(port="/dev/ttyACM0", baudrate=9600)# serial
        

        
        self.temperature = 0. # 수온
        self.waterQulity = 0. # 수질 수치
        self.waterLevel = 0. # 수위
        self.temperatureRange = 0. # 수온 범위
        self.lightIsOn = False # 전구 상태


        self.inputThread = Thread(self) # Thread 
        
        self.inputThread.running = True
        
        self.inputThread.start()
        
        

        


        self.mealButton.clicked.connect(self.sendSignalFormeal)
        self.waterButton.clicked.connect(self.sendSignalForWater)
        self.minusMealButton.clicked.connect(self.minusMealPlan)
        self.plusMealButton.clicked.connect(self.plusMealPlan)



        self.inputThread.update.connect(self.updateInput) # link Thread
        


    def updateInput(self) : # 아두이노신호 받는 함수 (반복됨)
        if self.pySerial.in_waiting != 0:
            try:
                self.temperature = 0. ### 이후 아두이노 input으로 대체
                self.waterQulity = 0.
                self.waterLevel = eval(self.pySerial.readline().decode())["waterLevel"]
            except SyntaxError:
                pass
            self.tempNowLabel.setText(str(self.temperature))
            self.waterLevelLabel.setText(str(self.waterLevel))
            self.waterQulityLabel.setText(str(self.waterQulity))
        

    def updateOutput(self) : # 아두이노로 신호 보내주는 함수
        commend = str(30)
        self.pySerial.write(commend.encode())
        # pass



    def sendSignalFormeal(self) : # 배식신호 발송 함수
        pass

    def sendSignalForWater(self) : # 물 추가신호 발송 함수
        pass


    def plusMealPlan(self) : # 배식 시간 추가 함수
        pass

    def minusMealPlan(self) : # 배식시간 제거 함수
        pass

    def turnOnLight(self) : # 전구 키는 함수
        pass

    def turnOffLight(self) : # 전구 끄는 함수
        pass






def main() :
    app = QApplication(sys.argv)
    myWindows = iotComputer()
    myWindows.show()
    sys.exit(app.exec())


if __name__ == "__main__" : 
    main()