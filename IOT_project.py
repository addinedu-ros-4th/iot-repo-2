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
import pandas as pd
import mysql.connector

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pyqtgraph as pg

from datetime import datetime
from PyQt5 import QtCore


    
class Thread(QThread) :
    update = pyqtSignal()
    update2 = pyqtSignal()
    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = False


    def run(self):
        while self.running == True:
            self.update.emit()
            time.sleep(1)



path = "./IoTproject.ui"
from_class = uic.loadUiType(path)[0]

class settingWindow(QDialog):
    def __init__(self, iotComputer):
        super().__init__()
        
        self.ui = uic.loadUi("IoTproject_sub.ui", self)
        self.iotComputer = iotComputer
        self.show()
        
        
        list_view = QListView()
        self.properQualityCB.setView(list_view) 
        self.properQualityCB.view().setResizeMode(QListView.Adjust)
        for i in range(41) :
            self.properTemperatureCB.addItem(str(i))

        for i in range(101) :
            self.properQualityCB.addItem(str(i))
            
            
        ###### DB option
        self.user = "joe"
        self.password = "0000"
        self.database = "amrbase"

        #####
            
        self.saveSettingButton.clicked.connect(self.saveSettingData)
        
        
    def quitWindow(self):
        self.hide()
        
    def saveSettingData(self) : 
        conn = mysql.connector.connect( # db 초기화
            user = self.user,
            password = self.password,
            database = self.database
        )
        
        cur = conn.cursor(buffered = True)
        
        sql = "select count(*) from aquarium_setting"
        cur.execute(sql)
        result = cur.fetchall()
        settingNumber = result[0][0] + 1
        
        sql = f"insert into aquarium_setting (ID, proper_level, proper_temp, proper_quality)\
        values({settingNumber}, {self.properHeightCB.currentText()}, {self.properTemperatureCB.currentText()}, {self.properQualityCB.currentText()})"

        cur.execute(sql)
        conn.commit()
        conn.close()

