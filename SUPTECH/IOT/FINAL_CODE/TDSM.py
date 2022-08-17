from itertools import count
import RPi.GPIO as GPIO
from ast import Try
from datetime import date, datetime
from gpiozero import LED
import sys,time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import lcd
import requests
from requests.structures import CaseInsensitiveDict
import os
from time import sleep
import lcd

from pymongo import MongoClient
import pymongo
import urllib 


MONGODB_USER="pi4"
MONGODB_PASS=os.getenv("MONGODB_PASS")
MONGODB_DB = 'water_quality_db'
MONGODB_COLLECTION = 'sensor_logs'

def mongo_db_connection():
    CONNECTION_STRING = "mongodb+srv://pi4:"+ urllib.parse.quote(MONGODB_PASS) +"@cluster0.wbrzjmu.mongodb.net/?retryWrites=true&w=majority"
    
    try:
        client = MongoClient(CONNECTION_STRING)
        dbname = client[MONGODB_DB]
        collection_name = dbname[MONGODB_COLLECTION]
        print("Database connected successfully!")
        return collection_name 
    except:
        print("Database could not be connected!")

PH_STANDARD_RANGE = (5.5,8.5)
TUR_STANDARD_RANGE = (1,1800)
TDS_STANDARD_RANGE = (1000,2500)
WF_STANDARD_RANGE = (500,1000)

# Constants for SMS_API 
SMS = {
    "ID":"aptech15", 
    "NUMBER": "923132241383" ,
    "BRAND": "APTECH KOR"
}

# Constants for WHATSAPP_API
WHATSAPP = {
    "URL" : "https://graph.facebook.com/v13.0/109450551816278/messages",
    "NUMBER": "923486812804" 
}
# Func to send SMS
def sendSMS(MSG_BODY):
    url = "http://api.m4sms.com/api/#sendSMS?id="+SMS["ID"]+"&pass="+os.getenv("SMS_API_PASSWORD")+"&mobile="+SMS["NUMBER"]+"&brandname="+SMS["BRAND"]+"&msg="+MSG_BODY+"&language=English&network=1;"
    try:
        r = requests.get(url)
        print("SMS SENT TO "+SMS["NUMBER"])

    except:
        print("SMS FAILED TO SENT")
      

# Func to send WHATSAPP
def sendWhatsApp(TDS,PH,TS,WFS,STATUS):
    headers = CaseInsensitiveDict()
    headers = {
        'Authorization': 'Bearer '+os.getenv('WHATSAPP_TOKEN'),
        'Content-Type': 'application/json'
        }
    data = '{ "messaging_product": "whatsapp", "recipient_type": "individual", "to": "'+ WHATSAPP["NUMBER"] +'", "type": "template", "template": { "name": "techwiz_sensor_values", "language": { "code": "en" }, "components": [ { "type": "body", "parameters": [ { "type": "text", "text": "'+str(TDS)+'" }, { "type": "text", "text": "'+str(PH)+'" }, { "type": "text", "text": "'+str(TS)+'" }, { "type": "text", "text": "'+str(WFS)+'" }, { "type": "text", "text": "'+str(STATUS)+'" } ] } ] } }'
    try:
        resp = requests.post(WHATSAPP["URL"], headers=headers, data=data)
        #print(resp.status_code)
        print("WhatsApp SENT TO "+WHATSAPP["NUMBER"])
    except:
        print("WhatsApp FAILED TO SENT, Error Code: ", resp.status_code) 

# Func for LCD display
def displayLCD(LINE_,VALUE,ALIGN):
    LINE_NUMBER = {1: lcd.LCD_LINE_1,2: lcd.LCD_LINE_2}
    lcd.lcd_init()
    lcd.lcd_byte(LINE_NUMBER[LINE_], lcd.LCD_CMD)
    lcd.lcd_string(str(VALUE),ALIGN)


#Calling SCL & SDA ports from Pi Board
i2c = busio.I2C(board.SCL, board.SDA)  
ads = ADS.ADS1115(i2c)
ads.gain = 1


