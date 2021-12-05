from telethon import TelegramClient, events, sync
from memeder.database_sql import connection, cursor, add_meme
from tqdm import tqdm

from telethon.tl.types import InputPhotoFileLocation

api_id = 15806656
api_hash = 'f5fc3ffced16b257c1b36aace17014b9'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

def meme_stole():
    messages = client.get_messages('ffmemesbot')
    msg = messages[0]
    meme_id = msg.photo.id
    # print(dir(msg.photo))
    # print(msg.photo.dc_id)
    #
    # print(InputPhotoFileLocation(msg.photo.id, msg.photo.access_hash, msg.photo.file_reference, msg.photo.sizes))

    messages[0].click()

    add_meme(connection, cursor, tg_id=str(meme_id), author_id=1, date=None)

    return meme_id

for i in tqdm(range(30)):
    mem_id = meme_stole()
