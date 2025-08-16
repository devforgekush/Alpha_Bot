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

8. Publishing a voice-enabled image (GHCR) and using it on Railway

If you need voice features in production, the recommended approach is to publish a prebuilt voice-enabled image to a container registry and point Railway to that image instead of building on Railway.

Steps to publish to GitHub Container Registry (GHCR):

- Create a Personal Access Token (PAT) with the `write:packages` scope.
- Add the token to your repository secrets as `CR_PAT` (Repository -> Settings -> Secrets -> Actions).
- Go to the Actions tab, open "Publish Voice-enabled Image" and run it (choose a tag, e.g. `latest`). The workflow will build the image with `--build-arg ENABLE_VOICE=true` and push to `ghcr.io/<owner>/alpha-bot-voice:<tag>`.

Notes:
- If the build fails, inspect the Action logs to see missing system packages or pip build errors. You can iterate on `Dockerfile` pinning or add required apt packages.
- Use the debug workflow `Publish Voice Build (debug)` (no push) to test the build without publishing (Actions -> select the workflow and run).

Using the published image on Railway:

1. In Railway, choose the option to deploy from a Container Registry image.
2. Use the image URI `ghcr.io/<your-github-username>/alpha-bot-voice:<tag>`.
3. Add environment variables from `sample.env` in the Railway UI (do not commit secrets).
4. Start the service. The image includes voice dependencies and native libs; ensure you have assistant `STRING_SESSION` env set for auto-joining calls.

Helpful tips:
- Consider using `workflow_dispatch` to build the voice image on-demand after any changes that affect voice.
- If you prefer Docker Hub, adapt the GHCR workflow to log in/push to Docker Hub using `DOCKER_USERNAME`/`DOCKER_PASSWORD` secrets.


