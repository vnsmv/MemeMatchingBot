from telethon import TelegramClient, events, sync

api_id = 15806656
api_hash = 'f5fc3ffced16b257c1b36aace17014b9'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

def meme_stole():
    messages = client.get_messages('ffmemesbot')
    msg = messages[0]
    meme_id = msg.photo.id
    messages[0].click()
    return meme_id
