#!/usr/bin/python3
import argparse
from time import sleep

from ev3dev2.sensor.lego import ColorSensor

from pid_regulator import PidRegulator
from line_following_error_provider import LineFollowingErrorProvider
from robot import Robot
from transport_task_provider import TransportTaskProvider, Turn


class LineFollower():
    def __init__(self, errorProvider, regulator, robot, transportTaskProvider):
        self.errorProvider = errorProvider
        self.regulator = regulator
        self.robot = robot

        self.transportTaskProvider = transportTaskProvider
        self.fetched = False
        self.returnedToPath = False

    def run(self):
        while True:
            # self.handleTransportTask()

            error = self.errorProvider.calculateError()
            controlSignal = self.regulator.calculateControlSignal(error)
            self.robot.steer(controlSignal)

    def handleTransportTask(self):
        if not self.fetched:
            fetchTurn = self.transportTaskProvider.fetchTurn()

            if fetchTurn == Turn.LEFT:
                self.robot.rotateLeft()
            else:
                self.robot.rotateRight()

        if not self.fetched and self.transportTaskProvider.shouldFetch():
            self.robot.liftCrane()
            self.robot.rotateLeft()
            self.robot.rotateLeft()
            self.fetched = True

        if self.fetched and not self.returnedToPath:
            if fetchTurn == Turn.LEFT:
                self.robot.rotateLeft()
            else:
                self.robot.rotateRight()
            self.returnedToPath = True


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

    transportTaskProvider = TransportTaskProvider(ColorSensor.COLOR_GREEN)

    lineFollower = LineFollower(
        lineFollowingErrorProvider, pidRegulator, robot, transportTaskProvider)
    lineFollower.run()

# python3 line_follower.py --base_speed=650 --kp=35 --ki=0.04 --kd=1
