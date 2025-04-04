# -*- encoding: UTF-8 -*-

"""Example: Say `My {Body_part} is touched` when receiving a touch event"""

import qi
import argparse
import functools
import sys
import time
#from robot import Pepper

class ReactToTouch(object):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, app):
        super(ReactToTouch, self).__init__()

        # Get the services ALMemory, ALTextToSpeech.
        app.start()
        session = app.session
        self.memory_service = session.service("ALMemory")
        self.tts = session.service("ALTextToSpeech")
        # Connect to an Naoqi1 Event.
        try:
            
            self.touch = self.memory_service.subscriber("TouchChanged")
            self.id = self.touch.signal.connect(functools.partial(self.onTouched, "TouchChanged"))
            print("subscribe not error")
        except:
            self.touch = None
            print("subscribe error")
            print("Callbacks do not yet work with Python3, please run the code with Python2.7")
        self.activated_sensor = None

    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Disconnect to the event when talking,
        # to avoid repetitions
        self.touch.signal.disconnect(self.id)

        touched_bodies = []
        for p in value:
            if p[1]:
                touched_bodies.append(p[0])

        #self.say(touched_bodies)
        print("Touch detected")
        self.activated_sensor = touched_bodies
        # Reconnect again to the event
        self.id = self.touch.signal.connect(functools.partial(self.onTouched, "TouchChanged"))

    def reset(self):
       self.activated_sensor = None


    def say(self, bodies):
        if (bodies == []):
            return

        sentence = bodies[0]

        for b in bodies[1:]:
            sentence = sentence + " a " + b

        self.tts.say(sentence)

class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """

    def __init__(self, app):
        """
        Initialisation of qi framework and event detection.
        """
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        # Get the service ALMemory.
        try:
            self.memory = session.service("ALMemory")
        # Connect the event callback.
        except:
            print("robot.py session.service(ALMemory) error")
        try:
           self.subscriber = self.memory.getData("FaceDetected")
        except:
            self.subscriber = None
            print("aaa")
            print("Callbacks do not yet work with Python3, please run the code with Python2.7")
        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.face_detection = session.service("ALFaceDetection")
        self.got_face = False
        self.human_name = None

    def subscribe_2reco(self):
        # print(self.subscriber)
        self.subscriber.signal.connect(self.track_human)
        self.face_detection.subscribe("HumanGreeter")
        # return self.subscriber
        
    def track_human(self, value):
        """
        Callback for event FaceDetected.
        """
        self.got_face = True
        # First Field = TimeStamp.
        timeStamp = value[0]
        # Second Field = array of face_Info's.
        faceInfoArray = value[1]
        for j in range( len(faceInfoArray)-1 ):
            faceInfo = faceInfoArray[j]
            # First Field = Shape info, Second Field = Extra info
            faceExtraInfo = faceInfo[1]
            if faceExtraInfo[2] == "" or None:
                self.human_name = "noone"
            else:
                self.human_name = faceExtraInfo[2]
            print("Person recognized as %s"%self.human_name)
            self.got_face = False
        try:
            self.face_detection.unsubscribe("HumanGreeter")
        except:
            pass
        #self.subscriber.signal.disconnect(self.track_human)

    def learnFace(self, pId):
        """Add a new face in the database.
        :param str pId: The name of the person to save
        :returns bool: true if the operation succeeds
        """
        print("Learning face...")
        if pId is not "":
            return self.face_detection.learnFace(pId)

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        try:
            while True:
                try:
                    self.track_human(self.subscribe_2reco())
                except:
                    pass
                time.sleep(1)
        except KeyboardInterrupt:
            self.face_detection.unsubscribe("HumanGreeter")
            #stop
            sys.exit(0)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.0.125",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    PepperIP = "192.168.0.125"
    args = parser.parse_args()
    print("callback start")
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["ReactToTouch", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    react_to_touch = ReactToTouch(app)
    app.run()