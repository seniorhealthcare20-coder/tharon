FROM node:24-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv libgomp1 ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ADD tharon-source.tar.gz ./
RUN python3 -m venv /opt/speech && /opt/speech/bin/pip install --no-cache-dir -r /app/speech/requirements.txt
# Download public model weights at build time. Runtime transcription is offline.
RUN /opt/speech/bin/python -c "from faster_whisper.utils import download_model; download_model('tiny.en', output_dir='/opt/whisper/tiny.en')"
RUN npm ci --omit=dev
# Apply reviewed UI-only source changes over the existing pinned source archive.
COPY dashboard-update.py /app/dashboard-update.py
RUN python3 /app/dashboard-update.py
COPY non-referral-admin-update.py /app/non-referral-admin-update.py
RUN python3 /app/non-referral-admin-update.py
COPY viewer-access-update.py /app/viewer-access-update.py
RUN python3 /app/viewer-access-update.py
# Add separate moved-in and lost filters; fail safely if source differs.
RUN python3 -c 'from pathlib import Path; import json; p=Path("site/app.js"); s=p.read_text(); changes=json.loads('"'"'[["q:\'"'"'\'"'"',todayRep:", "q:\'"'"'\'"'"',closedOutcome:\'"'"'all\'"'"',todayRep:"], ["  if(UI.roadmapPhase", "  if(UI.closed&&UI.closedOutcome&&UI.closedOutcome!==\'"'"'all\'"'"')ls=ls.filter(l=>UI.closedOutcome===\'"'"'moved\'"'"'?l.stage===\'"'"'movein\'"'"':l.stage===\'"'"'lost\'"'"');\\n  if(!UI.closed){\\n  if(UI.roadmapPhase"], ["  if(UI.q){const q=UI.q.toLowerCase();", "  }\\n  if(UI.q){const q=UI.q.toLowerCase();"], ["    ${!UI.closed?`<label>Needs attention", "    ${UI.closed?`<label for=\\"closedOutcome\\">Outcome<select id=\\"closedOutcome\\" class=\\"input\\" data-change=\\"closedOutcome\\">${opt([[\'"'"'all\'"'"',\'"'"'All closed\'"'"'],[\'"'"'moved\'"'"',\'"'"'Moved in (won)\'"'"'],[\'"'"'lost\'"'"',\'"'"'Lost\'"'"']],UI.closedOutcome||\'"'"'all\'"'"')}</select></label>`:\'"'"'\'"'"'}\\n    ${!UI.closed?`<label>Needs attention"], ["  if(c===\'"'"'frep\'"'"')", "  if(c===\'"'"'closedOutcome\'"'"'){UI.closedOutcome=el.value;return render();}\\n  if(c===\'"'"'frep\'"'"')"]]'"'"'); exec("for old,new in changes:\n if s.count(old)!=1: raise SystemExit(\"Unexpected source; no deployment patch applied\")\n s=s.replace(old,new,1)"); p.write_text(s)'
ENV NODE_ENV=production TZ=America/Los_Angeles TRANSCRIBE_LOCAL=true WHISPER_MODEL_DIR=/opt/whisper/tiny.en HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
EXPOSE 3000
USER node
CMD ["node", "server/index.mjs"]

