import os
import schedule
import time
import datetime
import subprocess

def backup_database():
    USER = "root"
    PASSWORD = "letmein"
    HOST = "localhost"
    DB_NAME = "flask_api_db"
    BACKUP_PATH = "/Users/bangvoanh/Documents/directories/MyAppPyFl/backupdb"
    
    BACKUP_FILE = os.path.join(BACKUP_PATH, f"{DB_NAME}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.sql")
    
    subprocess.run(f"mysqldump -u {USER} -p{PASSWORD} -h {HOST} {DB_NAME} > {BACKUP_FILE}", shell=True)
    
    os.system(f"find {BACKUP_PATH} -type f -name '*.sql' -mtime +7 -exec rm {{}} \\;")

schedule.every().day.at("02:00").do(backup_database)

while True:
    schedule.run_pending()
    time.sleep(60)  


# python /Users/bangvoanh/Documents/directories/MyAppPyFl/backupdb/backup.py
