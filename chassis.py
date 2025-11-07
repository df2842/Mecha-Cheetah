import time

from leg import Leg

class Chassis:
    def __init__(self, fl_hip_servo_id=-1, fl_knee_servo_id=-1, fr_hip_servo_id=-1, fr_knee_servo_id=-1,
                 bl_hip_servo_id=-1, bl_knee_servo_id=-1, br_hip_servo_id=-1, br_knee_servo_id=-1):
        self._fl_leg = Leg(hip_servo_id=fl_hip_servo_id, knee_servo_id=fl_knee_servo_id, inverted=False)
        self._fr_leg = Leg(hip_servo_id=fr_hip_servo_id, knee_servo_id=fr_knee_servo_id, inverted=True)
        self._bl_leg = Leg(hip_servo_id=bl_hip_servo_id, knee_servo_id=bl_knee_servo_id, inverted=False)
        self._br_leg = Leg(hip_servo_id=br_hip_servo_id, knee_servo_id=br_knee_servo_id, inverted=True)

        self._phase1_cmds = {
            "fl": {"hip": 75, "knee": 100},
            "fr": {"hip": 75, "knee": 50},
            "bl": {"hip": -75, "knee": -50},
            "br": {"hip": -75, "knee": -100},
        }

        self._phase2_cmds = {
            "fl": {"hip": -75, "knee": 50},
            "fr": {"hip": -75, "knee": 100},
            "bl": {"hip": 75, "knee": -100},
            "br": {"hip": 75, "knee": -50},
        }

    def wait_for_legs_idle(self):
        while not (self._fl_leg.is_idle() and self._fr_leg.is_idle() and
                   self._bl_leg.is_idle() and self._br_leg.is_idle()):
            time.sleep(0.01)

    def walk(self, time_ms):
        start_time = time.time() * 1000.0
        current_phase = 1

        while (time.time() * 1000.0 - start_time) < time_ms:
            if current_phase == 1:
                moves = self._phase1_cmds
                current_phase = 2
            else:
                moves = self._phase2_cmds
                current_phase = 1

            self._fl_leg.move_all(hip_servo_position=moves["fl"]["hip"], knee_servo_position=moves["fl"]["knee"], hip_speed=1.0, knee_speed=1.0)
            self._fr_leg.move_all(hip_servo_position=moves["fr"]["hip"], knee_servo_position=moves["fr"]["knee"], hip_speed=1.0, knee_speed=1.0)
            self._bl_leg.move_all(hip_servo_position=moves["bl"]["hip"], knee_servo_position=moves["bl"]["knee"], hip_speed=1.0, knee_speed=1.0)
            self._br_leg.move_all(hip_servo_position=moves["br"]["hip"], knee_servo_position=moves["br"]["knee"], hip_speed=1.0, knee_speed=1.0)

            self.wait_for_legs_idle()

            if (time.time() * 1000.0 - start_time) >= time_ms:
                break

        self.sit()

    def sit(self):
        self._fl_leg.move_all(hip_servo_position=-75, knee_servo_position=100, hip_speed=1, knee_speed=1)
        self._fr_leg.move_all(hip_servo_position=-75, knee_servo_position=100, hip_speed=1, knee_speed=1)
        self._bl_leg.move_all(hip_servo_position=75, knee_servo_position=-100, hip_speed=1, knee_speed=1)
        self._br_leg.move_all(hip_servo_position=75, knee_servo_position=-100, hip_speed=1, knee_speed=1)

        self.wait_for_legs_idle()

    def get_fl_leg(self):
        return self._fl_leg

    def get_fr_leg(self):
        return self._fr_leg

    def get_bl_leg(self):
        return self._bl_leg

    def get_br_leg(self):
        return self._br_leg