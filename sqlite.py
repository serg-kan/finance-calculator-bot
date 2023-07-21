import sqlite3 as sq
from datetime import datetime

async def db_start():
    global db, cur
    
    try:
        db = sq.connect('new.db')
        cur = db.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS profile(
                    user_id TEXT PRIMARY KEY, 
                    name TEXT)
                ''')

        cur.execute('''CREATE TABLE IF NOT EXISTS records(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    amount REAL,
                    user_id TEXT)
                ''')
        
        db.commit()
        print('Connection successful')
        return db, cur
    except sq.Error as e:
        print ('Error occured')

async def create_profile(user_id, name):
    user = cur.execute("SELECT 1 FROM profile where user_id == '{key}'".format(key=user_id)).fetchone()

    if not user:
        cur.execute('INSERT INTO profile VALUES(?, ?)', (user_id, name))
        db.commit()

async def add_record(amount, user_id):
    print('ADD RECORD', amount, user_id)
    try:
        cur.execute('''
                    INSERT INTO records(amount, user_id) 
                    VALUES (?,?)
                ''', (amount, user_id))
        db.commit()
        
    except sq.Error as e:
        print('Error', e)


async def get_records_month(user_id):
    month = datetime.now().month
    month_str = '0' + str(month) if month < 10 else str(month)

    try:
        total = cur.execute('''
                    SELECT SUM(amount) FROM records
                    WHERE strftime('%m', timestamp) = (?) AND user_id = (?)
                ''', (month_str, user_id)).fetchone()
        db.commit()

        return total[0]        
    except sq.Error as e:
        print('Error', e)