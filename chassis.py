import time

from leg import Leg

class Chassis:
    def __init__(self, fl_hip_servo_id=-1, fl_knee_servo_id=-1, fr_hip_servo_id=-1, fr_knee_servo_id=-1,
                 bl_hip_servo_id=-1, bl_knee_servo_id=-1, br_hip_servo_id=-1, br_knee_servo_id=-1):
        self._fl_leg = Leg(hip_servo_id=fl_hip_servo_id, knee_servo_id=fl_knee_servo_id, inverted=False)
        self._fr_leg = Leg(hip_servo_id=fr_hip_servo_id, knee_servo_id=fr_knee_servo_id, inverted=True)
        self._bl_leg = Leg(hip_servo_id=bl_hip_servo_id, knee_servo_id=bl_knee_servo_id, inverted=False)
        self._br_leg = Leg(hip_servo_id=br_hip_servo_id, knee_servo_id=br_knee_servo_id, inverted=False)
        
        self._phase1_cmds = {
            "fl": {"hip": 45,  "knee": -45, "hip_speed_scalar": 1, "knee_speed_scalar": 0.33},
            "br": {"hip": 45,  "knee": -45, "hip_speed_scalar": 1, "knee_speed_scalar": 0.33},
            "fr": {"hip": -45, "knee": 45, "hip_speed_scalar": 1, "knee_speed_scalar": 1},
            "bl": {"hip": -45, "knee": 45, "hip_speed_scalar": 1, "knee_speed_scalar": 1},
        }
        
        self._phase2_cmds = {
            "fl": {"hip": 0,  "knee": 0, "hip_speed_scalar": 1, "knee_speed_scalar": 1},
            "br": {"hip": 0,  "knee": 0, "hip_speed_scalar": 1, "knee_speed_scalar": 1},
            "fr": {"hip": 0, "knee": -30, "hip_speed_scalar": 1, "knee_speed_scalar": 1.67},
            "bl": {"hip": 0, "knee": -30, "hip_speed_scalar": 1, "knee_speed_scalar": 1.67},
        }
        
        self._phase3_cmds = {
            "fl": {"hip": -45,  "knee": 45, "hip_speed_scalar": 1, "knee_speed_scalar": 1},
            "br": {"hip": -45,  "knee": 45, "hip_speed_scalar": 1, "knee_speed_scalar": 1},
            "fr": {"hip": 45, "knee": -45, "hip_speed_scalar": 1, "knee_speed_scalar": 0.33},
            "bl": {"hip": 45, "knee": -45, "hip_speed_scalar": 1, "knee_speed_scalar": 0.33},
        }
        
        self._phase4_cmds = {
            "fl": {"hip": 0,  "knee": -30, "hip_speed_scalar": 1, "knee_speed_scalar": 1.67},
            "br": {"hip": 0,  "knee": -30, "hip_speed_scalar": 1, "knee_speed_scalar": 1.67},
            "fr": {"hip": 0, "knee": 0, "hip_speed_scalar": 1, "knee_speed_scalar": 1},
            "bl": {"hip": 0, "knee": 0, "hip_speed_scalar": 1, "knee_speed_scalar": 1},
        }

    def wait_for_legs_idle(self):
        while not (self._fl_leg.is_idle() and self._fr_leg.is_idle() and
                   self._bl_leg.is_idle() and self._br_leg.is_idle()):
            time.sleep(0.01)

    def walk(self, time_ms):
        start_time = time.time() * 1000.0
        speed = 0.5
        
        cycle_time = 0.19
        
        current_phase = 4
        self.stand()

        while (time.time() * 1000.0 - start_time) < time_ms:
            if current_phase == 1:
                moves = self._phase1_cmds
                current_phase = 2
            elif current_phase == 2:
                moves = self._phase2_cmds
                current_phase = 3
            elif current_phase == 3:
                moves = self._phase3_cmds
                current_phase = 4
            else:
                moves = self._phase4_cmds
                current_phase = 1

            self._fl_leg.move_all(hip_servo_position=moves["fl"]["hip"], knee_servo_position=moves["fl"]["knee"], 
                                  hip_speed=moves["fl"]["hip_speed_scalar"] * speed, knee_speed=moves["fl"]["knee_speed_scalar"] * speed)
            self._fr_leg.move_all(hip_servo_position=moves["fr"]["hip"], knee_servo_position=moves["fr"]["knee"], 
                                  hip_speed=moves["fr"]["hip_speed_scalar"] * speed, knee_speed=moves["fr"]["knee_speed_scalar"] * speed)
            self._bl_leg.move_all(hip_servo_position=moves["bl"]["hip"], knee_servo_position=moves["bl"]["knee"], 
                                  hip_speed=moves["bl"]["hip_speed_scalar"] * speed, knee_speed=moves["bl"]["knee_speed_scalar"] * speed)
            self._br_leg.move_all(hip_servo_position=moves["br"]["hip"], knee_servo_position=moves["br"]["knee"], 
                                  hip_speed=moves["br"]["hip_speed_scalar"] * speed, knee_speed=moves["br"]["knee_speed_scalar"] * speed)

            time.sleep(cycle_time)
            
        self.stand()

    def sit(self):
        self._fl_leg.move_all(hip_servo_position=-80, knee_servo_position=100, hip_speed=0.5, knee_speed=1)
        self._fr_leg.move_all(hip_servo_position=-80, knee_servo_position=100, hip_speed=0.5, knee_speed=1)
        self._bl_leg.move_all(hip_servo_position=90, knee_servo_position=-100, hip_speed=0.5, knee_speed=1)
        self._br_leg.move_all(hip_servo_position=90, knee_servo_position=-100, hip_speed=0.5, knee_speed=1)

        self.wait_for_legs_idle()
        
    def stand(self):
        self._fl_leg.move_all(hip_servo_position=0, knee_servo_position=0, hip_speed=1, knee_speed=1)
        self._fr_leg.move_all(hip_servo_position=0, knee_servo_position=0, hip_speed=1, knee_speed=1)
        self._bl_leg.move_all(hip_servo_position=0, knee_servo_position=0, hip_speed=1, knee_speed=1)
        self._br_leg.move_all(hip_servo_position=0, knee_servo_position=0, hip_speed=1, knee_speed=1)

        self.wait_for_legs_idle()

    def get_fl_leg(self):
        return self._fl_leg

    def get_fr_leg(self):
        return self._fr_leg

    def get_bl_leg(self):
        return self._bl_leg

    def get_br_leg(self):
        return self._br_leg