# This example requires the 'message_content' intent.

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

import os 

import discord
from dotenv import load_dotenv

PCF8574_address = 0x27
PCF8574A_address = 0x3F
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

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        lcd.setCursor(0,0)
        lcd.message(message.content)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
