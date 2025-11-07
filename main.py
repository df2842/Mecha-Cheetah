from pylx16a.lx16a import *
import time

from constants import *
from chassis import Chassis
from leg import Leg

if __name__ == "__main__":
    LX16A.initialize("/dev/ttyUSB0")

    chassis = Chassis(fl_hip_servo_id=FL_HIP_SERVO_ID, fl_knee_servo_id=FL_KNEE_SERVO_ID, fr_hip_servo_id=FR_HIP_SERVO_ID, fr_knee_servo_id=FR_KNEE_SERVO_ID,
                      bl_hip_servo_id=BL_HIP_SERVO_ID, bl_knee_servo_id=BL_KNEE_SERVO_ID, br_hip_servo_id=BR_HIP_SERVO_ID, br_knee_servo_id=BR_KNEE_SERVO_ID)
    chassis.sit()
    time.sleep(1)

    chassis.walk(5000)