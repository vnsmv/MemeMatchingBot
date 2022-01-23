import argparse
import logging

import numpy as np
from tqdm import tqdm

from telethon.sync import TelegramClient


def infinite_generator():
    while True:
        yield


def meme_stole(client, source_name, target_name):
    messages = client.get_messages(source_name, 1)

    msg = messages[0]
    i = msg.id

    is_meme = False
    if msg.reply_markup is not None:
        if msg.reply_markup.rows is not None:
            if len(msg.reply_markup.rows) == 1:
                if msg.reply_markup.rows[0].buttons is not None:
                    if len(msg.reply_markup.rows[0].buttons) == 2:
                        b1 = msg.reply_markup.rows[0].buttons[0].data.decode('utf-8')
                        b2 = msg.reply_markup.rows[0].buttons[1].data.decode('utf-8')
                        if b1.startswith('r') and b1.endswith('_1') and b2.startswith('r') and b2.endswith('_2'):
                            is_meme = True
                            logging.info(f'Message [{i}]: ok')
                        else:
                            logging.warning(f'Message [{i}]: (level 6) did not pass `data` check; call \\start')
                    else:
                        logging.warning(f'Message [{i}]: (level 5) did not pass `buttons len` check; call \\start')
                else:
                    logging.warning(f'Message [{i}]: (level 4) did not pass `buttons` check; call \\start')
            else:
                logging.warning(f'Message [{i}]: (level 3) did not pass `rows len` check; call \\start')
        else:
            logging.warning(f'Message [{i}]: (level 2) did not pass `rows` check; call \\start')
    else:
        logging.warning(f'Message [{i}]: (level 1) did not pass `reply markup` check; call \\start')

    if is_meme:
        client.forward_messages(target_name, msg)
        msg.click(np.random.randint(2))
    else:
        client.send_message(source_name, '/start')

    # add_meme(connection, cursor, tg_id=str(meme_id), author_id=1, date=None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, type=str, choices=('test', 'deploy'))
    args = parser.parse_known_args()[0]

    logging_filename = 'stole_memes.log'
    logging.basicConfig(filename=logging_filename, level=logging.WARNING)

    source_name = 'ffmemesbot'

    if args.host == 'test':
        target_name = 'MemderTestBot'
    else:  # args.host == 'deploy':
        target_name = 'DatingMemeBot'

    api_id = 15806656
    api_hash = 'f5fc3ffced16b257c1b36aace17014b9'

    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    # client.send_message(target_name, '/start')

    for _ in tqdm(infinite_generator()):
        meme_stole(client, source_name, target_name)


if __name__ == '__main__':
    main()


# ### ffmemesbot keyboards: ###

# reply_markup = ReplyInlineMarkup(
#     rows=[
#         KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='💛 ХОЧУ! 💚', data=b'date_location',
#                                                           requires_password=False)]),
#         KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='Нет, хочу только мемы', data=b'date_no',
#                                                           requires_password=False)])
#     ]
# )
# reply_markup = ReplyInlineMarkup(
#     rows=[KeyboardButtonRow(buttons=[KeyboardButtonCallback(text='👍', data=b'r24641179_1', requires_password=False),
#                                      KeyboardButtonCallback(text='👎', data=b'r24641179_2', requires_password=False)])]
# )


