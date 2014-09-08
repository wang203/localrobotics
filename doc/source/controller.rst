Controller
======================================================================



Design Features
----------------------------------------------------------------------


Code
-----

Python objects of the libdrone and the TrackingSensorModule are instantiated and the drone is configured, these objects are then passed to the VideoController class::

  drone = libardrone.ARDrone2()
  trackingSensorModule = TrackingSensorModule()
  drone.configureDrone()	
  controller = VideoController(drone, trackingSensorModule)



VideoController
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The VideoController is a thread that takes the drone and the sensing class as the arguments during creation of an object.

The run method of the thread passes the drone and the sensing object to the control module as the control module is in charge of controlling the Drone with input/feedback from the camera sensor::

  controlModule = ControlModule(self.drone, self.sensorModule)
  controlModule.completeController()


ManualController
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The manual controller is a thread that takes in the drone as an argument and uses the keyboard keys to control the movement of the drone.
