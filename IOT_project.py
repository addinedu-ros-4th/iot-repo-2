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
        while self.running == True:
            self.update.emit()
            time.sleep(0.05)



path = "./IoTproject.ui"
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
        self.mealCount = 0

        self.inputThread = Thread(self) # Thread 
        self.inputThread.running = True
        self.inputThread.start()
        
        self.commendList = [0, 0, 0, 0, 0, 0] # meal, water, light, meal_count, water_level, servo_angle


        


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
        

    



    def sendSignalFormeal(self) : # 배식신호 발송 함수
        self.commendList[0] = 1
        commend = str(self.commendList).replace("[", "").replace("]", "")
        self.pySerial.write(commend.encode())
        self.commendList[0] = 0


    def sendSignalForWater(self) : # 물 추가신호 발송 함수
        self.commendList[1] = 1
        commend = str(self.commendList).replace("[", "").replace("]", "")
        self.pySerial.write(commend.encode())
        self.commendList[1] = 0


    def plusMealPlan(self) : # 배식 시간 추가 함수
        Feed_number = self.mealCB.currentText()
        Feed_time = self.timeEdit.text()
        meal_item_text = f"횟수: {Feed_number}, 시간: {Feed_time}"

        self.model = self.mealList.model()
        if self.model is None:  # 모델이 없을 경우 새 모델 생성
            self.model = QStandardItemModel()

        item = QStandardItem(meal_item_text)

        # 중복제거
        for row in range(self.model.rowCount()):
            index = self.model.index(row, 0)
            if self.model.data(index) == meal_item_text:
                return 

        # 아이템 시간정렬
        inserted = False
        for row in range(self.model.rowCount()):
            index = self.model.index(row, 0)
            item_time = self.model.data(index).split("시간:")[1].strip()  # 시간 정보 추출

            # AM , PM 비교
            time1 = QTime.fromString(Feed_time, "h:mm AP")
            time2 = QTime.fromString(item_time, "h:mm AP")

            # 새 아이템의 시간이 현재 아이템의 시간보다 작다면 삽입
            if time1 < time2:
                self.model.insertRow(row, item)
                inserted = True
                break

        # 만약 모든 아이템의 시간보다 크다면 마지막에 삽입
        if not inserted:
            self.model.appendRow(item)

        self.mealList.setModel(self.model)
        

    def minusMealPlan(self) : # 배식시간 제거 함수
        selected_indexes = self.mealList.selectedIndexes()  # 선택된 항목의 인덱스 가져오기
        for index in selected_indexes:
            self.model.removeRow(index.row())  # 모델에서 선택된 항목 제거
        self.mealList.setModel(self.model) # 모델 재설정

    def turnOnLight(self) : # 전구 키는 함수
        if self.commendList[2] != 1:
            self.commendList[2] = 1
            commend = str(self.commendList).replace("[", "").replace("]", "")
            self.pySerial.write(commend.encode())

    def turnOffLight(self) : # 전구 끄는 함수
        if self.commendList[2] != 0:
            self.commendList[2] = 0
            commend = str(self.commendList).replace("[", "").replace("]", "")
            self.pySerial.write(commend.encode())






def main() :
    app = QApplication(sys.argv)
    myWindows = iotComputer()
    myWindows.show()
    sys.exit(app.exec())


if __name__ == "__main__" : 
    main()