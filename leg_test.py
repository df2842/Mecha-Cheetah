from math import sin, cos
from pylx16a.lx16a import *
import time

import constants

LX16A.initialize("COM3")

try:
    fl_hip = LX16A(constants.FL_HIP_SERVO_ID)
    fl_knee = LX16A(constants.FL_KNEE_SERVO_ID)
except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    exit()

t = 0
while True:
    fl_hip.move(sin(t) * constants.HIP_SERVO_RANGE + constants.SERVO_ZERO_POSITION)
    fl_knee.move(cos(t) * constants.KNEE_SERVO_RANGE + constants.SERVO_ZERO_POSITION)

    time.sleep(0.05)
    t += 0.05