#!/bin/bash
DB_PATH="App/Backend/test.db"  # ← укажите свой путь к БД
BACKUP_DIR="backups"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
cp "$DB_PATH" "$BACKUP_DIR/test_${DATE}.db"
find "$BACKUP_DIR" -type f -mtime +7 -delete  # удалять бэкапы старше 7 дней