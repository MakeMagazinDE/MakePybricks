from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

hub = TechnicHub()

motor= Motor(port=Port.A)

while 1:
    print(motor.angle())
    wait(100)
