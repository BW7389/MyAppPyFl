#!/bin/bash

USER="root"
PASSWORD="letmein"
HOST="localhost"
DB_NAME="flask_api_db"
BACKUP_PATH="/Users/bangvoanh/Documents/directories/MyAppPyFl/backupdb"

BACKUP_FILE="$BACKUP_PATH/$DB_NAME-$(date +%Y%m%d%H%M%S).sql"

mysqldump -u $USER -p$PASSWORD -h $HOST $DB_NAME > $BACKUP_FILE

find $BACKUP_PATH -type f -name "*.sql" -mtime +7 -exec rm {} \;
