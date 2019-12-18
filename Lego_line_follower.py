#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

class Sokoban:
    def __init__(self, speed_initializing, max_speed_execution, solution, black_ref = 100, white_ref = 0, robot_center_parameter = 80, robot_rotation_parameter = 0, orientation = "N", motor_rigth = Motor(Port.B), motor_left = Motor(Port.C), sensor_rigth = ColorSensor(Port.S2), sensor_left = ColorSensor(Port.S1), sensor_stop = ColorSensor(Port.S3), sensor_gyro = GyroSensor(Port.S4), Kp = 5, Ki = 0 , Kd = 0):
        self.speed_initializing = speed_initializing
        self.max_speed_execution = max_speed_execution
        self.solution = solution
        self.black_ref = black_ref
        self.white_ref = white_ref
        self.robot_center_parameter = robot_center_parameter
        self.robot_rotation_parameter = robot_rotation_parameter
        self.orientation = orientation
        self.motor_rigth = motor_rigth
        self.motor_left = motor_left
        self.sensor_rigth = sensor_rigth
        self.sensor_left = sensor_left
        self.sensor_stop = sensor_stop
        self.sensor_gyro = sensor_gyro
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.watch = StopWatch()

    def gostraigth(self, Direction):
        error = 0
        steering_rigth = 1
        steering_left = 1
        steering = 0
        direction = 0
        integral = 0
        last_error = 0
        self.motor_rigth.reset_angle(0)
        self.motor_left.reset_angle(0)
        if Direction == "forward":
            direction = 1
        if Direction == "backward":
            direction = -1
        while (self.sensor_stop.reflection() > 5 * self.black_ref or ((self.motor_rigth.angle() + self.motor_left.angle()) / 2) < 350) and (((self.motor_rigth.angle() + self.motor_left.angle()) / 2) < 1150):
            self.motor_rigth.run(direction * steering_rigth * self.max_speed_execution)
            self.motor_left.run(direction * steering_left * self.max_speed_execution)
            error = self.sensor_left.reflection() - self.sensor_rigth.reflection()
            integral += error
            derivative = last_error - error
            steering = ((error * self.Kp) + (integral * self.Ki) + (derivative * self.Kd))
            if steering < 0 or steering == 0:
                if steering == 0:
                    steering_rigth = 1
                    steering_left = 1
                elif steering > -40:
                    steering_rigth = 1
                    steering_left = ((100 - abs(steering))/100)
                elif steering == -40 or steering < -40:
                    steering_rigth = 1
                    steering_left = 0.6
            if steering > 0:
                if steering < 40:
                    steering_rigth = ((100 - abs(steering))/100)
                    steering_left = 1
                elif steering == 40 or steering > 40:
                    steering_rigth = 0.6
                    steering_left = 1
            last_error = error
        print(self.motor_rigth.angle(),self.motor_left.angle())

    def rotate(self, direction):
        self.motor_rigth.reset_angle(0)
        self.motor_left.reset_angle(0)
        self.sensor_gyro.reset_angle(0)
        if direction == "left":
            while True:
                self.motor_rigth.run(self.speed_initializing)
                self.motor_left.run(-self.speed_initializing)
                if abs(self.sensor_left.reflection() - self.sensor_rigth.reflection()) < 0.9 * self.white_ref and abs(self.sensor_gyro.angle()) > 85:
                    break
        if direction == "rigth":
            while True:
                self.motor_rigth.run(-self.speed_initializing)
                self.motor_left.run(+self.speed_initializing)
                if abs(self.sensor_left.reflection() - self.sensor_rigth.reflection()) < 0.9 * self.white_ref and abs(self.sensor_gyro.angle()) > 85:
                    break

    def startup(self):
        brick.light(Color.RED) # Make the light red
        brick.display.clear() # Clear the display
        if brick.battery.voltage() < 6000: # Check the battery voltage
        # if brick.battery.voltage() < 7000: # Check the battery voltage
            brick.sound.beeps(10) # Makes 10 simple beeps if the voltage is below 7V, and displays a warning about the battery
            brick.display.text("Low Battery!", (30, 50)) # Print "Low Battery" near the middle of the screen for 1000000 ms in case the battery voltage is less then 7 V
            wait(1000000)
        counting_back = ["Counting back: 5", "Counting back: 4", "Counting back: 3", "Counting back: 2", "Counting back: 1", "START"] # Counting back from 5 with 1 second increments and display "Start"
        for counter in counting_back:
            brick.display.text(counter, (30, 50))
            wait(1000)
        brick.display.clear()

    def calibration(self):
        brick.display.text("Calibration!", (30, 50))
        wait(1000)
        while self.sensor_rigth.reflection() > 50 and self.sensor_left.reflection() > 50:
            self.motor_rigth.run(self.speed_initializing)
            self.motor_left.run(self.speed_initializing)
        print("left_sensor value = ", self.sensor_left.reflection(), " rigth_sensor value = ", self.sensor_rigth.reflection(), " gyro_sensor value = ", self.sensor_gyro.angle())
        self.motor_rigth.reset_angle(0)
        self.motor_left.reset_angle(0)
        while (((self.motor_rigth.angle() + self.motor_left.angle()) / 2) >= (-100)):
            self.motor_rigth.run(-self.speed_initializing)
            self.motor_left.run(-self.speed_initializing)
        for i in range(1, 3):
            self.motor_rigth.reset_angle(0)
            self.motor_left.reset_angle(0)
            while (((self.motor_rigth.angle() + self.motor_left.angle()) / 2) <= (+200)):
                self.motor_rigth.run(self.speed_initializing)
                self.motor_left.run(self.speed_initializing)
                if ((self.sensor_rigth.reflection() + self.sensor_left.reflection()) / 2 ) <= self.black_ref:
                    self.black_ref = ((self.sensor_rigth.reflection() + self.sensor_left.reflection()) / 2 )
            self.motor_rigth.reset_angle(0)
            self.motor_left.reset_angle(0)
            while (((self.motor_rigth.angle() + self.motor_left.angle()) / 2) >= (-200)):
                self.motor_rigth.run(-self.speed_initializing)
                self.motor_left.run(-self.speed_initializing)
                if ((self.sensor_rigth.reflection() + self.sensor_left.reflection()) / 2 ) >= self.white_ref:
                    self.white_ref = ((self.sensor_rigth.reflection() + self.sensor_left.reflection()) / 2 )
        print("white_ref = ", self.white_ref, " black_ref = ", self.black_ref)

