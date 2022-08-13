import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import lcd

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.gain = 1

channel = AnalogIn(ads, ADS.P2)

print("(:>5)\t(:>5)".format('raw','v'))

while True:
    print(channel.value)
    time.sleep(0.5)
    # lcd.lcd_init()
    # lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    # lcd.lcd_string(str(channel.value),2)