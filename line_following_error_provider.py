from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor


class LineFollowingErrorProvider():
    def __init__(self):
        self.leftColorSensor = ColorSensor(INPUT_1)
        self.rightColorSensor = ColorSensor(INPUT_2)

        self.correction = 1

    def calibrateSensors(self):
        self.leftColorSensor.calibrate_white()
        self.rightColorSensor.calibrate_white()

        leftLightIntensity = self.leftColorSensor.reflected_light_intensity
        rightLightIntensity = self.rightColorSensor.reflected_light_intensity

        self.correction = leftLightIntensity / rightLightIntensity

        print('Left sensor intensity: ', leftLightIntensity)
        print('Right sensor intensity: ', rightLightIntensity)
        print('Correction: ', self.correction)

    def calculateError(self):
        return self.leftColorSensor.reflected_light_intensity - self.correction * self.rightColorSensor.reflected_light_intensity
