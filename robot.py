from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_C
from time import sleep


class Robot():
    def __init__(self, baseSpeed=500, dt=50):
        self.leftMotor = LargeMotor(OUTPUT_A)
        self.rightMotor = LargeMotor(OUTPUT_C)
        self.baseSpeed = baseSpeed
        self.dt = dt

    def steer(self, controlSignal):
        # ograniczenie sterowania
        leftMotorU = max(-1000, min(self.baseSpeed - controlSignal, 1000))
        rightMotorU = max(-1000, min(self.baseSpeed + controlSignal, 1000))

        # sterowanie silnikami
        self.leftMotor.run_timed(
            time_sp=self.dt, speed_sp=leftMotorU, stop_action="coast")
        self.rightMotor.run_timed(
            time_sp=self.dt, speed_sp=rightMotorU, stop_action="coast")

        sleep(self.dt / 1000)
