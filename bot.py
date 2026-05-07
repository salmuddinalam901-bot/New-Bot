# ==========================================
# PREMIUM FORCE JOIN BOT
# PYROGRAM VERSION
# ==========================================

# INSTALL:
# pip install pyrogram tgcrypto

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import UserNotParticipant
from datetime import datetime

# ==========================================
# CONFIG
# ==========================================

API_ID = 8301532042
API_HASH = "dca5976cd8d7fbac4d4ccf4f79399048"
BOT_TOKEN = "8477142285:AAGPD9gBSMacQdeAe3NzWWTaqCpC6aO8T8M"

# WITHOUT @
FORCE_CHANNEL = "YourChannel"

# ADMIN ID
ADMINS = [8301532042]

# ==========================================
# BOT CLIENT
# ==========================================

bot = Client(
    "PremiumForceJoinBot",
    api_id=8301532042,
    api_hash=dca5976cd8d7fbac4d4ccf4f79399048,
    bot_token=8477142285:AAGPD9gBSMacQdeAe3NzWWTaqCpC6aO8T8M
)

# ==========================================
# DATABASE
# ==========================================

users = []

# ==========================================
# FORCE JOIN CHECK
# ==========================================

async def check_join(user_id):
    try:
        await bot.get_chat_member(FORCE_CHANNEL, user_id)
        return True
    except UserNotParticipant:
        return False
    except:
        return False

# ==========================================
# SAVE USER
# ==========================================

@bot.on_message(filters.private)
async def save_user(client, message):

    if message.from_user.id not in users:
        users.append(message.from_user.id)

# ==========================================
# START COMMAND
# ==========================================

@bot.on_message(filters.command("start"))
async def start(client, message):

    user_id = message.from_user.id
    first_name = message.from_user.first_name

    joined = await check_join(user_id)

    if not joined:

        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📢 Join Channel",
                        url=f"https://t.me/+5zjaEkMl3uw5OTI1{FORCE_CHANNEL}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "✅ Verify",
                        callback_data="verify"
                    )
                ]
            ]
        )

        return await message.reply_photo(
            photo="https://picsum.photos/600/300",
            caption=f"""
👋 Hello {first_name}

❌ To use this bot,
join our channel first.

📢 @{FORCE_CHANNEL}

Then click verify button.
            """,
            reply_markup=buttons
        )

    await message.reply_text(
        f"""
✅ Welcome {first_name}

🎉 Verification Successful

🤖 Premium Force Join Bot
⏰ Time: {datetime.now().strftime("%H:%M:%S")}
        """
    )

# ==========================================
# VERIFY BUTTON
# ==========================================

@bot.on_callback_query(filters.regex("verify"))
async def verify(client, callback_query):

    user_id = callback_query.from_user.id

    joined = await check_join(user_id)

    if not joined:

        return await callback_query.answer(
            "❌ Please Join Channel First",
            show_alert=True
        )

    await callback_query.message.edit_text(
        f"""
✅ Verification Successful

👤 User: {callback_query.from_user.first_name}

Now you can use bot.
        """
    )

# ==========================================
# HELP COMMAND
# ==========================================

@bot.on_message(filters.command("help"))
async def help_command(client, message):

    await message.reply_text(
        """
📚 Commands List

/start - Start Bot
/help - Help Menu
/about - About Bot
/ping - Bot Ping
/users - Total Users
/broadcast - Broadcast Message
        """
    )

# ==========================================
# ABOUT COMMAND
# ==========================================

@bot.on_message(filters.command("about"))
async def about(client, message):

    await message.reply_text(
        """
🤖 Premium Force Join Bot

✅ Auto Verify System
✅ Inline Keyboard
✅ Broadcast System
✅ User Counter
✅ Fast & Secure

Made With Pyrogram ❤️
        """
    )

# ==========================================
# PING COMMAND
# ==========================================

@bot.on_message(filters.command("ping"))
async def ping(client, message):

    start_time = datetime.now()

    msg = await message.reply_text("🏓 Pinging...")

    end_time = datetime.now()

    ping_ms = (end_time - start_time).microseconds / 1000

    await msg.edit_text(
        f"🏓 Pong!\n⚡ {ping_ms:.2f} ms"
    )

# ==========================================
# USER COUNT
# ==========================================

@bot.on_message(filters.command("users"))
async def user_count(client, message):

    if message.from_user.id not in ADMINS:
        return

    await message.reply_text(
        f"👥 Total Users: {len(users)}"
    )

# ==========================================
# BROADCAST
# ==========================================

@bot.on_message(filters.command("broadcast"))
async def broadcast(client, message):

    if message.from_user.id not in ADMINS:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/broadcast Hello"
        )

    text = message.text.split(None, 1)[1]

    success = 0
    failed = 0

    for user in users:

        try:
            await bot.send_message(user, text)
            success += 1
        except:
            failed += 1

    await message.reply_text(
        f"""
✅ Broadcast Completed

✔ Success: {success}
❌ Failed: {failed}
        """
    )

# ==========================================
# OWNER COMMAND
# ==========================================

@bot.on_message(filters.command("owner"))
async def owner(client, message):

    await message.reply_text(
        """
👑 Bot Owner

Made By Developer
        """
    )

# ==========================================
# RUN BOT
# ==========================================

print("✅ Premium Force Join Bot Started")

bot.run()