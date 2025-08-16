#!/usr/bin/env bash
# Start script used by Procfile on Railway/Heroku-style platforms.
set -e

echo "🔁 Running start script..."

# Optionally install voice requirements when ENABLE_VOICE=true
if [ "$ENABLE_VOICE" = "true" ]; then
  echo "🔊 ENABLE_VOICE=true — installing voice dependencies..."
  if [ -f requirements-voice.txt ]; then
    pip install --no-cache-dir -r requirements-voice.txt
  else
    echo "⚠️ requirements-voice.txt not found, skipping."
  fi
fi

# Pre-warm imageio-ffmpeg to ensure binary is downloaded and available
python - <<'PY'
try:
    import imageio_ffmpeg
    print('✅ imageio-ffmpeg present, fetching ffmpeg binary...')
    print(imageio_ffmpeg.get_ffmpeg_exe())
except Exception as e:
    print('⚠️ imageio-ffmpeg not available or failed to fetch binary:', e)
PY

# Exec the Python start script (replaces the shell process)
exec python3 start_simple.py
