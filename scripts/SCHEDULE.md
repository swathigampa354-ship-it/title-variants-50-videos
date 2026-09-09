# Schedule 5 TikTok posts via Taisly

## Locked plan
| Day | Video | Pace |
|-----|-------|------|
| 1 | `day-3/Video_50.mp4` | reverse order |
| 2 | `day-3/Video_49.mp4` | 1 post / day |
| 3 | `day-3/Video_48.mp4` | TikTok only |
| 4 | `day-3/Video_47.mp4` | |
| 5 | `day-3/Video_46.mp4` | |

Skip `Video_01`–`15` (already used). Remaining later: `Video_45` → `Video_16`.

## Blocker in Arena
This Arena sandbox **cannot complete TLS to `app.taisly.com`** (handshake reset).  
So MCP / curl / the Python client all fail **from inside the agent**.  
Posting must run on a machine that can reach Taisly (your laptop, or GitHub Actions).

Your Taisly key is saved only on the agent disk (`~/.config/taisly/api_key`), **not** in git.

---

## Option A — Run on your laptop (fastest)

```bash
git clone -b arena/01a08487-title-variants-50-videos \
  https://github.com/swathigampa354-ship-it/title-variants-50-videos.git
cd title-variants-50-videos

export TAISLY_API_KEY='taisly_…'   # your key

# 1) Verify TikTok is connected
python3 scripts/schedule_tiktok_day3.py --start 2026-09-10 --time 10:00 --dry-run

# 2) Schedule the 5 posts (edit start/time/caption as you want)
python3 scripts/schedule_tiktok_day3.py \
  --start 2026-09-10 \
  --time 10:00 \
  --caption ""
```

`--dry-run` only lists connected accounts + the plan.  
Without it, uploads + schedules immediately.

---

## Option B — GitHub Actions

1. In the repo, create:
   `.github/workflows/schedule-tiktok.yml`
2. Paste the contents of `scripts/schedule-tiktok.workflow.yml`
3. Commit on branch `arena/01a08487-title-variants-50-videos`
4. Open **Actions → Schedule TikTok posts (Taisly) → Run workflow**
5. Inputs:
   - `taisly_api_key` = your key  
   - `start_date` = e.g. `2026-09-10`  
   - `post_time` = e.g. `10:00` (IST)  
   - `dry_run` = `true` first, then `false`

(Arena’s GitHub App is not allowed to push files under `.github/workflows/`, so the YAML lives under `scripts/` until you copy it.)

---

## What success looks like
- Platforms response includes a TikTok account with status CONNECTED  
- Each of the 5 uploads returns `"success": true` + a `historyId`  
- Taisly History shows 5 scheduled posts, one calendar day apart  

## After you’re done
Rotate the Taisly API key and the GitHub PAT you pasted in chat (they appeared in plaintext).
