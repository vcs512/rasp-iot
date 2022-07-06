import pigpio

servo_H = 18
servo_V = 17

pwm = pigpio.pi()

pwm.set_mode(servo_H, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo_H, 50)
pwm.set_mode(servo_V, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo_V, 50)

pwm.set_servo_pulsewidth(servo_H, 1500)
pwm.set_servo_pulsewidth(servo_V, 1500)
