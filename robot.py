from ev3dev2.motor import LargeMotor, MediumMotor, MoveSteering, OUTPUT_A, OUTPUT_B, OUTPUT_C
from time import sleep


class Robot():
    def __init__(self, baseSpeed=500, dt=50):
        self.leftMotor = LargeMotor(OUTPUT_C)
        self.rightMotor = LargeMotor(OUTPUT_A)
        self.steeringDrive = MoveSteering(OUTPUT_C, OUTPUT_A)
        self.craneMotor = MediumMotor(OUTPUT_B)
        self.baseSpeed = baseSpeed
        self.dt = dt

    def steer(self, controlSignal):
        # ograniczenie sterowania
        leftMotorU = max(-1000, min(self.baseSpeed + controlSignal, 1000))
        rightMotorU = max(-1000, min(self.baseSpeed - controlSignal, 1000))

        # sterowanie silnikami
        self.leftMotor.run_timed(
            time_sp=self.dt, speed_sp=leftMotorU, stop_action="coast")
        self.rightMotor.run_timed(
            time_sp=self.dt, speed_sp=rightMotorU, stop_action="coast")

        sleep(self.dt / 1000)

    def rotateLeft(self):
        self.steeringDrive.on_for_rotations(-72, 40, 1)
        sleep(1)

    def rotateRight(self):
        self.steeringDrive.on_for_rotations(72, 40, 1)
        sleep(1)

    def liftCrane(self):
        self.craneMotor.on_for_degrees(20, 45)
        sleep(1)

    def dipCrane(self):
        self.craneMotor.on_for_degrees(-20, 45)
        sleep(1)
