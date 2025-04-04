# -*- coding: utf-8 -*-

import qi
import argparse
import sys
import time
from robot import Pepper

robot = Pepper("192.168.0.125", 9559)




# try:
#     raw_input("Press the enter key to exit")    
# finally:
#     pass
# robot.speech_service.subscribe("my_dialog") #이건뭐 꼼작을 안함

topicContent2 = ("topic: ~mytopic2()\n"
                    "language: kok\n"
                    "proposal: This is KUPepper, How to help you??\n")
robot.autonomous_life_service.setState("interactive")
loaded_topic=robot.dialog_service.loadTopicContent(topicContent4) #load topic content
robot.dialog_service.activateTopic(loaded_topic) #activate topic
robot.dialog_service.subscribe("my_dialog") #start dialog engine
robot.dialog_service.setFocus("topic1") #set focus to the topic
robot.dialog_service.setConfidenceThreshold(loaded_topic,0.05) #set confidence threshold
robot.autonomous_life_service.switchFocus("pepper_test-c675d3/behavior_1") #package-uuid/behavior-path
loaded_topic=robot.dialog_service.loadTopicContent(topicContent2) #load topic content
robot.dialog_service.activateTopic(loaded_topic) #activate topic
robot.dialog_service.subscribe("my_dialog") #start dialog engine

while True:
    print(robot.memory_service.getData("ALSpeechRecognition/Status"))
    time.sleep(0.1)