#---------------------------------------------------------Execution---------------------------------------------------------#

# Competition2019 = Sokoban(100, 100, "ULLDRurdllddUUURRDD")

# Competition2019.startup()
# Competition2019.calibration()
# Competition2019.Execution()

#-----------------------------------------------------------Tests-----------------------------------------------------------#
Competition2019 = Sokoban(150, 350, "LLLUdrrruuDDLLLULdULrrdrrruruDLDLLLLrrrrurLDLLLLLrrrrru", 5.0, 68)
# Competition2019.calibration()
# trial map at home
# Competition2019.gostraigth("forward")
# Competition2019.gostraigth("forward")
# Competition2019.gostraigth("forward")
# Competition2019.rotate("left")
# Competition2019.gostraigth("forward")
# Competition2019.gostraigth("forward")
# Competition2019.rotate("left")
# Competition2019.gostraigth("forward")
# Competition2019.gostraigth("forward")
# Competition2019.gostraigth("forward")
# Competition2019.rotate("left")
# Competition2019.gostraigth("forward")
# Competition2019.gostraigth("forward")
# Competition2019.rotate("left")

#--------------------------------------------------------Our solution--------------------------------------------------------#
#L
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#U
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#d
Competition2019.rotate("left")
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#u
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#u
Competition2019.gostraigth("forward")
#D
Competition2019.rotate("left")
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#D
Competition2019.gostraigth("forward")
#L
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#U
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#L
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#d
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#U
Competition2019.rotate("left")
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#L
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.rotate("left")
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#d
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#r
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#u
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#u
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#D
Competition2019.rotate("left")
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#L
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#D
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#L
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#r
Competition2019.rotate("left")
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#u
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#L
Competition2019.rotate("left")
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#D
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#L
Competition2019.rotate("rigth")
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#L
Competition2019.gostraigth("forward")
#r
Competition2019.rotate("left")
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#r
Competition2019.gostraigth("forward")
#u
Competition2019.rotate("left")
Competition2019.gostraigth("forward")