class iotComputer(QMainWindow, from_class):

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("control_app")
        self.setGeometry(0, 0, 1410, 810)
        self.pySerial = sri.Serial(port="/dev/ttyACM0", baudrate=9600)
        

        ###### DB option
        self.user = "joe"
        self.password = "0000"
        self.database = "amrbase"

        ######


        self.conn = mysql.connector.connect( # db 초기화
            user = self.user,
            password = self.password,
            database = self.database
        )
        
        self.cur = self.conn.cursor(buffered = True)
        sql = "delete from aquarium"

        self.cur.execute(sql)
        self.conn.commit()
        
        sql = "delete from aquarium_action"
        self.cur.execute(sql)
        self.conn.commit()
        
        sql = "select * from aquarium_setting"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        
        for value in result:
            self.settingID.addItem(str(value[0]))
        
        self.settingDF = pd.DataFrame(result, columns= ["ID", "properLevel", "properTemp", "properQuality"])
        
        for col_index, column in enumerate(self.settingDF.columns):
            value = self.settingDF.loc[0][column]
            
            item = QTableWidgetItem(str(value))
            self.settingTable.setItem(0, col_index, item)
        
                
        self.conn.close()

        self.count = 0
        self.waterTemperature = 0. # 수온
        self.waterQuality = 0. # 수질 수치
        self.waterLevel = 0. # 수위
        self.temperatureRange = 0. # 수온 범위
        self.lightIsOn = False # 전구 상태
        self.mealCount = 0
        self.lightStatus = False
        
        self.planList = ""
        self.mealCountList = ""

        self.settingID.currentIndexChanged.connect(self.changeSetting)
        
        
        
        # self.getSettingData()
        startTime = time.strftime('%H:%M:%S').split(":")
        self.startTimeTypeMilliSecond = (int(startTime[0]) * 60**2 + int(startTime[1]) * 60 + int(startTime[2])) * 1000 # 시작시 시간(단위 : ms)
        
        self.inputThread = Thread(self) # Thread 
        self.inputThread.running = True
        self.inputThread.start()
        
        self.dbThread = Thread(self) # Thread 
        self.dbThread.running = True
        self.dbThread.start()
        
        # meal, water, light, meal_count, water_level, servo_angle, start_time(ms), plan
        self.commendList = [0, 0, 0, self.mealCountList, 0, 0, self.startTimeTypeMilliSecond, self.planList] 
        

        self.levelPlot = self.levelGraph.plot(pen = "b")
        self.qualityPlot = self.qualityGraph.plot(pen = "g")
        self.tempPlot = self.tempGraph.plot(pen = "r")


        commend = str(self.commendList).replace("[", "").replace("]", "")
        self.pySerial.write(commend.encode())
        

        
        self.minusMealButton.clicked.connect(self.minusMealPlan)
        self.plusMealButton.clicked.connect(self.plusMealPlan)

        
        self.addSettingButton.clicked.connect(self.showSettingWindow)
        self.callSettingButton.clicked.connect(self.callSetting)
                
        self.inputThread.update.connect(self.updateInput) # link Thread
    
    
    def showSettingWindow(self):
        setting_window = settingWindow(self)
        setting_window.exec_()
    
    def callSetting(self):
        self.conn = mysql.connector.connect( # db 초기화
            user = self.user,
            password = self.password,
            database = self.database
        )
        self.cur = self.conn.cursor(buffered = True)
        sql = "select * from aquarium_setting"
        self.cur.execute(sql)
        result = self.cur.fetchall()
        
        for value in result:
            self.settingID.addItem(str(value[0]))
        
        self.settingDF = pd.DataFrame(result, columns= ["ID", "properLevel", "properTemp", "properQuality"])
        
        for col_index, column in enumerate(self.settingDF.columns):
            value = self.settingDF.loc[0][column]
            
            item = QTableWidgetItem(str(value))
            self.settingTable.setItem(0, col_index, item) 
     
    def changeSetting(self) :
        settingID = int(self.settingID.currentText())
        for col_index, column in enumerate(self.settingDF.columns):
            value = self.settingDF.loc[settingID-1][column]
            
            item = QTableWidgetItem(str(value))
            self.settingTable.setItem(0, col_index, item)        

    def updateInput(self) : # 아두이노신호 받는 함수 (반복됨)
        if self.pySerial.in_waiting != 0:
            try:

                decodedDict = eval(self.pySerial.readline().decode())


                self.waterQuality = decodedDict["waterQuality"]
                self.waterLevel = decodedDict["waterLevel"]
                self.waterTemperature = decodedDict["waterTemperature"]
                self.lightStatus = decodedDict["light"]
                self.pumpStatus = decodedDict["pump"]
                self.servoStatus = decodedDict["servo"]
                
                print(self.commendList, decodedDict)
                
            except SyntaxError:
                print("error")
                
            self.fishbowlHistoryLabel.setText("어항기록 - 현재시간 : " + time.strftime("%Y-%m-%d %H:%M:%S"))
            self.tempNowLabel.setText(str(self.waterTemperature) + "°C")
            self.waterLevelLabel.setText(str(self.waterLevel) + "cm")
            self.waterQualityLabel.setText(str(self.waterQuality) + "mg")

            self.showStatusOfFishbowl()    
                
            if self.lightStatus:
                self.lightButton.setText("온열등 끄기")
            elif not self.lightStatus:
                self.lightButton.setText("온열등 켜기")
            
            self.saveData()

            
            
        
    # def getSettingData(self) : 
    #     sql = "select * from settingData"
    #     self.cul.execute(sql)
    #     result = self.cul.fetchall()
        
    #     settingDf = pd.DataFrame(result, columns= ["properTemperature", "properHeight", "properQuality"])

    #     self.properHeight = settingDf["properHeight"] # 적정 수위 -  
    #     self.properTemperature = settingDf["properTemperature"] #적정 온도
    #     self.properTemperatureRange = settingDf["properTemperatureRange"] #온도 범위
    #     self.properQuality = settingDf["properQuality"] # 적정 탁도

    #     self.properHeightLabel.setText("적정수위 : " + str(self.properHeight[0]))
    #     self.properTemperatureLabel.setText("적정온도 : " + str(self.properTemperature[0]))
    #     # self.properTemperatureRangeLabel.setText("온도 범위 : " + str(self.properTemperatureRange[0]))
    #     self.properQualityLabel.setText("적정수질 : " + str(self.properQuality[0]))



    def showStatusOfFishbowl(self) :
        text = "어항상태 -"
        

        if self.waterTemperature > self.properTemperature[0] + self.properTemperatureRange[0] : # 
            text += " 냉각 필요"
            self.tempStateLabel.setText("부적합")
        elif self.waterTemperature < self.properTemperature[0] - self.properTemperatureRange[0] : # 
            text += " 보온 필요"
            self.tempStateLabel.setText("부적합")
        else :
            self.tempStateLabel.setText("적합")


        if self.waterLevel < self.properHeight[0] : 
            text += " 물 보충 필요"
            self.levelStateLabel.setText("부적합")
        else : 
            self.levelStateLabel.setText("적합")


        if self.waterQuality < self.properQuality[0] : 
            text += " 물 교체 필요"
            self.qulityStateLabel.setText("부적합")
        else:
            self.qulityStateLabel.setText("적합")

        if text == "어항상태 -" :
            text += "정상"

        self.fishbowlStateLabel.setText(text)
        
    def saveData(self) :
        
        
        
        sql = f"insert into aquarium (time, water_height, water_quality, water_temperature)\
        values(current_timestamp, {self.waterLevel}, {self.waterQuality}, {self.waterTemperature})"

        self.cul.execute(sql)
        self.conn.commit()
        
        
        # sql = f"insert into aquarium_action (time, light, pump, servo)\
        #     values(current_timestamp, {self.lightStatus}, {self.pumpStatus}, {self.servoStatus})"
            
        # cur.execute(sql)
        # conn.commit()
        
        # conn.close()
        
        self.getDataLog()
        
    def getDataLog(self):
        
        sql = "select * from aquarium"
        self.cul.execute(sql)
        result = self.cul.fetchall()
        
        

        self.aquariumDf = pd.DataFrame(result, columns= ["datetime", "water_level", "water_quality", "water_temperature"])
        self.posixTimeList = self.aquariumDf["datetime"].apply(lambda ts: ts.timestamp())
        self.dataLength = len(self.posixTimeList)
        self.drawChart(self.posixTimeList, self.aquariumDf)
       

    
        
    def drawChart(self, x, y):
        self.levelGraph.plot(x, y["water_level"], pen = pg.mkPen(color = "b", width = 2))
        self.levelGraph.getPlotItem().hideAxis("bottom")
        self.qualityGraph.plot(x, y["water_quality"], pen = pg.mkPen(color = "g", width = 2))
        self.qualityGraph.getPlotItem().hideAxis("bottom")
        self.tempGraph.plot(x, y["water_temperature"], pen = pg.mkPen(color = "r", width = 2))
        self.tempGraph.getPlotItem().hideAxis("bottom")

        


    def planSignal(self, Feed_time, Feed_number) :
        if "PM" in Feed_time :
            addNum = 12
        else :
            addNum = 0

        planTime = Feed_time.replace("AM","").replace("PM","").split(":")
        planTime = ((addNum + int(planTime[0])) * 60**2 + int(planTime[1]) * 60) * 1000
        
        if self.planList == "":
            self.planList = self.planList + str(planTime)
        else:
            self.planList = self.planList + "," + str(planTime)
        if self.mealCountList == "":
            self.mealCountList += str(Feed_number)
        else:
            self.mealCountList += "," + str(Feed_number)
        self.commendList = [0, 0, 0, self.mealCountList + ",0", 0, 0, self.startTimeTypeMilliSecond, self.planList + ",0"]

        self.sendSignal()


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

        self.planSignal(Feed_time, Feed_number)
        
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

    def sendSignal(self):
        commend = str(self.commendList).replace("[", "").replace("]", "")
        self.pySerial.write(commend.encode())

    def turnOnLight(self) : # 전구 키는 함수
        if self.commendList[2] != 1 :
            self.commendList[2] = 1
            self.sendSignal()

    def turnOffLight(self) : # 전구 끄는 함수
        if self.commendList[2] != 0 :
            self.commendList[2] = 0
            self.sendSignal()


def main() :
    app = QApplication(sys.argv)
    myWindows = iotComputer()
    myWindows.show()
    sys.exit(app.exec())


if __name__ == "__main__" : 
    main()
