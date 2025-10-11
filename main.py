from pylx16a.lx16a import *

from constants import *
from leg import Leg

if __name__ == "__main__":
    LX16A.initialize("COM3")

    fl_leg = Leg(hip_servo_id=FL_HIP_SERVO_ID, knee_servo_id=FL_KNEE_SERVO_ID, inverted=False)

    fl_leg.move_all(hip_servo_position=50, knee_servo_position=-50, hip_speed=0.5, knee_speed=1)
    fl_leg.move_all(hip_servo_position=-50, knee_servo_position=50, hip_speed=0.5, knee_speed=1)