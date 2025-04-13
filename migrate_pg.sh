#!/bin/bash

# ==== Параметры подключения ====

# Старая база (только чтение)
SRC_DB="postgresql://giveme_db_owner:npg_jz6QFDUleS3b@ep-restless-frost-a27vpz63-pooler.eu-central-1.aws.neon.tech/giveme_db?sslmode=require"

# Новая база (куда зальём данные)
DST_DB="postgresql://givemekz_db_owner:npg_J2kgfUrC5sVQ@ep-odd-frost-a2gjhhqr-pooler.eu-central-1.aws.neon.tech/givemekz_db?sslmode=require"

# Имя файла резервной копии
BACKUP_FILE="giveme_backup.bak"

echo "📦 Создание дампа из старой базы..."
pg_dump --no-owner --no-privileges --no-publications --no-subscriptions --no-tablespaces \
  -Fc -v -d "$SRC_DB" -f "$BACKUP_FILE"

if [ $? -ne 0 ]; then
  echo "❌ Ошибка при создании дампа. Остановка."
  exit 1
fi

echo "♻️ Восстановление дампа в новую базу..."
pg_restore --no-owner -v -d "$DST_DB" "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "✅ Данные успешно перенесены в новую базу!"
else
  echo "❌ Ошибка при восстановлении данных!"
fi
