
from robot_hat import PWM, Servo
from robot_hat.utils import reset_mcu
from time import sleep

reset_mcu()
sleep(0.2)

if __name__ == '__main__':
    servos_pin = ['P0', 'P1', 'P2', 'P11']
    print(f"Set servo to zero")
    for pin in servos_pin:
        # print(f"Servo {pin} set to zero")
        Servo(PWM(pin)).angle(10)
        sleep(0.1)
        Servo(PWM(pin)).angle(0)
        sleep(0.1)
    while True:
        sleep(1)
