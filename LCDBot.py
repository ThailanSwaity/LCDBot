import RPi.GPIO as GPIO

buttonPin = 12
backlightState = True

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

import os 

import discord
from dotenv import load_dotenv

PCF8574_address = 0x27
PCF8574A_address = 0x3F

current_message = ""

try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print('I2C Address Error!')
        exit(1)

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        lcd.clear()
        mcp.output(3,1) # Turn on LCD backlight
        lcd.begin(16,2) # set number of LCD lines and columns

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        lcd.clear()
        lcd.setCursor(0,0)
        if (len(message.content) > 16):
            lcd.message(message.content[:16])
            lcd.setCursor(0,1)
            lcd.message(message.content[16:])
        else:
            lcd.message(message.content)
        # current_message = message.content

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

def buttonEvent(channel):
    global backlightState
    backlightState = not backlightState
    mcp.output(3,backlightState)

if __name__ == "__main__":

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while(1):
        GPIO.add_event_detect(buttonPin,GPIO.FALLING,callback=buttonEvent,bouncetime=300)

#        m_length = len(current_message)
#        if (m_length > 16):
#            for i in range(0, m_length-16):
#                lcd.clear()
#                lcd.setCursor(0,0)
#                lcd.message(current_message[i:(i+16)])
#                sleep(1)
#        else:
#            lcd.message(message.content)
    
