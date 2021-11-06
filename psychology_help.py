import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random
from datetime import datetime
from datetime import timedelta
import sqlite3

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet  = client.open("Psychology_Help")
sheet = spreadsheet.sheet1
list_of_dicts = sheet.get_all_records()

def RandomPeopleHelpers():
    list_telegrams = []
    for user_data in list_of_dicts:
        list_telegrams.append(user_data['Helpers'])
    talk_person = random.choice(list_telegrams)
    return talk_person

def PutToDiary(username, mood):
    connection = sqlite3.connect('Stress_diary.db')
    cursor = connection.cursor()
    now = datetime.now()
    now_str = now.strftime("%d/%m/%Y")
    cursor.execute(f"UPDATE stress_diary SET ('{now_str}') = ? WHERE username = followthesun ", (mood,))
    connection.commit()


#PutToDiary('followthesun', 'chill')
dates = [i for i  in range(0,366)]

# def FillLines(tablename):
#     connection = sqlite3.connect('Stress_diary.db')
#     cursor = connection.cursor()
#     days = [i for i in range(0, 366)]
#     now = datetime.now()
#     #cursor.execute(f"INSERT INTO Stress_diary {now.strptime("%d/%m/%Y")} WHERE username = ?", (username,))
#     for date in dates:
#         days = timedelta(date)
#         date_summ = now + days
#         cursor.execute(f"ALTER TABLE {tablename} add column '%s' 'TEXT'" % date_summ.strftime("%d/%m/%Y"))
#     user_data = cursor.fetchone()
#     connection.commit()
#     connection.close()

def MoodTable(username, mood):
    tablename = CheckInDb(username)
    dtime = datetime.now().strftime("%d/%m/%Y")
    connection = sqlite3.connect('Stress_diary.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {tablename} VALUES (?,?)", (dtime, mood))
    connection.commit()
    cursor.execute(f"SELECT * FROM {tablename} DESC LIMIT 5")
    results = cursor.fetchall()
    moods = []
    for result in results:
        moods.append(result[1])
    connection.close()
    moods = set(moods)
    return moods

def CheckInDb(username):
    connection = sqlite3.connect('Stress_diary.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT ID FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]
    except TypeError:
        cursor.execute("INSERT INTO users VALUES (?, NULL)", (username,))
        cursor.execute("SELECT ID FROM users WHERE username = ?", (username,))

    user_id = cursor.fetchone()[0]
    user_id = 'ID_'+str(user_id)
    cursor.execute(f"create table if not exists {user_id} (datetime, mood)")
    connection.commit()
    connection.close()
    return user_id
    #cursor.execute(f"UPDATE stress_diary SET ('{now_str}') = ? WHERE username = followthesun ", (mood,))

def PutValues(username):
    connection = sqlite3.connect('Stress_diary.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM  ORDER BY CreateDate DESC LIMIT 5")

CheckInDb('son mum girlfriend')
