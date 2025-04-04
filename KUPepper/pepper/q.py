import qi
from robot import Pepper, HumanGreeter
import time
PepperIP = "192.168.0.125"
robot = Pepper(PepperIP,9559)
map_path = "2024-02-14T082317.984Z.explo" #
#navigation
# robot.load_map(map_path)
# robot.navigation_service.startLocalization()
# print(robot.navigation_service.getRobotPositionInMap())
# robot.navigation_service.navigateToInMap([0, 0, 0])
# print(robot.navigation_service.getRobotPositionInMap())
# robot.navigation_service.stopLocalization()
# robot.show_map(on_robot=True)
#activity
# print(robot.autonomous_life_service.getFocusHistory())
# print(robot.autonomous_life_service.getFocusContext())
# print(robot.autonomous_life_service.getActivityStatistics())
# robot.autonomous_life_service.switchFocus("pepper_test-c675d3/behavior_1") #package-uuid/behavior-path
#autonomous life
# robot.autonomous_life_service.setState("solitary")
#play song for using url
robot.autonomous_life_service.setState("safeguard")
web_page = "https://www.youtube.com/watch?v=6NbCxN1HE1k&ab_channel=SunsetMood/"
robot.show_web(web_page)
robot.set_volume(45)
robot.tablet_service.setBrightness(1.0)
# video = "https://vt.tumblr.com/tumblr_o600t8hzf51qcbnq0_480.mp4"
# robot.tablet_service.playVideo(video)
#behavior
# print(robot.list_behavior())
# robot.start_behavior("System/animations/Stand/Gestures/Hide_1")
#tablet service
# robot.tablet_service.turnScreenOn(True)
# robot.tablet_service.goToSleep()
# robot.tablet_service.wakeUp()
#tts wih human
# robot.ask_wikipedia()
# robot.recordSound()
# robot.say("now i listen")
# robot.rest()
# robot.stand()
# robot.set_korean_language()
# robot.autonomous_life_on()
# # robot.face_tracking()
# while True:
#     if robot.memory_service.getData("FaceDetected"):
#         robot.say("안녕하세요~")
#         time.sleep(1.3)
# robot.load_map(map_path)
# robot.show_map(on_robot=True)
# robot.stop_face_tracking()
# robot.testing()
# robot.play_sound("/home/nao/speech.wav")
# robot.say("안녕 나는 페퍼야, 너는 누구니??")