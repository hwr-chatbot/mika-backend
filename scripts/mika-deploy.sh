#!/bin/bash
set -e

APP_DIR="/home/s_winklerf23/apps/mika-backend"
REPO_URL="git@github-backend:hwr-chatbot/mika-backend.git"

echo "📁 Wechsle ins App-Verzeichnis: $APP_DIR"

if [ ! -d "$APP_DIR/.git" ]; then
  echo "📦 Verzeichnis existiert nicht oder kein Git-Repo. Klone Repository..."
  git clone "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"

echo "🔄 Hole aktuelle Änderungen aus Git..."
git pull origin main

echo "📦 Installiere Abhängigkeiten..."
poetry install

echo "🚀 Starte oder restarte Rasa mit Actions via PM2..."

if pm2 describe rasa-backend > /dev/null 2>&1; then
  echo "🔄 Prozess 'rasa-backend' gefunden, starte Neustart..."
  pm2 restart rasa-backend --update-env
else
  echo "🚀 Prozess 'rasa-backend' nicht gefunden, starte neu..."
  pm2 start --name rasa-backend --interpreter python3 -- "poetry run rasa run --enable-api --cors http://localhost:5173"
  pm2 start --name rasa-actions --interpreter python3 -- "poetry run rasa run actions --cors http://localhost:5173"
fi

echo "✅ Deployment abgeschlossen!"
