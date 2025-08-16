Railway deployment guide for Alpha_Bot

This project is designed to run on Railway using Docker. Voice support is optional and disabled by default.

1. Overview
- The Dockerfile accepts a build-arg `ENABLE_VOICE` (default: false). Set it to `true` to install voice-related packages from `requirements-voice.txt`.
- `requirements.txt` contains core dependencies only. Heavy voice deps live in `requirements-voice.txt`.
- The container is started via the `start` wrapper which calls `start_simple.py`.

2. Required environment variables
Use `sample.env` as a template. At minimum, set:
- API_ID
- API_HASH
- BOT_TOKEN
- OWNER_ID
- MONGO_DB_URI

3. Railway setup
- Create a new Railway project and select "Deploy from GitHub" or "Deploy Dockerfile".
- If using the Dockerfile directly, set the following build environment variable in Railway:
  - ENABLE_VOICE=false
- Add environment variables from `sample.env` in your Railway project's Environment tab (do not commit secrets).

4. Build & Run (local testing)
- Build without voice (recommended):
```powershell
docker build -t alpha-bot . --build-arg ENABLE_VOICE=false
```

- Run locally with env file:
```powershell
docker run --rm --env-file .\sample.env -e PYTHONUTF8=1 alpha-bot
```

- To build with voice (may require native build toolchain):
```powershell
docker build -t alpha-bot-voice . --build-arg ENABLE_VOICE=true
```

5. Troubleshooting
- If the Docker build fails on voice packages, try enabling the build with `ENABLE_VOICE=true` locally where build tools are available. Railway build containers may not have enough resources for heavy native builds.
- If you see emoji/encoding errors on Windows consoles, set `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8` when running locally.

6. CI (optional)
A GitHub Actions workflow can be used to validate that the Dockerfile builds without voice packages (see `.github/workflows/docker-build.yml`).

7. Security
- Never commit secret tokens. Use Railway's environment variables manager to store secrets.

