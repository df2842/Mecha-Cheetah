from pylx16a.lx16a import *

from constants import *

class Leg:
    def __init__(self, hip_servo_id=-1, knee_servo_id=-1, inverted=False):
        if not isinstance(inverted, bool): inverted = False

        self._hip_servo_id = hip_servo_id
        self._hip = None
        self._knee_servo_id = knee_servo_id
        self._knee = None
        self._inverted = inverted
        self._running = False

        if (not hip_servo_id in SERVO_ZERO_POSITION or not hip_servo_id in HIP_SERVO_MIN_POSITION or
                not knee_servo_id in SERVO_ZERO_POSITION or not knee_servo_id in KNEE_SERVO_MIN_POSITION):
            return

        try:
            self._hip = LX16A(hip_servo_id)
            self._knee = LX16A(knee_servo_id)

            self._running = True

        except Exception as e:
            self._hip = None
            self._knee = None

    def move_hip(self, servo_position=0, speed=1.0):
        if (not self._running or
                not isinstance(servo_position, (int, float)) or
                not isinstance(speed, (int, float))):
            return

        speed = max(0.0, min(speed, 1.0))
        if speed == 0: return

        if self._inverted: servo_position *= -1
        servo_position += SERVO_ZERO_POSITION[self._hip_servo_id]
        servo_position = max(HIP_SERVO_MIN_POSITION[self._hip_servo_id], min(servo_position, HIP_SERVO_MAX_POSITION[self._hip_servo_id]))

        while abs(self._hip.get_physical_angle() - self._hip.get_commanded_angle()) > SERVO_TOLERANCE:
            continue

        rotation_duration = int(min(30.0, abs(servo_position - self._hip.get_physical_angle()) * SERVO_INVERSE_MAX_SPEED / speed) * 1000.0)

        self._hip.move(angle=servo_position, time=rotation_duration)

    def move_knee(self, servo_position=0, speed=1.0):
        if (not self._running or
                not isinstance(servo_position, (int, float)) or
                not isinstance(speed, (int, float))):
            return

        speed = max(0.0, min(speed, 1.0))
        if speed == 0: return

        if self._inverted: servo_position *= -1
        servo_position += SERVO_ZERO_POSITION[self._knee_servo_id]
        servo_position = max(KNEE_SERVO_MIN_POSITION[self._knee_servo_id], min(servo_position, KNEE_SERVO_MAX_POSITION[self._knee_servo_id]))

        while abs(self._knee.get_physical_angle() - self._knee.get_commanded_angle()) > SERVO_TOLERANCE:
            continue

        rotation_duration = int(min(30.0, abs(servo_position - self._knee.get_physical_angle()) * SERVO_INVERSE_MAX_SPEED / speed) * 1000.0)

        self._knee.move(angle=servo_position, time=rotation_duration)

    def move_all(self, hip_servo_position=0, knee_servo_position=0, hip_speed=1.0, knee_speed=1.0):
        while (abs(self._hip.get_physical_angle() - self._hip.get_commanded_angle()) > SERVO_TOLERANCE or
               abs(self._knee.get_physical_angle() - self._knee.get_commanded_angle()) > SERVO_TOLERANCE):
            continue

        self.move_hip(servo_position=hip_servo_position, speed=hip_speed)
        self.move_knee(servo_position=knee_servo_position, speed=knee_speed)

    def stop_hip(self):
        self._hip.move_stop()

    def stop_knee(self):
        self._knee.move_stop()

    def stop_all(self):
        self._hip.move_stop()
        self._knee.move_stop()