#!/usr/bin/env python3

from time import sleep
from robot import Robot 
from canon import Canon
    
robot = Robot()
canon = Canon()
states = {
    'start': 0,
    'line': 1,
    'choose': 2,
    'stop': 3,
    'back': 4,
    'win': 5,
}
line_colors = ['Black', 'Red', 'Green', 'Blue']

robot.gyro.calibrate()
sleep(1)
direction_choosen = False
stopped = False
while True:
    colors = robot.get_colors()
    angle = robot.get_angle()
    print(angle, colors)
    
    # Départ
    if robot.state == 0:   
        robot.nb_choosen_direction = 0
        robot.set_leds_color('AMBER') 
        if robot.buttons.enter:
            robot.gyro.reset()    
            robot.change_state(states['line'])
            
    
    # Suivi de ligne
    elif robot.state == 1:
        robot.set_leds_color('GREEN')
        robot.move()
        
        # Choisis une direction si sur du noir 
        if colors[0] == 'Black' and colors[1] == 'Black':
            robot.change_state(states['choose'])
            
        # S'arrête si sur du rouge
        elif colors[0] == 'Red' and colors[1] == 'Red':
            robot.change_state(states['stop'])
        
        # Tourne à gauche    
        elif colors[0] in line_colors:
            robot.set_motors_speed(30, 0)

        # Tourne à droite
        elif colors[1] in line_colors:
            robot.set_motors_speed(0, 30)
        
        # Sinon va tout droit
        else:
            robot.set_motors_speed(30, 30)
                  
         
        # # Si obstacle devant, s'arrête   
        # if robot.get_distance() < 20 : 
        #     robot.stop()
    
    
    # Choisit une direction
    elif robot.state == 2:
        robot.set_left_led_color('GREEN')
        robot.set_right_led_color('AMBER')
        
        if not direction_choosen:
            direction_choosen = True
            robot.choose_direction()
        else:
            # Corrige la trajectoire si angle de sortie pas bon
            if (angle > 0 and angle > 91) or (angle < 0 and angle > -89):
                robot.set_motors_speed(20, 10)
            elif (angle < 0 and angle < -91) or (angle > 0 and angle < 89):
                robot.set_motors_speed(10, 20)
            else:
                robot.set_motors_speed(20, 20)
            robot.move()

        # Sort d'un carré noir
        if colors[0] != 'Black' and colors[1] != 'Black':
            robot.change_state(states['line'])
            direction_choosen = False
    
    
    # Stop
    elif robot.state == 3:
        robot.set_leds_color('RED')
        if not stopped:
            robot.stop_at_finish()
            stopped = True
            canon.fire()
        
        if robot.buttons.left:
            stopped = False
            robot.change_state(states['start'])
        
        if robot.buttons.right:
            stopped = False
            robot.change_state(states['back'])
            
    # Recule
    elif robot.state == 4:
        robot.tank.on_for_seconds(-20, -20, 2)
        robot.stop()
        sleep(1000)
        if False: # à changer : Pepper s'est trompé
            # Retourne dans sa cachette
            robot.tank.on_for_seconds(20, 20, 2)
            robot.change_state(states['stop'])
        elif True: # à changer : dernier trouvé
            robot.change_state(states['win'])
        
    # Danse de la victoire
    elif robot.state == 5:
        robot.set_motors_speed(-100,100)
        robot.move()

    else:
        raise Exception('State error')
    
    if robot.buttons.down:
        robot.stop()
        robot.change_state(states['start'])
        direction_choosen = False
        stopped = False


    sleep(0.01)