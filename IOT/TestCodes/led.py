from gpiozero import LED
from time import sleep

led1 = LED(2)
led2 = LED(3)
led3 = LED(4)
while True:
    led1.on()
    led2.on()
    led3.on()
    sleep(0.1)
    led1.off()
    led2.off()
    led3.off()
    sleep(0.1)


# inp = int(input("Enter number"))
# led1 = LED(2)
# led2 = LED(3)
# led3 = LED(4)
# for i in range(100000):
#     if (inp == 1):
#         led1.on()
#         led2.off()
#         led3.on()
#         print("light is ON")
#         sleep(2)
#         led1.off()
#         led2.on()
#         led3.off()
#         sleep(1)
#     else:
#         led1.off()
#         led2.off()
#         led3.off()
#         print("light is OFF")
