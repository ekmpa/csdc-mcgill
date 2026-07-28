# Calendar

## Automated calendar sync

The homepage featured seminar card is data-driven from `_data/events.yml`.

To enable automatic sync from Google Calendar via GitHub Actions:

1. Ensure the target calendar is publicly readable.
2. Add repository variable:
   - `GOOGLE_CALENDAR_ID` (optional; defaults to `mcgillcsdc@gmail.com`)
3. Optionally add repository secret:
   - `GOOGLE_CALENDAR_API_KEY` (optional; if missing, sync falls back to the public ICS feed)
3. Run `.github/workflows/auto-sync-calendar-events.yml` manually once, or wait for the scheduled run.

The sync script is `src/python/sync_google_calendar_events.py`.

## Auto-merge behavior

Calendar sync pull requests are configured to auto-merge.

For that to work reliably:

1. Auto-merge must be enabled in the repository settings.
2. Any required branch protection checks on `main` must pass.
3. If required checks do not run for bot-created pull requests, use a dedicated token for PR creation instead of relying only on the default `GITHUB_TOKEN`.