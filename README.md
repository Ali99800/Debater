## Deploying to Vercel (Docker container)

This repository deploys a Streamlit app using a Docker container on Vercel.

### 1. (Optional) Install Vercel CLI

```bash
npm i -g vercel
```

### 2. Log in & link the project

```bash
vercel login
vercel link
```

### 3. Deploy

```bash
vercel --prod
```

Vercel detects `vercel.json` + `Dockerfile`, builds the image, and serves the app from the container.
The app binds to `0.0.0.0` and uses the Vercel-provided `PORT` automatically.
