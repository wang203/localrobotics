Tracking Sensor Module
======================================================================



Design Features
----------------------------------------------------------------------


Code
-----

The Tracking Sensor module is the class in which the camera and display of the visual image is handled. The Visual component is handled by the external library numpy and cv2.

detectCircles
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This function interacts with the control module and returns the circles detected.

	* Arguments: frame : image frame received from the drone
	* return : circles : circles detected by the cv2.HoughCircles functions.

The function snippet is as follows::

  gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(3,3),0)
        canny = cv2.Canny(gray,100,200)
        circles = cv2.HoughCircles(canny,3,1,20,param1=120,param2=10,minRadius=15,maxRadius=25)
        if circles != None:
            n = np.shape(circles)
            circles=np.reshape(circles,(n[1],n[2]))
            det_circle_count = circles.size/3
        return circles


drawTrackingImages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function draws the circle around the object detected and the line drawn is the distance between the center of the drone and the object.

	* Arguments:
		frame : image frame received from the drone.
		circles : circles returned from the detectCircles function.
	* return : frame

The function snippet is as follows::

  for circle in circles:
            cv2.circle(frame,(circle[0],circle[1]),circle[2],(0,0,255))
            cv2.line(frame, self.getCenter(),(circle[0],circle[1]),(255,0,0))
        return frame


displayDroneCamera
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The displayDroneCamera function will display the frame using the cv2 library.

	* Arguments: frame : image frame received from the drone

The function snippet is as follows::

  cv2.imshow("Drone Camera",cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

calculatePosition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The calculatePosition function will calculate the distance between the drone and the object. Its the function where a primitve motion planning is done.

The function snippet is as follows::

  if circles.size == 3:
            x = circles[0][0]
            y = circles[0][1]
            target_y = self.getCenter()[1] - y
            target_x = x - self.getCenter()[0]
            kX = 1.0/320*0.1
            kY = -1.0/320*0.1
        return (kX*target_x, kY*target_y)

