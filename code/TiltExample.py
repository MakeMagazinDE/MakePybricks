from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Direction, Port, Side, Stop
from pybricks.tools import wait

# Initialize the hub.
hub = TechnicHub()

motor= Motor(port=Port.D,reset_angle=True)
motor.reset_angle(0)


while True:
    # Read the tilt values.
    pitch, roll = hub.imu.tilt()

    # Print the result.
    print(pitch, roll)
    
    # Try either one
    motor.track_target(-roll)
    #motor.run_target(1500,-roll,wait=False)
    wait(100)