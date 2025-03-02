import json
from telethon import TelegramClient, events

# 🔹 Load JSON Configuration
with open("config.json", "r") as file:
    config = json.load(file)

# 🔹 Store all running bot instances
bot_clients = []

# 🔹 Setup all Bots
for bot in config["bots"]:
    api_id = bot["api_id"]
    api_hash = bot["api_hash"]
    bot_token = bot["bot_token"]
    source_channels = bot["source_channels"]
    target_channels = bot["target_channels"]

    # 🔹 Create a new Telegram Client for each Bot
    client = TelegramClient(f"bot_session_{bot_token.split(':')[0]}", api_id, api_hash).start(bot_token=bot_token)

    @client.on(events.NewMessage(chats=source_channels))  # जब भी नया मैसेज आए
    async def auto_forward(event):
        for channel in target_channels:
            try:
                await event.forward_to(channel)
                print(f"✅ Message Forwarded from {event.chat_id} to {channel}")
            except Exception as e:
                print(f"❌ Error Forwarding to {channel}: {str(e)}")

    bot_clients.append(client)  # Store bot client

# 🔹 Start all bots
print("🚀 All Bots are Running...")
for bot_client in bot_clients:
    bot_client.run_until_disconnected()
