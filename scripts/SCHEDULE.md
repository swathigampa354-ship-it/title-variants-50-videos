# Schedule 5 TikTok posts via Taisly

## Plan
| Day | Video | Notes |
|-----|-------|-------|
| 1 | `day-3/Video_50.mp4` | reverse order |
| 2 | `day-3/Video_49.mp4` | |
| 3 | `day-3/Video_48.mp4` | |
| 4 | `day-3/Video_47.mp4` | |
| 5 | `day-3/Video_46.mp4` | |

- Skip Video_01–15 (already used)
- 1 post per day × 5 days
- TikTok only (account connected in Taisly)

## Why GitHub Actions?
The Arena sandbox **cannot open TLS to `app.taisly.com`** (connection reset during handshake).
GitHub-hosted runners can reach Taisly, so scheduling runs there.

## Run it (2 minutes)

1. Open:
   https://github.com/swathigampa354-ship-it/title-variants-50-videos/actions/workflows/schedule-tiktok.yml
2. Click **Run workflow**
3. Branch: `arena/01a08487-title-variants-50-videos`
4. Fill inputs:
   - **taisly_api_key**: your `taisly_...` key
   - **start_date**: first day, e.g. `2026-09-10`
   - **post_time**: IST time, e.g. `10:00`
   - **caption**: optional
   - **dry_run**: `true` first to verify TikTok is connected, then `false` to schedule
5. Run → open the job log for platform list + history IDs

### Optional: store key as repo secret
Repo → Settings → Secrets and variables → Actions → New secret  
Name: `TAISLY_API_KEY`  
Value: your key  

Then the workflow input can still override it.

## Local script (outside Arena)
```bash
export TAISLY_API_KEY=taisly_...
python3 scripts/schedule_tiktok_day3.py --start 2026-09-10 --time 10:00 --dry-run
python3 scripts/schedule_tiktok_day3.py --start 2026-09-10 --time 10:00 --caption "your caption"
```
