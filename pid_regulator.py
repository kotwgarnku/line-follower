class PidRegulator():
    def __init__(self, kp=1, ki=0, kd=0, dt=50):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.dt = dt

        self.integral = 0
        self.previousError = 0

    def calculateControlSignal(self, error):
        self.integral += (error * self.dt)
        derivative = (error - self.previousError)

        self.previousError = error

        return (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
