from telethon import TelegramClient, events
import re
import asyncio
import os
from datetime import datetime

# 🔐 Telegram API info
api_id = 29608877
api_hash = 'c4d08a13c392feaec054f6111bf7807b'

# ✅ Source চ্যানেল লিস্ট (Updated)
source_channels = [
    'yonogames',
    'yonorummychannel',
    'yonoslotsofficial',
    'MBMBETtm',
    'yonoarcadeofficial',
    'Official_567Slots',
    'yonovip',
    'spinwinner',
    'slotswinnerofficial',
    'spincrushofficial',
    'indslotcom',
    'spin777slots',
    'spinluckyofficial',
    'spingoldcom',
    'Channel_789Jackpots',
    'Bingo101official',
    'gogorummyofficial',
    'bet213',
    'official_indbingo',
    'spin101',
    'Netavip',
    'en365official',
    'jaihoarcadeofficial',
    'jaihospin',
    'rummy91official',
    'jaiho777',
    'jaihorummy',
    'abcrummyofficial',
    'sagaslotscom',
    'JaiHoSlots',
    'Indrummy',
    'Official_TopRummy',
    'digitalphotoo'
]

# 🎯 Destination চ্যানেল
destination_channel = 'allyono_gamescode' #'tsitest'  

# 🔌 Telethon client
client = TelegramClient('forward_session', api_id, api_hash)

# 🧼 Clean text function


def clean_text(text):
    if not text:
        return ''

    # 🔐 Save raw text
    # folder = 'raw_messages'
    # os.makedirs(folder, exist_ok=True)
    # filename = datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.txt'
    # with open(os.path.join(folder, filename), 'w', encoding='utf-8') as f:
    #     f.write(text)

    # 🛡️ Extract code blocks first
    code_blocks = []

    def preserve_code(match):
        code_blocks.append(match.group(0))
        return f"__CODEBLOCK_{len(code_blocks)-1}__"

    # Preserve multiline and inline code
    text = re.sub(r'```[\s\S]*?```', preserve_code, text)
    text = re.sub(r'`[^`\n]+`', preserve_code, text)

    # 🧼 Clean all t.me, bit.ly, and domains (not www.)
    # Pattern: Match only valid links and domains outside `www.`
    pattern = re.compile(
        r'\b(?!(?:https?://)?www\.)(?:https?://)?(?:[\w\-]+\.)?(?:t\.me|bit\.ly|[a-zA-Z0-9\-]+\.(com|net|in|vip|org|xyz|me|info|app|site|link))\S*',
        flags=re.IGNORECASE
    )

    text = pattern.sub('https://t.me/TopSmartIdea/20240', text)

    # Remove @usernames (outside code blocks)
    text = re.sub(r'@\w+', '', text)

    # 🔄 Restore code blocks
    for i, block in enumerate(code_blocks):
        text = text.replace(f"__CODEBLOCK_{i}__", block)

    return text.strip()



# 🔁 Message handler
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    try:
        msg = event.message
        raw_text = msg.text or msg.message or ''
       # if not re.search(r'\bpromo\s*code\b|\bpromocode\b', raw_text, re.IGNORECASE):
        if not re.search(r'\b(promo\s*code|promocode|promo|code)\b', raw_text, re.IGNORECASE):
            return  # Skip if no keyword matched



        caption = clean_text(raw_text)
        caption = caption[:1000]  # 🔐 Enforce 1000-character limit

        if msg.media:
            await client.send_file(destination_channel, file=msg.media, caption=caption)
            print("📸 Media sent successfully.")
        elif caption:
            await client.send_message(destination_channel, caption)
            print(f"✅ Text sent: {caption[:50]}")
    except Exception as e:
        print("❌ Error:", e)


# ▶️ Start the client
print("🤖 Bot is running... Ctrl+C চাপলে বন্ধ হবে")
with client:
    client.run_until_disconnected()
