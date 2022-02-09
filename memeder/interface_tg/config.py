

MEME_BUTTONS = {
    'b1_neutral':    ('\U0001F610	',                                                          '104'),
    'b2_like':       ('\U0001F4A3' + '\U0001F4A5',                                              '1000'),
    'b2_dislike':    ('\U0001F4A9',                                                             '1001'),

    # 'b2_like':       ('\U0001F602',                                                             '1000'),
    # 'b2_dislike':    ('\U0001F615',                                                         '1001'),

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

    'bm_memes':         ('Back to memes',                                                          'memes'),

    'DB_PENDING':       (None,                                                                     '10003'),
}


MENU_BUTTONS = {
    # button_text, message, profile_column (if any), profile_value (if any)
    'm_start':          (None, 'In main menu.\nHere, you can configure your profile to find your best match!', None,
                         None),

    'm0_gender':        ('Gender \U0001F466 \U0001F467', 'Choose your gender:', None, None),
    'm0_preferences':   ('Preferences', 'Show me:', None, None),
    'm0_profile':       ('Edit profile \U0001F58A \U0001F320', 'In profile settings:', None, None),
    'm0_goals':         ('I am searching for \U0001F498 \U0001F923', 'I am here for:', None, None),
    'm0_memes':         ('\U0001F519 MEMES \U0001F519', None, None, None),

    'm_main_menu':      ('\U0001F519 Main menu \U0001F519', 'Main menu:', None, None),

    'm1_boy':           ('Boy \U0001F468', 'Success!', 'sex', 5000),
    'm1_girl':          ('Girl \U0001F469', 'Success!', 'sex', 5001),

    'm2_boys':          ('Boys \U0001F466', "Got it! \nDon't hesitate to write first \U0001F609", 'preferences', 3000),
    'm2_girls':         ('Girls \U0001F469', 'Ok, fingers crossed! \U0001F91E', 'preferences', 3001),
    'm2_all':           ('All \U0001F469 \U0001F9D1', 'Ok, we will show you all users', 'preferences', 3002),
    'm2_memes':         ('Only memes \U0001F60E', 'Just memes, good choice \U0001F60F', 'preferences', 3003),

    'm3_bio':           ('Bio \U0001F53C', 'Send me your bio with text message :)', 'bio_update_flag', True),
    'm3_photo':         ('Photo \U0001F53C', 'Just send me your photo :)', 'photo_update_flag', True),
    'm3_del_bio':       ('Clear bio \U0001F6AB', 'Successfully deleted bio', 'use_bio', False),
    'm3_del_photo':     ('Clear photo \U0001F6AB', 'Successfully deleted photo', 'use_photo', False),

    'm4_friends':       ('Friends \U0001F92A', 'Yeap!', 'goals', 4000),
    'm4_relationships': ('Relationships \U0001F498', 'Good look to find you love \U0001F49E', 'goals', 4001),
    'm4_idk':           ("I don't know \U0001F914", 'Same \U0001F600', 'goals', 4002),
    'm4_memes':         ('Memes and only memes \U0001F63C', 'Just memes, got it!', 'goals', 4003),


}

menu_routing_buttons = ['m0_gender', 'm0_preferences', 'm0_profile', 'm0_goals', 'm_main_menu']
menu_update_buttons = [b for b in MENU_BUTTONS.keys() if b.startswith(('m1', 'm2', 'm3', 'm4'))]
