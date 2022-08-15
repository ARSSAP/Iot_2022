import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import lcd
import requests

def sendMsg(sms_api_msg_body):
    sms_api_id = "aptech15"
    sms_api_password = "111554"
    sms_api_number = '923131115563' 
    sms_api_brand_name= "APTECH KOR"
    url = "http://api.m4sms.com/api/sendsms?id="+sms_api_id+"&pass="+sms_api_password+"&mobile="+sms_api_number+"&brandname="+sms_api_brand_name+"&msg="+sms_api_msg_body+"&language=English&network=1;"
    r = requests.get(url)
    print(r.text)

def sendWhatsAppMsg():
    headers = {
    'Authorization': 'Bearer EAAKqBIer3dwBAFZA7t3RkXtgaqWiKipZBujVx47OwY3Sja1fJ992MUBEc9rx4XB5ZAIZCZCgwOoyhZAQwuO8GWh1j0iFmwuNmAJrecPWSLTyaONjNHd392Y3JOqn6ouXLyavC4FXU8dQGgEcDq3flwjEeW6e2D6ac3DbqiyqqmtJ0okRVXyAwxxZBH1idZCwWQjDm0N0RnbTGAZDZD',
    'Content-Type': 'application/json',
    }
    data = '{ \\"messaging_product\\": \\"whatsapp\\", \\"to\\": \\"923457847091\\", \\"type\\": \\"template\\", \\"template\\": { \\"name\\": \\"hello_world\\", \\"language\\": { \\"code\\": \\"en_US\\" } } }'
    response = requests.post('https://graph.facebook.com/v13.0/109450551816278/messages', headers=headers, data=data)

i2c = busio.I2C(board.SCL, board.SDA)  

ads0 = ADS.ADS1115(i2c)
ads1 = ADS.ADS1115(i2c)
ads2 = ADS.ADS1115(i2c)
ads3 = ADS.ADS1115(i2c)

ads0.gain = 1
ads1.gain = 1
ads2.gain = 1
ads3.gain = 1

channel0 = AnalogIn(ads0, ADS.P0)
channel1 = AnalogIn(ads1, ADS.P1)
channel2 = AnalogIn(ads2, ADS.P2)
channel3 = AnalogIn(ads3, ADS.P3)

print("(:>5)\t(:>5)".format('raw','v'))

run = True

while run:

    #channel0

    roundedVolts = round(channel0.voltage)
    values = [channel0.value , roundedVolts] 
    time.sleep(0.5)
    lcd.lcd_init()
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    PHValue = str(round(channel0.value/10000)) +" Ph"
    lcd.lcd_string(str(PHValue),2)

    if PHValue == '-3.5' :
        print("Water is 'SLIGHTLY BASIC' in condition")
        PHCondition = "SLIGHTLY BASIC"
        PH_Values = str(PHValue)+ PHCondition 
        print(PH_Values)
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + PH_Values)
        sendWhatsAppMsg()
    elif PHValue== '-7' :
        print("Water is 'HEAVILY BASIC' in condition")
        PHCondition = "HEAVILY BASIC"
        PH_Values = str(PHValue)+ PHCondition 
        print(PH_Values)
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + PH_Values)
        sendWhatsAppMsg()
    elif PHValue == '0' :
        print("Water is 'NORMAL' in condition")
        PHCondition = "NORMAL"
        PH_Values = str(PHValue)+ PHCondition 
        print(PH_Values)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + PH_Values)
    elif PHValue == '3.5' :
        print("Water is 'SLIGHTLY ACIDIC' in condition")
        PHCondition = "SLIGHTLY ACIDIC"
        PH_VAlues = str(PHValue)+ PHCondition 
        print(PH_VAlues)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + PH_VAlues)
    elif PHValue== '14':
        print("Water is 'HEAVILY ACIDIC' in condition")
        PHCondition = "HEAVILY ACIDIC"
        PH_VAlues = str(PHValue)+ PHCondition 
        print(PH_VAlues)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + PH_VAlues)
    

    # #channel1
    
    roundedVolts = round(channel1.voltage)
    values = [channel1.value , roundedVolts] 
    time.sleep(0.5)
    lcd.lcd_init()
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    TURValue = str(round(channel1.value/500)) +" NM"
    lcd.lcd_string(str(TURValue),1)
    

    if TURValue <= '5' :
        print("Water is 'CLEAR' in condition")
        TURCondition = "CLEAR"
        TUR_Values = str(TURValue)+"  Condition: "+TURCondition
        print(TUR_Values)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + TUR_Values)
    elif TURValue <= '55' :
        print("Slightly Polluted")
        TURCondition = "Slightly Polluted"
        TUR_Values = str(TURValue)+"  Condition: "+TURCondition
        print(TUR_Values)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + TUR_Values)
    elif TURValue == '515' :
        print("HIGHLY POLLUTED")
        TURCondition = "HIGHLY POLLUTED"
        TUR_Values = str(TURValue)+"  Condition: "+TURCondition
        print(TUR_Values)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + TUR_Values)
    

    # #channel2
    
    roundedVolts = round(channel2.voltage)
    values = [channel2.value , roundedVolts] 
    time.sleep(0.5)
    lcd.lcd_init()
    lcd.lcd_byte(lcd.LCD_LINE_1, lcd.LCD_CMD)
    TDSValue = str(round(channel2.value/50)) +" S/m"
    lcd.lcd_string(str(TDSValue),2)
    
    if TDSValue<= '100' :
        print("Water is 'CLEAR' in condition")
        TDSCondition = "Slightly Conductive = High Pollution"
        TDSVAlues = str(TDSValue)+"   "+TDSCondition
        print(TDSVAlues)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + TDSVAlues)
    elif TDSValue <= '200' :
        print("Slightly Polluted")
        TDSCondition = "NORMAL Conductive = NORMAL"
        TDSVAlues = str(TDSValue)+"   "+TDSCondition
        print(TDSVAlues)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS" + TDSVAlues)
    elif TDSValue== '515' :
        print("HIGHLY CONDUCTIVE")
        TDSCondition = "HIGHLY CONDUCTIVE = CLEAR"
        TDSVAlues = str(TDSValue)+"   "+TDSCondition
        print(TDSVAlues)
        sendWhatsAppMsg()
        sendMsg("YOUR WATER Test RESULTS ARE:  TDS"  + TDSVAlues)
    # #channel3

    
    roundedVolts = round(channel3.voltage)
    values = [channel3.value , roundedVolts] 
    time.sleep(0.5)
    lcd.lcd_init()
    lcd.lcd_byte(lcd.LCD_LINE_2, lcd.LCD_CMD)
    FlowValue = str(round(channel3.value/50)) +" Flow"
    lcd.lcd_string(str(FlowValue),1)
    time.sleep(1)
    TUR_VAlues = str(FlowValue)
    print(FlowValue)
    sendWhatsAppMsg()
    sendMsg("YOUR WATER Test RESULTS ARE:  Flow" + FlowValue)
    break
    

# User_inp = input("CONTINUE Sampling ? press 1   To CLose Press 0  :")
# if(User_inp == 1):
#     run = True
# elif(User_inp == 0):
#     run = False

    