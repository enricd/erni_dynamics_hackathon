from picarx import Picarx
from robot_hat import Grayscale_Module, Music
from time import sleep, time
from datetime import datetime

px = Picarx()
gm = Grayscale_Module('A0', 'A1', 'A2')

current_state = None
px_power = 100
last_state = "stop"
gm_state = "stop"
recovery_counter = 0

# Detection thresholds
line_threshold = 60
time_threshold = 300

# Proportional control
p_control = 0.14
max_turn = 23
  
b_filter = 0.4
last_left = 0
last_mid = 0
last_right = 0

def get_status(val_list):
    global last_left, last_mid, last_right
    
    left = val_list[0] * b_filter + last_left*(1-b_filter)
    mid = val_list[1] * b_filter + last_mid*(1-b_filter)
    right = val_list[2] * b_filter + last_right*(1-b_filter)
    
    last_left = left
    last_mid = mid
    last_right = right
    
    if not left>line_threshold and not mid>line_threshold and not right>line_threshold:
        return 0, 'recovery'
    
    left_control = val_list[1] - val_list[2]
    right_control = val_list[1] - val_list[0]
  
    control_signal = (right_control - left_control)*p_control
    
    if abs(control_signal) > max_turn:
        control_signal = max_turn * control_signal/abs(control_signal)
       
    if control_signal > 0:
        return control_signal, 'left'
    elif control_signal <= 0:
        return control_signal, 'right' 


if __name__=='__main__':
    try:
        m = Music()
        m.sound_effect_threading("/home/pi/Sound/Tokyo Drift (Fast & Furious).mp3")
        px.dir_servo_calibrate(-3)
        with open(f'log_{datetime.now()}.txt', 'w') as file:
            while True:
                start_t = time()
                for i in range(2):
                    gm_val_list = gm.get_grayscale_data()
                    control, gm_state = get_status(gm_val_list)
                # file.write(f'Time: {datetime.now()}, Elapsed: {time() - start_t}, Sensor: {gm_val_list}, State: {gm_state}, Last_state: {last_state}, Control: {control}\n')
                # print(f'Time: {datetime.now()}, Elapsed: {time() - start_t}, Sensor: {gm_val_list}, State: {gm_state}, Last_state: {last_state}, Control: {control}\n')

                if gm_state == "recovery":
                    if last_state == "right":
                        control = -max_turn
                    elif last_state == "left":
                        control = max_turn
                        
                    recovery_counter += 1
                    if recovery_counter > time_threshold:
                        px.set_dir_servo_angle(0)  
                        px.forward(0)
                        break

                else:
                    last_state = gm_state
                    recovery_counter = 0

                px.set_dir_servo_angle(int(control))
                px.forward(px_power) 

    finally:
        px.stop()
        print("stop and exit")
        sleep(0.1)


                