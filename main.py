import os
import re
import asyncio
import ipinfo
from ping3 import ping
from telethon import TelegramClient
from telethon.tl.types import Message, PeerChannel
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SOURCE_CHANNEL = int(os.getenv("@ipmoonir"))  # مثال: -1002743822648
DEST_CHANNEL = int(os.getenv("@MsipCn"))      # مثال: -1002714790180

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
ipinfo_handler = ipinfo.getHandler()

async def extract_vless_links(text):
    return re.findall(r'(vless://[\w\d\-]+@[\d\.]+:\d+[^\s]*)', text)

def get_ip_from_vless(link):
    match = re.search(r'@([\d\.]+):', link)
    return match.group(1) if match else None

def get_country(ip):
    try:
        details = ipinfo_handler.getDetails(ip)
        country = details.country_name or "Unknown"
        emoji = getattr(details, "country_flag", {}).get("emoji", "")
        return f"{country} {emoji}".strip()
    except:
        return "Unknown"

def get_ping(ip):
    try:
        delay = ping(ip, timeout=2)
        return int(delay * 1000) if delay else None
    except:
        return None

def best_iranian_cities(ping_val):
    if ping_val is None or ping_val > 1000:
        return ""
    return "ϟ ᴛᴇʜʀᴀɴ ϟ ꜱʜɪʀᴀᴢ ϟ ᴇsғᴀʜᴀɴ ϟ ᴋᴀʀᴀᴊ ϟ"

def format_output(vless_link, country, ip, ping_val):
    cities = best_iranian_cities(ping_val)
    ping_text = f"Ping: {ping_val} ms" if ping_val is not None else "Ping: Timeout"
    return f"""Location : {country}
{vless_link}
{cities}
#vless# | {ping_text}
Bot ϟ @NamiraNet ϟ"""

async def main():
    client = TelegramClient("session", API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    try:
        source_entity = PeerChannel(abs(SOURCE_CHANNEL))
        dest_entity = PeerChannel(abs(DEST_CHANNEL))
    except Exception as e:
        print(f"خطا در ساخت entity کانال: {e}")
        return

    async for message in client.iter_messages(source_entity, limit=20):
        if not isinstance(message, Message) or not message.text:
            continue
        links = await extract_vless_links(message.text)
        for link in links:
            ip = get_ip_from_vless(link)
            if ip:
                country = get_country(ip)
                ping_val = get_ping(ip)
                formatted = format_output(link, country, ip, ping_val)
                await bot.send_message(chat_id=DEST_CHANNEL, text=formatted)
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
