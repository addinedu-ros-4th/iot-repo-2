# IoT 프로젝트 2조 저장소 - IoT를 활용한 스마트 어항 
![아두이노-_-iot-프로젝트-001](https://github.com/addinedu-ros-4th/iot-repo-2/assets/162243509/7c2da023-244b-443f-b850-9963e7ce8309)
![완성](https://github.com/seungyeonSeok/iot-/assets/162243509/bd6d6638-651a-4bfe-bdcc-81fa5c025d41) 
# 시스템 구성도 
![시스템구성도](https://github.com/addinedu-ros-4th/iot-repo-2/assets/162243509/482496b4-b52b-4568-b69c-db7211786ee8)
# 프로젝트 개요 
<h3> IoT를 활용해 물고기가 서식하기 좋은 환경으로 수온, 수질, 수위, 배식을 관리하는 스마트 어항 관리 시스템  <h3> 
  
### 기술 키워드 : ![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![C++](https://img.shields.io/badge/c++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white) ![Arduino](https://img.shields.io/badge/arduino-00878F?style=for-the-badge&logo=arduino&logoColor=white) ![Pyserial](https://img.shields.io/badge/PySerial-000000?style=for-the-badge&logo=serial&logoColor=white) ![Mysql](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![Qt](https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=Qt&logoColor=white) ![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)   
  - 팀명 : 언더더씨 
  - 팀원 : 이지호 이재혁 장종찬 석승연

  - 기간 : 24.3.7 ~ 24.3.13
## 목표 구현 기능
||분류|목표 기능|
|---|---|---|
|1| **어항 환경 측정** |센서(수온: 온도 센서/수위: 초음파 센서/수질: 탁도센서)로 각 센서 값 측정해 DB에 저장 |
|2| **어항관리- 수온** |실시간 수온 센서 값이 적정 수온 범위를 벗어나면 온열등 작동을 통한 온도 조절   |
|3| **어항관리- 수위** |실시간 수위 센서 값이 적정 수위 값을 벗어나면 펌프 작동을 통한 물 보충  |
|4| **어항관리- 수질** |실시간 수질 센서 값이 적정 수질 값을 벗어나면 어항 청소 시기 경고  |
|5| **어항 관리 동작 기록** |어항 관리 동작이 실행되면 DB에 동작값을 저장 |
|6| **배식기 작동** |배식 신호가 들어오면 서보모터가 달린 배식기를 구동시켜 정량의 사료 공급 |
|7| **예약 배식** |예약 시간, 횟수를 설정하면 해당 시간에 해당 횟수만큼 배식기 작동 |
|8| **즉각 배식** |GUI 내 밥 주기 버튼 클릭을 통해 임의로 배식기 작동   |
|9| **실시간 모니터링** |모든 과정 및 데이터, 어항 상태, 어항 기록을 GUI에 디스플레이 |
|10| **어항 환경 설정** |GUI에서 적절 온도, 수질, 수위 값을 임의로 지정해 어항 환경 설정에 적용/ 해당 설정 값 DB에 저장  |
|11| **통신** |아두이노와 pc간의 시리얼 통신|
## 역할 분담
|구분|이름|역할|
|---|---|---|
|팀장|이지호| DB 구축, pyqt DB 연결, 데이터 전송, pyqt 구성, 하드웨어 구성|
|팀원|이재현| 기초 베이스 작성, 통신 시스템 및 배식 계획 시스템 작성, Ui 연결, pyqt 구성, 하드웨어 구성|
|팀원|장종찬| 아두이노 회로도 작성,자료정리 및 보조, pyqt 구성, 하드웨어 구성|
|팀원|석승연| GUI 담당, 자료 제작, pyqt 구성, 하드웨어 구성|   

# 하드웨어 구성 
![전체](https://github.com/seungyeonSeok/iot-/assets/162243509/02b3eb07-174a-42b0-b661-12839bb5e7b6)
## 아두이노 회로도 세팅 
![아두이노_회로도](https://github.com/seungyeonSeok/iot-/assets/162243509/e35273b9-ae4b-4cf8-bb96-8d5019e555c6) 
## 하드웨어 파트별 구성 
### 1) 수온 
![수온하드웨어](https://github.com/seungyeonSeok/iot-/assets/162243509/80395899-e0ab-47d8-899f-fc1e1c2e46b7) 
- **방수형 온도 센서**: 어항 내 온도 인식
- **온열등 + 소켓 +  릴레이 스위치  + 콘센트 플러그**: 온열등 작동 신호 수신 여부에 따라 온열등 작동/ 정지
### 2) 수위 
![수위하드웨어](https://github.com/seungyeonSeok/iot-/assets/162243509/b179e6d8-7083-4a0b-95a4-7f7c8fe7f913)
- **초음파 센서**:어항 천장에 부착하여 수면까지 거리를 인식 
- **워터 펌프 + 릴레이 모듈 + 배터리**: 물 발송 신호 수신여부에 따라 펌프 작동/ 정지
### 3) 수질 
![수질하드웨어](https://github.com/seungyeonSeok/iot-/assets/162243509/76228ff6-21a5-4b17-9d2e-86847707ce1b)
- **탁도**: 어항 내 tds값 인식 
### 4) 배식 
![배식기](https://github.com/seungyeonSeok/iot-/assets/162243509/90a13bb8-61e5-486f-bdfb-18ea28488733)
- **서보모터**: 배식 신호 수신시 서보모터 가동해 배식통 회전
<br>

# 소프트웨어 구성
## State Diagram  
![상태도](https://github.com/seungyeonSeok/iot-/assets/162243509/e0cb7e1a-64b4-4a95-b5fa-a2c53670e0a5)
## Database - mysql 사용 
![디비](https://github.com/seungyeonSeok/iot-/assets/162243509/7c986707-7c3f-4d69-b460-7acb427b8525)
## UI 
![ui전체](https://github.com/seungyeonSeok/iot-/assets/162243509/26296661-1c88-4585-8a61-bc1e91ba34e9)
### 주요 기능 -  ➊ 어항 환경 설정 ➋ 어항 상태 ➌ 어항 기록 차트  ➍ 배식 설정 

### 1) 어항 환경 설정 
![ui-1번](https://github.com/seungyeonSeok/iot-/assets/162243509/e7b59789-acc5-4726-a26b-19750bf47a6d)
|  |이름|기능|
|---|---|---|
|①|**콤보 버튼**|어항 환경설정이 DB에 저장될 때의 ID값을 선택-설정 가능|
|②|**설정 추가 버튼**|팝업창을 띄워 각 센서별 적정값을 사용자 임의로 지정 가능|
|③|**팝업창- 설정 적용 버튼**|각 센서별로 지정한 값을 그 센서의 적정값으로 적용 |
|④|**설정 호출 버튼**|DB내 저장된 설정값 불러옴 |
|⑤|**설정 적용 버튼**|불러온 설정값을 적정값으로 적용 |

### 2) 어항 상태 
![ui-2번](https://github.com/seungyeonSeok/iot-/assets/162243509/8be76c63-2f09-4407-8dd1-677dae107f2e)
| |이름|기능|
|---|---|---|
|①|**실시간 센서값 표시 라벨**|각 센서별로 실시간으로 인식되고 있는 센서값 표시 |
|②|**적합/부적합 표시 라벨**|각 센서별로 실시간 센서값을 적정값과 비교해 적정하면 "적합"/어긋나면 "부적합" 표시  |
|③|**적정 값 표시 라벨**|각 센서별 적정하다 설정된 값인 적정값 표시|
|④|**어항 상태 표시 라벨**|3개 센서 모두 적합하면 "어항 상태  - 정상" 표시 / 부적합이 뜬 센서 있으면 어항 상태에 그 센서에 해당하는 경고 메세지 표시 |

### 3) 어항 기록 차트 
![ui-3번](https://github.com/seungyeonSeok/iot-/assets/162243509/060e3a72-0c94-4efb-a7a1-80aae13fed1e)
|  |이름|기능|
|---|---|---|
|①|**각 센서별 차트 표시**|DB에서 각 센서별로 센서값 데이터를 가져와 그래프 작성/실시간 업데이트|
|②|**현재 시간 표시**|실시간 날짜 & 시간 표시| 
|③|**로그 확인 버튼**|DB에서 로그 호출해 팝업창에서 센서/활동/환경 설정 로그 확인 가능| 
### 4) 배식 설정 
![ui-4번](https://github.com/seungyeonSeok/iot-/assets/162243509/79506a37-fd37-44f7-89b6-b95c5d8c83f3)
|  |이름|기능|
|---|---|---|
|①|**밥주기 버튼**|즉각배식-서보모터가 달린 배식기를 즉시 구동|
|②|**배식 횟수 콤보박스**|예약 배식 시간이 되었을때 배식기를 작동시킬 횟수를 사용자 임의로 설정 가능| 
|③|**배식 시간 콤보박스**|예약할 배식 시간을 사용자 임의로 설정 가능| 
|④|**예약 배식 시간 추가 버튼**|설정된 배식 시간/횟수로 배식 일정을 예약하여 해당 시간에 해당 횟수만큼 배식기 작동| 
|⑤|**예약 배식 시간 제거 버튼**|예약된 배식 일정을 제거함|
## 완성 
![완성모습](https://github.com/seungyeonSeok/iot-/assets/162243509/3cd7f170-31cc-4584-8cab-966450c5327c)

## 시연 영상
- https://drive.google.com/file/d/1nD5fZbdj8otzbWBBvT8c_mBsCkRcFCS9/view?usp=drive_link

## 피드백 
### 아쉬운 점
- **탁도센서의 고장**- 수질쪽의 데이터를 획득하지 못함
- **통신 개선 필요** - 아두이노로 명령리스트를 보낼때 'String' 형태로 전송했는데, 이를 일일이 ','로 구분하는 과정이 요구되어 번거롭고 오류가 발생할 가능성이 증가 

### 향후 계획
- **무선화 통신**
- **DB 활용 방안 모색**- DB를 활용한 더 다양한 기능 모색 · 추가
- **펌프 양방향 구동**- 펌프를 양방향으로 구동시켜 물을 통째로 교체하는 기능 추가

## 발표 자료 
- https://drive.google.com/file/d/1b3TimQDEieZcXCeqEaBqRGLRVPsNjqWq/view?usp=drive_link
