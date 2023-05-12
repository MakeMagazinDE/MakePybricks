from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
#from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = TechnicHub()

motor= Motor(port=Port.D,reset_angle=True)
motor.reset_angle(0)

motor.control.limits(torque=30)
motor.hold()

while 1:
    print(motor.angle())
    wait(100)
