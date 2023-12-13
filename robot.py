#!/usr/bin/env python3

from random import randint

from ev3dev2.motor import OUTPUT_A, OUTPUT_D, SpeedPercent, MoveTank, Motor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, UltrasonicSensor, ColorSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.button import Button


class Robot:
    def __init__(self) -> None:
        # self.touch_sensor = TouchSensor()
        # self.ultrasonic_sensor = UltrasonicSensor(INPUT_4)
        self.gyro = GyroSensor(INPUT_3)
        self.leds = Leds()
        self.tank = MoveTank(OUTPUT_A, OUTPUT_D)
        self.sound = Sound()
        self.colors = (ColorSensor(INPUT_1), ColorSensor(INPUT_2))
        self.buttons = Button()
        
        self.default_speed = SpeedPercent(20)
        self.left_motor_speed = self.default_speed
        self.right_motor_speed = self.default_speed
        
        self.state = 0
        self.nb_choosen_direction = 0
        self.target_place = 3 # Numéro de la cachette entre 1 et 4
     
    
    def change_state(self, new_state):
        self.state = new_state
    
    def set_left_led_color(self, color):
        self.leds.set_color("LEFT", color)
        
    def set_right_led_color(self, color):
        self.leds.set_color("RIGHT", color)
        
    def set_leds_color(self, color):
        self.set_left_led_color(color)
        self.set_right_led_color(color)
        
    # def is_ts_pressed(self):
    #     return self.touch_sensor.is_pressed
    
    # def get_distance(self):
    #     return self.ultrasonic_sensor.distance_centimeters
    
    def get_colors(self):
        return self.colors[0].color_name, self.colors[1].color_name
    
    def get_angle(self):
        return self.gyro.angle
        
    def set_motors_speed(self, left_speed, right_speed):
        self.right_motor_speed = SpeedPercent(left_speed)
        self.left_motor_speed = SpeedPercent(right_speed)
        
    
    def move(self):
        self.tank.on(self.left_motor_speed, self.right_motor_speed)
          
    def turn_around(self):
        self.tank.on_for_degrees(self.left_motor_speed, -self.right_motor_speed, 360)
        
    def stop(self):
        self.set_motors_speed(0, 0)
        self.tank.off()
        
        
    def speak(self, text):
        self.sound.speak(text)
        
    def choose_direction(self):        
        left_speed = self.default_speed
        right_speed = self.default_speed
        
        self.tank.on_for_rotations(left_speed, right_speed, 1)
        
        # Choisit la direction aleatoirement
        # if randint(0, 1) == 0:
        #     left_speed *= -1
        # else:
        #     right_speed *= -1 
        
        # On utilise la valeur binaire du numéro de la cachette pour déterminer le chemin à suivre : 0 = Gauche / 1 = Droite
        direction = "%02d" % int(bin(self.target_place-1)[2:]) # Valeur binaire formatee avec forcement 2 chiffres (1 -> 01)
        direction = int(direction[self.nb_choosen_direction]) # 1er chiffre = 1er carre noir / 2eme chiffre = 2eme carre noir
        self.nb_choosen_direction += 1
        
        if direction == 0:
            left_speed *= -1
        else:
            right_speed *= -1               

        while abs(self.get_angle()) < 90:
            self.tank.on(left_speed, right_speed) 
        self.stop()


    def stop_at_finish(self):
        self.tank.on_for_rotations(self.default_speed, self.default_speed, 1)
        self.stop()