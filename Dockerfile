FROM node:24-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv libgomp1 ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ADD tharon-source.tar.gz ./
RUN python3 -m venv /opt/speech && /opt/speech/bin/pip install --no-cache-dir -r /app/speech/requirements.txt
# Download public model weights at build time. Runtime transcription is offline.
RUN /opt/speech/bin/python -c "from faster_whisper.utils import download_model; download_model('tiny.en', output_dir='/opt/whisper/tiny.en')"
RUN npm ci --omit=dev
ENV NODE_ENV=production TZ=America/Los_Angeles TRANSCRIBE_LOCAL=true WHISPER_MODEL_DIR=/opt/whisper/tiny.en HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
EXPOSE 3000
USER node
CMD ["node", "server/index.mjs"]
