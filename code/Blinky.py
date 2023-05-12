from pybricks.hubs import TechnicHub
from pybricks.parameters import Color
from pybricks.tools import wait

hub = TechnicHub()
hub.light.blink(Color.GREEN, [500,500])

wait(10000)
