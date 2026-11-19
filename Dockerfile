FROM node:24-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv libgomp1 ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
# Build checks and runtime use the same Pacific calendar.
ENV TZ=America/Los_Angeles
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
COPY personal-access-update.py /app/personal-access-update.py
RUN python3 /app/personal-access-update.py && npm test
# Keep desktop Today header above the homepage greeting.
COPY homepage-layout.css /app/homepage-layout.css
RUN cat /app/homepage-layout.css >> /app/site/styles.css
# Reviewed lead age and staff update tracking; no resident data migration.
COPY lead-aging-update.py /app/lead-aging-update.py
RUN python3 /app/lead-aging-update.py && npm test
# Owner-only staff monitoring, 7/14/30-day lead age options and simpler homepage.
COPY owner-monitoring-update.py /app/owner-monitoring-update.py
RUN python3 /app/owner-monitoring-update.py && npm test
# Save operational updates independently from incomplete packet requirements.
COPY pending-paperwork-save-update.py /app/pending-paperwork-save-update.py
RUN python3 /app/pending-paperwork-save-update.py && npm test
# Named Zach lead editing, preserving private link and owner-only monitoring.
COPY zach-edit-access-update.py /app/zach-edit-access-update.py
RUN python3 /app/zach-edit-access-update.py && npm test
# Simple approval-only filters and independent paperwork checkbox; Private Pay everywhere.
COPY simple-referrals-update.py /app/simple-referrals-update.py
RUN python3 /app/simple-referrals-update.py && npm test
# Confirm scheduled move-in dates, flag overdue arrivals, and restore age shortcuts.
COPY confirmed-movein-update.py /app/confirmed-movein-update.py
RUN python3 /app/confirmed-movein-update.py && npm test
# Keep the homepage clean; Add referral opens voice and file intake.
COPY homepage-referral-link-update.py /app/homepage-referral-link-update.py
RUN python3 /app/homepage-referral-link-update.py && npm test
# Steven-only marketer dashboard under More; no homepage clutter.
COPY personal-marketer-dashboard-update.py /app/personal-marketer-dashboard-update.py
RUN python3 /app/personal-marketer-dashboard-update.py && npm test
# Add only the requested original lead-maker filter.
COPY lead-maker-filter-update.py /app/lead-maker-filter-update.py
RUN python3 /app/lead-maker-filter-update.py && npm test
# Olivia sees her and Morgan leads outside Gaby buildings.
COPY olivia-access-update.py /app/olivia-access-update.py
RUN python3 /app/olivia-access-update.py && npm test
# Owner-only read-only preview of Olivia live view.
COPY olivia-preview-update.py /app/olivia-preview-update.py
RUN python3 /app/olivia-preview-update.py && npm test
# Public Olivia layout with fictional sample leads; no live records.
COPY olivia-layout-update.py /app/olivia-layout-update.py
RUN python3 /app/olivia-layout-update.py && npm test
# LOA is a separate short-term hospital contract option for every building.
COPY loa-program-update.py /app/loa-program-update.py
RUN python3 /app/loa-program-update.py && npm test
# Show LOA with a rate amount instead of a waiver tier.
COPY loa-rate-update.py /app/loa-rate-update.py
RUN python3 /app/loa-rate-update.py && npm test
# Match the approved homepage count and list to referrals awaiting scheduling.
COPY approved-unscheduled-update.py /app/approved-unscheduled-update.py
RUN python3 /app/approved-unscheduled-update.py && npm test
# Morgan edits every lead; cross-building duplicate warnings and reversible cleanup.
COPY morgan-duplicates-update.py /app/morgan-duplicates-update.py
RUN python3 /app/morgan-duplicates-update.py && npm test
ENV NODE_ENV=production TZ=America/Los_Angeles TRANSCRIBE_LOCAL=true WHISPER_MODEL_DIR=/opt/whisper/tiny.en HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
EXPOSE 3000
USER node
CMD ["node", "server/index.mjs"]

