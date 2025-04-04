import qi
from robot import Pepper, HumanGreeter
import callbacks
import numpy as np
import time
import sys
import speech_recognition as sr
import os
PepperIP = "192.168.0.125"
robot = Pepper(PepperIP,9559)
a = HumanGreeter(robot.app)
robot.say("HI HIHIHIHIHIHIHI")

robot.recordSound()
robot.download_file("speech.wav")
r = sr.Recognizer()
kr_audio = sr.AudioFile("D:/Pepper_Controller_main/pepper/tmp_files/speech.wav")
with kr_audio as source:
    audio = r.record(source)
print(r.recognize_google(audio, language='ko-KR'))
robot.say(r.recognize_google(audio, language='ko-KR').encode('utf8'))
# robot.chatbot()
# a.track_human(5)
# print("----------------")
# print(round(robot.motion_service.getAngles("HeadPitch", True)[0],1))
# print("----------------")
# move = round(robot.motion_service.getAngles("HeadPitch", True)[0],1)*10
# print(type(np.random.randint(-10, 10)))
# robot.motion_service.move(0,0,round(robot.motion_service.getAngles("HeadPitch", True)[0],1))

# robot.do_hand_shake()
# a.run()
# robot.show_web("https://www.google.com/")
# robot.pick_a_volunteer()
# robot.show_web("http://192.168.0.82:80/")
# robot.sound_detect_service.setParameter("Sensitivity", 1.0)
# robot.listen("en-US")
# robot.chatbot()
#test sonar
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"))
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"))
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"))
# print(robot.memory_service.getData("Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value"))

# explore
# robot.set_security_distance(0.15)
# robot.exploration_mode(20)
# robot.show_map(on_robot=True)

#robot.robot_localization()


# robot.stop_localization()
# robot.load_map(file_name="map.png",file_path="./")
# robot.robot_localization()
# robot.navigate_to(0, 0)
# robot.navigate_to(1, 0)
# robot.navigate_to(3, 0)


# robot.stop_localization()

# try:
#     while True:
        
#         print((round(robot.motion_service.getAngles("HeadPitch", True)[0],1)+0.5)*10)
#         robot.motion_service.move(0,0,(round(robot.motion_service.getAngles("HeadPitch", True)[0],1)+0.5)*10)
#         robot.motion_service.move(1,0,0)
#         time.sleep(0.1)
# except KeyboardInterrupt:
#     #stop
#     sys.exit(0)


# a.subscribe_2reco()
#HumanGreeter.track_human(10)
#a = robot.recognize_person
#robot.get_face_properties()
#robot.say(a)
# robot.pick_a_volunteer()
