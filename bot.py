import json
from telethon import TelegramClient, events
import asyncio

# 🔹 Load JSON Configuration
with open("config.json", "r") as file:
    config = json.load(file)

# 🔹 Store all running bot instances
bot_clients = []

async def get_channel_id(client, channel):
    """Convert channel link or username to numeric ID."""
    try:
        entity = await client.get_entity(channel)
        return entity.id
    except Exception as e:
        print(f"❌ Error fetching ID for {channel}: {str(e)}")
        return None

async def setup_bot(bot):
    """Setup each bot instance."""
    api_id = bot["api_id"]
    api_hash = bot["api_hash"]
    bot_token = bot["bot_token"]

    # 🔹 Create Telegram Client
    client = TelegramClient(f"bot_session_{bot_token.split(':')[0]}", api_id, api_hash)
    await client.start(bot_token=bot_token)

    # 🔹 Convert Links to Channel IDs
    source_channels = [await get_channel_id(client, channel) for channel in bot["source_channels"]]
    target_channels = [await get_channel_id(client, channel) for channel in bot["target_channels"]]

    # 🔹 Remove None values (if any link fails)
    source_channels = [ch for ch in source_channels if ch is not None]
    target_channels = [ch for ch in target_channels if ch is not None]

    if not source_channels or not target_channels:
        print("❌ Error: Missing valid source or target channels. Skipping bot.")
        return

    @client.on(events.NewMessage(chats=source_channels))  # जब भी नया मैसेज आए
    async def auto_forward(event):
        for channel in target_channels:
            try:
                await event.forward_to(channel)
                print(f"✅ Message Forwarded from {event.chat_id} to {channel}")
            except Exception as e:
                print(f"❌ Error Forwarding to {channel}: {str(e)}")

    bot_clients.append(client)  # Store bot client

# 🔹 Initialize all bots
async def main():
    tasks = [setup_bot(bot) for bot in config["bots"]]
    await asyncio.gather(*tasks)
    print("🚀 All Bots are Running...")
    await asyncio.gather(*(client.run_until_disconnected() for client in bot_clients))

# 🔹 Run the bots
asyncio.run(main())
