

MEME_BUTTONS = {
    'b1_neutral':    ('\U0001F610	',                                                          '104'),
    'b2_like':       ('\U0001F4A3' + '\U0001F4A5',                                              '1000'),
    'b2_dislike':    ('\U0001F44E',                                                             '1001'),

    'b1_rofl':       ('\U0001F923',                                                              '100'),
    'b1_smiling':    ('\U0001F600',                                                              '101'),
    'b1_smirking':   ('\U0001F60F',                                                              '102'),
    'b1_blushing':   ('\U0000263A',                                                              '103'),
    'b1_upside':     ('\U0001F643',                                                              '104'),
    'b1_thinking':   ('\U0001F914',                                                              '105'),
    # 'b1_neutral':    ('\U0001F610',                                                              '106'),
    'b1_yawning':    ('\U0001F971',                                                              '107'),

    'bu_users':      ('Matching \U0001F3B0',                                                     'user'),

    'DB_EMPTY':      (None,                                                                      '1002')
}

USER_BUTTONS = {
    # TODO: configure buttons, the emoji are random now.
    'b1_chat':          ('Chat \U0001F4AC',                                                        None),
    'b1_next':          ('Next \U000023ED',                                                        '10001'),

    'bm_memes':         ('\U0001F519 memes \U0001F519',                                            'memes'),

    'DB_PENDING':       (None,                                                                     '10003'),
}


MENU_BUTTONS = {
    # button_text, message, profile_column (if any), profile_value (if any)
    'm_start':          (None, 'Вы в главном меню.\nЗдесь выможете настроить свой профиль и выбрать предпочтения!\n'
                               'А также в любой момент вернуться к мемам:)', None, None),

    'm0_gender':        ('Выбрать пол \U0001F466 \U0001F467', 'Выбери пол из предложенных в меню:', None, None),
    'm0_preferences':   ('Предпочтения', 'Показывай мне только:', None, None),
    'm0_profile':       ('Профиль \U0001F58A \U0001F320', 'Настройки профиля:', None, None),
    'm0_goals':         ('Цель знакомства \U0001F498 \U0001F923', 'Что вы хотите найти?', None, None),
    'm0_memes':         ('\U0001F519 MEMES \U0001F519', None, None, None),

    'm_main_menu':      ('\U0001F519 Главное меню \U0001F519', 'Главное меню:', None, None),

    'm1_boy':           ('Boy \U0001F468', 'Успешно обновили информацию!)', 'sex', 5000),
    'm1_girl':          ('Girl \U0001F469', 'Успешно обновили информацию!)', 'sex', 5001),

    'm2_boys':          ('Boys \U0001F466', "Отлично!\nНе стесняемся писать первыми \U0001F609", 'preferences', 3000),
    'm2_girls':         ('Girls \U0001F469', 'Ok, fingers crossed! \U0001F91E', 'preferences', 3001),
    'm2_all':           ('Всех пользователей \U0001F469 \U0001F9D1',
                         'Отлично, мы будем показывать пользователей вне зависимости от пола', 'preferences', 3002),
    'm2_memes':         ('Только мемы \U0001F60E', 'Только мемы, отличный выбор \U0001F60F', 'preferences', 3003),

    'm3_bio':           ('Био \U0001F53C', 'Теперь обычным текстовым сообщением можешь отправить мне свое био!',
                         'bio_update_flag', True),
    'm3_photo':         ('Фото \U0001F53C', 'Просто отправь мне свое фото :)', 'photo_update_flag', True),
    'm3_del_bio':       ('Удалить био \U0001F6AB', 'Удалили био!', 'use_bio', False),
    'm3_del_photo':     ('Удалить фото \U0001F6AB', 'Удалили фото!', 'use_photo', False),

    'm4_friends':       ('Друзья \U0001F92A', 'Хорошо!', 'goals', 4000),
    'm4_relationships': ('Отношения \U0001F498', 'Удачи при поиске \U0001F49E', 'goals', 4001),
    'm4_idk':           ("Понятия не имею \U0001F914", 'хех, я тоже \U0001F600', 'goals', 4002),
    'm4_memes':         ('Только мемы \U0001F63C', 'Только мемы, отлично!', 'goals', 4003),


}

menu_routing_buttons = ['m0_gender', 'm0_preferences', 'm0_profile', 'm0_goals', 'm_main_menu']
menu_update_buttons = [b for b in MENU_BUTTONS.keys() if b.startswith(('m1', 'm2', 'm3', 'm4'))]

MATCHING_MESSAGES = {
    1: 'Чтобы получать рекомендации пользователей, нужно просмотреть хотя бы {} мемов.'
       'Вам осталось посмотреть еще {}.',

    -1: 'Мы пока что не обновили рекомендации пользоваталей для вас.'
        'Но за просмотром мемов время летит незаметно \U0001F60F',
    -2: 'Чтобы получать рекомендации пользователей, нужно вначале указать свой пол.'
        'Это можно сделать из главного меню (нажми /start).\n'
        'P.S. После этого нам потребуется какое-то время, чтобы обновить \U0001F3B0 рекомендации.',
    -3: 'Чтобы получать рекомендации пользователей, нужно вначале указать свои предпочтения.'
        'Либо сейчас у вас выбран просмотр только мемов.'
        'Установить или поменять предпочтения можно из главного меню (нажми /start).'
        'P.S. После этого нам потребуется какое-то время, чтобы обновить \U0001F3B0 рекомендации.',
    -4: 'Чтобы получать рекомендации пользователей, нужно вначале указать цель для знакомств.'
        'Либо сейчас у вас выбран просмотр только мемов.'
        'Установить или поменять цели можно из главного меню (нажми /start).'
        'P.S. После этого нам потребуется какое-то время, чтобы обновить \U0001F3B0 рекомендации.',
}
