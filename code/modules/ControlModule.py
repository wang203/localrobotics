'''
@author: oliver lewis May 28, 2014
'''

from lib import libardrone
import cv2
from modules.TrackingSensorModule import TrackingSensorModule
import datetime
#import pika
import json

command = {10:'takeoff', ord('l'):'land', ord(' '):'hover', ord('w'):'move_forward', ord('s'):'move_backward', ord('a'):'move_left', ord('d'):'move_right', 81:'turn_left', 82:'move_up',83:'turn_right',84:'move_down',8:'emergency'}
class ControlModule():
    def __init__(self, drone, trackingSensorModule):
        self.drone = drone
        self.trackingSensorModule = trackingSensorModule
        #self.auto_control = False
        self.auto_control = True
        #self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        #self.channel = self.connection.channel()
        #self.channel.exchange_declare(exchange="drone", exchange_type="direct", passive=False)


    def sendCommand(self, command):
        self.drone.apply_command(command)
        
    def sendPosition(self, x_pos, y_pos):
        self.drone.at(libardrone.at_pcmd, True, x_pos, y_pos, 0, 0)
        
    def hover(self):
        self.drone.hover()
        
    def stopDrone(self):
        self.drone.land()
        self.drone.halt()

    def autoControlDrone(self, circles):
        method_frame, header_frame, body = self.channel.basic_get('control')
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            d = json.loads(body)
            print body
            print str("position" in d["control"])
            if "position" in d["control"]:
                print d["control"]["position"][0], d["control"]["position"][1]
                self.sendPosition(d["control"]["position"][0], d["control"]["position"][1])
            else:
                self.hover()
        else:
            self.hover()

    def autoControlDroneLocal(self, circles):
        #print "Auto Control Drone Local!"
        if circles != None:
            pos_x, pos_y = self.trackingSensorModule.calculatePosition(circles)
            #print pos_x, pos_y
            self.sendPosition(pos_x, pos_y)

    def completeController(self):
        try:
            #f = open('workfile.txt', 'w')
            d = {}
            while True:                               
		frame = self.drone.get_image()

                #f.write(str(datetime.datetime.now()))
                #f.write("\n")
                #str_alt =  "altitude : ",self.drone.get_navdata()[0]["altitude"]
                #f.write(str(str_alt))
                #f.write("\n")
                '''detect_circles'''
                circles = self.trackingSensorModule.detectCircles(frame)
                if circles != None:
                    frame = self.trackingSensorModule.drawTrackingImages(frame, circles)
                
                self.trackingSensorModule.displayDroneCamera(frame)
                
                '''(x,y) = calculate_positions()'''
                if self.auto_control:
                    #self.autoControlDrone(circles)
                    self.autoControlDroneLocal(circles)

                k = cv2.waitKey(1) & 0xFF
                #print k, "################"
                if k in command:
                    self.sendCommand(command[k])
                elif k == ord('c'):
                    self.auto_control = True
                elif k == ord('x'):
                    self.auto_control = False
                elif k == ord('q'):
                    break
        finally:
            self.stopDrone()       
                
