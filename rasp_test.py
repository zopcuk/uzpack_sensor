from gpiozero import LED
from time import sleep
from gpiozero import Motor

motor = Motor(18, 23)

while True:
    motor.forward()
    sleep(1)
    motor.backward()
    sleep(1)
    motor.stop()
    sleep(1)

'''led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
    print("aaa")'''


