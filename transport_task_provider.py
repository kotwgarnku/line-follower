from enum import Enum

from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor


class Turn(Enum):
    LEFT = 1
    RIGHT = 2


class TransportTaskProvider():
    def __init__(self, fetchColor, fetchDistance=20):
        self.leftColorSensor = ColorSensor(INPUT_1)
        self.rightColorSensor = ColorSensor(INPUT_2)
        self.infraredSensor = InfraredSensor(INPUT_3)

        self.fetchColor = fetchColor
        self.fetchDistance = fetchDistance

    def fetchTurn(self):
        if self.leftColorSensor.color == self.fetchColor:
            return Turn.LEFT
        elif self.rightColorSensor.color == self.fetchColor:
            return Turn.RIGHT
        else:
            return None

    def shouldFetch(self):
        return abs(self.distanceFromItem - self.fetchDistance) < 8

    def distanceFromItem(self):
        return self.infraredSensor.proximity
