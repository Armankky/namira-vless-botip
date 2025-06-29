import os
import re
import asyncio
import ipinfo
from ping3 import ping
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import Message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")  # مثال: @source_channel_username
DEST_CHANNEL = os.getenv("DEST_CHANNEL")      # مثال: @dest_channel_username

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
Bot ϟ @jhjkkjkkbot ϟ"""

async def main():
    client = TelegramClient("bot", API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)

    async with client:
        async for message in client.iter_messages(SOURCE_CHANNEL, limit=20, reverse=True):
            if not isinstance(message, Message) or not message.text:
                continue
            print("debugID:", message.id)
            print("debugInfo:", message.text)
            links = await extract_vless_links(message.text)
            for link in links:
                ip = get_ip_from_vless(link)
                if ip:
                    country = get_country(ip)
                    ping_val = get_ping(ip)
                    formatted = format_output(link, country, ip, ping_val)
                    await client.send_message(DEST_CHANNEL, formatted)
                    await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
