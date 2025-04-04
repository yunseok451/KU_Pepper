#!/usr/bin/env python
# -*- coding: utf-8 -*-

import qi
import Tkinter
from robot import Pepper
import threading
import sys
import time
import cv2
from flask import Flask, render_template, redirect, url_for, request
import socket
import speech_recognition as sr
import numpy
############################################################################################

#flask 웹서버


app = Flask(__name__)
web_host = "192.168.0.125"
web_page = "http://192.168.0.125:8080/"


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('main.html')
    
@app.route('/start', methods=['GET', 'POST'])
def test1():
    if request.method == 'POST':
        return render_template('main.html')
        # return "test page 1"
        app.test2 = 1    
    return redirect(url_for('main_page'))
 
@app.route('/test2', methods=['GET', 'POST'])
def test2():
    if request.method == 'POST':
        # return "test page 2"
        app.test2 = 2
    return redirect(url_for('main_page'))


#플라스크 변수: 전역변수랑 같음(웹 이벤트 작동 시 사용)
app.test2 = 0

############################################################################################



class KUpepper:
    def __init__(self, ip, port):
        #페퍼 라이브러리
        self.ip = ip
        self.port = port
        self.robot = Pepper(self.ip, self.port)
        self.robot.say("HI Pepper")

        #베이스 라인 코드
        # self.event = threading.Event()
        # socket_thread = threading.Thread(target=self.socket_Server_connect)
        # socket_thread.start()
        # self.base_thread = threading.Thread(target=self.baseline)
        # self.base_thread.daemon = True
        # self.base_thread.start()

        # self.event = threading.Event()
        # self.base_thread = threading.Thread(target=self.person_recognition)
        # self.base_thread.daemon = True
        # self.base_thread.start()
        self.person_recognition()

        #GUI
        # self.window = Tkinter.Tk()
        # self.base_interface_robot()
        # self.result_map= 0 
        # self.resolution=0 
        # self.offset_x =0 
        # self.offset_y =0




    #이벤트 작동 간 쓰레드 중지
    def stopThreadUntilOneTheEnd(self):
        if self.event.is_set():
            while True:
                if self.event.is_set():
                    time.sleep(0.1)
                else:
                    break

    #현재 상태 출력 모음
    def status_print(self):
        print("focus activity:", self.robot.autonomous_life_service.focusedActivity())
        print("context:", self.robot.memory_service.getData('Diagnosis/Temperature/Tablet/Error'))
        # print("key list:", self.robot.memory_service.getDataListName( ))
        # print("context:", self.robot.autonomous_life_service.getFocusHistory())    
        # print("context:", self.robot.autonomous_life_service.getFocusContext())
        # print("laser x:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Vertical/Right/Seg01/X/Sensor/Value"))
        # print("laser y:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Vertical/Right/Seg01/Y/Sensor/Value"))
        print("laser front value:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/LaserSensor/Front/Reg/Status/Sensor/Value"))
        print("usersession:", self.robot.user_session.getOpenUserSessions())
        print("front sonar value:", self.robot.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value"))

    #기본 파라미터 구성
    def base_parameter(self):
        self.robot.set_security_distance(distance=0.2)
        self.set_vocabulary()
        self.robot.text_to_speech.setLanguage("Korean") #타블렛 화면도 한글로 
        topicContent2 = ("topic: ~mytopic2()\n"
                            "language: enu\n"
                            "proposal: This is KUPepper, How to help you??\n")
        self.robot.autonomous_life_service.setState("interactive")
        self.robot.autonomous_life_service.switchFocus("web_site-9108dc/behavior_1") #package-uuid/behavior-path
        loaded_topic=self.robot.dialog_service.loadTopicContent(topicContent2) #load topic content
        self.robot.dialog_service.activateTopic(loaded_topic) #activate topic
        self.robot.dialog_service.subscribe("my_dialog") #start dialog engine
        # self.load_map_and_localization()
        # print(self.robot.navigation_service.getMetricalMap())

    #페퍼 상호작용
    def interaction(self):
        #머리 터치 시 상호작용
        if self.robot.memory_service.getData("Device/SubDeviceList/Head/Touch/Front/Sensor/Value"):
            self.robot.say("무슨 일이신가요?")
    
    #웹 상호작용
    def web_interaction(self):
        #이동 상호작용
        # print("interaction number: ", app.test2)
        if app.test2 == 1:
            app.test2 = 0

            self.navigation_mode_button_web()
        elif app.test2 == 2:
            app.test2 = 0
            # self.talk_pepper()
     
    #기본 루프
    def baseline(self):
        while_count = 0
        self.base_parameter()

        try:
            while True:
                self.stopThreadUntilOneTheEnd()
                word =self.robot.memory_service.getData("WordRecognized")
                # print(word) #확인용
                # if self.robot.memory_service.getData("ALSpeechRecognition/Status") == "SpeechDetected":
                #     self.talk_pepper()
                if word[1]>=0.40:
                    self.robot.say("네에, 말씀하세요")
                    self.person_recognition()
                    self.listen_pepper()
                    self.talk_pepper()
                    

                self.web_interaction()
                self.interaction()
                time.sleep(0.1)
                while_count += 1


        except KeyboardInterrupt:
            #stop
            sys.exit(0)
        print("exit")

    #맵 종류
    #2024-02-14T082317.984Z.explo(8층 pbl실 기본 explore() 맵)
    #2024-02-16T133625.109Z.explo(앞 부분만 찍은 explore() 맵)
    #2024-02-16T140640.347Z.explo
    #2024-02-16T140903.087Z.explo( 의자로 맵 만든 거 explore())
    #2014-04-04T023359.452Z.explo( 의자로 맵 만든 거2)
    #2014-04-04T030206.953Z.explo(세번째)
    #2024-02-27T084209.829Z.explo 방향 확인 하기 위한 임시 =

    #맵 로드 후 로컬라이제이션
    def load_map_and_localization(self):
        self.event.set()
        self.robot.stop_localization()
        # self.robot.load_map(file_name="2024-02-15T080619.628Z.explo")
        # self.robot.load_map(file_name="2024-02-15T074705.482Z.explo")
        self.robot.load_map(file_name="2024-02-27T084209.829Z.explo")
        self.robot.first_localization()
        self.event.clear()

    def session_reset(self):
        self.robot.session.reset

    #gpt
    def talk_pepper(self):
        self.listen_pepper() #페퍼가 녹음파일을 가짐
        self.robot.download_file("speech.wav") #이거 녹음 파일 한번 처리하고 분석해야할꺼같음

        # self.robot.say(r.recognize_google(audio, language='ko-KR').encode('utf8'))
        #여기서 recognize로 인식하는데 인식못했을때는 죄송합니다 하고 다시 인식하게 만들어야함

        try:
            msg =self.audio_to_text()
            data = self.get_data_gpt(msg) 
            self.robot.say(data) #받은 string을 말하기- 질문에 답변
        except:
            self.robot.say("죄송합니다. 다시 말해주시겠습니까?") #인식못했을때
        finally:
            self.event.clear()
            time.sleep(0.1)
    
    def listen_pepper(self):
        self.event.set()
        self.robot.audio_recorder.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0)) #녹화 시작

        #여기서 endofprocess가 나올때까지 기다리는데 일정시간 지나면 끝내는 코드를 넣어야함
        while True:
            print(self.robot.memory_service.getData("ALSpeechRecognition/Status"))
            if self.robot.memory_service.getData("ALSpeechRecognition/Status") == "EndOfProcess":
                self.robot.audio_recorder.stopMicrophonesRecording()
                break

        # self.robot.audio_service.playFile("/home/nao/speech.wav") #mp3파일 재생 확인용
        pass

    def audio_to_text(self):
        r = sr.Recognizer()
        kr_audio = sr.AudioFile("tmp_files/speech.wav")
        with kr_audio as source:
            audio = r.record(source)
       
        msg = r.recognize_google(audio, language='ko-KR') #음성을 변환
        return msg

    def get_data_gpt(self,msg):
        self.client_soc.sendall(msg.encode(encoding='utf-8')) #변환텍스트를 서버로 전달
        data = self.client_soc.recv(1000)#메시지 받는 부분
        return data

    def dialog(self):
        while True:
            self.person_recognition()
            self.listen_pepper()
            self.talk_pepper()
            #답변에 만족하셨나요? or 다른 질문은 없으신가요?
            #상대의 답변을 듣고 목적파악!
            self.check_purpose()
            #목적(상태)에 맞게 동작!
            pass
        pass

    #사람인식
    def person_recognition(self):
        self.robot.sonar_service_.subscribe("testapp")

        try:
            while True:
                print(self.robot.memory_service.getData("Device/SubDeviceList/Platform/InfraredSpot/Right/Sensor/Value"))
                time.sleep(0.2)

        except KeyboardInterrupt:
            #stop
            self.robot.sonar_service_.unsubscribe("testapp")
            sys.exit(0)
    

    #상대방의 목적확인
    def check_purpose(self):
        pass

    def set_vocabulary(self):
    #setVocabulary
        self.robot.speech_service.pause(True) 
        self.robot.speech_service.removeAllContext() #context를 지워야하는지 몰루
        self.robot.speech_service.deleteAllContexts()
        self.robot.speech_service.setVocabulary(["cooper",'pepper','fe puff','pepeo'],False) #true 하면 "<...> hi <...>" 이렇게 나옴
        self.robot.speech_service.pause(False)

    #error
    def sonar_getdata(self):
        print("sonarleft" , self.robot.sonar_service.SonarLeftDetected())
        print("sonarright" ,self.robot.sonar_service.SonarRightDetected())
        print("sonarnothingleft", self.robot.sonar_service.SonarLeftNothingDetected())
        print("sonarnothingright",self.robot.sonar_service.SonarRightNothingDetected())
        pass

    #no need
    def security_data(self):
        print("othogna:" ,self.robot.motion_service.getOrthogonalSecurityDistance())
        print("tangential:" ,self.robot.motion_service.getTangentialSecurityDistance())
        print("enable security: ", self.robot.motion_service.getExternalCollisionProtectionEnabled("All"))
        # print("aa: ", self.robot.motion_service.isCollision())

    #기본 움직임
    def base_move(self):
        # print((round(self.robot.motion_service.getAngles("HeadPitch", True)[0],1)+0.5)*10)
        # self.robot.motion_service.move(0,0,(round(self.robot.motion_service.getAngles("HeadPitch", True)[0],1)+0.5)*10)
        # self.robot.motion_service.move(1,0,0)
        print((round(self.robot.motion_service.getAngles("HeadYaw", True)[0],1)))
        self.robot.motion_service.move(0,0,(round(self.robot.motion_service.getAngles("HeadYaw", True)[0],1)))
        self.robot.motion_service.move(1,0,0)

    #GUI에 기능 적용
    def base_interface_robot(self):

        self.window.geometry("400x200")
        self.window.title("pepper")
        self.frame_1 = Tkinter.Frame(self.window)
        self.frame_1.pack(side="top")
        self.frame_2 = Tkinter.Frame(self.window)
        self.frame_2.pack(side="top")
        self.exploration_pepper_button()
        self.navigation_pepper_button()
        self.webpage_reset_button()
        self.show_map_button()
        self.slam_start_button()
        self.slam_stop_button()


        #마지막에 있어야함
        self.window.mainloop()

    def exploration_mode_button_push(self, text):
        try:
            self.event.set()
            result = text.get("1.0", "end")
            self.robot.exploration_mode(int(result))
        except: 
            pass
        self.event.clear()

    def navigation_mode_button_web(self):
        self.event.set()
        move_pepper = threading.Thread(target=self.move(0, 0))
        self.event.clear()
        
    def navigation_mode_button_push(self,text,text2):
        
        self.event.set()
        x = text.get("1.0", "end")
        y = text.get("1.0", "end")
        move_pepper = threading.Thread(target=self.move(int(x),int(y)))
        move_pepper.start()

        self.event.clear()

    def show_map_button_push(self):
        self.event.set()               
        show_map_thread = threading.Thread(target=self.robot.show_map)
        show_map_thread.start()
        show_map_thread.join()
        imshow_map_thread = threading.Thread(target=self.imshow_map)
        imshow_map_thread.start()   
        self.event.clear()

    def imshow_map(self):
            cv2.imshow("RobotMap", self.robot.robot_map)
            cv2.setMouseCallback("RobotMap", self.mouse_callback)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flags, param):
        # 마우스 왼쪽 버튼을 클릭할 때
        if event == cv2.EVENT_LBUTTONDOWN:
            # map_y = (x * self.robot.resolution + self.robot.offset_x)
            # map_x = (y * self.robot.resolution - self.robot.offset_y)
            map_x = (x * self.robot.resolution + self.robot.offset_x)
            map_y = -1 * (y * self.robot.resolution - self.robot.offset_y)
            # map_x = x
            # map_y = y
            print("mouse click:", map_x, map_y)
            self.move(map_x,map_y)
            pos = self.robot.pos[0]
            goal_x = (pos[0] - self.robot.offset_x) / self.robot.resolution
            goal_y = -1 * ((pos[1] - self.robot.offset_y) / self.robot.resolution)
            self.robot.robot_map = cv2.circle(self.robot.robot_map, (int(goal_x), int(goal_y)), 3, (255, 0, 0), -1)
            self.show_map_button_push()

    def web_page_reset(self):
        self.event.set()
        self.web_thread = threading.Thread(target=self.robot.show_web(web_page))
        self.web_thread.start()     
        self.robot.say("web page reset")
        self.event.clear()

    def move(self,x,y):
        try:
            self.event.set()
            self.robot.navigate_to(x, y)
            map_x = (x * self.robot.resolution)
            map_y = -1 * (y * self.robot.resolution)
            # map_x = x
            # map_y = y
            print("mouse click:", map_x, map_y)
            pos = self.robot.pos[0]
            goal_x = (pos[0] - self.robot.offset_x) / self.robot.resolution
            goal_y = -1 * ((pos[1] - self.robot.offset_y) / self.robot.resolution)
            self.robot.robot_map = cv2.circle(self.robot.robot_map, (int(goal_x), int(goal_y)), 3, (255, 0, 0), -1)
            self.show_map_button_push()
        except:
            print("open the map first")
        self.event.clear()

    def slam_start_button_push(self):
        self.event.set()
        self.slam_start_thread = threading.Thread(target=self.robot.slam(status=True))
        self.event.clear()

    def slam_stop_button_push(self):
        self.event.set()
        self.slam_stop_thread = threading.Thread(target=self.robot.slam(status=False))
        self.event.clear()

    def session_reset(self):
        self.robot.session.reset

    #gui 기능(버튼 등) 설계
    def navigation_pepper_button(self):
        text = Tkinter.Text(self.frame_2, height =1, width= 5)
        text2 = Tkinter.Text(self.frame_2, height =1, width= 3)
        button = Tkinter.Button(self.frame_2, text="이동(x,y)", command=lambda: self.navigation_mode_button_push(text, text2))
        text.pack()
        text2.pack()
        button.pack()
        # button.grid(row=1, column=1)
        # text.grid(row=1, column=2)
        # text2.grid(row=1, column=3)
        self.window.bind("<")
        
    def exploration_pepper_button(self):
        text = Tkinter.Text(self.frame_1, height =1, width= 5)
        button = Tkinter.Button(self.frame_1, text="맵핑 모드", command=lambda: self.exploration_mode_button_push(text))
        button.pack()
        text.pack()
        # button.grid(row=1,column=1)
        # text.grid(row=1,column=2)
        self.window.bind("<")

    def webpage_reset_button(self):
        button = Tkinter.Button(self.window, text="웹페이지 리셋", command=self.web_page_reset)
        button.pack()
        self.window.bind("<")

    def show_map_button(self):
        button = Tkinter.Button(self.window, text="맵 확인", command=self.show_map_button_push)
        button.pack()
        self.window.bind("<")

    def slam_start_button(self):
        button = Tkinter.Button(self.window, text="수동 맵핑 시작", command=self.slam_start_button_push)
        button.pack()
        self.window.bind("<")

    def slam_stop_button(self):
        button = Tkinter.Button(self.window, text="수동 맵핑 금지", command=self.slam_stop_button_push)
        button.pack()
        self.window.bind("<")
        # label = Tkinter.Label(self.window, text="안녕하세요!")
        # # 레이블 위치 설정
        # label.place(x=150, y=150)
        # 버튼 위치 설정
        # button.place(x=180, y=200)

    def socket_Server_connect(self):
            host = web_host
            port = 3333

            # 서버소켓 오픈/ netstat -a로 포트 확인
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))

            # 클라이언트 접속 준비 완료
            server_socket.listen(1)

            print('echo server start')

            #  클라이언트 접속 기다리며 대기 
            self.client_soc, addr = server_socket.accept()
            print('connected client addr:', addr)

            time.sleep(999999)
            print('서버 종료.')
            # socket_Server_connect.close()

def main():
    pepper = KUpepper("192.168.0.125", "9559")

if __name__ == "__main__":
    base_thread = threading.Thread(target=main)
    base_thread.daemon = True
    base_thread.start()

    # app.run(host=web_host, port=8080, debug=False)

    main()
    

    

    
