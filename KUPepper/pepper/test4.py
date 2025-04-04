# -*- coding: utf-8 -*-

import qi
import argparse
import sys
import time
from robot import Pepper

robot = Pepper("192.168.0.125", 9559)


robot.detect_service.subscribe("my_detect") #start dialog engine


#평상시에 페퍼 단어를 인식해야함


# topicContent2 = ("topic: ~mytopic2()\n"
#                     "language: enu\n"
#                     "proposal: This is KUPepper, How to help you??\n")
# robot.autonomous_life_service.setState("interactive")
# loaded_topic=robot.dialog_service.loadTopicContent(topicContent2) #load topic content
# robot.dialog_service.activateTopic(loaded_topic) #activate topic
# robot.dialog_service.subscribe("my_dialog") #start dialog engine
# robot.dialog_service.setFocus("mytopic2") #set focus to the topic

robot.speech_service.pause(True) 
robot.speech_service.removeAllContext() #context를 지워야하는지 몰루
robot.speech_service.deleteAllContexts()
robot.speech_service.setVocabulary(["Cuper",'pepper'],False) #true 하면 "<...> hi <...>" 이렇게 나옴
robot.speech_service.pause(False)

while True:
    print(robot.memory_service.getData("WordRecognized"))
    time.sleep(0.1)

# print(robot.memory_service.getDataList("Sound"))  #  ['SoundDetected', 'ALSignsAndFeedback/SoundDetected']
