import asyncio
from telethon.sync import TelegramClient

# ---------------------------------------------------------------
# 请替换为你在 my.telegram.org 获取到的真实信息
# ---------------------------------------------------------------
# 示例 ID，请务必替换
api_id = 26510293
api_hash = 'd37649353255275bdca55f9b0e179673'

# ---------------------------------------------------------------
# 定义 session 文件的名称。
# Telethon 会自动添加 .session 后缀。
# 这里我们将其命名为 'user_session'，最终会生成 'user_session.session'
# ---------------------------------------------------------------
session_name = 'user_session'

async def main():
    # 创建一个 TelegramClient 实例。
    # 第一个参数是 session 文件的名称（不带扩展名）。
    # 如果当前目录下不存在名为 'user_session.session' 的文件，
    # Telethon 会提示你登录并创建一个新的。
    print("Starting client...")
    async with TelegramClient(session_name, api_id, api_hash) as client:
        # 检查你是否已经授权登录
        me = await client.get_me()
        if me:
            print(f"Session file '{session_name}.session' created successfully!")
            print(f"Logged in as: {me.first_name} {me.last_name or ''} (@{me.username or ''})")
            print(f"User ID: {me.id}")
        else:
            print("Failed to create session.")

if __name__ == "__main__":

