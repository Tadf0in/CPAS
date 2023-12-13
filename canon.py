#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, SpeedPercent, Motor
from ev3dev2.button import Button
from ev3dev2.led import Leds
from ev3dev2.sound import Sound


class Canon:
    def __init__(self) -> None:        
        self.yaw_motor = Motor(OUTPUT_B)
        self.pitch_motor = Motor(OUTPUT_C)
        
        self.sound = Sound()
        
        self.turn_speed = 5
        self.yaw_speed = 0
        self.pitch_speed = 0
        
    def pitch_down(self):
        self.pitch_speed = -self.turn_speed
    
    def pitch_up(self):
        self.pitch_speed = self.turn_speed
    
    def yaw_left(self):
        self.yaw_speed = self.turn_speed
    
    def yaw_right(self):
        self.yaw_speed = -self.turn_speed
        
    def stop(self):
        self.yaw_speed = 0
        self.pitch_speed = 0
        
    def fire(self):
        self.stop()
        self.sound.speak('fire')
        self.pitch_motor.on_for_degrees(SpeedPercent(100), 90)
        self.pitch_motor.on_for_degrees(SpeedPercent(-100), 5)
        self.pitch_motor.on_for_degrees(SpeedPercent(-5), 85)
    
    
        
canon = Canon()
buttons = Button()
leds = Leds()


while True and __name__ == '__main__':
    leds.set_color("LEFT", "RED")
    leds.set_color("RIGHT", "RED")
    
    canon.pitch_motor.on(canon.pitch_speed)
    canon.yaw_motor.on(canon.yaw_speed)
    
    if buttons.down:
        canon.pitch_down()
        
    elif buttons.up:
        canon.pitch_up()
        
    elif buttons.left:
        canon.yaw_left() 
        
    elif buttons.right:
        canon.yaw_right()
    
    elif buttons.enter:
        canon.fire()
        
    else:
        canon.stop()
        
        
    sleep(0.01)