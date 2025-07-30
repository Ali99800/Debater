
## Deploying to Vercel (Docker container)

Vercel can run your Streamlit app inside a Docker container. This repository already contains a `Dockerfile` and `vercel.json` so deployment is **one-command**.

### 1. (Optional) Install Vercel CLI

```bash
npm i -g vercel
```

### 2. Log in & link the project

```bash
vercel login        # authenticate
vercel link         # run inside the repo to create / link a Vercel project
```

### 3. Add the required environment variables

In the Vercel dashboard (`Project → Settings → Environment Variables`) create the two variables your app needs:

* `OPENAI_API_KEY`
* `GOOGLE_API_KEY`

### 4. Deploy

Deploy from the CLI or by pushing to your connected Git repository (GitHub / GitLab / Bitbucket):

```bash
# from the project root
overcel --prod
```

Vercel detects the `Dockerfile`, builds the image and starts the container. The Dockerfile:

* Uses Python 3.11-slim
* Installs dependencies from `requirements.txt`
* Exposes port `8501`
* Runs `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

The `$PORT` environment variable is automatically injected by Vercel, so no extra configuration is needed.

### 5. Enjoy your live URL

Once the build succeeds Vercel will provide a public HTTPS endpoint where you can interact with your Dual-AI Dissertation Debate app.
