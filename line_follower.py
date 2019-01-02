#!/usr/bin/python3
import argparse

from pid_regulator import PidRegulator
from line_following_error_provider import LineFollowingErrorProvider
from robot import Robot


class LineFollower():
    def __init__(self, errorProvider, regulator, robot):
        self.errorProvider = errorProvider
        self.regulator = regulator
        self.robot = robot

    def run(self):
        while True:
            error = self.errorProvider.calculateError()
            controlSignal = self.regulator.calculateControlSignal(error)
            self.robot.steer(controlSignal)


def parseArguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--base_speed')
    parser.add_argument('--kp')
    parser.add_argument('--ki')
    parser.add_argument('--kd')

    args = parser.parse_args()

    return tuple(map(float, (args.base_speed, args.kp, args.ki, args.kd)))


if __name__ == "__main__":
    dt = 50

    (baseSpeed, kp, ki, kd) = parseArguments()

    lineFollowingErrorProvider = LineFollowingErrorProvider()
    lineFollowingErrorProvider.calibrateSensors()

    pidRegulator = PidRegulator(kp, ki, kd, dt)

    robot = Robot(baseSpeed, dt)

    lineFollower = LineFollower(
        lineFollowingErrorProvider, pidRegulator, robot)
    lineFollower.run()

# python3 line_follower.py --base_speed=500 --kp=30 --ki=0.02 --kd=1
