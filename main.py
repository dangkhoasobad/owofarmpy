import discord
import asyncio
import requests
import random
import json

# Đọc cấu hình từ file config.json
with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config["TOKEN"]
WEBHOOK_URL = config["WEBHOOK_URL"]
OWO_BOT_ID = config["OWO_BOT_ID"]

client = discord.Client(intents=discord.Intents.all())

# Trạng thái farm
is_farming = False

# Phân loại các icon thú hiếm
rare_animals = {
    "patreon": "<:patreon:449705754522419222>",
    "special": "<:special:427935192137859073>",
    "gem": "<:gem:510023576489951232>",
    "legendary": "<:legendary:417955061801680909>",
    "cpatreon": "<:cpatreon:483053960337293321>"
}

random_messages = ["owo", "uwu", "OwO"]

async def send_webhook(message):
    """Gửi thông báo qua webhook."""
    payload = {
        'content': message,
        'allowed_mentions': {
            'parse': ['everyone']
        }
    }
    requests.post(WEBHOOK_URL, json=payload)

async def farm_owo(channel):
    """Bắt đầu quá trình farm OwO."""
    global is_farming
    while is_farming:
        # Gửi đồng thời owo hunt và owo battle
        await channel.send("owo hunt")
        await channel.send("owo battle")
        
        # Gửi tin nhắn ngẫu nhiên
        await channel.send(random.choice(random_messages))
        
        await asyncio.sleep(20)  # Đợi 20 giây trước khi tiếp tục lặp lại

async def pray_owo(channel):
    """Lệnh 'owo pray' chạy riêng biệt với hunt và battle."""
    while is_farming:
        await channel.send("owo pray")
        await asyncio.sleep(360)  # 6 phút = 360 giây

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    global is_farming

    if message.author == client.user:
        return

    # Quét tin nhắn từ OwO bot để phát hiện thú hiếm
    if message.author.id == int(OWO_BOT_ID):
        # Duyệt qua từng loại thú hiếm theo icon và ID
        for rarity, icon in rare_animals.items():
            if icon in message.content:
                await send_webhook(f"✨ **{rarity.capitalize()} animal found!** {icon} appeared!")
                break

    # Các lệnh bot
    if message.content == "!help":
        await message.channel.send("Bot hỗ trợ các lệnh:\n"
                                   "!help - Hiển thị các lệnh\n"
                                   "!batdaufarm - Bắt đầu farm OwO\n"
                                   "!tamdung - Tạm dừng farm\n"
                                   "!tieptuc - Tiếp tục farm\n")

    elif message.content == "!batdaufarm":
        if not is_farming:
            is_farming = True
            await message.channel.send("Bắt đầu farm OwO!")
            
            # Chạy farm và pray song song
            asyncio.create_task(farm_owo(message.channel))
            asyncio.create_task(pray_owo(message.channel))
        else:
            await message.channel.send("Farm đang chạy rồi!")

    elif message.content == "!tamdung":
        if is_farming:
            is_farming = False
            await message.channel.send("Đã tạm dừng farm OwO!")
        else:
            await message.channel.send("Farm chưa chạy!")

    elif message.content == "!tieptuc":
        if not is_farming:
            is_farming = True
            await message.channel.send("Tiếp tục farm OwO!")
            
            # Chạy lại farm và pray song song sau khi tiếp tục
            asyncio.create_task(farm_owo(message.channel))
            asyncio.create_task(pray_owo(message.channel))
        else:
            await message.channel.send("Farm đang chạy rồi!")

client.run(TOKEN)
