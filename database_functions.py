import sqlite3

def MoodTable(username, mood):
    tablename = CheckInDb(username)
    dtime = datetime.now().strftime("%d/%m/%Y")
    connection = sqlite3.connect('Stress_diary.db')
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO {tablename} VALUES (?,?, NULL)", (dtime, mood))
    connection.commit()
    cursor.execute(f"SELECT * FROM {tablename} ORDER BY ID DESC  LIMIT 7")
    results = cursor.fetchall()
    moods = []
    print(results)
    for result in results:
        moods.append(result[1])
    connection.close()
    return moods

def CheckInDb(username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT ID FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]
        return user_id, True
    except TypeError:
        cursor.execute("INSERT INTO users VALUES (?, NULL)", (username,))
        cursor.execute("SELECT ID FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]
        user_id = 'ID_' + str(user_id)
        cursor.execute(f"create table if not exists {user_id} (datetime, mood, ID int AUTO_INCREMENT)")
        connection.commit()
        connection.close()
        return user_id, False

def InsertUserData(user_id, phrase, photo):
    pass
