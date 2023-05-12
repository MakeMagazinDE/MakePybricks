from pybricks.hubs import MoveHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = MoveHub()

# aus Calibrate MM, leider rot/orange manchmal fehlerhaft
Color.orange_mm = Color(10, 97, 27)
Color.gelb_mm   = Color(50, 93, 23)
Color.gruen_mm  = Color(126, 82, 14)
Color.blau_mm   = Color(217, 96, 23)
Color.rot_mm    = Color(355, 99, 24)
Color.NONE      = Color(0,0,2)
#Color.braun_mm  = Color(350, 94, 9) # braun wir zu oft als NONE erkannt

# Tuples sind nicht indizierbar daher die Doppelung :( Python-Fu anyone?
my_colors =   (Color.NONE,Color.orange_mm, Color.gelb_mm, Color.gruen_mm, Color.blau_mm, Color.rot_mm)
list_colors = [Color.NONE,Color.orange_mm, Color.gelb_mm, Color.gruen_mm, Color.blau_mm, Color.rot_mm]

# Fach 
fach=[0,0,220,440,660,870]


# Disable the stop button.
hub.system.set_stop_button(None)

# Lipo save (angefrickelter 2S-Lipo)
if hub.battery.voltage()<6000:
    print("Battery is dying!")
    hub.system.shutdown()

# Farbsensor und Farbdefinitionen laden
sensor = ColorDistanceSensor(Port.C)
sensor.detectable_colors(my_colors)

# Motoren
beltmot = Motor(Port.B)
dispmot = Motor(Port.D,Direction.CLOCKWISE,gears=[],reset_angle=True)

# Homing Förderband (X-Achse)
def homebelt():
    print("Homing...")
    beltmot.run_until_stalled(-150, then=Stop.COAST,duty_limit=30)
    beltmot.reset_angle(0)

# Homing Auswerfer (Dispenser, Y-Achse) 
def homedisp():
    dispmot.run_until_stalled( 150, then=Stop.COAST,duty_limit=30)
    dispmot.reset_angle(0)

# X-Achse Fach anfahren 
def step(f):
    beltmot.run_target(1000,f,Stop.HOLD,True)

# Y-Achse/Dispenser MM in Sensor befördern/auswerfen
def out():
    dispmot.run_angle(400,-90,then=Stop.COAST_SMART, wait=False)
    # Auf Jam checken und ggfs zurückwackeln (verbesserungsfähig...)
    while not(dispmot.done()):
        if dispmot.stalled():
            print("Jamed!")
            # Jam blinken
            hub.light.blink(Color.RED, [300,300])
            dispmot.run_angle(300,40,then=Stop.COAST_SMART, wait=True)
            wait(100)
            dispmot.run_angle(300,-10,then=Stop.COAST_SMART, wait=True)
            wait(100)
            hub.light.on(Color.GREEN)



# Main ###################################################################
# Homing X/Y
homebelt()
homedisp()

# Auf Knopfdruck warten (MMs laden)
hub.light.blink(Color.GREEN, [500,500])
while not(hub.button.pressed()):
    pass
hub.light.on(Color.GREEN)

# first turn ?? Gut nur bei vorher leerem Magazin
out()

# Mainloop
while 1:
    # Farbe scannen
    col=sensor.color()
    # hmmm hier auch liste nehmen?! try: ersetzen...
    try:
        idx=list_colors.index(col)
        print("Erkannt:",col,"idx/Fach:",idx,fach[idx])
    except:
        idx=0
    
    # idx==0 meint "Color.NONE"
    if idx>0:
        step(fach[idx])
        out()
    else:
        #Magazin laden blinken 
        hub.light.on(Color.ORANGE)
        hub.light.blink(Color.ORANGE, [500,500])
        while not(hub.button.pressed()):
            wait(50)
            pass
        out()
        hub.light.on(Color.GREEN)  
    wait(200)
    
    