import os
import re
import asyncio
import ipinfo
from ping3 import ping
from telethon import TelegramClient, errors
from telethon.tl.types import Message
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()  # بارگذاری متغیرهای محیطی از .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")  # اگر عدد است، تبدیل می‌کنیم در ادامه
DEST_CHANNEL = os.getenv("DEST_CHANNEL")      # همین‌طور

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
        # استفاده از پرچم به شکل ایموجی ممکن است محدود باشد
        emoji = getattr(details, "country_flag", {}).get("emoji", "")
        return f"{country} {emoji}".strip()
    except Exception:
        return "Unknown"

def get_ping(ip):
    try:
        delay = ping(ip, timeout=2)
        return int(delay * 1000) if delay else None
    except Exception:
        return None

def best_iranian_cities(ping_val):
    if ping_val is None or ping_val > 1000:
        return ""
    return "ϟ ᴛᴇʜʀᴀɴ ϟ ꜱʜɪʀᴀᴢ ϟ ᴇsғᴀʜᴀɴ ϟ ᴋᴀʀᴀᴊ ϟ"

def format_output(vless_link, country, ip, ping_val):
    cities = best_iranian_cities(ping_val)
    ping_text = f"Ping:{ping_val}" if ping_val is not None else "Ping: Timeout"
    return f"""Location : {country}
{vless_link}
{cities}
#vless# | {ping_text}
Bot ϟ @NamiraNet ϟ"""

async def main():
    client = TelegramClient("session", API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)  # شروع با توکن ربات

    # تبدیل SOURCE_CHANNEL به int اگر عدد باشد، یا بگذار رشته بماند (مثلاً @channelusername)
    source_channel = SOURCE_CHANNEL
    if source_channel.isdigit() or (source_channel.startswith("-") and source_channel[1:].isdigit()):
        source_channel = int(source_channel)

    # تلاش برای گرفتن entity کانال با هندل (username) یا ID
    try:
        source_entity = await client.get_entity(source_channel)
    except errors.UsernameInvalidError:
        print("SOURCE_CHANNEL مقدار نادرست است یا کانال پیدا نشد.")
        return
    except errors.ChannelInvalidError:
        print("کانال معتبر نیست یا دسترسی ندارید.")
        return
    except Exception as e:
        print("خطا در دریافت entity کانال:", e)
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
                await bot.send_message(chat_id=int(DEST_CHANNEL), text=formatted)
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
