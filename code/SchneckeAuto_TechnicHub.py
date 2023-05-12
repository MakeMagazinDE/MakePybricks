from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = TechnicHub()
outmot  = Motor(Port.D, positive_direction=Direction.CLOCKWISE,gears=None,reset_angle=False)

# globale Endstops
rstop = 0
lstop = 0

# Initialize "random" seed.
_rand = hub.battery.voltage() + hub.battery.current()

# Return a random integer N such that a <= N <= b.
def randint(a, b):
    global _rand
    _rand = 75 * _rand % 65537  # Lehmer
    return _rand * (b - a + 1) // 65537 + a


def home():
    global rstop
    global lstop
    print("Homing...")
    outmot.run_until_stalled(-1050, then=Stop.COAST,duty_limit=24)
    outmot.reset_angle(0)      # Anschlag auf 0
    rstop=outmot.angle()+50    # etwas Toleranz
    outmot.run_until_stalled( 1050, then=Stop.COAST,duty_limit=24)
    lstop=outmot.angle()-50
    print("Homing done...")
    print("Stops:", rstop,lstop)

def seek(to):
    print("seek from",outmot.angle(),"to",to,"distance",abs(outmot.angle()-to))
    outmot.track_target(to)
    if outmot.angle()>to:
        while outmot.angle()>=to:
           pass
    else:
        while outmot.angle()<=to:
            pass


# main
home()

while 1:
    seek(randint(lstop,rstop))
