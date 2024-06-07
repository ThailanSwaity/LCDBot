from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

import os 

import discord
import asyncio
from dotenv import load_dotenv

PCF8574_address = 0x27
PCF8574A_address = 0x3F

current_message = ""
message_changed = False

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.main_task())

    async def main_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            m_length = len(current_message)
            if (m_length > 16):
                for i in range(0, m_length-16):
                    if (message_changed):
                        message_changed = False
                        break
                    lcd.clear()
                    lcd.setCursor(0,0)
                    lcd.message(current_message[i:(i+16)])
                    await asyncio.sleep(1)
            else:
                lcd.message(message.content)
            await asyncio.sleep(1)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        lcd.clear()
        mcp.output(3,1) # Turn on LCD backlight
        lcd.begin(16,2) # set number of LCD lines and columns

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        lcd.clear()
        lcd.setCursor(0,0)
        if (message.content=='off'):
            mcp.output(3,0)
        elif (message.content=='on'):
            mcp.output(3,1)
        else:
            current_message = message.content
            message_changed = True

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

if __name__ == "__main__":

   
