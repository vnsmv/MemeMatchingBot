import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet  = client.open("Tilda_Form_4745453_20211029233945")
sheet = spreadsheet.sheet1
list_of_dicts = sheet.get_all_records()

def find_answers(username):
    for record in list_of_dicts:
        username_tbl = record['telegram']
        if username_tbl[0] == '@':
            username_tbl = username_tbl[1:]
        if username_tbl == username:
            print(record)
            return record
    return []

def stress_level(data):
    answers_list = list(data.keys())
    for answer in answers_list:
        if data[answer] == '':
            del data[answer]
    answers_list = list(data.keys())
    score = 0
    for answer in answers_list:
        if answer[0:3] == 'int':
            score = score + 1
        elif answer[0:3] == 'beh':
            score = score + 1
        elif answer[0:3] == 'emo':
            score = score + 1.5
        elif answer[0:3] == 'phy':
            score = score + 2

    norm_coeff = 100/66
    return score * norm_coeff

def stress_percantage(username):
    user_data = find_answers(username)
    print(stress_level(user_data))
    return stress_level(user_data)

def append_gsheets(data):
    spreadsheet  = client.open("Dataset")
    sheet = spreadsheet.sheet1
    sheet.append_row(data.split())
