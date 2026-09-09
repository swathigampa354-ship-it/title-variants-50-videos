# Schedule 5 TikTok posts via Taisly

## Locked plan
| Day | Video | Pace |
|-----|-------|------|
| 1 | `day-3/Video_50.mp4` | reverse order |
| 2 | `day-3/Video_49.mp4` | 1 post / day |
| 3 | `day-3/Video_48.mp4` | TikTok only |
| 4 | `day-3/Video_47.mp4` | |
| 5 | `day-3/Video_46.mp4` | |

Skip `Video_01`–`15` (already used). Later pool: `Video_45` → `Video_16`.

## Why not from the Arena agent directly?
This sandbox **cannot complete TLS to `app.taisly.com`** (handshake reset).  
MCP / curl / Node / Python all fail here. Your **browser** (and your laptop) can still reach Taisly.

---

## Option A — Browser UI (open the LIVE PREVIEW)

1. Open the **Taisly Scheduler UI** preview (port 8765).
2. Paste your Taisly API key (`taisly_…`).
3. Click **1. Check auth + platforms** → confirm TikTok appears.
4. Set start date / time (IST) + optional caption.
5. Click **3. Schedule 5 posts**.

If the browser shows a CORS error talking to Taisly, use Option B.

---

## Option B — Laptop script (most reliable)

```bash
git clone -b arena/01a08487-title-variants-50-videos \
  https://github.com/swathigampa354-ship-it/title-variants-50-videos.git
cd title-variants-50-videos

export TAISLY_API_KEY='taisly_…'

python3 scripts/schedule_tiktok_day3.py --start 2026-09-10 --time 10:00 --dry-run
python3 scripts/schedule_tiktok_day3.py --start 2026-09-10 --time 10:00 --caption ""
```

---

## Option C — GitHub Actions
Copy `scripts/schedule-tiktok.workflow.yml` → `.github/workflows/schedule-tiktok.yml`,
commit on the branch, then **Actions → Run workflow**.

(Arena cannot push files under `.github/workflows/`.)

---

## Security
Rotate the Taisly API key and any GitHub PAT pasted in chat after this is done.
