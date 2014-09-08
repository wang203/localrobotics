Control Module
======================================================================



Design Features
----------------------------------------------------------------------


Code
-----

The control module is the class in which the motion planning of the drone is calculated, the control module also sends control commands to the drone based on the messages received from the visual sensing component. The commands sent from the keyboard during manual control are as follows::

  {10:'takeoff', ord('l'):'land', ord(' '):'hover', ord('w'):'move_forward', ord('s'):'move_backward', ord('a'):'move_left', ord('d'):'move_right', 81:'turn_left', 82:'move_up',83:'turn_right',84:'move_down',8:'emergency'}



completeController
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This function interacts with the tracking module and with the drone.
Sequentially the steps can be listed as follows:
	1) Get image.
	2) Detect circles.
	3) Draw tracking images if circles detected.
	4) Display the camera input from the drone.
	5) If auto control is enabled go to the auto control fucntion.
	6) If manual control is enabled wait for the input from the keyboard.
	7) Send keyboard command to the drone.
	8) Finally the stop drone function is called.

The function snippet is as follows::

  try:
            while True:                               
                frame = self.drone.get_image()
                '''detect_circles'''
                circles = self.trackingSensorModule.detectCircles(frame)
                if circles != None:
                    frame = self.trackingSensorModule.drawTrackingImages(frame, circles)
                
                self.trackingSensorModule.displayDroneCamera(frame)
                
                '''(x,y) = calculate_positions()'''
                if self.auto_control:
                    self.autoControlDrone(circles)                
                
                k = cv2.waitKey(1) & 0xFF
                print k, "################"
                if k in command:
                    self.sendCommand(command[k])
                elif k == ord('c'):
                    self.auto_control = True
                elif k == ord('x'):
                    self.auto_control = False
        finally:
            self.stopDrone() 


autoControlDrone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function is used if the auto control is enabled. The auto control of the drone will use the input received from the camera to detect the object and try to follow or hover exactly above the object.

	* Arguments: circles : circles detected from the camera
	* return : none

Sequentially the steps can be listed as follows:
	1) If circles are present then calculate the position of the center.
	2) send this position to the drone by calling the sendPosition function and by sending the X and Y co-ordinates of the center.
	3) Else the drone is made to hover over the object.

The function snippet is as follows::

  if circles != None:
            if(circles.size == 3):
                position = self.trackingSensorModule.calculatePosition(circles)
                self.sendPosition(position[0], position[1])
            else:
                self.hover()
        else:
            self.hover()


hover
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The hover function will cause the drone to hover.

The function snippet is as follows::

  self.drone.hover()

stopDrone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The stopDrone function will make the drone land.

The function snippet is as follows::

  self.drone.land()
  self.drone.halt()


sendCommand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The sendCommand function will send the command to the drone

The function snippet is as follows::

  self.drone.apply_command(command)

sendPosition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The sendPosition function will send the X and Y position to the drone and the drone will use its 'at' commands to send the position.

The function snippet is as follows::

  self.drone.at(libardrone.at_pcmd, True, x_pos, y_pos, 0, 0) 





