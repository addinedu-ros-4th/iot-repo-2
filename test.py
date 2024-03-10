import time


startTime = time.strftime('%H:%M:%S').split(":")
startTime = (int(startTime[0]) * 60**2 + int(startTime[1]) * 60 + int(startTime[2])) * 1000
print(startTime)