#Assigning Channel of ADS1115 to sensors
channel0 = AnalogIn(ads, ADS.P0) # For pH sensor
channel1 = AnalogIn(ads, ADS.P1) # For Turbidity sensor
channel2 = AnalogIn(ads, ADS.P2) # For TDS sensor
channel3 = AnalogIn(ads, ADS.P3) # For WaterFlow sensor


run = True

while run:
 
    # Calculating pH
    PH_VOL = channel0.voltage
    PH_VAL = round(-5.70*PH_VOL+21.34,2)

    # Calculating Turbidity
    TUR_VOL = channel1.voltage
    TUR_VAL = round(-1120.4*(TUR_VOL**2)+(5742.3*TUR_VOL)-4353.8)
    
    #Calculating TDS
    TDS_VOL = channel2.voltage
    TDS_VAL = round((133.42/TDS_VOL**3-255.86*TDS_VOL**2+857.39*TDS_VOL)*0.5)
    
    WF_VAL = round(channel3.value)

    logs = str(datetime.now()),": pH: ",str(PH_VAL),", Tur: ",str(TUR_VAL),", TDS: ",str(TDS_VAL),", WF: ",str(WF_VAL) + "\n"
    print(logs)
    file = open("logs.txt","a")
    file.writelines(logs)
    file.close()

    IS_PH_OK = PH_VAL >= PH_STANDARD_RANGE[0] and PH_VAL <= PH_STANDARD_RANGE[1]
    IS_TUR_OK = TUR_VAL >= TUR_STANDARD_RANGE[0] and TUR_VAL <= TUR_STANDARD_RANGE[1]
    IS_TDS_OK = TDS_VAL >= TDS_STANDARD_RANGE[0] and TDS_VAL <= TDS_STANDARD_RANGE[1]
    #IS_WF_OK = WF_VAL >= WF_STANDARD_RANGE[0] and WF_VAL <= WF_STANDARD_RANGE[1]

    IS_DRINKABLE = (IS_PH_OK and IS_TUR_OK and IS_TDS_OK)
    STATUS = "CLEAN" if IS_DRINKABLE else "POLLUTED"

    sensor_log = {
            "ph_sensor_value" : PH_VAL,
            "tds_sensor_value" : TDS_VAL,
            "tur_sensor_value" : TUR_VAL,
            "wf_sensor_value" : WF_VAL,
            "status" : STATUS,
            "date_added": datetime.now()
            }
    
    LINE1="P:" + str(round(PH_VAL,2)) + ", T:" + str(round(TUR_VAL,2))
    LINE2="C:" + str(round(TDS_VAL,2)) + ", W:" + str(round(WF_VAL,2))
    
    db =  mongo_db_connection()

    SMS_MSG_BODY = "Water Quality Tester\n" + "pH: " + str(round(PH_VAL,2)) + "\nTurbidity: " + str(round(TUR_VAL,2)) + "\nConductivity: " + str(round(TDS_VAL,2)) + "\nWaterFlow: " + str(round(WF_VAL,2)) + "\n\nThe water is: " + STATUS

    if IS_DRINKABLE:
        print("Water is ", STATUS)
      
        displayLCD(1,"Water: " + STATUS,1)
        sleep(5)
        displayLCD(1,LINE1,1)
        sleep(2)
        displayLCD(1,LINE2,1)
        try:
            db.insert_one(sensor_log)
            print("Data logged successfully in db")
        except:
            print("Data not inserted in db")
        sendWhatsApp(str(round(TDS_VAL)),str(round(PH_VAL,2)),str(round(TUR_VAL,2)),str(round(WF_VAL,2)),STATUS)
        sendSMS(SMS_MSG_BODY)
    else: 
        print("Water is ", STATUS)

        displayLCD(1,"Water: " + STATUS,1)
        sleep(5)
        displayLCD(1,LINE1,1)
        sleep(2)
        displayLCD(2,LINE2,1)
        try:
            db.insert_one(sensor_log)
            print("Data logged successfully in db")
        except:
            print("Data not inserted in db")
        sendWhatsApp(str(round(TDS_VAL)),str(round(PH_VAL,2)),str(round(TUR_VAL,2)),str(round(WF_VAL,2)),STATUS)
        sendSMS(SMS_MSG_BODY)
    sleep(10)
    #break
    

