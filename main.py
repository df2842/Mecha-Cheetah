from pylx16a.lx16a import *
import time

from constants import *
from leg import Leg

if __name__ == "__main__":
    LX16A.initialize("COM3")

    fl_leg = Leg(hip_servo_id=FL_HIP_SERVO_ID, knee_servo_id=FL_KNEE_SERVO_ID, inverted=False)
    fr_leg = Leg(hip_servo_id=FR_HIP_SERVO_ID, knee_servo_id=FR_KNEE_SERVO_ID, inverted=True)
    bl_leg = Leg(hip_servo_id=BL_HIP_SERVO_ID, knee_servo_id=BL_KNEE_SERVO_ID, inverted=False)
    br_leg = Leg(hip_servo_id=BR_HIP_SERVO_ID, knee_servo_id=BR_KNEE_SERVO_ID, inverted=True)

    fl_leg.move_all(hip_servo_position=0, knee_servo_position=0, hip_speed=1, knee_speed=1)
    fr_leg.move_all(hip_servo_position=0, knee_servo_position=0, hip_speed=1, knee_speed=1)
    bl_leg.move_all(hip_servo_position=0, knee_servo_position=0, hip_speed=1, knee_speed=1)
    br_leg.move_all(hip_servo_position=0, knee_servo_position=0, hip_speed=1, knee_speed=1)

    time.sleep(3)

    fl_leg.move_all(hip_servo_position=-75, knee_servo_position=100, hip_speed=1, knee_speed=1)
    fr_leg.move_all(hip_servo_position=-75, knee_servo_position=100, hip_speed=1, knee_speed=1)
    bl_leg.move_all(hip_servo_position=75, knee_servo_position=-100, hip_speed=1, knee_speed=1)
    br_leg.move_all(hip_servo_position=75, knee_servo_position=-100, hip_speed=1, knee_speed=1)